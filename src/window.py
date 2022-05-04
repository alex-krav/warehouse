import tkinter as tk
from tkinter import ttk
from tkinter import font
from tkinter import messagebox
import logging
from random import randrange

title = "Управління складом"

class View():
    
    def __init__(self, root):
        self.root = root
        self.mainframe = None
        self.cat_id = 0
        self.good_lambda = lambda item: (item[0], item[1] + ' ' + item[2], item[3], item[4], item[5], item[6])
        self.setup()

    def setup(self):
        self.setup_containers()
        self.setup_list_cat()
        self.setup_list_good()
        self.setup_add_cat()
        self.setup_add_good()

    def setup_containers(self):
        # main containers
        self.list_cat = tk.Frame(self.root, bg='grey', width=800, height=200, padx=3, pady=3) #cyan,grey,white,lavender
        self.list_good = tk.Frame(self.root, bg='grey', width=800, height=400, padx=3, pady=3)
        self.add_cat = tk.Frame(self.root, bg='cyan', width=300, height=200, padx=3, pady=3)
        self.add_good = tk.Frame(self.root, bg='lavender', width=300, height=400, padx=3, pady=3)
        # ttk.Separator(self.add_good, orient=tk.HORIZONTAL).grid(column=0, row=0, columnspan=2) #rowspan=1, sticky='ns'

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.list_cat.grid(row=0, column=0, sticky="nsew") 
        self.list_good.grid(row=1, column=0, sticky="nsew")
        self.add_cat.grid(row=0, column=1, sticky="nsew")
        self.add_good.grid(row=1, column=1, sticky="nsew")

    def setup_list_cat(self):
        list_cat_label = tk.Label(self.list_cat, text='Категорії')
        edit_cat_button = tk.Button(self.list_cat, text='Редагувати', command=self.edit_category)
        del_cat_button = tk.Button(self.list_cat, text='Видалити', command=self.delete_category)

        self.list_cat.grid_rowconfigure(0, weight=1)
        self.list_cat.grid_columnconfigure(0, weight=1)

        list_cat_label.grid(row=0, column=0, sticky='w')
        edit_cat_button.grid(row=0, column=1, sticky='e')
        del_cat_button.grid(row=0, column=2, sticky='e')

        self.catCols = ('Назва',)
        self.categories = [
            ('продукти харчування',1),
            ('побутова техніка',2),
            ('зброя',3),
            ('спорт',4),
            ('туризм',5),
            ('медикаменти',6),
            ('книжки',7),
            ('будівельні матеріали',8),
            ('косметика',9),
            ('авто',10),
            ('ремонт',11),
            ('сад & город',12),
            ('лаки і фарби',13),
        ]
        self.catsTree = self.create_treeview(self.list_cat, self.catCols)
        self.load_data(self.catsTree, self.catCols, self.categories)
    
    def delete_category(self):
        currentCat = self.catsTree.focus()
        catValues = self.catsTree.item(currentCat).get('values')
        self.categories.remove(tuple(catValues))

        self.catsTree = self.create_treeview(self.list_cat, self.catCols)
        self.load_data(self.catsTree, self.catCols, self.categories)

        self.good_cat.set(self.categories[0][0]) # default value
        self.good_cat_select = tk.OptionMenu(self.add_good, self.good_cat, *list(map(lambda t: t[0], self.categories)))
        self.good_cat_select.grid(row=1, column=1, sticky='ne')

    def delete_good(self):
        currentGood = self.goodsTree.focus()
        goodValues = self.goodsTree.item(currentGood).get('values')
        goodTuple = (goodValues[0], *(goodValues[1].split()), str(goodValues[2]), goodValues[3], goodValues[4], goodValues[5])
        logging.debug(goodTuple)
        self.goods.remove(tuple(goodTuple))

        self.goodsTree = self.create_treeview(self.list_good, self.goodCols)
        self.load_data(self.goodsTree, self.goodCols, self.goods, self.good_lambda)

    def create_treeview(self, root, dataCols):
        # list of categories
        tree = ttk.Treeview(root, columns=dataCols, show='headings')
        ysb = ttk.Scrollbar(root, orient=tk.VERTICAL, command= tree.yview)
        xsb = ttk.Scrollbar(root, orient=tk.HORIZONTAL, command= tree.xview)
        tree['yscroll'] = ysb.set
        tree['xscroll'] = xsb.set

        tree.grid(row=1, column=0, columnspan=3, sticky=tk.NSEW)
        ysb.grid(row=1, column=3, sticky=tk.NS)
        xsb.grid(row=2, column=0, sticky=tk.EW)

        return tree

    def load_data(self, tree, dataCols, items, mapping_func=None):
        for c in dataCols:
            tree.heading(c, text=c.title())            
            # tree.column(c, width=font.Font().measure(c.title()))

        for item in items: 
            # tree.insert("", 'end', item[0], text=item[0], values=(item[1].replace(" ", "\ ")))
            if mapping_func:
                item = mapping_func(item)
            tree.insert('', 'end', values=item)
            
            # and adjust column widths if necessary
            # for idx, val in enumerate(item):
                # iwidth = font.Font().measure(val)
                # if tree.column(dataCols[idx], 'width') < iwidth:
                    # tree.column(dataCols[idx], width = iwidth)

    def setup_list_good(self):
        list_good_label = tk.Label(self.list_good, text='Товари')
        edit_good_button = tk.Button(self.list_good, text='Редагувати', command=self.edit_good)
        del_good_button = tk.Button(self.list_good, text='Видалити', command=self.delete_good)
        export_label = tk.Label(self.list_good, text='Експорт')
        export_sqlite_postgres_button = tk.Button(self.list_good, text='SQLite ->\nPostgres', command=self.export_sqlite_postgres)
        export_postgres_mysql_button = tk.Button(self.list_good, text='Postgres\n-> MySQL', command=self.export_postgres_mysql)

        self.list_good.grid_rowconfigure(0, weight=1)
        self.list_good.grid_columnconfigure(0, weight=1)

        list_good_label.grid(row=0, column=0, sticky="w")
        edit_good_button.grid(row=0, column=1, sticky="e")
        del_good_button.grid(row=0, column=2, sticky="e")

        export_label.grid(row=3, column=0, sticky='w')
        export_sqlite_postgres_button.grid(row=3, column=1, sticky='e')
        export_postgres_mysql_button.grid(row=3, column=2, sticky='e')

        self.goodCols = ('Назва','Кількість','Термін, дн','Початок','Кінець')
        self.goods = [
            ('молоко','1','літр','3','01.05.2022','04.05.2022',1),
            ('телевізор','1','штука','10','01.05.2022','11.05.2022',2),
            ('Javelin','100','штука','7','12.04.2022','19.04.2022',3),
            ('каремат','18','штука','5','19.04.2022','24.04.2022',4),
            ('спальний мішок','50','штука','8','10.03.2022','19.03.2022',5),
            ('турнікет','10','штука','14','1.05.2022','15.05.2022',6),
            ('бетон','10','тонна','14','1.05.2022','15.05.2022',7),
            ('морозиво','3','палета','14','1.05.2022','15.05.2022',8),
            ('танк Т-72','1','штука','14','1.05.2022','15.05.2022',9),
            ('дизельне паливо','3','тонна','14','1.05.2022','15.05.2022',10),
        ]
        self.goodsTree = self.create_treeview(self.list_good, self.goodCols)
        self.load_data(self.goodsTree, self.goodCols, self.goods, self.good_lambda)
            
    def setup_add_cat(self):
        # add_cat
        add_cat_label = tk.Label(self.add_cat, text='Категорія')
        cat_title_label = tk.Label(self.add_cat, text='Назва')
        self.cat_title_input = tk.Entry(self.add_cat)
        save_cat_button = tk.Button(self.add_cat, text='Зберегти', command=self.save_category)

        self.add_cat.grid_rowconfigure(0, weight=1)
        self.add_cat.grid_columnconfigure(0, weight=1)

        add_cat_label.grid(row=0, column=0, sticky='nw')
        cat_title_label.grid(row=1, column=0, sticky='nw')
        self.cat_title_input.grid(row=1, column=1, sticky='ne')
        save_cat_button.grid(row=2, column=1, sticky='se')
    
    def setup_add_good(self):
        # add_good
        add_good_label = tk.Label(self.add_good, text='Товар')
        good_cat_label = tk.Label(self.add_good, text='Категорія')
        self.good_cat = tk.StringVar(self.add_good)
        self.good_cat.set(self.categories[0][0]) # default value
        self.good_cat_select = tk.OptionMenu(self.add_good, self.good_cat, *list(map(lambda t: t[0], self.categories))) 
        # good_cat_select.pack()
        good_title_label = tk.Label(self.add_good, text='Назва')
        good_title_input = tk.Entry(self.add_good)

        good_quantity_label = tk.Label(self.add_good, text='Кількість')
        good_quantity_input = tk.Entry(self.add_good)
        good_unit_label = tk.Label(self.add_good, text='Одиниця виміру')
        good_unit_input = tk.Entry(self.add_good)
        good_term_label = tk.Label(self.add_good, text='Термін, днів')
        good_term_input = tk.Entry(self.add_good)
        good_start_label = tk.Label(self.add_good, text='Дата початку зберігання')
        good_start_input = tk.Entry(self.add_good)
        good_end_label = tk.Label(self.add_good, text='Дата кінця зберігання')
        good_end_input = tk.Entry(self.add_good)
        save_cat_button = tk.Button(self.add_good, text='Зберегти', command=self.save_good)

        self.add_good.grid_rowconfigure(0, weight=1)
        self.add_good.grid_columnconfigure(0, weight=1)

        add_good_label.grid(row=0, column=0, sticky='nw')
        good_cat_label.grid(row=1, column=0, sticky='nw')
        self.good_cat_select.grid(row=1, column=1, sticky='ne')
        good_title_label.grid(row=2, column=0, sticky='nw')
        good_title_input.grid(row=2, column=1, sticky='ne')
        good_quantity_label.grid(row=3, column=0, sticky='nw')
        good_quantity_input.grid(row=3, column=1, sticky='ne')
        good_unit_label.grid(row=4, column=0, sticky='nw')
        good_unit_input.grid(row=4, column=1, sticky='ne')
        good_term_label.grid(row=5, column=0, sticky='nw')
        good_term_input.grid(row=5, column=1, sticky='ne')
        good_start_label.grid(row=6, column=0, sticky='nw')
        good_start_input.grid(row=6, column=1, sticky='ne')
        good_end_label.grid(row=7, column=0, sticky='nw')
        good_end_input.grid(row=7, column=1, sticky='ne')
        save_cat_button.grid(row=8, column=1, sticky='se')
          
    def export_sqlite_postgres(self):
        logging.info("Export SQLite to PostgreSQL")
    
    def export_postgres_mysql(self):
        logging.info("Export PostgreSQL to MySQL")

    def save_category(self):
        name = self.cat_title_input.get().strip().lower()
        if not name:
            messagebox.showwarning("Категорія", "Пуста назва")
        else:
            if self.cat_id: #edit existing
                i = 0
                found = False
                for i in range(len(self.categories)):
                    if self.categories[i][1] != self.cat_id and self.categories[i][0] == name:
                        found = True
                        break

                if found:
                    messagebox.showwarning("Категорія", "Така категорія вже є")
                else:
                    i = 0
                    for i in range(len(self.categories)):
                        if self.categories[i][1] == self.cat_id:
                            self.categories[i] = (name, self.cat_id)
                            break
            else: #add new
                found = False
                i = 0
                for i in range(len(self.categories)):
                    if self.categories[i][0] == name:
                        found = True
                        break

                if found:
                    messagebox.showwarning("Категорія", "Така категорія вже є")
                else:
                    nameTuple = (name, randrange(100,1000))
                    self.categories.append(nameTuple)                

            self.cat_id = 0
            self.cat_title_input.delete(0, 'end')

            self.catsTree = self.create_treeview(self.list_cat, self.catCols)
            self.load_data(self.catsTree, self.catCols, self.categories)

            self.good_cat.set(self.categories[0][0]) # default value
            self.good_cat_select = tk.OptionMenu(self.add_good, self.good_cat, *list(map(lambda t: t[0], self.categories))) 
            self.good_cat_select.grid(row=1, column=1, sticky='ne')

    def edit_category(self):
        currentCat = self.catsTree.focus()
        catName = self.catsTree.item(currentCat).get('values')
        
        # self.cat_title_input.setvar(catName[0])
        self.cat_id = catName[1]
        self.cat_title_input.delete(0,tk.END)
        self.cat_title_input.insert(0,catName[0])

        self.catsTree = self.create_treeview(self.list_cat, self.catCols)
        self.load_data(self.catsTree, self.catCols, self.categories)

        self.good_cat.set(self.categories[0][0]) # default value
        self.good_cat_select = tk.OptionMenu(self.add_good, self.good_cat, *list(map(lambda t: t[0], self.categories)))
        self.good_cat_select.grid(row=1, column=1, sticky='ne')

    def save_good(self):
        pass
    def edit_good(self):
        pass


def main():
    logging.basicConfig(format='[%(asctime)s] ln:%(lineno)d %(levelname)s: %(message)s', datefmt='%I:%M:%s', level=logging.DEBUG)
    logging.info('{} app started. Logger running.'.format(title))

    root = tk.Tk()
    root.title(title)
    root.geometry('{}x{}'.format(1100, 600))
    gui = View(root)
    root.mainloop()

if __name__ == "__main__":
    main()