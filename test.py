import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkcalendar import DateEntry, calendar_


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    def init_main(self):
        toolbar = tk.Frame(bg='#d7d8e0', bd=22)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='button.gif')
        btn_open_dialog = tk.Button(toolbar, text='ADD', command=self.open_dialog, bg='#d7d8e0', bd=0,
                                    compound=tk.TOP, image=self.add_img)
        btn_open_dialog.pack(side=tk.LEFT)

        self.update_img = tk.PhotoImage(file='update.gif')
        btn_edit_dialog = tk.Button(toolbar, text='REDACT', bg='#d7d8e0', bd=0, image=self.update_img,
                                    compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        self.delete_img = tk.PhotoImage(file='delete.gif')
        btn_delete = tk.Button(toolbar, text='DELETE', bg='#d7d8e0', bd=0, image=self.delete_img,
                               compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        self.search_img = tk.PhotoImage(file='search.gif')
        btn_search = tk.Button(toolbar, text='SEARCH', bg='#d7d8e0', bd=0, image=self.search_img,
                               compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        self.refresh_img = tk.PhotoImage(file='refresh.gif')
        btn_refresh = tk.Button(toolbar, text='REFRESH', bg='#d7d8e0', bd=0, image=self.refresh_img,
                                compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('ID', 'doctor', 'patient', 'todo', 'todo_date'), height=24, show='headings')

        self.tree.column('ID', width=60, anchor=tk.CENTER)
        self.tree.column('doctor', width=220, anchor=tk.CENTER)
        self.tree.column('patient', width=220, anchor=tk.CENTER)
        self.tree.column('todo_date', width=220, anchor=tk.CENTER)
        self.tree.column('todo', width=220, anchor=tk.CENTER)

        self.tree.heading('ID', text='ID')
        self.tree.heading('doctor', text='DOCTOR')
        self.tree.heading('patient', text='PATIENT')
        self.tree.heading('todo_date', text='DATE')
        self.tree.heading('todo', text='TODO')

        self.tree.pack(side=tk.LEFT)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def records(self, doctor, patient, todo, todo_date):
        print(todo_date)
        self.db.insert_data(doctor, patient, todo, todo_date)
        self.view_records()

    def update_record(self, doctor, patient, todo, todo_date):
        self.db.mycursor.execute('''UPDATE bio SET doctor=%s, patient=%s, todo=%s, todo_date=%s WHERE ID=%s''',
                                 (doctor, patient, todo, todo_date, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.mydb.commit()
        self.view_records()

    def view_records(self):
        self.db.mycursor.execute('''SELECT * FROM bio''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.mycursor.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.mycursor.execute('''DELETE FROM bio WHERE id=%s''', (self.tree.set(selection_item, '#1'),))
        self.db.mydb.commit()
        self.view_records()

    def search_records(self, doctor):
        description = ('%' + doctor + '%',)
        self.db.mycursor.execute('''SELECT * FROM bio WHERE doctor LIKE %s''', doctor)

        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.mycursor.fetchall()]

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.init_child()
        self.view = app

    def init_child(self):
        self.title('ADD')
        self.geometry('400x820+400+300')


        label_doctor = tk.Label(self, text='DOCTOR:')
        label_doctor.place(x=50, y=50)
        label_select = tk.Label(self, text='PATIENT:')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='TODO')
        label_sum.place(x=50, y=110)
        label_todo_date = tk.Label(self, text='DATE')
        label_todo_date.place(x=50, y=140)

        self.combobox = ttk.Combobox(self, values=['Ilham Sadikhov', 'Nigar Movsumova', 'Salahli Alpay'])
        self.combobox.current(0)
        self.combobox.place(x=200, y=50)

        self.entry_doctor = ttk.Entry(self)
        self.entry_doctor.place(x=200, y=80)

        self.todo = ttk.Entry(self)
        self.todo.place(x=200, y=110)

        self.todo_date = DateEntry(self, date_pattern='dd-mm-YYYY')
        self.todo_date.place(x=200, y=140)

        btn_cancel = ttk.Button(self, text='CLOSE', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='ADD')
        self.btn_ok.place(x=220, y=170)
        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.combobox.get(),
                                                                       self.entry_doctor.get(),
                                                                       self.todo.get(),
                                                                       self.todo_date.get()))

        self.grab_set()
        self.focus_set()


class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('REDACT')
        btn_edit = ttk.Button(self, text='REDACT')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.combobox.get(),
                                                                          self.entry_doctor.get(),
                                                                          self.todo.get(),
                                                                          self.todo_date.get()))

        self.btn_ok.destroy()

    def default_data(self):
        self.db.mycursor.execute('''SELECT * FROM bio WHERE id=%s''',
                                 (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.mycursor.fetchone()
        self.entry_doctor.insert(0, row[1])
        if row[2] != 'TODO':
            self.combobox.current(1)
        self.todo.insert(0, row[3])


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('SEARCH')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='SEARCH')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='CLOSE', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='SEARCH')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


class DB:
    def __init__(self):
        # self.conn = sqlite3.connect('bio.db')
        # self.c = self.conn.cursor()
        self.mydb = mysql.connector.connect(
            host="freedb.tech",
            user="freedbtech_adminadmin",
            password="adminadmin"
        )
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("USE freedbtech_bio")

        self.mycursor.execute(
            '''CREATE TABLE IF NOT EXISTS bio (id integer NOT NULL AUTO_INCREMENT primary key, doctor text, patient text, todo text, todo_date date )''')
        self.mydb.commit()


    def insert_data(self, doctor, patient, todo, todo_date):
        self.mycursor.execute('''INSERT INTO bio (doctor, patient, todo, todo_date) VALUES (%s, %s, %s, %s)''',
                              (doctor, patient, todo, todo_date))
        self.mydb.commit()


if __name__ == "__main__":
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title("Biomed Tibb Merkezi")
    root.geometry("99999x99999")
    root.mainloop()
