import tkinter as tk
import tkinter.ttk as ttk


class ExcelGUI(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, width=800, height=650, bg='white', bd=2, relief='groove', text='Параметры Excel',
                         font=("Georgia", 10), name='excel_frame')
        self.excel_split_label = tk.Label(self, text='Разбивка более\nмиллиона записей(TODO)', font=("Georgia", 11),
                                    width=22, background='white')
        self.excel_split_label.grid(column=0, row=0, sticky=tk.W)
        self.excel_split = ttk.Combobox(self, width=18, font=("Georgia", 8), name='excel_split')
        self.excel_split['values'] = ('По файлам', 'По листам')
        self.excel_split.current(0)
        self.excel_split.grid(column=1, row=0, pady=2, padx=5)
        self.grid(column=0, row=1, padx=5, pady=5)
