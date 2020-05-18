"""
Example for Many to Many Relationship using SQLAlchemy

"""

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

association_table = Table('association', Base.metadata,
    Column('student_id', Integer, ForeignKey('student_table.id')),
    Column('course_id', Integer, ForeignKey('course_table.id'))
)

class Student(Base):
    __tablename__ = 'student_table'

    id = Column(Integer, primary_key=True)
    student_name = Column(String)
    courses = relationship("Course",
                          secondary=association_table,
                          backref="students")

    def __repr__(self):
        return f'Student : {self.student_name}'

class Course(Base):
    __tablename__ = 'course_table'

    id = Column(Integer, primary_key=True)
    course_name = Column(String)

    def __repr__(self):
        return f'Course : {self.course_name}'


# Create the engine
engine = create_engine('sqlite:///:memory:', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# Create All Tables
Student.metadata.create_all(engine)
Course.metadata.create_all(engine)

# Create new entries for Student and Course
student1 = Student(student_name="John")
student2 = Student(student_name="Steve")
course1 = Course(course_name="CS101")
course2 = Course(course_name="DS101")

# Associate Student and Course
student1.courses.append(course1)
student1.courses.append(course2)
student2.courses.append(course1)

# Commit the changes
session.add(student1)
session.add(student2)
session.add(course1)
session.add(course2)
session.commit()

# Query the database and print
print("Courses for student1",student1.courses)
print("Courses for student2",student2.courses)
print("Students enrolled for course1",course1.students)
print("Students enrolled for course2",course2.students)
