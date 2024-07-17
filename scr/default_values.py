import csv

fields_excel = [
    ['Полный адрес', 'FULL_ADR', False, 'str', 1, 'str', False],
    ['Уникальный идентификатор адреса', 'ADR_NUM', False, 'int64', 2, 'float', True],
    ['Код состояния адреса', 'CODE_STATUS', False, 'int64', 3, 'int:5', True],
    ['Состояние адреса', 'ADR_STATUS', False, 'str', 4, 'str:140', False],
    ['Код вида объекта недвижимого имущества', 'PROP_TYPE', False, 'int64', 5, 'int:5', True],
    ['Количество подъездов (подъезд)', 'NUM_PORCH', False, 'object', 6, 'int32', True],
    ['Количество этажей (этаж)', 'NUM_FLOOR', False, 'str', 7, 'str:20', False],
    ['Инвентарный (кадастровый) номер', 'INVNUMBER', False, 'str', 8, 'str:18', False],
    ['Почтовый индекс', 'POSTINDEX', False, 'object', 9, 'int32', True],
    ['Дополнительные сведения', 'REMARK', False, 'str', 10, 'str', False],
    ['Дата последнего редактирования адреса', 'DATE_REG', False, 'object', 11, 'date', False],
    ['Код вида работ', 'ID_SPEC', False, 'object', 12, 'int:5', True],
    ['Вид работ', 'GROUND', False, 'str', 13, 'str:100', False],
    ['Код типа документа', 'CODE_DOC', False, 'object', 14, 'int:5', True],
    ['Тип документа', 'TYPE_DOC', False, 'str', 15, 'str', False],
    ['ФИО специалиста по адресации', 'FIO', False, 'str', 16, 'str', False],
    ['Код организации специалиста по адресации', 'CODE_ORG', False, 'Int64', 17, 'int:5', True],
    ['Наименование организации специалиста по адресации', 'ORG', False, 'str', 18, 'str:160', False],
    ['Идентификатор специалиста по адресации', 'CODE_FIO', False, 'object', 19, 'int32', True],
    ['Уникальный идентификатор записи об адресе', 'ID_ADR', False, 'object', 20, 'float', True],
    ['Код актуальности адреса', 'CODE_ACTUAL', False, 'int64', 21, 'int:5', True],
    ['Актуальность адреса объекта недвижимого имущества', 'ACTUAL', False, 'str', 22, 'str:15', False],
    ['Вид объекта недвижимого имущества', 'IMM_TYPE', False, 'str', 23, 'str:70', False],
    ['Код области', 'UIDREGION', False, 'object', 24, 'int:5', True],
    ['Наименование области', 'NAMEREGION', False, 'str', 25, 'str:15', False],
    ['Наименование области на белорусском языке', 'REGIONBEL', False, 'str', 26, 'str:15', False],
    ['Код района', 'UIDDISTR', False, 'object', 27, 'int:5', True],
    ['Наименование района', 'NAMEDISTR', False, 'str', 28, 'str:20', False],
    ['Наименование района на белорусском языке', 'DISTRBEL', False, 'str', 29, 'str:20', False],
    ['Идентификатор сельсовета', 'UIDSS', False, 'object', 30, 'int32', True],
    ['Наименование сельсовета', 'NAMESS', False, 'str', 31, 'str:25', False],
    ['Наименование сельсовета на белорусском языке', 'SSBEL', False, 'str', 32, 'str:25', False],
    ['Код СОАТО АТЕ и ТЕ', 'SOATO', False, 'object', 33, 'str:10', True],
    ['Уникальный идентификатор АТЕ и ТЕ', 'ID_ATE', False, 'object', 34, 'int32', True],
    ['Актуальность кода АТЕ и ТЕ', 'ATE_ACT', False, 'int64', 35, 'int:5', True],
    ['Актуальность АТЕ и ТЕ', 'ATE_ACTUAL', False, 'str', 36, 'str:15', False],
    ['Код категории населенного пункта', 'CATEGORY', False, 'object', 37, 'int:5', True],
    ['Полное наименование категории населенного пункта', 'NAME', False, 'str', 38, 'str:55', False],
    ['Краткое наименование категории населенного пункта', 'SHORTNAME', False, 'str', 39, 'str:6', False],
    ['Наименование населенного пункта на русском языке', 'NAMEOBJECT', False, 'str', 40, 'str:110', False],
    ['Наименование населенного пункта на белорусском языке', 'NAMEOBJBEL', False, 'str', 41, 'str:100', False],
    ['Уникальный идентификатор ЭВА', 'ID_EVA', False, 'object', 42, 'int32', True],
    ['Идентификатор актуальности ЭВА', 'EVA_ACT', False, 'object', 43, 'int:5', True],
    ['Актуальность ЭВА', 'EVA_ACTUAL', False, 'str', 44, 'str:15', False],
    ['Код вида ЭВА', 'ELEMENTTYPE', False, 'object', 45, 'int:5', True],
    ['Наименование вида ЭВА на русском языке', 'ELTYPENAME', False, 'str', 46, 'str:60', False],
    ['Наименование вида ЭВА на белорусском языке', 'ELTYPENAMEBEL', False, 'str', 47, 'str:60', False],
    ['Краткое наименование вида ЭВА на русском языке', 'SHORTELTYPE', False, 'str', 48, 'str:7', False],
    ['Краткое наименование вида ЭВА на белорусском языке', 'ELTTYPESHBEL', False, 'str', 49, 'str:7', False],
    ['Наименование ЭВА на русском языке', 'EVA_NAME', False, 'str', 50, 'str:170', False],
    ['Наименование ЭВА на белорусском языке', 'ELNAMEBEL', False, 'str', 51, 'str:170', False],
    ['Километр автодороги', 'KM', False, 'object', 52, 'int:5', True],
    ['Номер КС', 'NUM_HOUSE', False, 'int64', 53, 'int:5', True],
    ['Корпус КС', 'NUM_CORP', False, 'object', 54, 'int32', True],
    ['Индекс КС', 'IND_HOUSE', False, 'str', 55, 'str:4', False],
    ['Блок', 'BLOCK', False, 'object', 56, 'int:5'],
    ['Идентификатор специальной отметки', 'ID_OTM', False, 'object', 57, 'int:5'],
    ['Специальная отметка', 'OTMETKA', False, 'str', 58, 'str:20'],
    ['Номер ИП', 'NUM_ROOM', False, 'object', 59, 'int:5'],
    ['Индекс ИП', 'IND_ROOM', False, 'str', 60, 'str:4'],
    ['Код назначения недвижимого имущества', 'CODE_PURP', False, 'object', 61, 'int:5'],
    ['Назначение недвижимого имущества', 'PURPOSE', False, 'str', 62, 'str:9'],
    ['Номер зоны (СК 1963)', 'ZONE_NUMB', False, 'object', 63, 'int:5'],
    ['Координата X (СК 1963)', 'X_63', False, 'object', 64, 'float'],
    ['Координата Y (СК 1963)', 'Y_63', False, 'object', 65, 'float'],
    ['Широта (WGS 1984)', 'XCOORD', False, 'object', 66, 'float'],
    ['Долгота (WGS 1984)', 'YCOORD', False, 'object', 67, 'float'],
    ['Координата X (СК 1942)', 'XCK42', False, 'object', 68, 'float'],
    ['Координата Y (СК 1942)', 'YCK42', False, 'object', 69, 'float'],
    ['Дата регистрации создания адреса', 'DATE_CREATE', False, 'object', 70, 'date'],
    ['Дата упразднения', 'DATE_ANNUL', False, 'str', 71, 'date'],
    ['Орган. док', 'DOC_STATE', False, 'str', 72, 'str'],
    ['Дата документа', 'DOC_DATE', False, 'str', 73, 'date'],
    ['Номер документа', 'DOC_NUM', False, 'str', 74, 'str'],
    ['Примечание документа', 'DOC_REMARK', False, 'str', 75, 'str'],
    ['Должность специалиста по адресации', 'POSITION_SPEC', False, 'str', 76, 'str'],
    ['Родительское КС (для ЗУ)', 'PARENT', False, 'str', 77, 'str'],
    ['Индекс корпуса (для гаража)', 'IND_BY_CORP', False, 'object', 78, 'int32'],
    ['ID подтипа работ в модуле "Контроль целостности"', 'ID_KC', False, 'object', 79, 'int:5'],
    ['Количество ИП', 'COUNT_IP', False, "object", 80, "int32"],
    ['Количество ММ', 'COUNT_MM', False, "object", 81, "int32"],
    ['Количество ИП_ММ', 'COUNT_IP_MM', False, "object", 82, "int32"],
    ['Уникальный идентификатор наименования ЭВА', 'NAMEUID', False, "object", 83, "int32"],
    ['Родительское КС (для ИП)', 'PARENT_KS', False, "object", 84, "int32"],
    ["Полное наименование категории населенного пункта на белорусском языке", "NAME_BY", False, "object", 85, "str:55"],
    ["Краткое наименование категории населенного пункта на белорусском языке", "SHNAME_BY", False, "object", 86, "str:6"],
    ["Район в городе", "IN_DIST_NAM", False, "object", 87, "str"],
    ["Наименование гаражного кооператива", "GARAGE_IAE_NAME", False, "object", 88, "str"],
    ["Наименование ближайшего населенного пункта", "NEAREST_SETTLEMENT_NAME", False, "object", 89, "str"],

]


prj_data = {
    "WGS 84": 'GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]',
    "CK-63 (1)": 'PROJCS["CK1963(c)1",GEOGCS["GCS_Pulkovo_1942",DATUM["D_Pulkovo_1942",SPHEROID["Krasovsky_1940",6378245,298.3]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",1250000],PARAMETER["False_Northing",-12900.568],PARAMETER["Central_Meridian",24.95],PARAMETER["Scale_Factor",1],PARAMETER["Latitude_Of_Origin",-0.01666666666],UNIT["Meter",1]]',
    "CK-63 (2)": 'PROJCS["CK1963(c)2",GEOGCS["GCS_Pulkovo_1942",DATUM["D_Pulkovo_1942",SPHEROID["Krasovsky_1940",6378245,298.3]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",2250000],PARAMETER["False_Northing",-12900.568],PARAMETER["Central_Meridian",27.95],PARAMETER["Scale_Factor",1],PARAMETER["Latitude_Of_Origin",-0.01666666666],UNIT["Meter",1]]',
    "CK-63 (3)": 'PROJCS["CK1963(c)3",GEOGCS["GCS_Pulkovo_1942",DATUM["D_Pulkovo_1942",SPHEROID["Krasovsky_1940",6378245,298.3]],PRIMEM["Greenwich",0],UNIT["Degree",0.017453292519943295]],PROJECTION["Gauss_Kruger"],PARAMETER["False_Easting",3250000],PARAMETER["False_Northing",-12900.568],PARAMETER["Central_Meridian",30.95],PARAMETER["Scale_Factor",1],PARAMETER["Latitude_Of_Origin",-0.01666666666],UNIT["Meter",1]]'
}

csv_delimeter_values = {
    'Запятая': ',',
    'Точка': '.'
}

csv_separator_values = {
    'Точка с запятой': ';',
    'Табуляция': '\t',
    'Вертикальная черта': '|'
}

quoting_values = {
    'Нет': csv.QUOTE_NONE,
    'Только текст': csv.QUOTE_NONNUMERIC,
    'Все': csv.QUOTE_ALL
}

quoting_type = {
    'Двойные': '"',
    'Одиночные': "'"
}

floor_name = {
    1: '1-й',
    2: '2-й',
    3: '3-й',
    4: '4-й',
    5: '5-й',
    6: '6-й',
    7: '7-й',
    8: '8-й',
    9: '9-й',
    10: '10-й',
    11: '11-й',
    12: '12-й',
    13: '13-й',
    14: '14-й',
    15: '15-й',
    16: '16-й',
    17: '17-й',
    18: '18-й',
    19: '19-й',
    20: '20-й',
    21: '21-й',
    22: '22-й',
    23: '23-й',
    24: '24-й',
    25: '25-й',
    26: '26-й',
    27: '27-й',
    28: '28-й',
    29: '29-й',
    30: '30-й',
    31: '31-й',
    32: '32-й',
    33: '33-й',
    34: '34-й',
    35: '35-й',
    36: '36-й',
    37: '37-й',
    38: '38-й',
    39: '39-й',
    40: '40-й',
    41: '41-й',
    42: '42-й',
    43: '43-й',
    44: '44-й',
    45: '45-й',
    46: '46-й',
    47: '47-й',
    48: '48-й',
    49: '49-й',
    50: '50-й',
    51: '51-й',
    52: '52-й',
    53: '53-й',
    54: '54-й',
    55: '55-й',
    56: '56-й',
    57: '57-й',
    58: '58-й',
    59: '59-й',
    60: '60-й',
    61: '61-й',
    62: '62-й',
    63: '63-й',
    64: '64-й',
    65: '65-й',
    66: '66-й',
    67: '67-й',
    68: '68-й',
    69: '69-й',
    70: '70-й',
    71: '71-й',
    72: '72-й',
    73: '73-й',
    74: '74-й',
    75: '75-й',
    76: '76-й',
    77: '77-й',
    78: '78-й',
    79: '79-й',
    80: '80-й',
    81: '81-й',
    82: '82-й',
    83: '83-й',
    84: '84-й',
    85: '85-й',
    86: '86-й',
    87: '87-й',
    88: '88-й',
    89: '89-й',
    90: '90-й',
    91: '91-й',
    92: '92-й',
    93: '93-й',
    94: '94-й',
    95: '95-й',
    96: '96-й',
    97: '97-й',
    98: '98-й ',
    99: '99-й',
    100: '100-й',
    199: '199-й',
    200: 'Мансардный (мансарда)',
    201: 'Антресоль',
    202: 'Мезонин',
    203: 'Чердак',
    -1: '1-й подземный',
    -2: '2-й подземный',
    -3: '3-й подземный',
    -4: '4-й подземный',
    -5: '5-й подземный',
    -6: '6-й подземный',
    -7: '7-й подземный',
    -8: '8-й подземный',
    -9: '9-й подземный',
    -10: '10-й подземный',
    -11: '11-й подземный',
    -12: '12-й подземный',
    -13: '13-й подземный',
    -14: '14-й подземный',
    -15: '15-й подземный',
    -16: '16-й подземный',
    -17: '17-й подземный',
    -18: '18-й подземный',
    -19: '19-й подземный',
    -20: '20-й подземный',
    -21: '21-й подземный',
    -22: '22-й подземный',
    -23: '23-й подземный',
    -24: '24-й подземный',
    -25: '25-й подземный',
    -26: '26-й подземный',
    -27: '27-й подземный',
    -28: '28-й подземный',
    -29: '29-й подземный',
    -30: '30-й подземный',
    -100: 'Подвальный',
    -101: 'Цокольный',
    204: 'Технический чердак',
    205: 'Наземный цокольный',
    206: 'Техническое подполье'
}