"""
Example for One to Many Relationship using SQLAlchemy
This example uses back_populates to access the relationship bi-directional

"""

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Employer(Base):
    __tablename__ = 'employer_table'

    id = Column(Integer, primary_key=True)
    employer_name = Column(String)
    employees = relationship("Employee", back_populates='employer')

    def __repr__(self):
        return f'Employer : {self.employer_name}'

class Employee(Base):
    __tablename__ = 'employee_table'

    id = Column(Integer, primary_key=True)
    employer_id = Column(Integer, ForeignKey('employer_table.id'))
    employer = relationship("Employer", back_populates='employees')
    employee_name = Column(String)

    def __repr__(self):
        return f'Employee : {self.employee_name}'

# Create the engine
engine = create_engine('sqlite:///:memory:', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# Create All Tables
Employer.metadata.create_all(engine)
Employee.metadata.create_all(engine)

# Add an employee and employer & add reference
employer1 = Employer(employer_name="ABC Corp")
employee1 = Employee(employee_name="John")
employer1.employees.append(employee1)
session.add(employer1)
session.add(employee1)
session.commit()

# Add a new employer
employer2 = Employer(employer_name="DEF Corp")
session.add(employer2)
session.commit()

# Add an employee to an existing employer
employer = session.query(Employer).filter(
           Employer.employer_name=='DEF Corp').first()
employee = Employee(employee_name="Steve")
employee.employer_id = employer.id
session.add(employee)
session.commit()

# With only relationship
print("Employees for employer1",employer1.employees)
print("Employees for employer2",employer2.employees)

# With backref & back_populates
print("Employer for employee1",employee1.employer)
print("Employer for employee2",employee.employer)
