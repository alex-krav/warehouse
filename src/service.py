import logging
from datetime import datetime
from playhouse.shortcuts import model_to_dict
from model import pg_db, Category, Good, JOIN


class ConstraintException(Exception):
    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class CategoryService:
    def list() -> list(Category):
        query = Category.select().order_by(Category.name)
        return list(query)

    def find(name: str) -> Category:
        result = Category.select().where(Category.name == name.lower()).limit(1)
        return result.get() if len(result) > 0 else None

    def find_except(name: str, id: int) -> Category:
        result = Category.select().where(Category.id != id).where(
                    Category.name == name.lower()).limit(1)
        return result.get() if len(result) > 0 else None

    def add(name: str) -> Category:
        if not name.strip():
            raise ConstraintException("Ім'я не може бути пустим")
        return Category.create(name=name.strip().lower())

    def edit(id: int, name: str) -> bool:
        if not name.strip():
            raise ConstraintException("Ім'я не може бути пустим")
        category = Category[id]
        category.name = name.strip().lower()
        category.save()
        return True

    def delete(id: int) -> bool:
        category = Category[id]
        goods_qty = 0

        try:
            goods_qty = len(category.goods)
        except Exception as ex:
            logging.error(ex)

        if goods_qty:
            raise ConstraintException("В цій категорії є вантажі!")

        category.delete_instance()
        return True


class GoodService:
    def list(cat_id: int) -> list(Good):
        query = Good.select(Good, Category).join(Category, JOIN.INNER).where(
            Category.id == cat_id).order_by(Good.name)
        return list(query)

    def get(id: int) -> Good:
        return Good.select(Good, Category).where(Good.id == id).join(Category, 
            JOIN.INNER).get()

    def add(category_id: int, name: str, quantity: int, quantity_unit: str,
            start_date: str, term: int, end_date: str) -> Good:

        category = Category[category_id]

        if not name.strip():
            raise ConstraintException("Ім'я не може бути пустим")
        if int(quantity) < 1:
            raise ConstraintException('Кількість має бути цілим числом')
        if not quantity_unit.strip():
            raise ConstraintException('Одиниці виміру не можуть бути пустими')

        if not start_date.strip():
            raise ConstraintException('Початкова дата не може бути пустою')

        if not end_date.strip():
            raise ConstraintException('Кінцева не може бути пустою')

        start_date_obj = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()

        if start_date_obj >= end_date_obj:
            raise ConstraintException('Кінцева дата має бути більше за \
                початкову дату')

        return Good.create(category=category,
                           name=name.strip(), quantity=int(quantity), 
                           quantity_unit=quantity_unit.strip(),
                           start_date=start_date, end_date=end_date, 
                           term=int(term))

    def edit(id: int, category_id: int = None, name: str = None, quantity: int = None,
             quantity_unit: str = None, term: int = None, end_date: str = None) -> bool:

        good = Good[id]
        if category_id:
            category = Category[category_id]
            if category:
                good.category = category

        if name and name.strip():
            good.name = name.strip()
        if quantity and int(quantity) > 0:
            good.quantity = int(quantity)
        if quantity_unit and quantity_unit.strip():
            good.quantity_unit = quantity_unit.strip()
        if term and int(term) > 0:
            good.term = int(term)
        if end_date and end_date.strip():
            start_date_obj = good.start_date
            end_date_obj = datetime.strptime(end_date, '%Y-%m-%d').date()

            if start_date_obj >= end_date_obj:
                raise ConstraintException('Кінцева дата має бути більше за \
                    початкову дату')

            good.end_date = end_date

        good.save()
        return True

    def delete(id: int) -> bool:
        good = Good[id]
        good.delete_instance()
        return True


class ExportService:
    @staticmethod
    def export_sqlite_postgres():
        # get data from sqlite
        categories = []
        goods = []
        for category in Category.select():
            category_dict = model_to_dict(category)
            categories.append(category_dict)
            for good in category.goods.dicts():
                goods.append(good)

        # binding models to postgress db
        Category.bind(pg_db)
        Good.bind(pg_db)

        Category.delete().execute()
        Good.delete().execute()

        Category.insert_many(categories).execute()
        Good.insert_many(goods).execute()

    @staticmethod
    def export_postgres_mysql():
        # get data from postgres db
        Category.bind(pg_db)
        Good.bind(pg_db)

        categories = []
        goods = []
        for category in Category.select():
            category_dict = model_to_dict(category)
            categories.append(category_dict)
            for good in category.goods.dicts():
                goods.append(good)

        # binding models to mysql db
        Category.bind(mysql_db)
        Good.bind(mysql_db)

        Category.delete().execute()
        Good.delete().execute()

        Category.insert_many(categories).execute()
        Good.insert_many(goods).execute()



if __name__ == '__main__':
    logging.basicConfig(
        format='[%(asctime)s] ln:%(lineno)d %(levelname)s: %(message)s',
        datefmt='%I:%M:%s', level=logging.DEBUG)

    for cat in CategoryService.list():
        print(cat.id, cat.name)
    print()

    for good in GoodService.list(2):
        print(good.id, good.name, '-', good.category.id, good.category.name)
    print()

    print(str(GoodService.get(11)))
    print()

    cat = CategoryService.find_except('продукти харчування', 1)
    print(cat)

    print(len(CategoryService.list()))

    CategoryService.delete(1)
