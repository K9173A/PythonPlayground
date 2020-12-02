import os

from sqlalchemy import create_engine, orm, sql, text

from models import BaseModel, Person


DATABASE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.sqlite3')
if os.path.exists(DATABASE_PATH):
    os.remove(DATABASE_PATH)

engine = create_engine(f'sqlite:///{DATABASE_PATH}')
BaseModel.metadata.create_all(engine)
Session = orm.sessionmaker(bind=engine)

session = Session()

person = Person(first_name='Ivan', last_name='Ivanov', age=26)
session.add(person)
session.commit()

query = sql.select([Person]).where(Person.first_name == 'Ivan')

print(str(query))

connection = engine.connect()
results = connection.execute(query).fetchall()

for result in results:
    print(result)
