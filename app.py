from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Person

# Create the engine
engine = create_engine('sqlite:///:memory:', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# Create All Tables
Person.metadata.create_all(engine)

# Create a new entry
person1 = Person(name="John")
person2 = Person(name="Steve")

# Add the new person instance using session
session.add(person1)
session.add(person2)
session.commit()

# Query the database and print it
results = session.query(Person).filter_by(name='John')
for result in results:
    print(result)

results = session.query(Person).all()
for result in results:
    print(result)
