import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import logging
from service import *
from model import *
import re


class View():
    """
    INIT
    """
    title = "Управління складом"
    date_pattern = re.compile("^\d{4}-\d{2}-\d{2}$")
    catCols = ('Назва', )
    goodCols = ('Назва', 'Кількість', 'Початок', 'Кінець', 'Термін, дн', )
  
    def __init__(self, root):
        self.good_id_edit = 0
        self.cat_id_edit = 0
        self.cat_id_show_goods = 0

        self.root = root
        self.mainframe = None
        self.cat_name = None

        self.setup()

    """
    CONTAINERS
    """
    def setup(self):
        self.setup_containers()
        self.setup_cat_list_frame()
        self.setup_good_list_frame()
        self.setup_cat_add_frame()
        self.setup_good_add_frame()

    def setup_containers(self):
        self.cat_list_frame = tk.Frame(self.root, bg='grey', width=1000, height=200, padx=3, pady=3)
        self.good_list_frame = tk.Frame(self.root, bg='grey', width=1000, height=400, padx=3, pady=3)
        self.cat_form_frame = tk.Frame(self.root, bg='cyan', width=300, height=200, padx=3, pady=3)
        self.good_form_frame = tk.Frame(self.root, bg='lavender', width=300, height=400, padx=3, pady=3)
        # ttk.Separator(self.add_good, orient=tk.HORIZONTAL).grid(column=0, row=0, columnspan=2) #rowspan=1, sticky='ns'

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.cat_list_frame.grid(row=0, column=0, sticky="nsew") 
        self.good_list_frame.grid(row=1, column=0, sticky="nsew")
        self.cat_form_frame.grid(row=0, column=1, sticky="nsew")
        self.good_form_frame.grid(row=1, column=1, sticky="nsew")

    def setup_cat_list_frame(self):
        list_cat_label = tk.Label(self.cat_list_frame, text='Категорії')
        show_goods_button = tk.Button(self.cat_list_frame, text='Вантажі', command=self.show_category_goods)
        edit_cat_button = tk.Button(self.cat_list_frame, text='Редагувати', command=self.populate_category_form)
        del_cat_button = tk.Button(self.cat_list_frame, text='Видалити', command=self.delete_category)

        self.cat_list_frame.grid_rowconfigure(0, weight=1)
        self.cat_list_frame.grid_columnconfigure(0, weight=1)

        list_cat_label.grid(row=0, column=0, sticky='w')
        show_goods_button.grid(row=0, column=1, sticky='e')
        edit_cat_button.grid(row=0, column=2, sticky='e')
        del_cat_button.grid(row=0, column=3, sticky='e')

        self.good_cat = tk.StringVar(self.good_form_frame)
        self.refresh_categories();

    def setup_good_list_frame(self):
        list_good_label = tk.Label(self.good_list_frame, text='Вантажі')
        edit_good_button = tk.Button(self.good_list_frame, text='Редагувати', command=self.populate_good_form)
        del_good_button = tk.Button(self.good_list_frame, text='Видалити', command=self.delete_good)
        export_label = tk.Label(self.good_list_frame, text='Експорт')
        export_sqlite_postgres_button = tk.Button(self.good_list_frame, text='SQLite ->\nPostgres', command=self.export_sqlite_postgres)
        export_postgres_mysql_button = tk.Button(self.good_list_frame, text='Postgres\n-> MySQL', command=self.export_postgres_mysql)

        self.good_list_frame.grid_rowconfigure(0, weight=1)
        self.good_list_frame.grid_columnconfigure(0, weight=1)

        list_good_label.grid(row=0, column=0, sticky="w")
        edit_good_button.grid(row=0, column=1, sticky="e")
        del_good_button.grid(row=0, column=2, sticky="e")

        export_label.grid(row=3, column=0, sticky='w')
        export_sqlite_postgres_button.grid(row=3, column=1, sticky='e')
        export_postgres_mysql_button.grid(row=3, column=2, sticky='e')

        self.refresh_goods()

    def setup_cat_add_frame(self):
        add_cat_label = tk.Label(self.cat_form_frame, text='Категорія')
        cat_title_label = tk.Label(self.cat_form_frame, text='Назва')
        self.cat_title_input = tk.Entry(self.cat_form_frame)
        edit_cat_button = tk.Button(self.cat_form_frame, text='Оновити', command=self.edit_category)
        add_cat_button = tk.Button(self.cat_form_frame, text='Створити', command=self.add_category)

        self.cat_form_frame.grid_rowconfigure(0, weight=1)
        self.cat_form_frame.grid_columnconfigure(0, weight=1)

        add_cat_label.grid(row=0, column=0, sticky='nw')
        cat_title_label.grid(row=1, column=0, sticky='nw')
        self.cat_title_input.grid(row=1, column=1, columnspan=2, sticky='ne')
        edit_cat_button.grid(row=2, column=1, sticky='se')
        add_cat_button.grid(row=2, column=2, sticky='se')

    def setup_good_add_frame(self):
        add_good_label = tk.Label(self.good_form_frame, text='Вантаж')
        good_cat_label = tk.Label(self.good_form_frame, text='Категорія вантажу')
        good_title_label = tk.Label(self.good_form_frame, text='Назва')
        self.good_title_input = tk.Entry(self.good_form_frame)

        good_quantity_label = tk.Label(self.good_form_frame, text='Кількість')
        self.good_quantity_input = tk.Entry(self.good_form_frame)
        good_unit_label = tk.Label(self.good_form_frame, text='Одиниця виміру')
        self.good_unit_input = tk.Entry(self.good_form_frame)
        good_start_label = tk.Label(self.good_form_frame, text='Дата початку зберігання')
        self.good_start_input = tk.Entry(self.good_form_frame)
        good_term_label = tk.Label(self.good_form_frame, text='Термін, днів')
        self.good_term_input = tk.Entry(self.good_form_frame)
        good_end_label = tk.Label(self.good_form_frame, text='Дата кінця зберігання')
        self.good_end_input = tk.Entry(self.good_form_frame)
        edit_cat_button = tk.Button(self.good_form_frame, text='Оновити', command=self.edit_good)
        add_cat_button = tk.Button(self.good_form_frame, text='Створити', command=self.add_good)

        self.good_form_frame.grid_rowconfigure(0, weight=1)
        self.good_form_frame.grid_columnconfigure(0, weight=1)

        add_good_label.grid(row=0, column=0, sticky='nw')
        good_cat_label.grid(row=1, column=0, sticky='nw')
        good_title_label.grid(row=2, column=0, sticky='nw')
        self.good_title_input.grid(row=2, column=1, columnspan=2, sticky='ne')
        good_quantity_label.grid(row=3, column=0, sticky='nw')
        self.good_quantity_input.grid(row=3, column=1, columnspan=2, sticky='ne')
        good_unit_label.grid(row=4, column=0, sticky='nw')
        self.good_unit_input.grid(row=4, column=1, columnspan=2, sticky='ne')
        good_start_label.grid(row=5, column=0, sticky='nw')
        self.good_start_input.grid(row=5, column=1, columnspan=2, sticky='ne')
        good_term_label.grid(row=6, column=0, sticky='nw')
        self.good_term_input.grid(row=6, column=1, columnspan=2, sticky='ne')
        good_end_label.grid(row=7, column=0, sticky='nw')
        self.good_end_input.grid(row=7, column=1, columnspan=2, sticky='ne')
        edit_cat_button.grid(row=8, column=1, sticky='se')
        add_cat_button.grid(row=8, column=2, sticky='se')
    """
    HELPER FUNCTIONS
    """
    def create_treeview(self, root, dataCols):
        tree = ttk.Treeview(root, columns=dataCols, show='headings')
        ysb = ttk.Scrollbar(root, orient=tk.VERTICAL, command= tree.yview)
        xsb = ttk.Scrollbar(root, orient=tk.HORIZONTAL, command= tree.xview)
        tree['yscroll'] = ysb.set
        tree['xscroll'] = xsb.set

        tree.grid(row=1, column=0, columnspan=4, sticky=tk.NSEW)
        ysb.grid(row=1, column=4, sticky=tk.NS)
        xsb.grid(row=2, column=0, sticky=tk.EW)

        return tree

    def load_data(self, tree, dataCols, items):
        for c in dataCols:
            tree.heading(c, text=c.title())            

        for item in items: 
            tree.insert('', 'end', values=item)

    def refresh_categories(self):
        categories = CategoryService.list()
        self.show_categories_list(categories)
        self.show_categories_dropdown(categories)

    def show_categories_list(self, categories):
        self.catsTree = self.create_treeview(self.cat_list_frame, self.catCols)
        self.load_data(self.catsTree, self.catCols, categories)

    def show_categories_dropdown(self, categories):
        default_cat_name = categories[0].name if len(categories) else ""
        self.cat_name = default_cat_name
        self.good_cat.set(default_cat_name)
        if len(categories):
            self.good_cat_select = tk.OptionMenu(self.good_form_frame, self.good_cat, *list(map(lambda cat: cat.name, categories)), command=self.get_dropdown_cat_name)
        else:
            self.good_cat_select = tk.OptionMenu(self.good_form_frame, self.good_cat, [], command=self.get_dropdown_cat_name)    
        self.good_cat_select.grid(row=1, column=1, columnspan=2, sticky='ne')

    def refresh_goods(self):
        goods = GoodService.list(self.cat_id_show_goods)
        self.show_goods_list(goods)

    def show_goods_list(self, goods):
        self.goodsTree = self.create_treeview(self.good_list_frame, self.goodCols)
        self.load_data(self.goodsTree, self.goodCols, goods)

    def get_selected_category(self):
        currentCat = self.catsTree.focus()
        if not currentCat:
            return None
        catValues = self.catsTree.item(currentCat).get('values')
        return {'name':catValues[0], 'id':catValues[1]}

    def get_selected_category_id(self):
        selected_cat = self.get_selected_category()
        return selected_cat.get('id') if selected_cat else None

    def get_selected_category_name(self):
        selected_cat = self.get_selected_category()
        return selected_cat.get('name') if selected_cat else None

    def get_selected_good(self):
        currentGood = self.goodsTree.focus()
        if not currentGood:
            return None
        goodValues = self.goodsTree.item(currentGood).get('values')
        good_id = int(goodValues[5])
        return GoodService.get(good_id)
    
    def empty_good_form(self):
        self.good_id_edit = 0
        self.good_title_input.delete(0, 'end')
        self.good_quantity_input.delete(0, 'end')
        self.good_unit_input.delete(0, 'end')
        self.good_term_input.delete(0, 'end')
        self.good_start_input.delete(0, 'end')
        self.good_end_input.delete(0, 'end')

    def set_text(self, input, text):
        input.delete(0, tk.END)
        input.insert(0, text)

    """
    HANLDERS FOR CATEGORIES
    """
    def show_category_goods(self):
        cat_id = self.get_selected_category_id()
        if not cat_id:
            messagebox.showwarning("Вантажі категорії", "Оберіть категорію!")
            return
        self.cat_id_show_goods = cat_id 
        self.refresh_goods()

    def delete_category(self):
        cat_id = self.get_selected_category_id()
        if not cat_id:
            messagebox.showwarning("Видалення категорії", "Оберіть категорію!")
            return

        answer = messagebox.askquestion("Видалення категорії", "Видалити категорію?")
        if answer == "no":
            return

        try:
            CategoryService.delete(cat_id)
            self.refresh_categories()
            logging.info("Видалено категорію id={}".format(cat_id))
            messagebox.showinfo("Видалення категорії", "Категорію видалено")
        except Exception as ex:
            logging.error("Помилка видалення категорії: " + str(ex))
            messagebox.showerror("Видалення категорії", str(ex))

    def populate_category_form(self):
        cat_id = self.get_selected_category_id()
        if not cat_id:
            messagebox.showwarning("Редагування категорії", "Оберіть категорію!")
            return

        self.cat_id_edit = cat_id
        self.set_text(self.cat_title_input, self.get_selected_category_name())

    def edit_category(self):
        name = self.cat_title_input.get().strip().lower()
        id = self.cat_id_edit

        if not id:
            messagebox.showwarning("Редагування категорії", "Оберіть категорію!")
        elif not name:
            messagebox.showwarning("Редагування категорії", "Введіть назву!")
        elif CategoryService.find_except(name, id):
            messagebox.showwarning("Редагування категорії", "Така категорія вже є!")
        else:
            try:
                CategoryService.edit(id, name)
                self.cat_id_edit = 0
                self.cat_title_input.delete(0, 'end')
                self.refresh_categories()
                logging.info("Оновлено категорію: id={}, name={}".format(id, name))
                messagebox.showinfo("Редагування категорії", "Категорію оновлено")
            except Exception as ex:
                logging.error("Помилка оновлення категорії: " + str(ex))
                messagebox.showerror("Редагування категорії", str(ex))

    def add_category(self):
        name = self.cat_title_input.get().strip().lower()

        if not name:
            messagebox.showwarning("Нова категорія", "Введіть назву!")
        elif CategoryService.find(name):
            messagebox.showwarning("Нова категорія", "Така категорія вже є!")
        else:
            try:
                CategoryService.add(name)
                self.cat_title_input.delete(0, 'end')
                self.refresh_categories()
                logging.info("Створено категорію: name={}".format(name))
                messagebox.showinfo("Нова категорія", "Категорію створено")
            except Exception as ex:
                logging.error("Помилка створення категорії: " + str(ex))
                messagebox.showerror("Нова категорія", str(ex))

    """
    HANLDERS FOR GOODS
    """
    def get_dropdown_cat_name(self, selected_cat_name):
        self.cat_name = selected_cat_name

    def populate_good_form(self):
        good = self.get_selected_good()
        if not good:
            messagebox.showwarning("Редагування вантажу", "Оберіть вантаж!")
            return

        self.good_id_edit = good.id
        self.good_cat.set(good.category.name)
        self.cat_name = good.category.name

        self.set_text(self.good_title_input, good.name)
        self.set_text(self.good_quantity_input, good.quantity)
        self.set_text(self.good_unit_input, good.quantity_unit)
        self.set_text(self.good_term_input, good.term)
        self.set_text(self.good_start_input, good.show_start_date())
        self.set_text(self.good_end_input, good.show_end_date()) 

    def delete_good(self):
        good = self.get_selected_good()
        if not good:
            messagebox.showwarning("Видалення вантажу", "Оберіть вантаж!")
            return

        answer = messagebox.askquestion("Видалення вантажу", "Видалити вантаж?")
        if answer == "no":
            return

        try:
            GoodService.delete(good.id)
            self.refresh_goods()
            logging.info("Видалено вантаж: id={}".format(good.id))
            messagebox.showinfo("Видалення вантажу", "Вантаж видалено")
        except Exception as ex:
            logging.error("Помилка видалення вантажу: " + str(ex))
            messagebox.showerror("Видалення вантажу", str(ex))

    def edit_good(self):
        msgbox_title = "Редагування вантажу"
        success_msg = "Вантаж оновлено!"
        error_msg = "Помилка оновлення вантажу"

        good_id = self.good_id_edit
        if not good_id:
            messagebox.showwarning(msgbox_title, "Оберіть вантаж!")
            return

        cat_name = self.cat_name
        category = CategoryService.find(cat_name)
        if not category:
            messagebox.showwarning(msgbox_title, "Оберіть категорію!")
            return 

        name = self.good_title_input.get().strip().lower()
        if not name:
            messagebox.showwarning(msgbox_title, "Введіть назву!")
            return

        qty = 0
        try:
            qty = int(self.good_quantity_input.get().strip())
        except Exception as ex:
            messagebox.showwarning(msgbox_title, "Введіть кількість\n(ціле число)!")
            return

        qty_unit = self.good_unit_input.get().strip().lower()
        if not qty_unit:
            messagebox.showwarning(msgbox_title, "Введіть одиницю\nвимірюваня кількості!")
            return

        end_date = self.good_end_input.get().strip()

        try:
            datetime.strptime(end_date, '%Y-%m-%d')
            term = int(self.good_term_input.get().strip())
            if term < 1:
                messagebox.showwarning(msgbox_title, "Термін не може бути від'ємним")
                return
        except ValueError as ex:
            logging.error(ex)
            messagebox.showwarning(msgbox_title, "Введіть кінцеву дату або ціле число днів!\nЗразок: yyyy-mm-dd")
            return

        # term = 0
        # try:
        #     term = int(self.good_term_input.get().strip())
        #     if term < 1:
        #         term = None
        # except Exception as ex:
        #     logging.error(ex)
        #     term = None

        # if not term:
        #     messagebox.showwarning(msgbox_title, "Введіть ціле число днів")
        #     return

        try:
            GoodService.edit(good_id, category.id, name, qty, qty_unit, term, end_date)
            self.empty_good_form()
            if category.id == self.cat_id_show_goods:
                self.refresh_goods()
            logging.info("Оновлено вантаж: id={}, category_id={}, name={}, qty={}, qty_unit={}, term={}, end_date={}".format(
                            good_id, category.id, name, qty, qty_unit, term, end_date))
            messagebox.showinfo(msgbox_title, success_msg)
        except Exception as ex:
            logging.error(error_msg + ": " + str(ex))
            messagebox.showerror(msgbox_title, str(ex))  

    def add_good(self):
        msgbox_title = "Новий вантаж"
        success_msg = "Додано новий вантаж!"
        error_msg = "Помилка створення вантажу"

        cat_name = self.cat_name
        category = CategoryService.find(cat_name)
        if not category:
            messagebox.showwarning(msgbox_title, "Оберіть категорію!")
            return 

        name = self.good_title_input.get().strip().lower()
        if not name:
            messagebox.showwarning(msgbox_title, "Введіть назву!")
            return

        qty = 0
        try:
            qty = int(self.good_quantity_input.get().strip())
        except Exception as ex:
            messagebox.showwarning(msgbox_title, "Введіть кількість\n(ціле число)!")
            return

        qty_unit = self.good_unit_input.get().strip().lower()
        if not qty_unit:
            messagebox.showwarning(msgbox_title, "Введіть одиницю\nвимірюваня кількості!")
            return
        
        start_date = self.good_start_input.get().strip()
        if not self.date_pattern.match(start_date):
            messagebox.showwarning(msgbox_title, "Введіть дату початку!\nзразку: yyyy-mm-dd")
            return

        end_date = self.good_end_input.get().strip()
        if not self.date_pattern.match(end_date):
            end_date = None 

        term = 0
        try:
            term = int(self.good_term_input.get().strip())
            if term < 1:
                term = None
        except Exception as ex:
            logging.error(ex)
            term = None

        if not (end_date or term):
            messagebox.showwarning(msgbox_title, "Введіть кінцеву дату!\nзразку: yyyy-mm-dd\nабо ціле число днів")
            return

        try:
            GoodService.add(category.id, name, qty, qty_unit, start_date, term, end_date)
            self.empty_good_form()
            if category.id == self.cat_id_show_goods:
                self.refresh_goods()
            logging.info("Створено вантаж: category_id={}, name={}, qty={}, qty_unit={}, start_date={}, term={}, end_date={}".format(
                            category.id, name, qty, qty_unit, start_date, term, end_date))
            messagebox.showinfo(msgbox_title, success_msg)
        except Exception as ex:
            logging.error(error_msg + ": " + str(ex))
            messagebox.showerror(msgbox_title, str(ex)) 

    """
    HANLDERS FOR EXPORT
    """  
    def export_sqlite_postgres(self):
        logging.info("Експорт з SQLite до PostgreSQL")
        ExportService.export_sqlite_postgres()
    
    def export_postgres_mysql(self):
        logging.info("Експорт з PostgreSQL до MySQL")
        ExportService.export_postgres_mysql()

"""
MAIN
"""
def main():
    logging.basicConfig(level=logging.DEBUG)
    logging.info('Програма "{}" працює...'.format(View.title))

    root = tk.Tk()
    root.title(View.title)
    root.geometry('{}x{}'.format(1300, 600))
    gui = View(root)
    root.mainloop()
    mysql_db.close()


if __name__ == "__main__":
    main()
