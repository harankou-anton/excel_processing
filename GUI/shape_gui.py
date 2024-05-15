import tkinter as tk
import tkinter.ttk as ttk


class ShapeGUI(tk.LabelFrame):
    def __init__(self, master):
        super().__init__(master, width=800, height=650, bg='white', bd=2, relief='groove', text='Параметры Shape',
                         font=("Georgia", 10), name='shape_frame')

        # Разбивка данных при превышении лимита
        self.delete_coord_fields_label = tk.Label(self, text='Удалить поля\nс координатами', font=("Georgia", 11), width=22,
                                            background='white')
        self.delete_coord_fields_label.grid(column=0, row=0, sticky=tk.W)
        self.delete_coord_fields = tk.BooleanVar(value=False, name='delete_coord_fields')
        self.delete_coord_fields_button = ttk.Checkbutton(self, variable=self.delete_coord_fields)
        self.delete_coord_fields_button.grid(column=1, row=0, sticky=tk.W, padx=30)

        # Добавить prj файл
        self.prj_file_label = tk.Label(self, text='Добавить prj файл', font=("Georgia", 11), width=22, background='white')
        self.prj_file_label.grid(column=0, row=1, sticky=tk.W)
        self.prj_file = ttk.Combobox(self, width=18, font=("Georgia", 8), name='prj_file')
        self.prj_file['values'] = ('Нет', 'WGS 84', 'CK-63 (1)', 'CK-63 (2)', 'CK-63 (3)')
        self.prj_file.current(0)
        self.prj_file.grid(column=1, row=1, padx=5, pady=2)

        for child in self.winfo_children():
            child.configure(state='disable')

        self.grid(column=0, row=3, padx=5, pady=5, )
