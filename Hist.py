from tkinter import *
import sqlite3
from tkinter import messagebox
from tkinter import ttk


class History:
    def __init__(self, root):
        self.root = root
        self.f_history = Toplevel(self.root, bg='orange')
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        top_height = 500
        top_width = 680
        self.f_history.geometry(f'{top_width}x{top_height}+{(screen_width // 2) - (top_width // 2)}'
                                f'+{(screen_height // 2) - (top_height // 2)}')
        self.f_history.attributes('-topmost', 'true')
        self.f_history.grid_propagate(False)
        self.f_history.resizable(False, False)

        self.conn = sqlite3.connect('Rent.db')
        self.cur = self.conn.cursor()
        self.fetch = ''
        self.my_tree = ttk.Treeview()
        self.name = 'oid'
        self.order = 'ASC'
        self.bt_delete = Button(self.f_history, text='Delete', command=self.delete_history)
        self.bt_delete.grid(row=1, column=1, pady=15, padx=30, ipady=5, ipadx=30)
        self.e_search = Entry(self.f_history, width=20)
        self.e_search.grid(row=1, column=0, pady=15, ipady=5)
        self.e_search.bind('<KeyRelease>', self.search_history)
        self.search_history()

    def search_history(self, *_):
        self.conn = sqlite3.connect('Rent.db')
        self.cur = self.conn.cursor()
        if self.e_search.get() == '':
            self.cur.execute(f"SELECT *, oid FROM History ORDER BY {self.name} {self.order}")
            self.fetch = self.cur.fetchall()
        else:
            self.cur.execute(f"""SELECT model, 
            name, price, departure, arrival, total, oid FROM History WHERE model LIKE '%{self.e_search.get()}%' 
            OR name LIKE '%{self.e_search.get()}%'
            OR price LIKE '%{self.e_search.get()}%'
            OR departure LIKE '%{self.e_search.get()}%'
            OR arrival LIKE '%{self.e_search.get()}%'
            OR total LIKE '%{self.e_search.get()}%'
            OR oid LIKE '%{self.e_search.get()}%' ORDER BY {self.name} {self.order}""")
            self.fetch = self.cur.fetchall()

        self.my_tree = ttk.Treeview(self.f_history, height=20)
        s_scroll = Scrollbar(self.f_history, orient='vertical', command=self.my_tree.yview)
        s_scroll.grid(row=3, rowspan=10, column=10, sticky="NS", padx=(0, 10))
        self.my_tree.config(yscrollcommand=s_scroll.set)
        self.my_tree['columns'] = \
            ('oID', 'model', 'name', 'price', 'departure', 'arrival', 'total')
        self.my_tree.column('#0', width=0, minwidth=0)
        self.my_tree.column('oID', anchor=W, width=60, minwidth=25)
        self.my_tree.column('model', anchor=W, width=100, minwidth=25)
        self.my_tree.column('name', anchor=W, width=120, minwidth=25)
        self.my_tree.column('price', anchor=W, width=60, minwidth=25)
        self.my_tree.column('departure', anchor=W, width=100, minwidth=25)
        self.my_tree.column('arrival', anchor=W, width=100, minwidth=25)
        self.my_tree.column('total', anchor=W, width=100, minwidth=25)

        for h in self.my_tree['columns']:
            self.my_tree.heading(h, text=h, anchor=W, command=lambda n=h: sort(n))
        x = 0
        for info in self.fetch:
            self.my_tree.insert(parent='', index='end', iid=str(x), text='',
                                values=(info[6], info[0], info[1], info[2], info[3],
                                        info[4], info[5]))
            x += 1
        self.my_tree.grid(row=3, column=0, columnspan=9, padx=(10, 0))

        def sort(name):
            self.name = name
            if self.order == 'ASC':
                self.order = 'DESC'
            elif self.order == 'DESC':
                self.order = 'ASC'
            self.search_history()

    def delete_history(self):
        rsp = messagebox.askyesno(title="Delete", message="Delete this record from history?", parent=self.f_history)
        if rsp == 1:
            self.conn = sqlite3.connect('Rent.db')
            self.cur = self.conn.cursor()
            y = self.my_tree.selection()
            for i in y:
                item = self.my_tree.item(i, "values")[0]
                self.cur.execute("DELETE FROM History WHERE oid = " + item)
                self.my_tree.delete(i)
            self.conn.commit()
            self.conn.close()
        else:
            pass
