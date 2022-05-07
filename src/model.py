from peewee import *
from datetime import datetime
import logging

database = SqliteDatabase('/home/alex-krav/projects/warehouse/data/warehouse.db')

class BaseModel(Model):
    id = PrimaryKeyField()

    class Meta:
        database = database

class Category(BaseModel):
    name = CharField()

    class Meta:
        constraints = [SQL('UNIQUE ("name" COLLATE NOCASE)')]
        table_name = 'categories'

    def __str__(self):
        return 'Category[id={}, name={}]'.format(self.id, self.name)

class Good(BaseModel):
    category = ForeignKeyField(Category, backref='goods')
    name = CharField()
    quantity = IntegerField()
    quantity_unit = CharField()
    term = IntegerField()
    end_date = IntegerField()
    start_date = IntegerField()

    class Meta:
        table_name = 'goods'

    def show_start_date(self):
        return datetime.fromtimestamp(self.start_date).strftime('%Y-%m-%d')

    def show_end_date(self):
        return datetime.fromtimestamp(self.end_date).strftime('%Y-%m-%d')
        
    def show_quantity(self):
        return '{} {}'.format(self.quantity, self.quantity_unit) 

    def __str__(self):
        return 'Good[id={}, cat_id={}, name={}, qty={}, start={}, term={}, date={}]'.format(
            self.id, self.category.id, self.name, self.show_quantity(), self.show_start_date(), self.term, self.show_end_date())

def main():
    logging.basicConfig(format='[%(asctime)s] ln:%(lineno)d %(levelname)s: %(message)s', datefmt='%I:%M:%s', level=logging.DEBUG)

    database.connect()

    for cat in Category.select().order_by(Category.name).prefetch(Good):
        print(cat.name)
        for good in cat.goods:
            print(" "*4, good.name)
    print()
        
    for good in Good.select(Good,Category).join(Category, JOIN.INNER).order_by(Good.name):
        print(good.name, "-", good.category.name)
    print()

    print(str(Category[2]))
    print()
    print(str(Good.select(Good,Category).where(Good.id==11).join(Category, JOIN.INNER).get()))

    database.close()

if __name__ == "__main__":
    main()