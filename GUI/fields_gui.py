import tkinter as tk
import tkinter.ttk as ttk
from scr import default_values


def validate(symbol):
    return symbol.isdigit()


class FieldsGUI(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, width=745, height=680, bg='white', bd=2, relief='groove', text='Настройка полей',
                         font=("Georgia", 10), name='fields_frame')

        self.positions_set = set(range(1, 90))
        self.checked_variables = []
        self.get_position_values = None
        self.ind_position = None

        self.grid_propagate(False)
        self.fields_excel = default_values.fields_excel

        self.save_fields_config = tk.Button(self, text="Сохранить настройки полей", font=("Georgia", 8),
                                            name='save_fields_config')
        self.save_fields_config.grid(row=0, column=0, pady=5)

        self.upload_fields_config = tk.Button(self, text="Загрузить настройки полей", font=("Georgia", 8),
                                              name='upload_fields_config')
        self.upload_fields_config.grid(row=0, column=1, pady=5)

        self.my_canvas = tk.Canvas(self, bg='white', width=720, height=620)
        self.my_canvas.grid(column=0, row=1, sticky="news", columnspan=2)

        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.my_canvas.yview)
        self.scrollbar.grid(row=1, column=2, sticky='ns')
        self.my_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.inner_frame = tk.Frame(self.my_canvas, bg='white', bd=1, relief='groove')
        self.my_canvas.create_window((0, 0), window=self.inner_frame, anchor='nw')

        self.inner_digits_validation = self.inner_frame.register(validate)

        self.dict_checkboxes = {}  # ХРАНЯТСЯ ЗНАЧЕНИЯ ЧЕКБОКСОВ !!! ВАЖНО ДЛЯ КОРРЕКТНОГО ПРИМЕНЕНИЯ К НУЖНОЙ СТРОКЕ
        self.list_checkboxes = None
        for n, items in enumerate(self.fields_excel):
            self.dict_checkboxes[items[0]] = tk.BooleanVar(value=items[2])
            self.list_checkboxes = [value for value in self.dict_checkboxes.values()]
        for n in range(len(self.list_checkboxes)):
            ttk.Checkbutton(self.inner_frame, variable=self.list_checkboxes[n],
                            command=self.table_disable_enable).grid(row=n, column=0, sticky='news')
            tk.Label(self.inner_frame, text=self.fields_excel[n][0], width=63, anchor='w', bd=0.5, relief='solid',
                     background='white').grid(row=n, column=1, sticky='w')
            self.default_col3 = tk.StringVar(self.inner_frame, self.fields_excel[n][1])
            tk.Entry(self.inner_frame, width=25, textvariable=self.default_col3,
                     state=tk.DISABLED).grid(row=n, column=2, sticky='w', padx=10)
            tk.Entry(self.inner_frame, width=10, validate='key', validatecommand=(self.inner_digits_validation, '%S'),
                     state=tk.DISABLED).grid(row=n, column=3, sticky=tk.E, padx=7)

        self.inner_frame.update_idletasks()
        self.my_canvas.config(scrollregion=self.my_canvas.bbox("all"))

        self.grid(column=2, row=0, padx=5, pady=5, rowspan=20)


    def table_disable_enable(self, *args):
        self.get_position_values = set([int(self.inner_frame.grid_slaves(row=row, column=3)[0].get())
                                        for row in range(len(self.list_checkboxes))
                                        if self.inner_frame.grid_slaves(row=row, column=3)[0].get() != ''])

        for num, button in enumerate(self.list_checkboxes):
            if button.get() and button not in self.checked_variables:
                self.inner_frame.grid_slaves(row=num, column=2)[0].config(state=tk.NORMAL)
                self.inner_frame.grid_slaves(row=num, column=3)[0].config(state=tk.NORMAL)
                self.checked_variables.append(button)
                self.ind_position = min(self.positions_set - self.get_position_values)
                self.inner_frame.grid_slaves(row=num, column=3)[0].insert(0, str(self.ind_position))
                # self.positions_list.remove(self.positions_list[0])
            elif button.get() is False and button in self.checked_variables:
                self.checked_variables.remove(button)
                self.inner_frame.grid_slaves(row=num, column=3)[0].delete(0, tk.END)
                self.inner_frame.grid_slaves(row=num, column=2)[0].config(state=tk.DISABLED)
                self.inner_frame.grid_slaves(row=num, column=3)[0].config(state=tk.DISABLED)

    def update_fields_excel(self):
        for row in range(len(self.fields_excel)):
            self.fields_excel[row][1] = self.inner_frame.grid_slaves(row, 2)[0].get()
            self.fields_excel[row][2] = self.list_checkboxes[row].get()
            if self.inner_frame.grid_slaves(row, 3)[0].get() == "":
                self.fields_excel[row][4] = 0
            else:
                self.fields_excel[row][4] = int(self.inner_frame.grid_slaves(row, 3)[0].get())

    def validate_positions(self):
        self.numbers = {}
        for num, check_position in enumerate(self.list_checkboxes):
            if check_position.get():
                if self.inner_frame.grid_slaves(row=num, column=3)[0].get() == '':
                    return f'--Не указана позиция для поля ' \
                           f'{self.inner_frame.grid_slaves(row=num, column=1)[0]["text"]}\n'

                if self.inner_frame.grid_slaves(row=num, column=3)[0].get() not in self.numbers:
                    self.numbers[self.inner_frame.grid_slaves(row=num, column=3)[0].get()] = \
                        self.inner_frame.grid_slaves(row=num, column=1)[0]['text']
                else:
                    return f'--Указана одиноковая позиция для полей ' \
                           f'"{self.numbers[self.inner_frame.grid_slaves(row=num, column=3)[0].get()]}" и ' \
                           f'{self.inner_frame.grid_slaves(row=num, column=1)[0]["text"]}"\n'
