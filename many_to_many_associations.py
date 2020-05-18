"""
Example for Many to Many Relationship using SQLAlchemy using Associations
Associations allow to add extra fields

"""

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = 'student_table'

    id = Column(Integer, primary_key=True)
    student_name = Column(String)
    courses = relationship("Course", secondary="student_course_link")

    def __repr__(self):
        return f'Student : {self.student_name}'

class Course(Base):
    __tablename__ = 'course_table'

    id = Column(Integer, primary_key=True)
    course_name = Column(String)
    students = relationship(Student, secondary="student_course_link")

    def __repr__(self):
        return f'Course : {self.course_name}'

class StudentCourseLink(Base):
   __tablename__ = 'student_course_link'

   student_id = Column(Integer, ForeignKey('student_table.id'), primary_key=True)
   course_id = Column(Integer, ForeignKey('course_table.id'), primary_key=True)
   extra_data = Column(String(256))
   course = relationship(Course, backref="student_bref")
   student = relationship(Student, backref="course_bref")

# Create the engine
engine = create_engine('sqlite:///:memory:', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

# Create All Tables
Student.metadata.create_all(engine)
Course.metadata.create_all(engine)

student1 = Student(student_name="John")
course1 = Course(course_name="CS101")
student1_course1 = StudentCourseLink(student=student1, course=course1, extra_data='Full-Time-Student')

# Commit the changes
session.add(student1)
session.add(course1)
session.add(student1_course1)
session.commit()

# Query the database and print the records
q1 = session.query(StudentCourseLink).join(Student).filter(Student.student_name == 'John').one()
print(q1.student.student_name)

q2 = session.query(StudentCourseLink).filter(StudentCourseLink.extra_data == 'Full-Time-Student').one()
print(q2.student.student_name)

for x in session.query( Student, Course).filter(StudentCourseLink.student_id == Student.id,
   StudentCourseLink.course_id == Course.id).order_by(StudentCourseLink.student_id).all():
   print ("Student: {} Course: {}".format(x.Student.student_name, x.Course.course_name))
