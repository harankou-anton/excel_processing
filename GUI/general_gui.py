import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog


def validate(symbol: str):
    return symbol.isdigit()


class GeneralGUI(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, width=760, height=650, bg='white', bd=2, relief='groove', text='Общие параметры',
                         font=("Georgia", 10), name='general_frame')

        # Исходная папка
        self.download_folder_button = tk.Button(self, text="Папка с исходниками", font=("Georgia", 8), width=20,
                                                command=self.choose_download_folder, name='download_folder_button')
        self.download_folder_button.grid(column=0, row=0, pady=2)
        self.download_folder_path = tk.Entry(self, width=20, font=("Georgia", 8), name='download_folder_path')
        self.download_folder_path.grid(column=1, row=0, sticky=tk.W, pady=2, padx=5)

        # Конечная папка
        self.final_folder_button = tk.Button(self, text="Итоговая папка", font=("Georgia", 8), width=20,
                                             command=self.choose_final_folder, name='final_folder_button')
        self.final_folder_button.grid(column=0, row=1, pady=2)
        self.final_folder_path = tk.Entry(self, width=20, font=("Georgia", 8), name='final_folder_path')
        self.final_folder_path.grid(column=1, row=1, sticky=tk.W, pady=2, padx=5)

        # Выходной формат
        self.output_format_label = tk.Label(self, text='Выходной формат', font=("Georgia", 11), width=18,
                                            background='white', name='output_format_label')
        self.output_format_label.grid(column=0, row=2, pady=2)
        self.output_format = ttk.Combobox(self, width=18, font=("Georgia", 8), name='output_format')
        self.output_format['values'] = ('Excel', 'CSV', 'Shape')
        self.output_format.current(0)
        self.output_format.grid(column=1, row=2, pady=2)

        # Проверка координат
        self.check_coords_label = tk.Label(self, text='Проверять координаты', font=("Georgia", 11), width=22,
                                          name='check_coords_label', background='white')
        self.check_coords_label.grid(column=0, row=3)
        self.check_coords = tk.BooleanVar(value=False, name='check_coords')
        self.check_coords_button = ttk.Checkbutton(self, variable=self.check_coords, command=self.disable_enable_button,
                                                   name='check_coords_button')
        self.check_coords_button.grid(column=1, row=3, sticky=tk.W, padx=30)

        # Система координат
        self.sk = tk.IntVar(value=1, name='sk')
        self.wgs_btn = ttk.Radiobutton(self, text='WGS 84', value=1, variable=self.sk, state='disable', name='wgs_btn')
        self.wgs_btn.grid(column=0, row=4, pady=2)
        self.sk_btn = ttk.Radiobutton(self, text='CK-63', value=2, variable=self.sk, state='disable', name='sk_btn')
        self.sk_btn.grid(column=1, row=4, pady=2, sticky=tk.W)

        # ID_ATE//OBJ_ID
        self.checkbox_id_ate_label = tk.Label(self, text='Уникальный\nидентификатор нас.пункта', font=("Georgia", 11),
                                              width=22, background='white', name='checkbox_id_ate_label')
        self.checkbox_id_ate_label.grid(column=0, row=5)
        self.id_ate = tk.BooleanVar(value=False, name='id_ate')
        self.checkbox_id_ate_button = ttk.Checkbutton(self, variable=self.id_ate,
                                                      name='checkbox_id_ate_button')
        self.checkbox_id_ate_button.grid(column=1, row=5, sticky=tk.W, padx=30)

        # Округление координат
        self.validate_digits = self.register(validate)
        self.round_coords_number_label = tk.Label(self, text='Округление координат', font=("Georgia", 11), width=22,
                                                    pady=2, background='white', name='round_coords_number_label')
        self.round_coords_number_label.grid(column=0, row=6, sticky=tk.W)
        self.round_coords_number = tk.Entry(self, width=5, font=("Georgia", 8), validate='key',
                                         validatecommand=(self.validate_digits, '%S'), name='round_coords_number')
        self.round_coords_number.grid(column=1, row=6, sticky=tk.W, pady=2, padx=15)

        # Этаж для ИП
        self.checkbox_floor_for_ip_label = tk.Label(self, text='Значение этажа только\nдля ИП', font=("Georgia", 11),
                                                    width=22, background='white', name='checkbox_floor_for_ip_label')
        self.checkbox_floor_for_ip_label.grid(column=0, row=7)
        self.floor_for_ip = tk.BooleanVar(value=False, name='floor_for_ip')
        self.checkbox_floor_for_ip_button = ttk.Checkbutton(self, variable=self.floor_for_ip,
                                                            name='checkbox_floor_for_ip_button')
        self.checkbox_floor_for_ip_button.grid(column=1, row=7, pady=2, padx=30, sticky=tk.W)

        # Подъезд для ИП
        self.checkbox_porch_for_ip_label = tk.Label(self, text='Значение подъезда только\nдля ИП', font=("Georgia", 11),
                                                    width=22, background='white', name='checkbox_porch_for_ip_label')
        self.checkbox_porch_for_ip_label.grid(column=0, row=8)
        self.porch_for_ip = tk.BooleanVar(value=False, name='porch_for_ip')
        self.checkbox_porch_for_ip_button = ttk.Checkbutton(self, variable=self.porch_for_ip,
                                                            name='checkbox_porch_for_ip_button')
        self.checkbox_porch_for_ip_button.grid(column=1, row=8, pady=2, padx=30, sticky=tk.W)

        # Пересчёт кодов этажей
        self.checkbox_floor_recount_label = tk.Label(self, text='Пересчитать коды\nзначения этажей', font=("Georgia", 11),
                                                    width=22, background='white', name='checkbox_floor_recount_label')
        self.checkbox_floor_recount_label.grid(column=0, row=9)
        self.recount_floor = tk.BooleanVar(value=False, name='recount_floor')
        self.checkbox_floor_recount_button = ttk.Checkbutton(self, variable=self.recount_floor,
                                                            name='checkbox_floor_recount_button')
        self.checkbox_floor_recount_button.grid(column=1, row=9, pady=2, padx=30, sticky=tk.W)

        self.grid(column=0, row=0, padx=5, pady=5)

    def choose_download_folder(self):
        folder_name = filedialog.askdirectory()
        if folder_name != '':
            self.download_folder_path.delete(0, tk.END)
            self.download_folder_path.insert(0, folder_name)

    def choose_final_folder(self):
        folder_name = tk.filedialog.askdirectory()
        if folder_name != '':
            self.final_folder_path.delete(0, tk.END)
            self.final_folder_path.insert(0, folder_name)

    def disable_enable_button(self):
        if self.check_coords.get():
            self.wgs_btn.config(state='normal')
            self.sk_btn.config(state='normal')
        else:
            self.wgs_btn.config(state='disable')
            self.sk_btn.config(state='disable')

    def check_filling(self):
        if self.download_folder_path.get() == '':
            return '--Не указана "Папка с исходниками"\n'
        if self.final_folder_path.get() == '':
            return '--Не указана "Итоговая папка"\n'
        # if self.round_coords_number.get() == '':
        #     return '--Не указано значение "Округление координат"\n'

