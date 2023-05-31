import json
import os
import pandas as pd
import geopandas as gpd

"""
Настройка полей для обработки и формирования конечных файлов (описаны все доступные для выгрузки поля)
1 - название поля в выгруженном эксель файле из Реестра Адресов - !!!НЕ ИЗМЕНЯТЬ
2 - название поля в итоговом файле
3 - присутствует ли данное поле в выгруженном файле (True - присутствует, False - отсутствует)
4 - тип поля - !!!НЕ ИЗМЕНЯТЬ
5 - порядок полей в итоговом файле
"""

fields_excel = [['Полный адрес', 'FULL_ADR', False, 'str', 0, 'str'],
     ['Уникальный идентификатор адреса', 'ADR_NUM', True, 'int64', 1, 'float'],
     ['Код состояния адреса', 'CODE_STATUS', False, 'int64', 0, 'int:5'],
     ['Состояние адреса', 'ADR_STATUS', True, 'str', 2, 'str:140'],
     ['Код вида объекта недвижимого имущества', 'PROP_TYPE', False, 'int64', 0, 'int:5'],
     ['Количество подъездов (подъезд)', 'NUM_PORCH', True, 'object', 24, 'int32'],
     ['Количество этажей (этаж)', 'NUM_FLOOR', True, 'object', 25, 'str:20'],
     ['Инвентарный (кадастровый) номер', 'INVNUMBER', True, 'str', 26, 'str:18'],
     ['Почтовый индекс', 'POSTINDEX', True, 'object', 28, 'int32'],
     ['Дополнительные сведения', 'REMARK', True, 'str', 29, 'str'],
     ['Дата последнего редактирования адреса', 'DATE_REG', True, 'str', 33, 'date'],
     ['Код вида работ', 'ID_SPEC', False, 'object', 0, 'int:5'],
     ['Вид работ', 'GROUND', True, 'str', 34, 'str:100'],
     ['Код типа документа', 'CODE_DOC', False, 'object', 0, 'int:5'],
     ['Тип документа', 'TYPE_DOC', False, 'str', 0, 'str'],
     ['ФИО специалиста по адресации', 'FIO', False, 'str', 0, 'str'],
     ['Код организации специалиста по адресации', 'CODE_ORG', False, 'Int64', 0, 'int:5'],
     ['Наименование организации специалиста по адресации', 'ORG', False, 'str', 0, 'str:160'],
     ['Идентификатор специалиста по адресации', 'CODE_FIO', False, 'object', 0, 'int32'],
     ['Уникальный идентификатор записи об адресе', 'ID_ADR', False, 'object', 0, 'float'],
     ['Код актуальности адреса', 'CODE_ACTUAL', False, 'int64', 0, 'int:5'],
     ['Актуальность адреса объекта недвижимого имущества', 'ACTUAL', False, 'str', 0, 'str:15'],
     ['Вид объекта недвижимого имущества', 'IMM_TYPE', True, 'str', 3, 'str:70'],
     ['Код области', 'UIDREGION', False, 'object', 0, 'int:5'],
     ['Наименование области', 'NAMEREGION', True, 'str', 4, 'str:15'],
     ['Наименование области на белорусском языке', 'REGIONBEL', False, 'str', 0, 'str:15'],
     ['Код района', 'UIDDISTR', False, 'object', 0, 'int:5'],
     ['Наименование района', 'NAMEDISTR', True, 'str', 5, 'str:20'],
     ['Наименование района на белорусском языке', 'DISTRBEL', False, 'str', 0, 'str:20'],
     ['Идентификатор сельсовета', 'UIDSS', False, 'object', 0, 'int32'],
     ['Наименование сельсовета', 'NAMESS', True, 'str', 6, 'str:25'],
     ['Наименование сельсовета на белорусском языке', 'SSBEL', False, 'str', 0, 'str:25'],
     ['Код СОАТО АТЕ и ТЕ', 'SOATO', True, 'object', 7, 'str:10'],
     ['Уникальный идентификатор АТЕ и ТЕ', 'ID_ATE', True, 'object', 8, 'int32'],
     ['Актуальность кода АТЕ и ТЕ', 'ATE_ACT', False, 'int64', 0, 'int:5'],
     ['Актуальность АТЕ и ТЕ', 'ATE_ACTUAL', True, 'str', 9, 'str:15'],
     ['Код категории населенного пункта', 'CATEGORY', False, 'object', 0, 'int:5'],
     ['Полное наименование категории населенного пункта', 'NAME', False, 'str', 0, 'str:55'],
     ['Краткое наименование категории населенного пункта', 'SHORTNAME', True, 'str', 10, 'str:6'],
     ['Наименование населенного пункта на русском языке', 'NAMEOBJECT', True, 'str', 11, 'str:110'],
     ['Наименование населенного пункта на белорусском языке', 'NAMEOBJBEL', False, 'str', 0, 'str:100'],
     ['Уникальный идентификатор ЭВА', 'ID_EVA', True, 'object', 12, 'int32'],
     ['Идентификатор актуальности ЭВА', 'EVA_ACT', False, 'object', 0, 'int:5'],
     ['Актуальность ЭВА', 'EVA_ACTUAL', True, 'str', 13, 'str:15'],
     ['Код вида ЭВА', 'ELEMENTTYPE', False, 'object', 0, 'int:5'],
     ['Наименование вида ЭВА на русском языке', 'ELTYPENAME', False, 'str', 0, 'str:60'],
     ['Наименование вида ЭВА на белорусском языке', 'ELTYPENAMEBEL', False, 'str', 0, 'str:60'],
     ['Краткое наименование вида ЭВА на русском языке', 'SHORTELTYPE', True, 'str', 14, 'str:7'],
     ['Краткое наименование вида ЭВА на белорусском языке', 'ELTTYPESHBEL', False, 'str', 0, 'str:7'],
     ['Наименование ЭВА на русском языке', 'EVA_NAME', True, 'str', 15, 'str:170'],
     ['Наименование ЭВА на белорусском языке', 'ELNAMEBEL', False, 'str', 0, 'str:170'],
     ['Километр автодороги', 'KM', True, 'object', 16, 'int:5'],
     ['Номер КС', 'NUM_HOUSE', True, 'int64', 17, 'int:5'],
     ['Корпус КС', 'NUM_CORP', True, 'object', 18, 'int32'],
     ['Индекс КС', 'IND_HOUSE', True, 'str', 19, 'str:4'],
     ['Блок', 'BLOCK', True, 'object', 20, 'int:5'],
     ['Идентификатор специальной отметки', 'ID_OTM', False, 'object', 0, 'int:5'],
     ['Специальная отметка', 'OTMETKA', True, 'str', 21, 'str:20'],
     ['Номер ИП', 'NUM_ROOM', True, 'object', 22, 'int:5'],
     ['Индекс ИП', 'IND_ROOM', True, 'str', 23, 'str:4'],
     ['Код назначения недвижимого имущества', 'CODE_PURP', False, 'object', 0, 'int:5'],
     ['Назначение недвижимого имущества', 'PURPOSE', True, 'str', 27, 'str:9'],
     ['Номер зоны (СК 1963)', 'ZONE_NUMB', False, 'object', 0, 'int:5'],
     ['Координата X (СК 1963)', 'X_63', True, 'object', 30, 'float'],
     ['Координата Y (СК 1963)', 'Y_63', True, 'object', 31, 'float'],
     ['Широта (WGS 1984)', 'XCOORD', False, 'object', 0, 'float'],
     ['Долгота (WGS 1984)', 'YCOORD', False, 'object', 0, 'float'],
     ['Координата X (СК 1942)', 'XCK42', False, 'object', 0, 'float'],
     ['Координата Y (СК 1942)', 'YCK42', False, 'object', 0, 'float'],
     ['Дата регистрации создания адреса', 'DATE_CREATE', True, 'str', 32, 'date'],
     ['Дата упразднения', 'DATE_ANNUL', False, 'object', 0, 'date'],
     ['Орган. док', 'DOC_STATE', False, 'str', 0, 'str'],
     ['Дата документа', 'DOC_DATE', False, 'object', 0, 'date'],
     ['Номер документа', 'DOC_NUM', False, 'str', 0, 'str'],
     ['Примечание документа', 'DOC_REMARK', False, 'str', 0, 'str'],
     ['Должность специалиста по адресации', 'POSITION_SPEC', False, 'str', 0, 'str'],
     ['Родительское КС (для ЗУ)', 'PARENT', False, 'str', 0, 'str'],
     ['ID подтипа работ в модуле "Контроль целостности"', 'ID_KC', False, 'object', 0, 'int:5'],
     ['Наименование гаражного кооператива', 'GARAGE_IAE_NAME', True, 'object', 35, 'str'],
     ['Наименование ближайшего населенного пункта', 'NEAREST_SETTLEMENT_NAME', True, 'object', 36, 'str']]

class AddressFiles(object):
    def __init__(self, download_folder, final_folder, output_format, check_coords, change_id_ate,
                 round_coords, fields, sk=1, maska_file=""):
        self.download_folder = download_folder
        self.final_folder = final_folder
        self.maska_file = maska_file
        self.output_format = output_format
        self.check_coords = check_coords
        self.change_id_ate = change_id_ate
        self.round_coords = round_coords
        self.fields = fields
        self.sk = sk

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
                    final_order[field] == fields_excel[78][1] or final_order[field] == fields_excel[79][1]:
                final_order.pop(field)
        return header, types, final_order, types_shp

    def do_round_coords(self, dataframe):
        """
        Функция округляет значения координат, до указанного в параметрах класса "round_coords" значения
        """
        xy = None
        if self.sk == 1:
            xy = (65, 66)
        elif self.sk == 2:
            xy = (63, 64)
        if self.fields[65][2] and self.fields[66][2]:
            dataframe[self.fields[xy[0]][1]] = dataframe[self.fields[xy[0]][1]].apply(
                lambda x: round(float(x), self.round_coords) if x != '' else x)
            dataframe[self.fields[xy[1]][1]] = dataframe[self.fields[xy[1]][1]].apply(
                lambda x: round(float(x), self.round_coords) if x != '' else x)
        return dataframe

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
        data_regions = gpd.read_file(self.maska_file)
        df_coord = dataframe[dataframe[self.fields[xy[0]][1]] != ""]
        if self.fields[33][2]:
            object_number_check = None
            with open("scr/objectnumbers.json", 'r') as reader:
                object_number_check = json.loads(reader.read())
            to_gdf = gpd.GeoDataFrame(df_coord,
                                      geometry=gpd.points_from_xy(df_coord[self.fields[xy[0]][1]],
                                                                  df_coord[self.fields[xy[1]][1]]),
                                      columns=[self.fields[33][1]])
            intersect = to_gdf.sjoin(data_regions, how='inner')
            intersect['ID_DISTR_VALUES'] = intersect.apply(lambda x:
                                                           True if int(x[self.fields[33][1]])
                                                                   in object_number_check[int(x['IDDISTRICT'])]
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
        geo_dataframe.to_file(os.path.join(self.final_folder, name[:-4]) + '.shp', driver='ESRI Shapefile',
                              encoding='utf-8', schema=schema, index=False)

    def save_to_excel(self, dataframe, name):
        """
        Функция сохраняет обработанную таблицу в формат excel
        """

        if dataframe.shape[0] <= 1048575:
            with pd.ExcelWriter(os.path.join(self.final_folder, name[:-4]) + '.xlsx',
                                datetime_format='DD.MM.YYYY', engine='xlsxwriter', options={'strings_to_numbers': True}) as writter:
                dataframe.to_excel(writter, na_rep="", columns=self.get_fields()[2], index=False)
        else:
            for sheet in range((dataframe.shape[0] - 1) // 1048575 + 1):
                df_for_save = dataframe[0 + 1048575 * sheet:1048575 * (sheet + 1)]
                with pd.ExcelWriter(os.path.join(self.final_folder, name[:-4]) + '{0}.xlsx'.format(sheet + 1),
                                    datetime_format='DD.MM.YYYY', engine='xlsxwriter', options={'strings_to_numbers': True}) as writter:
                    df_for_save.to_excel(writter, na_rep="", columns=self.get_fields()[2], index=False)

    def save_to_csv(self, dataframe, file_name):
        """
        Функция сохраняет обработанную таблицу в формат csv
        """
        dataframe[self.fields[9][1]] = dataframe[self.fields[9][1]].str.replace(';', '_')
        dataframe[self.fields[9][1]] = dataframe[self.fields[9][1]].str.replace(r'\n', ' ', regex=True)
        dataframe.to_csv(os.path.join(self.final_folder, file_name[:-4]) + '_temp.csv', sep=';',
                         index=False, date_format='%d.%m.%Y', columns=self.get_fields()[2], encoding='utf-8')
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
        if fields_excel[10][2]:
            for_dates_parse.append(names.index(fields_excel[10][1]))
        if fields_excel[69][2]:
            for_dates_parse.append(names.index(fields_excel[69][1]))
        if fields_excel[70][2]:
            for_dates_parse.append(names.index(fields_excel[70][1]))
        if fields_excel[72][2]:
            for_dates_parse.append(names.index(fields_excel[72][1]))
        if len(for_dates_parse) == 0:
            for_dates_parse = False
        df = pd.read_csv(file_name, sep=";", dtype=dict(zip(names, types)), na_filter=False, names=names,
                         encoding='utf-8', header=0, parse_dates=for_dates_parse)

        if self.fields[9][2]:
            df['full_block'] = df.apply(lambda x: 'блок ' + str(x[self.fields[55][1]]) if x[self.fields[55][1]] != ''
            else "", axis=1)
            df['settlement'] = df.apply(lambda x: 'вблизи ' + x[self.fields[79][1]] if x[self.fields[79][1]] != ''
            else "", axis=1)


            df['full_remark'] = df[df.columns[[df.columns.get_loc('full_block'),
                                               df.columns.get_loc(self.fields[78][1]),
                                               df.columns.get_loc('settlement'),
                                               df.columns.get_loc(self.fields[9][1])]]].apply(
               lambda x: ', '.join(x[x!=''].astype(str)), axis=1
)
            df[self.fields[9][1]] = df.apply(lambda x: x['full_remark'], axis=1)

        if self.fields[23][2]:
            df[self.fields[23][1]] = df[self.fields[23][1]].apply(lambda x: "" if x == 5 else x)
        if self.fields[24][2]:
            df[self.fields[24][1]] = df[self.fields[24][1]].apply(lambda x: "" if x == 'Минск' else x)

        if self.check_coords is True:
            df = self.do_check_coords(df)

        if self.change_id_ate is True:
            df = self.do_change_id_ate(df)

        if self.round_coords is not False:
            df = self.do_round_coords(df)

        if self.output_format == 1:
            self.save_to_excel(df, excel_file)
        elif self.output_format == 2:
            self.save_to_csv(df, excel_file)
        elif self.output_format == 3:
            self.save_to_shp(df, excel_file)


def main():
    AddressFiles(download_folder=r'D:\test\2_6\cut',  # Папка со скачанными эксель файлами
                 final_folder=r'D:\test\2_6\готово',  # Папка для сохранения итоговых файлов
                 maska_file=r'd:\my_scripts\maska\district_maska_84_1.shp', # Файл с границами районов//городов областного подчинения для проверки координат (в файле обязательно поле "NAMEOBJECT" - наименование объекта)
                 output_format=3,  # Формат сохранения итоговых файлов (1-excel, 2-csv, 3-shp)
                 check_coords=False,  # Проверка корректности координат (True - выполняется, False - не выполняется)
                 change_id_ate=False, # Замена значения "Уникальный идентификатор АТЕ и ТЕ" на "Уникальный идентификатор населённого пункта" (True - выполняется, False - не выполняется)
                 round_coords=5, # Округление координат (Цифра - количество знаков после запятой, функция выполняется; False - не выполняется)
                 sk=2,  # Система координат для проверки координат и/или формирования шейпа(1 - WGS 84, 2-CK63)
                 fields=fields_excel)
        # .processing_data('Россонский-2023-05-26-2998.csv')  # Ссылка на переменную с настроенными данными по полям


if __name__ == '__main__':
    main()