from peewee import *

database = SqliteDatabase('/home/alex-krav/projects/warehouse/data/warehouse.db')

class BaseModel(Model):
    id = PrimaryKeyField()

    class Meta:
        database = database

class Category(BaseModel):
    name = CharField(unique=True)

    class Meta:
        table_name = 'categories'

class Good(BaseModel):
    category = ForeignKeyField(Category, backref='goods')
    name = CharField()
    quantity = IntegerField()
    quantity_unit = CharField()
    term = IntegerField()
    end_date = DateField()
    start_date = DateField()

    class Meta:
        table_name = 'goods'

def main():
    database.connect()

    for cat in Category.select().order_by(Category.name):
        print(cat.name)
        for good in cat.goods:
            print(" "*4, good.name)
    for good in Good.select():
        print(good.name, "-", good.category.name)

    print()
    query_cat = (Category.select(Category,Good).join(Good).order_by(Category.name,Good.name))
    for cat in query_cat:
        print(cat.name)
        for good in cat.goods:
            print(" "*4, good.name)

    query_good = Good.select().order_by(Good.name).prefetch(Category)
    for good in query_good:
            print(good.name, "-", good.category.name)

    database.close()

if __name__ == "__main__":
    main()