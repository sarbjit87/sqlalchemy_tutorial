"""
Example for One to One Relationship using SQLAlchemy
This example uses backref to access the relationship bi-directional

"""

from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, sessionmaker

Base = declarative_base()

class Person(Base):
    __tablename__ = 'person_table'

    id = Column(Integer, primary_key=True)
    person_name = Column(String)
    passport = relationship("Passport", uselist=False, backref='person')

    def __repr__(self):
        return f'Person : {self.person_name}'

class Passport(Base):
    __tablename__ = 'passport_table'

    id = Column(Integer, primary_key=True)
    passport_id = Column(Integer, ForeignKey('person_table.id'), unique=True)
    passport_number = Column(String)

    def __repr__(self):
        return f'Passport : {self.passport_number}'


# Create the engine
engine = create_engine('sqlite:///:memory:', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# Create All Tables
Person.metadata.create_all(engine)
Passport.metadata.create_all(engine)

# Add an employee and employer & add reference
person1 = Person(person_name="John Doe")
passport1 = Passport(passport_number="ABC123456")
person1.passport = passport1

passport2 = Passport(passport_number="DEF123456")
person2 = Person(person_name="Steve", passport=passport2)

session.add_all([person1, passport1, passport2, person2])
session.commit()


print("Passport id for person1",person1.passport)
print("Passport id for person2",person2.passport)
