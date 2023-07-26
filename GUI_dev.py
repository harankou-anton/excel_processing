import json
import os
import threading
import sys
from tkinter import *
from tkinter import filedialog
from tkinter.ttk import Combobox, Checkbutton, Radiobutton
from scr.RA_template2_8 import AddressFiles



# Тупо для иконки в exe
def resource_path2(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


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
    ['Блок', 'BLOCK', False, 'object', 77, 'int:5', True],
    ['Идентификатор специальной отметки', 'ID_OTM', False, 'object', 56, 'int:5', True],
    ['Специальная отметка', 'OTMETKA', False, 'str', 78, 'str:20', False],
    ['Номер ИП', 'NUM_ROOM', False, 'object', 57, 'int:5', True],
    ['Индекс ИП', 'IND_ROOM', False, 'str', 58, 'str:4', False],
    ['Код назначения недвижимого имущества', 'CODE_PURP', False, 'object', 59, 'int:5', True],
    ['Назначение недвижимого имущества', 'PURPOSE', False, 'str', 60, 'str:9', False],
    ['Номер зоны (СК 1963)', 'ZONE_NUMB', False, 'object', 61, 'int:5', True],
    ['Координата X (СК 1963)', 'X_63', False, 'object', 62, 'float', True],
    ['Координата Y (СК 1963)', 'Y_63', False, 'object', 63, 'float', True],
    ['Широта (WGS 1984)', 'XCOORD', False, 'object', 64, 'float', True],
    ['Долгота (WGS 1984)', 'YCOORD', False, 'object', 65, 'float', True],
    ['Координата X (СК 1942)', 'XCK42', False, 'object', 66, 'float', True],
    ['Координата Y (СК 1942)', 'YCK42', False, 'object', 67, 'float', True],
    ['Дата регистрации создания адреса', 'DATE_CREATE', False, 'object', 68, 'date', False],
    ['Дата упразднения', 'DATE_ANNUL', False, 'str', 69, 'date', False],
    ['Орган. док', 'DOC_STATE', False, 'str', 70, 'str', False],
    ['Дата документа', 'DOC_DATE', False, 'str', 71, 'date', False],
    ['Номер документа', 'DOC_NUM', False, 'str', 72, 'str', False],
    ['Примечание документа', 'DOC_REMARK', False, 'str', 73, 'str', False],
    ['Должность специалиста по адресации', 'POSITION_SPEC', False, 'str', 74, 'str', False],
    ['Родительское КС (для ЗУ)', 'PARENT', False, 'str', 75, 'str', False],
    ['ID подтипа работ в модуле "Контроль целостности"', 'ID_KC', False, 'object', 76, 'int:5', True],
    ["Наименование гаражного кооператива", "GARAGE_IAE_NAME", False, "object", 77, "str", False],
   ["Наименование ближайшего населенного пункта", "NEAREST_SETTLEMENT_NAME", False, "object", 78, "str", False],
]

current_file = ''
previous_file = ''
error_message = ''

window = Tk()
window.title('RA Excel Processing ver 0.5')
window.geometry('1140x630')
window.resizable(False, False)
path_image = resource_path2('favicon.png')
photo = PhotoImage(file=path_image)
window.iconphoto(False, photo)


def choose_download_folder():
    folder_name = filedialog.askdirectory()
    if folder_name != '':
        download_folder_path.delete(0, END)
        download_folder_path.insert(0, folder_name)


def choose_final_folder():
    folder_name = filedialog.askdirectory()
    if folder_name != '':
        final_folder_path.delete(0, END)
        final_folder_path.insert(0, folder_name)


def validate(symbol):
    return symbol.isdigit()


def choose_maska_file():
    file_name = filedialog.askopenfilename(defaultextension='.shp', filetypes=[("Shape File", '*.shp')])
    if file_name != '':
        maska_label_path.delete(0, END)
        maska_label_path.insert(0, file_name)


def sk_button(*args):
    if output_formats.current() == 2 or checkbox_ate.get() is True:
        wgs_btn.config(state='normal')
        sk_btn.config(state='normal')
    else:
        wgs_btn.config(state='disable')
        sk_btn.config(state='disable')


def float_format(*args):
    if output_formats.current() == 1:
        decimal_format.config(state='normal')
    else:
        decimal_format.config(state='disable')


def disable_enable_button(*args):
    sk_button()
    if checkbox_ate.get() is True:
        maska_label_button.config(state='normal')
    else:
        maska_label_button.config(state='disabled')
        maska_label_path.delete(0, END)


def disable_enable_button_round(*args):
    if checkbox_round_coords.get() is True:
        fill_round_entry.config(state='normal')
    else:
        fill_round_entry.config(state='disabled')


def update_fields_excel():
    for row in range(len(fields_excel)):
        fields_excel[row][1] = inner_frame.grid_slaves(row, 2)[0].get()
        fields_excel[row][2] = list_checkboxes[row].get()
        if inner_frame.grid_slaves(row, 3)[0].get() == "":
            fields_excel[row][4] = 0
        else:
            fields_excel[row][4] = int(inner_frame.grid_slaves(row, 3)[0].get())


def save_pattern():
    update_fields_excel()
    json_dump = json.dumps(fields_excel, ensure_ascii=False)
    save_file = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[("Json Files", '*.json')])
    with open(save_file, 'w', encoding='utf-8') as writter:
        writter.write(json_dump)


def upload_pattern():
    upload_file = filedialog.askopenfilename(defaultextension='.json', filetypes=[("Json Files", '*.json')])
    if upload_file != '':
        with open(upload_file, 'r', encoding='utf-8') as reader:
            get_fields_names = json.loads(reader.read())
            for row in range(len(get_fields_names)):
                list_checkboxes[row].set(get_fields_names[row][2])
                if list_checkboxes[row].get() is True:
                    inner_frame.grid_slaves(row, 2)[0].config(state=NORMAL)
                    inner_frame.grid_slaves(row, 3)[0].config(state=NORMAL)
                    inner_frame.grid_slaves(row, 2)[0].delete(0, END)
                    inner_frame.grid_slaves(row, 2)[0].insert(0, get_fields_names[row][1])
                    if get_fields_names[row][4] != 0:
                        inner_frame.grid_slaves(row, 3)[0].delete(0, END)
                        inner_frame.grid_slaves(row, 3)[0].insert(0, get_fields_names[row][4])
                    else:
                        inner_frame.grid_slaves(row, 3)[0].delete(0, END)
                else:
                    inner_frame.grid_slaves(row, 3)[0].delete(0, END)
                    inner_frame.grid_slaves(row, 2)[0].config(state=DISABLED)
                    inner_frame.grid_slaves(row, 3)[0].config(state=DISABLED)


def run_instrument():
    global current_file
    global error_message
    update_fields_excel()
    df = download_folder_path.get()
    ff = final_folder_path.get()
    output = output_formats['values'].index(f'{output_formats.get()}')+1
    check_coords = checkbox_ate.get()
    id_ate = checkbox_id_ate.get()
    sk_get = def_variable.get()
    dec = '.'
    if decimal_format.get() == 'Запятая':
        dec = ','
    if checkbox_round_coords.get() is False:
        round_coords = False
    else:
        round_coords = int(fill_round_entry.get())
    maska_file = maska_label_path.get()
    for csv_file in os.listdir(df):
        if csv_file[-4:] == '.csv':
            try:
                AddressFiles(download_folder=df, final_folder=ff, output_format=output, check_coords=check_coords,
                             change_id_ate=id_ate, round_coords=round_coords, sk=sk_get, decimal_format=dec,
                             fields=fields_excel, maska_file=maska_file).processing_data(csv_file)
                current_file = csv_file
            except Exception as error:
                error_message = repr(error)
                current_file = csv_file


def check_state(func):
    window.after(1000, check_if_done, func)


def check_if_done(r_i):
    global previous_file
    global error_message
    global current_file
    if not r_i.is_alive():
        start_button['text'] = 'Старт'
        start_button['state'] = 'normal'
        start_button['bg'] = '#54C571'

        if error_message == "":
            logger_window.insert(0.0, f'--Файл {current_file} обработан успешно\n')
        elif error_message == "ValueError('Number of passed names did not match number of header fields in the file')":
            logger_window.insert(0.0, f'--Не удалось обработать файл {current_file}. '
                                      f'Количество отмеченных полей и полей в файле не совпадает\n')
        elif "ValueError('Unable to convert" in error_message:
            logger_window.insert(0.0, f'--Не удалось обработать файл {current_file}. '
                                      f'Отмеченные поля и поля исходного файла не совпадают\n')
        else:
            logger_window.insert(0.0, f'--Не удалось обработать файл {current_file}. Ошибка {error_message}\n')
        logger_window.insert(0.0, '--Обработка завершена\n')
        current_file = ''
        previous_file = ''
        error_message = ''
    else:
        if previous_file != current_file and error_message == '':
            previous_file = current_file
            logger_window.insert(0.0, f'--Файл {previous_file} обработан успешно\n')
        elif previous_file != current_file and error_message != '':
            previous_file = current_file
            if error_message == "ValueError('Number of passed names did not match number of header fields in the file')":
                logger_window.insert(0.0, f'--Не удалось обработать файл {previous_file}. '
                                          f'Количество отмеченных полей и полей в файле не совпадает\n')
            elif "ValueError('Unable to convert" in error_message:
                logger_window.insert(0.0, f'--Не удалось обработать файл {previous_file}. '
                                          f'Отмеченные поля и поля исходного файла не совпадают\n')
            else:
                logger_window.insert(0.0, f'--Не удалось обработать файл {previous_file}. Ошибка {error_message}\n')
            error_message = ''

        check_state(r_i)


def table_disable_enable(*args):
    for num, button in enumerate(list_checkboxes):
        if button.get() is True:
            inner_frame.grid_slaves(row=num, column=2)[0].config(state=NORMAL)
            inner_frame.grid_slaves(row=num, column=3)[0].config(state=NORMAL)
        else:
            inner_frame.grid_slaves(row=num, column=3)[0].delete(0, END)
            inner_frame.grid_slaves(row=num, column=2)[0].config(state=DISABLED)
            inner_frame.grid_slaves(row=num, column=3)[0].config(state=DISABLED)


def start_button_func():
    if download_folder_path.get() == '':
        logger_window.insert(0.0, '--Не указана "Папка с исходниками"\n')
        return
    if final_folder_path.get() == '':
        logger_window.insert(0.0, '--Не указана "Итоговая папка"\n')
        return
    if checkbox_ate.get() is True and maska_label_path.get() == '':
        logger_window.insert(0.0, '--Не выбран "Файл маска" для проверки координат\n')
        return
    if checkbox_round_coords.get() is True and fill_round_entry.get() == '':
        logger_window.insert(0.0, '--Не указано значение "Округление координат"\n')
        return
    if checkbox_ate.get() is True and (list_checkboxes[27].get() is False and list_checkboxes[39].get() is False) and \
            list_checkboxes[33].get() is False:
        logger_window.insert(0.0, '--Для проверки координат должны быть отмечены и присутствовать в исходном файле '
                                  'поля "Наименование района" + "Наименование населенного пункта на русском языке" или '
                                  '"Уникальный идентификатор населённого пункта"\n')
        return
    numbers = {}
    for num, check_position in enumerate(list_checkboxes):
        if check_position.get() is True:
            if inner_frame.grid_slaves(row=num, column=3)[0].get() == '':
                logger_window.insert(
                    0.0, f'--Не указана позиция для поля {inner_frame.grid_slaves(row=num, column=1)[0]["text"]}\n')
                return

            if inner_frame.grid_slaves(row=num, column=3)[0].get() not in numbers:
                numbers[inner_frame.grid_slaves(row=num, column=3)[0].get()] = inner_frame.grid_slaves(
                    row=num, column=1)[0]['text']
            else:
                logger_window.insert(0.0, f'--Указана одиноковая позиция для полей '
                                          f'"{numbers[inner_frame.grid_slaves(row=num, column=3)[0].get()]}" и '
                                          f'"{inner_frame.grid_slaves(row=num, column=1)[0]["text"]}"\n')
                return

    start_button['text'] = 'Выполняется...'
    start_button['state'] = 'disable'
    start_button['bg'] = '#FF7F50'
    r_i = threading.Thread(target=run_instrument)
    r_i.start()
    check_state(r_i)


validate_digits = window.register(validate)

# Исходная папка
download_folder_label = Label(window, text='Папка с исходниками', font=("Georgia", 11), width=22)
download_folder_button = Button(window, text="Выбрать", command=choose_download_folder, font=("Georgia", 8))
download_folder_label.grid(column=0, row=0, sticky=W,)
download_folder_button.grid(column=1, row=0, pady=2)
download_folder_path = Entry(window, width=20, font=("Georgia", 8))
download_folder_path.grid(column=2, row=0, sticky=W, pady=2, padx=5)

# Конечная папка
final_folder_label = Label(window, text='Итоговая папка', font=("Georgia", 11), width=22)
final_folder_button = Button(window, text="Выбрать", command=choose_final_folder, font=("Georgia", 8))
final_folder_label.grid(column=0, row=1, sticky=W)
final_folder_button.grid(column=1, row=1, pady=2)
final_folder_path = Entry(window, width=20, font=("Georgia", 8))
final_folder_path.grid(column=2, row=1, sticky=W, pady=2, padx=5)

# Выходной формат
output_format_label = Label(window, text='Выходной формат', font=("Georgia", 11), width=22)
output_format_label.grid(column=0, row=2, sticky=W)
output_formats = Combobox(window, width=6, font=("Georgia", 8))
output_formats['values'] = ('Excel', 'CSV', 'Shape')
output_formats.current(0)
output_formats.grid(column=1, row=2, pady=2)
output_formats.bind("<<ComboboxSelected>>", float_format, add='+')
output_formats.bind("<<ComboboxSelected>>", sk_button, add='+')


# Система координат
wgs = 'WGS 84'
sk = 'CK-63'
def_variable = IntVar(value=1)
wgs_btn = Radiobutton(window, text=wgs, value=1, variable=def_variable, state='disable')
wgs_btn.grid(column=2, row=2, pady=2, sticky=W, padx=10)
sk_btn = Radiobutton(window, text=sk, value=2, variable=def_variable, state='disable')
sk_btn.grid(column=2, row=3, pady=2, sticky=W, padx=10)

# Проверка координат
checkbox_ate_label = Label(window, text='Проверять координаты', font=("Georgia", 11), width=22)
checkbox_ate_label.grid(column=0, row=3, sticky=W)
checkbox_ate = BooleanVar()
checkbox_ate.set(False)
checkbox_ate_button = Checkbutton(window, variable=checkbox_ate)
checkbox_ate_button.grid(column=1, row=3)


# Файл маска
checkbox_ate.trace('w', disable_enable_button)
maska_label = Label(window, text='Файл маски', font=("Georgia", 11), width=22)
maska_label.grid(column=0, row=4, sticky=W)
maska_label_button = Button(window, text="Выбрать", command=choose_maska_file, state='disabled', font=("Georgia", 8))
maska_label_button.grid(column=1, row=4)
maska_label_path = Entry(window, width=20, font=("Georgia", 8))
maska_label_path.grid(column=2, row=4, sticky=W, pady=2, padx=5)

# ID_ATE//OBJ_ID
checkbox_id_ate_label = Label(window, text='Уникальный\nидентификатор нас.пункта', font=("Georgia", 11), width=22)
checkbox_id_ate_label.grid(column=0, row=5, sticky=W)
checkbox_id_ate = BooleanVar()
checkbox_id_ate.set(False)
checkbox_id_ate_button = Checkbutton(window, variable=checkbox_id_ate)
checkbox_id_ate_button.grid(column=1, row=5)


# Округление координат
checkbox_round_coords_label = Label(window, text='Округление координат', font=("Georgia", 11), width=22, pady=2)
checkbox_round_coords_label.grid(column=0, row=6, sticky=W)
checkbox_round_coords = BooleanVar()
checkbox_round_coords.set(False)
checkbox_round_coords_button = Checkbutton(window, variable=checkbox_round_coords)
checkbox_round_coords_button.grid(column=1, row=6, pady=2)
checkbox_round_coords.trace('w', disable_enable_button_round)
fill_round_entry = Entry(window, state='disabled', width=5, font=("Georgia", 8),
                         validate='key', validatecommand=(validate_digits, '%S'))
fill_round_entry.grid(column=2, row=6, sticky=W, pady=2)

# Настрока полей
fields_settings_label = Label(window, text='Настройка полей', font=("Georgia", 11), width=15)
fields_settings_label.grid(column=3, row=0, sticky=W)

fields_table_frame = Frame(window, width=670, height=590, bg='white', bd=5, relief='ridge')
fields_table_frame.grid(column=3, row=1, columnspan=5, rowspan=70, padx=5)
fields_table_frame.grid_propagate(False)

my_canvas = Canvas(fields_table_frame, bg='white', width=490, height=390)
my_canvas.grid(column=0, row=0, sticky="news")

scrollbar = Scrollbar(fields_table_frame, orient=VERTICAL, command=my_canvas.yview)
scrollbar.grid(row=0, column=1, sticky='ns')
my_canvas.configure(yscrollcommand=scrollbar.set)

inner_frame = Frame(my_canvas, bg='white', bd=5)
my_canvas.create_window((0, 0), window=inner_frame, anchor='nw')

inner_digits_validation = inner_frame.register(validate)

list_checkboxes = []  # ХРАНЯТСЯ ЗНАЧЕНИЯ ЧЕКБОКСОВ !!! ВАЖНО ДЛЯ КОРРЕКТНОГО ПРИМЕНЕНИЯ К НУЖНОЙ СТРОКЕ
for n, items in enumerate(fields_excel):

    list_checkboxes.append(BooleanVar(value=items[2]))
    Checkbutton(inner_frame, variable=list_checkboxes[n], command=table_disable_enable).grid(row=n, column=0,
                                                                                             sticky='news')
    Label(inner_frame, text=items[0], width=51, anchor='w', bd=0.5, relief='solid').grid(row=n, column=1, sticky='w')
    default_col3 = StringVar(inner_frame, items[1])
    Entry(inner_frame, width=25, textvariable=default_col3, state=DISABLED).grid(row=n, column=2, sticky='w', padx=10)
    Entry(inner_frame, width=10, validate='key', validatecommand=(inner_digits_validation, '%S'), state=DISABLED)\
        .grid(row=n, column=3, sticky='e', padx=7)

inner_frame.update_idletasks()

# Сохранить//Загрузить настройки полей
save_fields_config = Button(window, text="Сохранить настройки полей", command=save_pattern, font=("Georgia", 8))
save_fields_config.grid(row=0, column=4)
save_fields_config = Button(window, text="Загрузить настройки полей", command=upload_pattern, font=("Georgia", 8))
save_fields_config.grid(row=0, column=5)

# Разделитель дробной части
decimal_format_label = Label(window, text='Разделитель дробной\nчасти (для csv файлов)', font=("Georgia", 11), width=22)
decimal_format_label.grid(column=0, row=7, sticky=W)
decimal_format = Combobox(window, width=6, font=("Georgia", 8), state='disable')
decimal_format['values'] = ('Точка', 'Запятая')
decimal_format.current(0)
decimal_format.grid(column=1, row=7, pady=2)

# Кнопка запуска обработки
start_button = Button(window, text="Старт", width=50, pady=3,
                      command=start_button_func, font=("Georgia", 9), bg='#54C571')
start_button.grid(row=8, column=0, columnspan=3)

# Окно статуса выполнения
logger_window = Text(window, width=50, height=21, borderwidth=3)
logger_window.grid(row=9, column=0, columnspan=3, pady=2)


my_canvas.config(width=640, height=575)
my_canvas.config(scrollregion=my_canvas.bbox("all"))

window.mainloop()
