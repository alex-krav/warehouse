from model import * 
import logging
import time
from datetime import datetime, timezone

class ConstraintException(Exception):
    def __init__(self, message):
        self.message = message
    def __str__(self):
        return self.message

class CategoryService:
    def list() -> list(Category):
        query = Category.select().order_by(Category.name)
        return list(query)

    def add(name: str) -> Category:
        try:
            if not name.strip():
                raise ConstraintException("Name cannot be empty")
            return Category.create(name=name.strip().lower())
        except Exception as ex:
            logging.error("Could not add category: " + str(ex))  

    def edit(id: int, name: str) -> bool:
        try:
            if not name.strip():
                raise ConstraintException("Name cannot be empty")
            category = Category[id]
            category.name = name.strip().lower()
            category.save()
            return True
        except Exception as ex:
            logging.error("Could not update category: " + str(ex))
            return False

    def delete(id: int) -> bool:
        try:
            category = Category[id]
            if len(category.goods):
                raise ConstraintException("There are goods with this category")
            category.delete_instance()
            return True
        except Exception as ex:
            logging.error("Could not delete category: " + str(ex))
            return False

class GoodService:
    def list(cat_id: int) -> list(Good):
        query = Good.select(Good,Category).join(Category, JOIN.INNER).where(Category.id == cat_id).order_by(Good.name)
        return list(query)

    def get(id: int) -> Good:
        return Good.select(Good,Category).where(Good.id==id).join(Category, JOIN.INNER).get()

    def add(category_id: int, name: str, quantity: int, quantity_unit: str, 
            start_date: str, term: int, end_date: str) -> Good:
        try:
            category = Category[category_id]

            if not name.strip():
                raise ConstraintException("Name cannot be empty")
            if int(quantity) < 1:
                raise ConstraintException("Quantity should be positive integer")
            if not quantity_unit.strip():
                raise ConstraintException("Quantity unit cannot be empty")

            if not start_date.strip():
                raise ConstraintException("Start date cannot be empty")
            year,month,day = start_date.split('-')
            start_date_datetime = datetime(int(year), int(month), int(day), tzinfo=timezone.utc)
            start_date_timestamp = int(time.mktime(start_date_datetime.timetuple()))
            
            if end_date and end_date.strip():                
                year,month,day = end_date.split('-')
                end_date_datetime = datetime(int(year), int(month), int(day), tzinfo=timezone.utc)
                end_date_timestamp = int(time.mktime(end_date_datetime.timetuple()))
                
                if (start_date_timestamp >= end_date_timestamp):
                    raise ConstraintException("End date should be more than start date")
                term = int((end_date_timestamp - start_date_timestamp) / 86_400)
            elif term and int(term) > 0:
                end_date_timestamp = start_date_timestamp + int(term) * 86_400
            else:
                raise ConstraintException("You should provide either term or end date")

            return Good.create(category=category, 
                               name=name.strip(), quantity=int(quantity), quantity_unit=quantity_unit.strip(),
                               start_date=start_date_timestamp, end_date=end_date_timestamp, term=int(term))
        except Exception as ex:
            logging.error("Could not add category: " + str(ex))  

    def edit(id: int, category_id: int=None, name: str=None, quantity: int=None, 
             quantity_unit: str=None, term: int=None, end_date: str=None) -> bool:
        try:
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
            
            if end_date and end_date.strip():
                year,month,day = end_date.split('-')
                end_date_datetime = datetime(int(year), int(month), int(day), tzinfo=timezone.utc)
                end_date_timestamp = int(time.mktime(end_date_datetime.timetuple()))

                if (good.start_date >= end_date_timestamp):
                    raise ConstraintException("End date should be more than start date")
                term = int((end_date_timestamp - good.start_date) / 86_400)

                good.end_date = end_date_timestamp
                good.term = term
            elif term and int(term) > 0:
                end_date_timestamp = good.start_date + int(term) * 86_400
                good.end_date = end_date_timestamp
                good.term = int(term)
            
            good.save()
            return True
        except Exception as ex:
            logging.error("Could not update good: " + str(ex))
            return False

    def delete(id: int) -> bool:
        try:
            good = Good[id]
            good.delete_instance()
            return True
        except Exception as ex:
            logging.error("Could not delete good: " + str(ex))
            return False 

class ExportService:
    def export_sqlite_postgres():
        pass

    def export_postgres_mysql():
        pass

if __name__ == "__main__":
    logging.basicConfig(format='[%(asctime)s] ln:%(lineno)d %(levelname)s: %(message)s', datefmt='%I:%M:%s', level=logging.DEBUG)

    for cat in CategoryService.list():
        print(cat.id, cat.name)
    print()

    for good in GoodService.list(2):
        print(good.id, good.name, '-', good.category.id, good.category.name)
    print()

    print(str(GoodService.get(11)))
