import json
import os
import threading
import sys
import tkinter as tk
from tkinter import filedialog
from tkinter.ttk import Style

from GUI.general_gui import GeneralGUI
from GUI.excel_gui import ExcelGUI
from GUI.csv_gui import CSVGUI
from GUI.shape_gui import ShapeGUI
from GUI.fields_gui import FieldsGUI

from scr.RA_template2_8 import AddressFiles


# Для иконки в exe
def resource_path2(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MainGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.configure(background='#E9F3FF')
        self.title('RA Excel Processing ver 1.0')
        self.resizable(False, False)
        self.path_image = resource_path2('favicon.png')
        self.photo = tk.PhotoImage(file=self.path_image)
        self.iconphoto(False, self.photo)

        Style().configure('TCheckbutton', background='white')
        Style().configure('TRadiobutton', background='white')

        self.current_file = ''
        self.previous_file = ''
        self.error_message = ''

        self.general_frame = GeneralGUI(self)
        self.general_frame.children['output_format'].bind("<<ComboboxSelected>>", self.additional_parameters)

        self.excel_frame = ExcelGUI(self)
        self.csv_frame = CSVGUI(self)
        self.shape_frame = ShapeGUI(self)
        self.fields_frame = FieldsGUI(self)
        self.fields_frame.children['save_fields_config'].config(command=self.save_pattern)
        self.fields_frame.children['upload_fields_config'].config(command=self.upload_pattern)

        # Окно статуса выполнения
        self.logger_frame = tk.LabelFrame(self, text='Результаты выполнения', bg='white', bd=2, relief='groove', font=("Georgia", 10))
        self.logger_window = tk.Text(self.logger_frame, width=48, height=41, borderwidth=1,)
        self.logger_window.grid(row=0, column=0, pady=5, padx=5,)
        self.logger_frame.grid(row=0, column=1, pady=5, padx=5, rowspan=5, sticky=tk.N)

        # Кнопка запуска обработки
        self.start_button = tk.Button(self, text="Старт", width=48, pady=3, font=("Georgia", 9), bg='#54C571',
                                      command=self.start_button_func)
        self.start_button.grid(row=4, column=0, padx=5, pady=5,)

    def additional_parameters(self, *args):
        for child in self.excel_frame.winfo_children():
            if self.general_frame.children['output_format'].current() == 0:
                child.configure(state='normal')
            else:
                child.configure(state='disable')

        for child in self.csv_frame.winfo_children():
            if self.general_frame.children['output_format'].current() == 1:
                child.configure(state='normal')
            else:
                child.configure(state='disable')
            self.csv_frame.enable_quote_type()
        for child in self.shape_frame.winfo_children():
            if self.general_frame.children['output_format'].current() == 2:
                child.configure(state='normal')
            else:
                child.configure(state='disable')

    def save_pattern(self):
        self.fields_frame.update_fields_excel()
        self.main_options = {'output_format': self.general_frame.children['output_format'].get(),
                             'check_coords': self.general_frame.getvar('check_coords'),
                             'sk': self.general_frame.getvar('sk'),
                             'id_ate': self.general_frame.getvar('id_ate'),
                             'round_coords_number': self.general_frame.children['round_coords_number'].get(),
                             'csv_delimeter': self.csv_frame.children['csv_delimeter'].get(),
                             'floor_for_ip': self.general_frame.getvar('floor_for_ip'),
                             'porch_for_ip': self.general_frame.getvar('porch_for_ip'),
                             'separator_csv': self.csv_frame.children['separator_csv'].get(),
                             'prj_file': self.shape_frame.children['prj_file'].get(),
                             'delete_coord_fields': self.shape_frame.getvar('delete_coord_fields'),
                             'excel_split': self.excel_frame.children['excel_split'].get()
                             }
        self.options = {'fields': self.fields_frame.fields_excel[:], 'main_options': self.main_options}
        self.json_dump = json.dumps(self.options, ensure_ascii=False)
        self.save_file = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[("Json Files", '*.json')])
        if self.save_file != '':
            with open(self.save_file, 'w', encoding='utf-8') as writter:
                writter.write(self.json_dump)

    def upload_pattern(self):
        self.upload_file = filedialog.askopenfilename(defaultextension='.json', filetypes=[("Json Files", '*.json')])
        if self.upload_file != '':
            with open(self.upload_file, 'r', encoding='utf-8') as reader:
                self.file_content = json.loads(reader.read())

                self.get_main_options = {}

                # Проверка для первых версий шаблона
                if type(self.file_content) == dict:
                    self.get_fields_names = self.file_content['fields']
                    self.get_main_options = self.file_content['main_options']
                else:
                    self.get_fields_names = self.file_content

                for key in self.fields_frame.dict_checkboxes.keys():
                    self.fields_frame.dict_checkboxes[key].set(False)
                for row in range(len(self.get_fields_names)):
                    self.fields_frame.dict_checkboxes[self.get_fields_names[row][0]].set(self.get_fields_names[row][2])

                self.dict_keys = [key for key in self.fields_frame.dict_checkboxes.keys()]
                self.list_checkboxes = [value for value in self.fields_frame.dict_checkboxes.values()]
                for row in range(len(self.list_checkboxes)):
                    for el in range(len(self.get_fields_names)):
                        if self.dict_keys[row] in self.get_fields_names[el]:
                            self.template_position = el
                            break
                    if self.list_checkboxes[row].get() is True:
                        self.fields_frame.checked_variables.append(self.list_checkboxes[row])
                        self.fields_frame.inner_frame.grid_slaves(row, 2)[0].config(state=tk.NORMAL)
                        self.fields_frame.inner_frame.grid_slaves(row, 3)[0].config(state=tk.NORMAL)
                        self.fields_frame.inner_frame.grid_slaves(row, 2)[0].delete(0, tk.END)
                        self.fields_frame.inner_frame.grid_slaves(row, 2)[0].insert(
                            0, self.get_fields_names[self.template_position][1])
                        if self.get_fields_names[self.template_position][4] != 0:
                            self.fields_frame.inner_frame.grid_slaves(row, 3)[0].delete(0, tk.END)
                            self.fields_frame.inner_frame.grid_slaves(row, 3)[0].insert(
                                0, self.get_fields_names[self.template_position][4])
                        else:
                            self.fields_frame.inner_frame.grid_slaves(row, 3)[0].delete(0, tk.END)
                    else:
                        self.fields_frame.inner_frame.grid_slaves(row, 3)[0].delete(0, tk.END)
                        self.fields_frame.inner_frame.grid_slaves(row, 2)[0].config(state=tk.DISABLED)
                        self.fields_frame.inner_frame.grid_slaves(row, 3)[0].config(state=tk.DISABLED)

                if self.get_main_options != {}:
                    for key, value in self.get_main_options.items():
                        if not self.general_frame.children.get(key):
                            self.general_frame.setvar(key, value)
                        elif isinstance(self.general_frame.children[key], tk.Entry):
                            self.general_frame.children[key].delete(0, tk.END)
                            self.general_frame.children[key].insert(0, value)
                        else:
                            self.general_frame.children[key].set(value)

                        if self.excel_frame.children.get(key):
                            self.excel_frame.children[key].set(value)

                        if self.csv_frame.children.get(key):
                            self.csv_frame.children[key].set(value)

                        if not self.shape_frame.children.get(key):
                            self.shape_frame.setvar(key, value)
                        else:
                            self.shape_frame.children[key].set(value)



                    self.additional_parameters()
                    self.general_frame.disable_enable_button()

    def run_instrument(self):
        self.fields_frame.update_fields_excel()
        df = self.general_frame.download_folder_path.get()
        ff = self.general_frame.final_folder_path.get()
        output = self.general_frame.output_format['values'].index(f'{self.general_frame.output_format.get()}') + 1
        check_coords = self.general_frame.check_coords.get()
        id_ate = self.general_frame.id_ate.get()
        sk_get = self.general_frame.sk.get()
        dec = self.csv_frame.csv_delimeter.get()
        floor_for_ip = self.general_frame.floor_for_ip.get()
        porch_for_ip = self.general_frame.porch_for_ip.get()
        separator_csv = self.csv_frame.separator_csv.get()
        round_coords = self.general_frame.round_coords_number.get()
        prj_file = self.shape_frame.prj_file.get()
        delete_coord_fields = self.shape_frame.delete_coord_fields.get()
        quote_type = self.csv_frame.quote_type_value.get()
        excel_split = self.excel_frame.excel_split.get()
        for csv_file in os.listdir(df):
            if csv_file[-4:] == '.csv':
                try:
                    AddressFiles(download_folder=df, final_folder=ff, output_format=output, check_coords=check_coords,
                                 change_id_ate=id_ate, round_coords=round_coords, sk=sk_get, decimal_format=dec,
                                 fields=self.fields_frame.fields_excel, floor_for_ip=floor_for_ip,
                                 porch_for_ip=porch_for_ip, separator_csv=separator_csv, prj_file=prj_file,
                                 delete_coord_fields=delete_coord_fields, quote_type=quote_type,
                                 excel_split=excel_split).processing_data(csv_file)
                    self.current_file = csv_file
                except Exception as error:
                    self.error_message = repr(error)
                    self.current_file = csv_file

    def check_state(self, func):
        self.after(1000, self.check_if_done, func)

    def check_if_done(self, r_i):
        if not r_i.is_alive():
            self.start_button.configure(text='Старт', state='normal', bg='#54C571')

            if self.error_message == "":
                self.logger_window.insert(0.0, f'--Файл {self.current_file} обработан успешно\n')
            elif self.error_message == "ValueError('Number of passed names did not match number of header fields in the file')":
                self.logger_window.insert(0.0, f'--Не удалось обработать файл {self.current_file}. '
                                          f'Количество отмеченных полей и полей в файле не совпадает\n')
            elif "ValueError('Unable to convert" in self.error_message:
                self.logger_window.insert(0.0, f'--Не удалось обработать файл {self.current_file}. '
                                          f'Отмеченные поля и поля исходного файла не совпадают\n')
            else:
                self.logger_window.insert(0.0, f'--Не удалось обработать файл {self.current_file}. Ошибка {self.error_message}\n')
            self.logger_window.insert(0.0, '--Обработка завершена\n')
            self.current_file = ''
            self.previous_file = ''
            self.error_message = ''
        else:
            if self.previous_file != self.current_file and self.error_message == '':
                self.previous_file = self.current_file
                self.logger_window.insert(0.0, f'--Файл {self.previous_file} обработан успешно\n')
            elif self.previous_file != self.current_file and self.error_message != '':
                self.previous_file = self.current_file
                if self.error_message == "ValueError('Number of passed names did not match number of header fields in the file')":
                    self.logger_window.insert(0.0, f'--Не удалось обработать файл {self.previous_file}. '
                                              f'Количество отмеченных полей и полей в файле не совпадает\n')
                elif "ValueError('Unable to convert" in self.error_message:
                    self.logger_window.insert(0.0, f'--Не удалось обработать файл {self.previous_file}. '
                                              f'Отмеченные поля и поля исходного файла не совпадают\n')
                else:
                    self.logger_window.insert(0.0, f'--Не удалось обработать файл {self.previous_file}. Ошибка {self.error_message}\n')
                self.error_message = ''

            self.check_state(r_i)

    def start_button_func(self):
        if self.general_frame.check_filling():
            self.logger_window.insert(0.0, self.general_frame.check_filling())
            return

        if self.general_frame.check_coords.get() and (self.fields_frame.list_checkboxes[27].get() is False and
                                                      self.fields_frame.list_checkboxes[39].get() is False) and \
                self.fields_frame.list_checkboxes[33].get() is False:
            self.logger_window.insert(0.0,
                                      '--Для проверки координат должны быть отмечены и присутствовать в исходном файле '
                                      'поля "Наименование района" + "Наименование населенного пункта на русском языке" или '
                                      '"Уникальный идентификатор населённого пункта"\n')
            return

        if self.fields_frame.validate_positions():
            self.logger_window.insert(0.0, self.fields_frame.validate_positions())
            return

        self.start_button.configure(text='Выполняется...', state='disabled', bg='#FF7F50')
        r_i = threading.Thread(target=self.run_instrument)
        r_i.start()
        self.check_state(r_i)


if __name__ == "__main__":
    app = MainGUI()
    app.mainloop()
