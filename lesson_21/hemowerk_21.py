from sqlalchemy import create_engine, Column, Integer, String, Table, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
import random

Base = declarative_base()

student_course = Table(
    'student_course', Base.metadata,
    Column('student_id', Integer, ForeignKey('students.id')),
    Column('course_id', Integer, ForeignKey('courses.id'))
)


class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    courses = relationship("Course", secondary=student_course, back_populates="students")

    def __repr__(self):
        return f"Student(id={self.id}, name='{self.name}')"


class Course(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    students = relationship("Student", secondary=student_course, back_populates="courses")

    def __repr__(self):
        return f"Course(id={self.id}, name='{self.name}')"


engine = create_engine('sqlite:///students.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

course_names = ["Math", "Physics", "Chemistry", "History", "Biology"]
courses = [Course(name=name) for name in course_names]
session.add_all(courses)
session.commit()

for i in range(1, 21):
    student = Student(name=f"Student {i}")
    student.courses = random.sample(courses, k=random.randint(1, 3))
    session.add(student)
session.commit()


def add_student_to_course(student_name, course_name):
    course = session.query(Course).filter_by(name=course_name).first()
    if course:
        student = Student(name=student_name)
        student.courses.append(course)
        session.add(student)
        session.commit()
        print(f"Added {student} to {course}")
    else:
        print("Course not found")


def get_students_in_course(course_name):
    course = session.query(Course).filter_by(name=course_name).first()
    if course:
        return course.students
    return []


def get_courses_for_student(student_name):
    student = session.query(Student).filter_by(name=student_name).first()
    if student:
        return student.courses
    return []


def update_student_name(old_name, new_name):
    student = session.query(Student).filter_by(name=old_name).first()
    if student:
        student.name = new_name
        session.commit()
        print(f"Updated student name from {old_name} to {new_name}")


def delete_student(name):
    student = session.query(Student).filter_by(name=name).first()
    if student:
        session.delete(student)
        session.commit()
        print(f"Deleted student {name}")


if __name__ == "__main__":
    add_student_to_course("New Student", "Math")
    print(get_students_in_course("Math"))
    print(get_courses_for_student("Student 1"))
    update_student_name("Student 1", "Renamed Student 1")
    delete_student("Renamed Student 1")
