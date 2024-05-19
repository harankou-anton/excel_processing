import tkinter as tk
import tkinter.ttk as ttk


class CSVGUI(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, width=800, height=650, bg='white', bd=2, relief='groove', text='Параметры CSV',
                           font=("Georgia", 10), name='csv_frame')

        # Разделитель дробной части
        self.csv_delimeter_label = tk.Label(self, text='Разделитель дробной части', font=("Georgia", 11), width=22,
                                             background='white', name='csv_delimeter_label')
        self.csv_delimeter_label.grid(column=0, row=0, sticky=tk.W)
        self.csv_delimeter = ttk.Combobox(self, width=18, font=("Georgia", 8), name='csv_delimeter')
        self.csv_delimeter['values'] = ('Точка', 'Запятая')
        self.csv_delimeter.current(0)
        self.csv_delimeter.grid(column=1, row=0, pady=2, padx=5)

        # Разделитель данных
        self.separator_csv_label = tk.Label(self, text='Разделитель данных', font=("Georgia", 11), width=22,
                                        background='white', name='separator_label')
        self.separator_csv_label.grid(column=0, row=1, sticky=tk.W)
        self.separator_csv = ttk.Combobox(self, width=18, font=("Georgia", 8), name='separator_csv')
        self.separator_csv['values'] = ('Точка с запятой', 'Табуляция', 'Вертикальная черта')
        self.separator_csv.current(0)
        self.separator_csv.grid(column=1, row=1)

        # Обернуть данные в кавычки
        self.quote_label = tk.Label(self, text='Обернуть в кавычки', font=("Georgia", 11), width=22,
                                    background='white', name='quote_label')
        self.quote_label.grid(column=0, row=2, sticky=tk.W)
        self.quote_value = ttk.Combobox(self, width=18, font=("Georgia", 8), name='quote_value')
        self.quote_value['values'] = ('Нет', 'Только текст', 'Все')
        self.quote_value.current(0)
        self.quote_value.grid(column=1, row=2)
        self.quote_value.bind("<<ComboboxSelected>>", self.enable_quote_type)

        # Вид кавычек
        self.quote_type_label = tk.Label(self, text='Тип кавычек', font=("Georgia", 11), width=22, background='white',
                                         name='quote_type_label')
        self.quote_type_label.grid(column=0, row=3, sticky=tk.W)
        self.quote_type = ttk.Combobox(self, width=18, font=("Georgia", 8), name='quote_type')
        self.quote_type['values'] = ('Двойные', 'Одиночные')
        self.quote_type.current(0)
        self.quote_type.grid(column=1, row=3)

        for child in self.winfo_children():
            child.configure(state='disable')

        self.grid(column=0, row=2, padx=5, pady=5, )

    def enable_quote_type(self, *args):
        if self.quote_value.current() == 0:
            self.quote_type.configure(state='disable')
        else:
            self.quote_type.configure(state='normal')
