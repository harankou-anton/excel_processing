import os

import numpy as np
import pandas as pd
import geopandas as gpd
import csv
import scr.default_values
import scr.frames_for_coords_check


fields_excel = scr.default_values.fields_excel


class AddressFiles(object):
    def __init__(self, download_folder, final_folder, output_format, check_coords, change_id_ate,
                 round_coords, fields, sk=1, maska_file="", decimal_format='.', floor_for_ip=False, porch_for_ip=False,
                 separator_csv=";", prj_file='Нет', delete_coord_fields=False, quote_value=csv.QUOTE_NONE,
                 quote_type='"', excel_split='По файлам', recount_floor=False):
        self.download_folder = download_folder
        self.final_folder = final_folder
        self.maska_file = maska_file
        self.output_format = output_format
        self.check_coords = check_coords
        self.change_id_ate = change_id_ate
        self.round_coords = round_coords
        self.fields = fields
        self.sk = sk
        self.decimal_format = decimal_format
        self.floor_for_ip = floor_for_ip
        self.porch_for_ip = porch_for_ip
        self.separator_csv = separator_csv
        self.prj_file = prj_file
        self.delete_coords_fields = delete_coord_fields
        self.quote_value = quote_value
        self.quote_type = quote_type
        self.excel_split = excel_split
        self.recount_floor = recount_floor

    def get_fields(self):
        """
        Функция настраивает состав и порядок полей итогового файла в соответствии с данными переменной "fields_excel"
        """
        header = [x[1] for x in self.fields if x[2]]
        types = [x[3] for x in self.fields if x[2]]
        types_shp = [x[5] for x in self.fields if x[2]]
        temp = list(self.fields)
        for el in range(len(temp))[::-1]:
            if temp[el][2] is False:
                temp.pop(el)
        temp = sorted(temp, key=lambda x: x[4])
        final_order = [x[1] for x in temp]
        for field in range(len(final_order))[::-1]:
            if final_order[field] == fields_excel[55][1] or final_order[field] == fields_excel[57][1] or \
                    final_order[field] == fields_excel[86][1] or final_order[field] == fields_excel[87][1]:
                final_order.pop(field)
        return header, types, final_order, types_shp

    def do_round_coords(self, dataframe):
        """
        Функция округляет значения координат, до указанного в параметрах класса "round_coords" значения
        """
        xy = None
        if self.fields[65][2] and self.fields[66][2]:
            xy = (65, 66)
        elif self.fields[63][2] and self.fields[64][2]:
            xy = (63, 64)
        dataframe[self.fields[xy[0]][1]] = dataframe[self.fields[xy[0]][1]].apply(
            lambda x: str(round(float(x), int(self.round_coords))) if x != '' else x)
        dataframe[self.fields[xy[1]][1]] = dataframe[self.fields[xy[1]][1]].apply(
            lambda x: str(round(float(x), int(self.round_coords))) if x != '' else x)
        return dataframe

    def change_decimal_sep(self, dataframe):
        """
        Функция изменяет разделитель дробной части на запятую для csv файлов
        """
        if self.fields[65][2] and self.fields[66][2]:
            dataframe[self.fields[65][1]] = dataframe[self.fields[65][1]].str.replace('.', ',', regex=False)
            dataframe[self.fields[66][1]] = dataframe[self.fields[66][1]].str.replace('.', ',', regex=False)
        if self.fields[63][2] and self.fields[64][2]:
            dataframe[self.fields[63][1]] = dataframe[self.fields[63][1]].str.replace('.', ',', regex=False)
            dataframe[self.fields[64][1]] = dataframe[self.fields[64][1]].str.replace('.', ',', regex=False)

    def do_check_coords(self, dataframe):
        """
        Функция проверяет попадание координат в территорию района//города областного подчинения по файлу указанному
        в параметрах класса "maska_file"
        Для записей с вылетевшими координатами удаляются значения координат
        """
        xy = None
        if self.sk == 1:
            xy = (65, 66)
        elif self.sk == 2:
            xy = (63, 64)
        data_regions = scr.frames_for_coords_check.create_maska_frame(self.sk)

        df_coord = dataframe[dataframe[self.fields[xy[0]][1]] != ""]
        if self.fields[33][2]:
            object_number_check = scr.frames_for_coords_check.get_objectnumber_by_id_district()

            to_gdf = gpd.GeoDataFrame(df_coord,
                                      geometry=gpd.points_from_xy(df_coord[self.fields[xy[0]][1]],
                                                                  df_coord[self.fields[xy[1]][1]]),
                                      columns=[self.fields[33][1]])
            intersect = to_gdf.sjoin(data_regions, how='inner')
            intersect['ID_DISTR_VALUES'] = intersect.apply(lambda x:
                                                           True if int(x[self.fields[33][1]])
                                                                   in object_number_check[str(int(x['IDDISTRICT']))]
                                                           else False, axis=1)

            correct_coords = intersect[intersect['ID_DISTR_VALUES'] == True]

        elif self.fields[39][2] and self.fields[27][2]:
            to_gdf = gpd.GeoDataFrame(df_coord,
                                      geometry=gpd.points_from_xy(df_coord[self.fields[xy[0]][1]],
                                                                  df_coord[self.fields[xy[1]][1]]),
                                      columns=[self.fields[27][1], self.fields[39][1]])
            intersect = to_gdf.sjoin(data_regions, how='inner')

            if self.fields[39][1] != 'NAMEOBJECT':
                correct_coords = intersect[(intersect[self.fields[27][1]] == intersect['NAMEOBJECT']) |
                                           (intersect[self.fields[39][1]] == intersect['NAMEOBJECT']) |
                                           ((intersect[self.fields[27][1]] == 'Березовский') &
                                            (intersect['NAMEOBJECT'] == 'Берёзовский')) |
                                           ((intersect[self.fields[27][1]] == 'Рогачевский') &
                                            (intersect['NAMEOBJECT'] == 'Рогачёвский'))]
            else:
                correct_coords = intersect[(intersect[self.fields[27][1]] == intersect['NAMEOBJECT_right']) |
                                           (intersect[f'{self.fields[39][1]}_left'] == intersect['NAMEOBJECT_right']) |
                                           ((intersect[self.fields[27][1]] == 'Березовский') &
                                            (intersect['NAMEOBJECT_right'] == 'Берёзовский')) |
                                           ((intersect[self.fields[27][1]] == 'Рогачевский') &
                                            (intersect['NAMEOBJECT_right'] == 'Рогачёвский'))]

        coords_index = set(df_coord.index.values)
        correct = set(correct_coords.index.values)
        for_delete = tuple(coords_index.difference(correct))
        for ind in for_delete:
            dataframe.at[ind, self.fields[xy[0]][1]] = ''
            dataframe.at[ind, self.fields[xy[1]][1]] = ''
        return dataframe

    def do_change_id_ate(self, dataframe):
        """
        Функция заменяет значения "Уникальный идентификатор АТЕ и ТЕ" на "Уникальный идентификатор населённого пункта"
        """
        dataframe[self.fields[33][1]] = dataframe.apply(
            lambda x: x[self.fields[33][1]] if x[self.fields[39][1]] != '' else None, axis=1)
        return dataframe

    def write_floor_for_ip(self, dataframe):
        """
        Функция оставляет значения поля "Количество этажей(этаж)" только для изолированных помещений
        """
        dataframe[self.fields[6][1]] = dataframe.apply(
            lambda x: x[self.fields[6][1]] if x[self.fields[4][1]] == 8
                                              or x[self.fields[22][1]] == 'Изолированное помещение' else '', axis=1)
        return dataframe

    def write_porch_for_ip(self, dataframe):
        """
        Функция оставляет значения поля "Количество подъездов (подъезд)" только для изолированных помещений
        """
        dataframe[self.fields[5][1]] = dataframe.apply(
            lambda x: x[self.fields[5][1]] if x[self.fields[4][1]] == 8
                                              or x[self.fields[22][1]] == 'Изолированное помещение' else '', axis=1)
        return dataframe

    def recount_floor_codes(self, dataframe):
        """
        Функция пересчитывает значения поля "Количество этажей(этаж)" с кодовых значений в текстовые
        """
        dataframe[self.fields[6][1]] = dataframe[self.fields[6][1]].apply(
            lambda x: scr.default_values.floor_name[int(x)] if x != '' else '')
        return dataframe

    def save_to_shp(self, dataframe, name):
        """
        Функция сохраняет данные в формате шейп файла
        """
        geo_dataframe = None
        if self.sk == 1:
            df_coords = dataframe[dataframe[self.fields[65][1]] != ""]
            geo_dataframe = gpd.GeoDataFrame(df_coords,
                                             geometry=gpd.points_from_xy(df_coords[self.fields[65][1]],
                                                                         df_coords[self.fields[66][1]]),
                                             columns=self.get_fields()[2])
        elif self.sk == 2:
            df_coords = dataframe[dataframe[self.fields[63][1]] != ""]
            geo_dataframe = gpd.GeoDataFrame(df_coords,
                                             geometry=gpd.points_from_xy(df_coords[self.fields[63][1]],
                                                                         df_coords[self.fields[64][1]]),
                                             columns=self.get_fields()[2])

        if self.fields[70][2]:
            geo_dataframe[self.fields[70][1]] = dataframe.apply(
                lambda x: x[self.fields[70][1]] if x[self.fields[70][1]] != '' else None, axis=1)

        if self.fields[72][2]:
            geo_dataframe[self.fields[72][1]] = dataframe.apply(
                lambda x: x[self.fields[72][1]] if x[self.fields[72][1]] != '' else None, axis=1)

        schema = gpd.io.file.infer_schema(geo_dataframe)
        for row_name in self.get_fields()[2]:
            schema['properties'][row_name] = self.get_fields()[3][self.get_fields()[0].index(row_name)]

        if self.delete_coords_fields:
            if self.sk == 1:
                geo_dataframe.drop(self.fields[65][1], axis=1, inplace=True)
                geo_dataframe.drop(self.fields[66][1], axis=1, inplace=True)
                del schema['properties'][self.fields[65][1]]
                del schema['properties'][self.fields[66][1]]
            elif self.sk == 2:
                geo_dataframe.drop(self.fields[63][1], axis=1, inplace=True)
                geo_dataframe.drop(self.fields[64][1], axis=1, inplace=True)
                del schema['properties'][self.fields[63][1]]
                del schema['properties'][self.fields[64][1]]
        geo_dataframe.to_file(os.path.join(self.final_folder, name[:-4]) + '.shp', driver='ESRI Shapefile',
                              encoding='utf-8', schema=schema, index=False)
        if self.prj_file != 'Нет':
            with open(f'{os.path.join(self.final_folder, name[:-4])}.prj', mode='w', encoding='utf-8') as writter:
                writter.write(scr.default_values.prj_data[self.prj_file])

    def save_to_excel(self, dataframe, name, save_format='По файлам'):
        """
        Функция сохраняет обработанную таблицу в формат excel
        """
        if save_format == 'По листам':
            with pd.ExcelWriter(os.path.join(self.final_folder, name[:-4]) + '.xlsx', datetime_format='DD.MM.YYYY',
                                engine='xlsxwriter') as writter:
                for sheet in range((dataframe.shape[0]-1)//1048575 + 1):
                    df_for_save = dataframe[0+1048575*sheet:1048575*(sheet+1)]
                    df_for_save.replace('', np.nan, inplace=True)
                    for column in df_for_save.columns:
                        if column != self.fields[7][1]:
                            df_for_save[column] = df_for_save[column].astype("float", errors='ignore')
                    df_for_save.to_excel(
                        writter, na_rep="", columns=self.get_fields()[2], index=False,
                        sheet_name='Sheet{0}'.format(sheet+1))

        else:
            if dataframe.shape[0] <= 1048575:
                dataframe.replace('', np.nan, inplace=True)
                for column in dataframe.columns:
                    if column != self.fields[7][1]:
                        dataframe[column] = dataframe[column].astype("float", errors='ignore')
                with pd.ExcelWriter(os.path.join(self.final_folder, name[:-4]) + '.xlsx',
                                    datetime_format='DD.MM.YYYY', engine='xlsxwriter') as writter:
                    dataframe.to_excel(writter, na_rep="", columns=self.get_fields()[2], index=False)

            else:
                for sheet in range((dataframe.shape[0] - 1) // 1048575 + 1):
                    df_for_save = dataframe[0 + 1048575 * sheet:1048575 * (sheet + 1)]
                    df_for_save.replace('', np.nan, inplace=True)
                    for column in df_for_save.columns:
                        if column != self.fields[7][1]:
                            df_for_save[column] = df_for_save[column].astype("float", errors='ignore')
                    with pd.ExcelWriter(os.path.join(self.final_folder, name[:-4]) + '{0}.xlsx'.format(sheet + 1),
                                        datetime_format='DD.MM.YYYY', engine='xlsxwriter') as writter:
                        df_for_save.to_excel(writter, na_rep="", columns=self.get_fields()[2], index=False)

    def save_to_csv(self, dataframe, file_name, delimeter_csv, quote_value, quotes_type):
        """
        Функция сохраняет обработанную таблицу в формат csv
        """
        dataframe[self.fields[9][1]] = dataframe[self.fields[9][1]].str.replace(';', '_')
        dataframe[self.fields[9][1]] = dataframe[self.fields[9][1]].str.replace(r'\n', ' ', regex=True)

        if quote_value == csv.QUOTE_NONNUMERIC:
            dataframe.replace('', np.nan, inplace=True)
            for column in dataframe.columns:
                if column != self.fields[7][1]:
                    dataframe[column] = dataframe[column].astype("float", errors='ignore')

        dataframe.to_csv(os.path.join(self.final_folder, file_name[:-4]) + '_temp.csv', sep=delimeter_csv,
                         quoting=quote_value, index=False, date_format='%d.%m.%Y', columns=self.get_fields()[2],
                         encoding='utf-8', quotechar=quotes_type)
        with open(os.path.join(self.final_folder, file_name[:-4]) + '_temp.csv', 'r', encoding='utf-8') as temp_file:
            open_file = temp_file.read()
            open_file = open_file.replace(".0;", ";")
            final_file = open(os.path.join(self.final_folder, file_name[:-4]) + '.csv', 'w', encoding='utf-8')
            final_file.write(open_file)
            final_file.close()
        os.remove(os.path.join(self.final_folder, file_name[:-4]) + '_temp.csv')

    def processing_data(self, excel_file):
        """
        Функция перезаписывает значения в поле "Дополнительные сведения", удаляет значения "Код области" и
        "Наименование области" для адресов г. Минска, а также запускает функции которые установлены в параметрах класса
        """

        file_name = os.path.join(self.download_folder, excel_file)
        names = self.get_fields()[0]
        types = self.get_fields()[1]
        for_dates_parse = []
        if self.fields[10][2]:
            for_dates_parse.append(names.index(self.fields[10][1]))
        if self.fields[69][2]:
            for_dates_parse.append(names.index(self.fields[69][1]))
        if self.fields[70][2]:
            for_dates_parse.append(names.index(self.fields[70][1]))
        if self.fields[72][2]:
            for_dates_parse.append(names.index(self.fields[72][1]))
        if len(for_dates_parse) == 0:
            for_dates_parse = False
        df = pd.read_csv(file_name, sep=";", dtype=dict(zip(names, types)), na_filter=False, names=names,
                         encoding='utf-8', header=0, parse_dates=for_dates_parse, dayfirst=True)

        if self.fields[9][2]:
            df['full_block'] = df.apply(lambda x: 'блок ' + str(x[self.fields[55][1]]) if x[self.fields[55][1]] != ''
            else "", axis=1)
            df['settlement'] = df.apply(lambda x: 'вблизи ' + x[self.fields[87][1]] if x[self.fields[87][1]] != ''
            else "", axis=1)

            df['full_remark'] = df[df.columns[[df.columns.get_loc('full_block'),
                                               df.columns.get_loc(self.fields[86][1]),
                                               df.columns.get_loc('settlement'),
                                               df.columns.get_loc(self.fields[9][1])]]].apply(
               lambda x: ', '.join(x[x!=''].astype(str)), axis=1
)
            df[self.fields[9][1]] = df.apply(lambda x: x['full_remark'], axis=1)

        if self.fields[23][2]:
            df[self.fields[23][1]] = df[self.fields[23][1]].apply(lambda x: "" if x == 5 else x)
        if self.fields[24][2]:
            df[self.fields[24][1]] = df[self.fields[24][1]].apply(lambda x: "" if x == 'Минск' else x)
        if self.fields[6][2]:
            df[self.fields[6][1]] = df[self.fields[6][1]].apply(lambda x: "" if x == 0 else x)

        if self.check_coords is True:
            df = self.do_check_coords(df)

        if self.change_id_ate is True:
            df = self.do_change_id_ate(df)

        if self.round_coords.isnumeric():
            df = self.do_round_coords(df)

        if self.decimal_format == ',':
            self.change_decimal_sep(df)

        if self.floor_for_ip is True:
            self.write_floor_for_ip(df)

        if self.porch_for_ip is True:
            self.write_porch_for_ip(df)

        if self.recount_floor is True:
            self.recount_floor_codes(df)

        if self.output_format == 1:
            self.save_to_excel(df, excel_file, self.excel_split)
        elif self.output_format == 2:
            self.save_to_csv(df, excel_file,
                             scr.default_values.csv_separator_values[self.separator_csv],
                             scr.default_values.quoting_values[self.quote_value],
                             scr.default_values.quoting_type[self.quote_type])
        elif self.output_format == 3:
            self.save_to_shp(df, excel_file)

