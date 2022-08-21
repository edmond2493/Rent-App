from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkcalendar import *
import sqlite3
from Hist import History
from PIL import Image, ImageTk
from io import BytesIO
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

root = Tk()
root.title("Car Rent")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
app_width = 1400
app_height = 900
root.geometry(f'{app_width}x{app_height}+{(screen_width//2)-(app_width//2)}+{(screen_height//2)-(app_height//2)}')
root.resizable(False, False)
for row_1 in range(20):
    root.rowconfigure(row_1, weight=1)
    root.columnconfigure(row_1, weight=1)

conn1 = sqlite3.connect('Rent.db')
cur1 = conn1.cursor()
cur1.execute("""CREATE TABLE IF NOT EXISTS Cars (
                model text,
                name text,
                price integer,
                status text,
                photo blob,
                departure timestamp,
                arrival timestamp)""")
cur1.execute("""CREATE TABLE IF NOT EXISTS History (
                model text,
                name text,
                price integer,
                departure timestamp,
                arrival timestamp,
                total integer)""")
conn1.commit()
conn1.close()
all_cars = f'SELECT model, name, photo, oid FROM Cars ORDER BY model'
available = f'SELECT model, name, photo, oid FROM Cars WHERE status ="Available" ORDER BY model'
rented = f'SELECT model, name, photo, oid FROM Cars WHERE status ="Rented" ORDER BY model'


class TopFrame:
    def __init__(self):
        # ------------------------------------------ TOP LEFT FRAME ----------------------------------------------------
        self.f_top_l = Frame(root, height=100, width=498, bg='#b3b3b3')
        self.f_top_l.grid(row=0, column=0, rowspan=3, columnspan=7, sticky="NSEW")
        self.f_top_l.grid_propagate(False)
        for row_2 in range(5):
            self.f_top_l.columnconfigure(row_2, weight=1)
        for row_3 in range(3):
            self.f_top_l.rowconfigure(row_3, weight=1)
        self.l_app_name = Label(self.f_top_l, text="Car Rent", font=('arial', 30, 'italic'), bg='#b3b3b3')
        self.l_app_name.grid(row=1, column=2)

        # -----------------------------------------TOP RIGHT FRAME------------------------------------------------------
        self.f_top_r = Frame(root, height=100, width=900, bg='#b3b3b3')
        self.f_top_r.grid(row=0, column=8, columnspan=13, rowspan=3, sticky="NSEW")
        self.f_top_r.grid_propagate(False)
        for row_2 in range(12):
            self.f_top_r.columnconfigure(row_2, weight=1)
        for row_3 in range(3):
            self.f_top_r.rowconfigure(row_3, weight=1)

        # --------------------------------------BUTTONS TOP RIGHT FRAME-------------------------------------------------
        self.bt_all = Button(self.f_top_r, text='All Cars', width=15, height=2,
                             command=lambda: Photos().default_cars(all_cars))
        self.bt_all.grid(row=1, column=0, columnspan=2)
        self.e_search = Entry(self.f_top_r, width=18)
        self.e_search.grid(row=2, column=0, padx=(14, 0), ipady=3)
        self.bt_available = Button(self.f_top_r, text='Available', width=15, height=2,
                                   command=lambda: Photos().default_cars(available))
        self.bt_available.grid(row=1, column=2, columnspan=2)
        self.bt_rented = Button(self.f_top_r, text='Rented', width=15, height=2,
                                command=lambda: Photos().default_cars(rented))
        self.bt_rented.grid(row=1, column=4, columnspan=2)
        self.bt_add = Button(self.f_top_r, text='Add Car', width=15, height=2, command=self.add_new)
        self.bt_add.grid(row=1, column=6, columnspan=2)
        self.bt_delete = Button(self.f_top_r, text='Delete', width=15, height=2, command=Photos().delete)
        self.bt_delete.grid(row=1, column=8, columnspan=2)
        self.bt_history = Button(self.f_top_r, text='History', width=15, height=2, command=lambda: History(root))
        self.bt_history.grid(row=1, column=10, columnspan=2)
        self.e_search.bind('<KeyRelease>', lambda event: Photos().default_cars(f"""SELECT model, 
        name, photo, oid FROM Cars WHERE model LIKE '%{self.e_search.get()}%' 
        OR name LIKE '%{self.e_search.get()}%'
        OR price LIKE '%{self.e_search.get()}%'"""))

        # ----------------------------------------NEW CAR FRAME---------------------------------------------------------
        self.f_new = Frame(root, height=100, width=900, bg='#b3b3b3')
        self.f_new.grid_propagate(False)
        for row_2 in range(12):
            self.f_new.columnconfigure(row_2, weight=1)
        for row_3 in range(3):
            self.f_new.rowconfigure(row_3, weight=1)
        self.l_model = Label(self.f_new, text='Model')
        self.l_model.grid(row=1, column=0)
        self.l_status = Label(self.f_new, text='Status')
        self.l_status.grid(row=1, column=2)
        self.l_name = Label(self.f_new, text='Name')
        self.l_name.grid(row=1, column=4)
        self.l_price = Label(self.f_new, text="Price")
        self.l_price.grid(row=1, column=6)
        self.cars = ['Audi', 'BMW', 'Citroen', 'Ford', 'Honda', 'Mazda', 'Mercedes', 'Mitsubishi',
                     'Nissan', 'Peugeot', 'Porsche', 'Renault', 'Toyota', 'Volkswagen', 'Volvo']
        self.sv_model = StringVar(self.f_new)
        self.om_model = ttk.OptionMenu(self.f_new, self.sv_model, '', *self.cars)
        self.om_model.grid(row=1, column=1)
        self.sv_status = StringVar(self.f_new)
        self.status = ttk.OptionMenu(self.f_new, self.sv_status, 'Available', 'Available',
                                     'Rented', 'Out of service')
        self.status.grid(row=1, column=3)
        self.e_name = Entry(self.f_new)
        self.e_name.grid(row=1, column=5)
        self.e_price = Entry(self.f_new)
        self.e_price.grid(row=1, column=7)
        self.bt_add_photo = Button(self.f_new, text="Photo", command=self.file_dialogs)
        self.bt_add_photo.grid(row=1, column=9)
        self.bt_confirm = Button(self.f_new, text='Confirm', command=self.confirm)
        self.bt_confirm.grid(row=4, column=9)
        self.bt_cancel = Button(self.f_new, text='Cancel', command=self.cancel)
        self.bt_cancel.grid(row=4, column=10)
        self.get_image = ''

    def file_dialogs(self):
        self.get_image = filedialog.askopenfilenames(title="SELECT IMAGE",
                                                     filetypes=(("All file", "*.*"),
                                                                ("png", "*.png"), ("jpg", "*.jpg")))

    @staticmethod
    def convert_image(filename):
        with open(filename, "rb") as file:
            photo_image = file.read()
        return photo_image

    def confirm(self):
        conn = sqlite3.connect('Rent.db')
        cur = conn.cursor()
        insert_photo = self.convert_image(self.get_image[-1])

        cur.execute("INSERT INTO Cars VALUES(:model, :name, :price, :status, :photo, :departure, :arrival)",
                    {
                        'model': self.sv_model.get(),
                        'name': self.e_name.get(),
                        'price': self.e_price.get(),
                        'status': self.sv_status.get(),
                        'photo': insert_photo,
                        'departure': '',
                        'arrival': ''
                    })
        conn.commit()
        conn.close()
        self.e_name.delete(0, END)
        self.sv_model.set('Select')
        self.e_price.delete(0, END)
        self.sv_status.set('Available')

        TopFrame()
        Category()
        Photos().default_cars(all_cars)

    def add_new(self):
        self.f_new.grid(row=0, column=8, columnspan=13, rowspan=2, sticky="NSEW")

    def cancel(self):
        self.f_new.grid_remove()
        self.f_top_r.grid()


class Category:
    def __init__(self):
        f_category = Frame(root, height=798, width=250, bg='#b3b3b3')
        f_category.grid(row=4, column=0, rowspan=17, columnspan=3, sticky="SW")
        f_category.grid_propagate(False)
        for row_2 in range(3):
            f_category.columnconfigure(row_2, weight=1)
        conn = sqlite3.connect('Rent.db')
        cur = conn.cursor()
        cur.execute("SELECT DISTINCT model FROM Cars ORDER BY model")
        info = cur.fetchall()
        row = 0
        for i in info:
            Button(f_category, text=i[0], width=15, height=2, command=lambda n=i[0]: Photos().default_cars(f'''
            SELECT model, name, photo, oid FROM Cars WHERE model ="{n}"''')).\
                grid(row=row, column=1, pady=10)
            row += 1

        conn.commit()
        conn.close()


class Photos:
    def __init__(self):
        self.f_photos = Frame(root, height=798, width=1148, bg='#A1D163')
        self.f_photos.grid(row=4, column=4, rowspan=17, columnspan=17, sticky="NSEW")
        self.f_photos.grid_propagate(False)
        self.f_delete = ''
        self.c_cnv = Canvas(self.f_photos, height=800, width=1130, bg='#A1D163')
        self.c_cnv.pack(side=LEFT, fill=BOTH, expand=1)
        self.s_scroll = ttk.Scrollbar(self.f_photos, orient=VERTICAL, command=self.c_cnv.yview)
        self.s_scroll.pack(side=RIGHT, fill=Y)
        self.c_cnv.configure(yscrollcommand=self.s_scroll.set)
        self.c_cnv.bind('<Configure>', lambda event: self.c_cnv.configure(scrollregion=self.c_cnv.bbox('all')))
        self.f_scroll = Frame(self.c_cnv, bg='#A1D163')
        self.c_cnv.create_window((0, 0), window=self.f_scroll, anchor='nw')
        for row_2 in range(4):
            self.f_scroll.columnconfigure(row_2, weight=1)

    def default_cars(self, query, *_):
        conn = sqlite3.connect('Rent.db')
        cur = conn.cursor()
        cur.execute(query)
        info = cur.fetchall()
        column = 0
        row = 0
        row2 = 1
        z = 0
        width = 272
        height = 200
        for i in info:
            img = Image.open(BytesIO(i[2]))
            img = img.resize((width, height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            btn = Button(self.f_scroll, image=photo, width=272, height=200,
                         command=lambda n=i[3]: Full(str(n)))
            btn.image = photo
            btn.grid(row=row, column=column, padx=2, pady=2)
            lbl = Label(self.f_scroll, text=f"{i[0]} - {i[1]}", bg='#A1D163')
            lbl.grid(row=row2, column=column)
            if z < 3:
                column += 1
                z += 1
            elif z == 3:
                z = 0
                column = 0
                row2 += 2
                row += 2
        conn.commit()
        conn.close()

    def delete(self):
        self.f_photos.grid_remove()
        self.f_delete = Frame(root, height=748, width=1148, bg='orange')
        self.f_delete.grid(row=5, column=4, rowspan=15, columnspan=17, sticky="NSEW")
        self.f_delete.grid_propagate(False)

        self.c_cnv = Canvas(self.f_delete, height=750, width=1130, bg='red')
        self.c_cnv.pack(side=LEFT, fill=BOTH, expand=1)
        self.s_scroll = ttk.Scrollbar(self.f_delete, orient=VERTICAL, command=self.c_cnv.yview)
        self.s_scroll.pack(side=RIGHT, fill=Y)
        self.c_cnv.configure(yscrollcommand=self.s_scroll.set)
        self.c_cnv.bind('<Configure>', lambda event: self.c_cnv.configure(scrollregion=self.c_cnv.bbox('all')))
        self.f_scroll = Frame(self.c_cnv, bg='red')
        self.c_cnv.create_window((0, 0), window=self.f_scroll, anchor='nw')
        for row_2 in range(4):
            self.f_scroll.columnconfigure(row_2, weight=1)
        f_delete_l = Frame(root, height=48, width=1148, bg='red')
        f_delete_l.grid(row=4, column=4, columnspan=17, rowspan=1, sticky="NSEW")
        f_delete_l.grid_propagate(False)
        for row_2 in range(3):
            f_delete_l.columnconfigure(row_2, weight=1)
            f_delete_l.rowconfigure(row_2, weight=1)
        l_delete = Label(f_delete_l, text="Delete car with a click", font=('arial', 20, 'bold'), bg='red')
        l_delete.grid(row=1, column=1)

        conn = sqlite3.connect('Rent.db')
        cur = conn.cursor()
        cur.execute(f'SELECT model, name, photo, oid, status FROM Cars WHERE status = "Available" ORDER BY model')
        info = cur.fetchall()
        column = 0
        row = 1
        row2 = 2
        z = 0
        width = 272
        height = 200

        for i in info:
            img = Image.open(BytesIO(i[2]))
            img = img.resize((width, height), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            btn = Button(self.f_scroll, image=photo, width=272, height=200, command=lambda n=i[3], m=i[4]: dlt(n, m))
            btn.image = photo
            btn.grid(row=row, column=column, padx=2, pady=2)
            lbl = Label(self.f_scroll, text=f"{i[0]} - {i[1]}", bg='red')
            lbl.grid(row=row2, column=column)
            if z < 3:
                column += 1
                z += 1
            elif z == 3:
                z = 0
                column = 0
                row2 += 2
                row += 2
        conn.commit()
        conn.close()

        def dlt(oid, status):
            if status == "Available":
                rsp = messagebox.askyesno("Delete", "proceed?")
                if rsp == 1:
                    conn2 = sqlite3.connect('Rent.db')
                    cur2 = conn2.cursor()
                    cur2.execute("DELETE FROM Cars WHERE oid = " + str(oid))
                    conn2.commit()
                    conn2.close()
                    Photos().delete()
                else:
                    pass
            else:
                Label(f_delete_l, text='Car is not available').grid(row=2, column=1)


class Full:
    def __init__(self, oid):
        Photos().f_photos.grid_remove()
        self.id = oid
        f_full = Frame(root, height=798, width=1148, bg='#7FE5E2')
        f_full.grid(row=4, column=4, rowspan=17, columnspan=17, sticky="SE")
        f_full.grid_propagate(False)
        for row_2 in range(14):
            f_full.columnconfigure(row_2, weight=1)
            f_full.rowconfigure(row_2, weight=1)
        for row_3 in range(5):
            f_full.rowconfigure(row_3, weight=1)
        calendar = Calendar(root, selectmode="day", date_pattern="yyyy-mm-dd")
        cal = calendar.get_date()
        conn = sqlite3.connect('Rent.db')
        cur = conn.cursor()
        cur.execute("SELECT model, name, price, status, photo, departure, arrival FROM cars WHERE oid = " + oid)
        info = cur.fetchall()
        self.i = info[0]

        width = 950
        height = 600
        img = Image.open(BytesIO(self.i[4]))
        img = img.resize((width, height), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
        lbl = Label(f_full, image=photo, width=950, height=600)
        lbl.image = photo
        lbl.grid(row=0, rowspan=3, column=2, columnspan=10, sticky="N")
        l_text = Label(f_full, text=f"{self.i[0]} - {self.i[1]} - Price {self.i[2]}/day", font=('arial', 20, 'bold'))
        l_text.grid(row=4, column=4, columnspan=4)
        l_status = Label(f_full, text=self.i[3], font=('arial', 20, 'bold'))
        l_status.grid(row=4, column=8)
        bt_edit = Button(f_full, text="Edit", width=15, height=2, command=lambda: Edit(oid))
        bt_edit.grid(row=5, column=5)
        bt_rent = Button(f_full, text="Rent", width=15, height=2, command=lambda: self.rent(cal))
        bt_confirm = Button(f_full, text="Confirm", width=15, height=2, command=lambda: self.confirm(cal))
        if self.i[3] == 'Available':
            bt_rent.grid(row=5, column=6)
        elif self.i[3] == 'Rented':
            bt_confirm.grid(row=5, column=6)
            cur.execute(f'''SELECT
                             departure,
                             julianday('{cal}') - julianday(departure) AS difference
                            FROM Cars WHERE oid =''' + oid)
            info = cur.fetchall()
            j = info[0][1]
            total = self.i[2] * j
            l_total = Label(f_full, text=f"day {round(j)} - Total to pay = {round(total, 2)}")
            l_total.grid(row=5, column=8)

    def rent(self, depart):
        conn = sqlite3.connect('Rent.db')
        cur = conn.cursor()
        try:
            cur.execute(f'''SELECT
                            departure, arrival, 
                            JULIANDAY(arrival) - JULIANDAY(departure) 
                            AS difference FROM Cars WHERE oid = ''' + self.id)

            cur.execute("UPDATE Cars SET departure=NULL, arrival=NULL WHERE oid = " + self.id)
        except sqlite3.NotSupportedError:
            pass
        cur.execute("UPDATE Cars SET departure = :departure WHERE oid = :oid",
                    {
                        'departure': depart,
                        'arrival': '',
                        'oid': self.id
                    })
        cur.execute("UPDATE Cars SET status = :status WHERE oid = :oid", {'status': 'Rented', 'oid': self.id})
        conn.commit()
        conn.close()
        Full(self.id)

    def confirm(self, arrival):
        conn = sqlite3.connect('Rent.db')
        cur = conn.cursor()
        cur.execute(f"""UPDATE Cars 
                    SET arrival = :arrival,
                        status = :status
                    WHERE oid = :oid""",
                    {'arrival': arrival, 'status': 'Available', 'oid': self.id})
        cur.execute(f'''SELECT
                        departure, arrival, 
                        JULIANDAY(arrival) - JULIANDAY(departure) 
                        AS difference FROM Cars WHERE oid = ''' + self.id)
        tot = cur.fetchone()
        cur.execute("INSERT INTO History VALUES(:model, :name, :price, :departure, :arrival, :total)",
                    {
                        'model': self.i[0],
                        'name': self.i[1],
                        'price': self.i[2],
                        'departure': str(self.i[5]),
                        'arrival': str(tot[1]),
                        'total': int(tot[2] or 0) * self.i[2]
                    })
        conn.commit()
        conn.close()
        Full(self.id)


class Edit:
    def __init__(self, oid):
        self.top_edit = Toplevel(root, bg='green')
        top_width = 650
        top_height = 300
        self.top_edit.geometry(f'{top_width}x{top_height}+{(screen_width//2)-(top_width//2)}'
                               f'+{(screen_height//2)-(top_height//2)}')
        self.top_edit.attributes('-topmost', 'true')
        self.id = oid
        self.conn = sqlite3.connect('Rent.db')
        self.cur = self.conn.cursor()
        self.cur.execute('SELECT model, name, price, photo FROM Cars WHERE oid = ' + oid)
        i = self.cur.fetchone()

        self.l_model = Label(self.top_edit, text='Model: ')
        self.l_model.grid(row=0, column=0)
        self.e_model = Entry(self.top_edit, width=15)
        self.e_model.grid(row=0, column=1)
        self.e_model.insert(0, i[0])

        self.l_name = Label(self.top_edit, text='Name: ')
        self.l_name.grid(row=1, column=0)
        self.e_name = Entry(self.top_edit, width=15)
        self.e_name.grid(row=1, column=1, ipady=10)
        self.e_name.insert(0, i[1])

        self.l_price = Label(self.top_edit, text='Price: ')
        self.l_price.grid(row=2, column=0)
        self.e_price = Entry(self.top_edit, width=15)
        self.e_price.grid(row=2, column=1)
        self.e_price.insert(0, i[2])

        self.bt_confirm = Button(self.top_edit, text='confirm', command=self.confirm)
        self.bt_confirm.grid(row=3, column=0)
        self.bt_cancel = Button(self.top_edit, text='cancel', command=self.top_edit.destroy)
        self.bt_cancel.grid(row=3, column=1)

        self.width_2 = 465
        self.height_2 = 290
        self.img = Image.open(BytesIO(i[3]))
        self.img = self.img.resize((self.width_2, self.height_2), Image.LANCZOS)
        self.photo = ImageTk.PhotoImage(self.img)
        self.lbl2 = Button(self.top_edit, image=self.photo, width=465, height=290, command=self.file)
        self.lbl2.image = self.photo
        self.lbl2.grid(row=0, column=2, rowspan=10, sticky="E")
        self.get_image = ''

    @staticmethod
    def convert_image(filename):
        with open(filename, "rb") as file:
            photo_image = file.read()
        return photo_image

    def file(self):
        try:
            self.get_image = filedialog.askopenfilenames(title="SELECT IMAGE", parent=self.top_edit,
                                                         filetypes=(("All file", "*.*"),
                                                                    ("png", "*.png"), ("jpg", "*.jpg")))

            self.img = Image.open(f'{self.get_image[0]}')
            self.img = self.img.resize((self.width_2, self.height_2), Image.LANCZOS)
            self.photo = ImageTk.PhotoImage(self.img)
            self.lbl2.configure(image=self.photo)
        except FileExistsError:
            pass

    def confirm(self):
        insert_photo = self.convert_image(self.get_image[-1])
        self.cur.execute('UPDATE Cars SET model = :model, name = :name, price = :price, photo = :photo '
                         'WHERE oid = ' + self.id,
                         {'model': self.e_model.get(),
                          'name': self.e_name.get(),
                          'price': self.e_price.get(),
                          'photo': insert_photo
                          })
        self.conn.commit()
        self.conn.close()
        self.top_edit.destroy()
        Full(self.id)


TopFrame()
Category()
Photos().default_cars(all_cars)
root.mainloop()
