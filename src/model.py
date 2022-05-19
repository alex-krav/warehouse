from peewee import *
import logging

mysql_db = SqliteDatabase('C:\\Python staff\\django_zalik\\warehouse\\data\\warehouse.db')
pg_db = PostgresqlDatabase('warehouse', user='daryna', password='password',
                           host='localhost', port=5432)


class BaseModel(Model):
    id = PrimaryKeyField()

    class Meta:
        database = mysql_db


class Category(BaseModel):
    name = CharField()

    class Meta:
        constraints = [SQL('UNIQUE ("name" COLLATE NOCASE)')]
        table_name = 'categories'

    def to_string(self):
        return 'Category[id={}, name={}]'.format(self.id, self.name)

    def __str__(self):
        return '{} {}'.format(self.name.replace(' ', '\ '), self.id)


class Good(BaseModel):
    category = ForeignKeyField(Category, backref='goods', on_delete='CASCADE')
    name = CharField()
    quantity = IntegerField()
    quantity_unit = CharField()
    term = IntegerField()
    end_date = DateField(formats=['%Y-%m-%d'])
    start_date = DateField(formats=['%Y-%m-%d'])

    class Meta:
        table_name = 'goods'

    def show_start_date(self):
        return self.start_date

    def show_end_date(self):
        return self.end_date

    def show_quantity(self):
        return '{} {}'.format(self.quantity, self.quantity_unit)

    def to_string(self):
        return 'Good[id={}, cat_id={}, name={}, qty={}, start={}, term={}, date={}]'.format(
            self.id, self.category.id, self.name, self.show_quantity(), self.show_start_date(), self.term,
            self.show_end_date())

    def __str__(self):
        qty_str = '{}\ {}'.format(self.quantity, self.quantity_unit.replace(' ', '\ '))
        return '{} {} {} {} {} {}'.format(self.name.replace(' ', '\ '), qty_str, self.show_start_date(),
                                          self.show_end_date(), self.term, self.id)


def main():
    logging.basicConfig(level=logging.DEBUG)

    mysql_db.connect()

    for cat in Category.select().order_by(Category.name).prefetch(Good):
        print(cat.name)
        for good in cat.goods:
            print(" " * 4, good.name)
    print()

    for good in Good.select(Good, Category).join(Category, JOIN.INNER).order_by(Good.name):
        print(good.name, "-", good.category.name)
    print()

    print(str(Category[2]))
    print()
    print(str(Good.select(Good, Category).where(Good.id == 11).join(Category, JOIN.INNER).get()))

    good = Good[11]
    print(good)


if __name__ == "__main__":
    main()
