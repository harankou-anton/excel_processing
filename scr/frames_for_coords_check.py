import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
import geopandas as gpd
import pyproj

database_url = r"postgresql://koren:qm$s}#CwH~@172.31.14.45:5432/addr_sys"
engine = create_engine(database_url)


def get_objectnumber_by_id_district():
    Session = sessionmaker(bind=engine)
    exp = text("""
    select case when id_district is not null then id_district else 0 end "id_district", objectnumber
    from ate.ateobjects
    where (registration_type= 1 or jrnreq_out is null) and category < 240 and category not in (101, 202)""")
    result = {}
    with Session() as session:
        execute = session.execute(exp)
        execute = execute.all()
        for data in execute:
            if str(int(data[0])) not in result:
                result[str(int(data[0]))] = [int(data[1])]
            else:
                result[str(int(data[0]))].append(int(data[1]))
    return result


def create_maska_frame(cs):
    if cs == 1:
        exp = """
            select a1.nameobject as "DISTRICT", a.nameobject as "NAMEOBJECT", 
            case when a1.id_district is not null then a1.id_district else 0 end "IDDISTRICT", a.geom
            from ate.ateobjects a
            left join (select * from ate.ateobjects where category = 102 and act=1) a1 on a1.id_district = a.id_district
            where a.category in (102, 111, 112) and a.act=1
            """
        gdf: gpd.GeoDataFrame = gpd.GeoDataFrame.from_postgis(sql=exp, con=engine, geom_col="geom")
        return gdf

    else:
        exp = """
        select a1.nameobject as "DISTRICT", a.nameobject as "NAMEOBJECT", 
        case when a1.id_district is not null then a1.id_district else 0 end "IDDISTRICT", b.geom_sk63
        from ate.ateobjects a
        left join (select * from ate.ateobjects where category = 102 and act=1) a1 on a1.id_district = a.id_district
        left join ate.ateobjects_borders b ON b.gid = a.gid
        where a.category in (102, 111, 112) and a.act=1 and b.zone={}
        """

        sk_63_1 = pyproj.Proj("""
        PROJCS["CK1963(c)1",GEOGCS["GCS_Pulkovo_1942",DATUM["D_Pulkovo_1942",SPHEROID["Krasovsky_1940",6378245,298.3]],
        PRIMEM["Greenwich",0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],
        PARAMETER["False_Easting",1250000],PARAMETER["False_Northing",-12900.568],
        PARAMETER["Central_Meridian",24.95],PARAMETER["Scale_Factor",1],
        PARAMETER["Latitude_Of_Origin",-0.01666666666],UNIT["Meter",1]]
        """)
        sk_63_2 = pyproj.Proj("""
        PROJCS["CK1963(c)2",GEOGCS["GCS_Pulkovo_1942",DATUM["D_Pulkovo_1942",SPHEROID["Krasovsky_1940",6378245,298.3]],
        PRIMEM["Greenwich",0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],
        PARAMETER["False_Easting",2250000],PARAMETER["False_Northing",-12900.568],PARAMETER["Central_Meridian",27.95],
        PARAMETER["Scale_Factor",1],PARAMETER["Latitude_Of_Origin",-0.01666666666],UNIT["Meter",1]]
        """)
        sk_63_3 = pyproj.Proj("""
        PROJCS["CK1963(c)3",GEOGCS["GCS_Pulkovo_1942",DATUM["D_Pulkovo_1942",SPHEROID["Krasovsky_1940",6378245,298.3]],
        PRIMEM["Greenwich",0],UNIT["Degree",0.0174532925199433]],PROJECTION["Gauss_Kruger"],
        PARAMETER["False_Easting",3250000],PARAMETER["False_Northing",-12900.568],
        PARAMETER["Central_Meridian",30.95],PARAMETER["Scale_Factor",1],
        PARAMETER["Latitude_Of_Origin",-0.01666666666],UNIT["Meter",1]]
        """)

        gdf_63_1: gpd.GeoDataFrame = gpd.GeoDataFrame.from_postgis(sql=exp.format(1), con=engine, geom_col="geom_sk63",
                                                                   crs=sk_63_1.to_proj4())
        gdf_63_2: gpd.GeoDataFrame = gpd.GeoDataFrame.from_postgis(sql=exp.format(2), con=engine, geom_col="geom_sk63",
                                                                   crs=sk_63_2.to_proj4())
        gdf_63_3: gpd.GeoDataFrame = gpd.GeoDataFrame.from_postgis(sql=exp.format(3), con=engine, geom_col="geom_sk63",
                                                                   crs=sk_63_3.to_proj4())

        gdf_63_1.crs = None
        gdf_63_2.crs = None
        gdf_63_3.crs = None

        gdf: gpd.GeoDataFrame = pd.concat([gdf_63_1, gdf_63_2, gdf_63_3], ignore_index=True)
        return gdf
