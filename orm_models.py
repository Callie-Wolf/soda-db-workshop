# orm_models.py
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class Student(Base):
    __tablename__ = "Students"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    major = Column(String(100))
    gpa = Column(Float)

class DB:
    def __init__(self, db_url="sqlite:///students.db"):
        # check_same_thread False allows Flask dev server threads to use the same DB
        self.engine = create_engine(db_url, connect_args={"check_same_thread": False})
        self.SessionLocal = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

    def add_students(self, students_list):
        """
        students_list: list of dicts with keys: name, major, gpa
        """
        session = self.SessionLocal()
        try:
            for s in students_list:
                stu = Student(name=s["name"], major=s.get("major"), gpa=s.get("gpa"))
                session.add(stu)
            session.commit()
        finally:
            session.close()

    def get_students_with_min_gpa(self, gpa_min=0.0):
        session = self.SessionLocal()
        try:
            return session.query(Student).filter(Student.gpa >= gpa_min).order_by(Student.gpa.desc()).all()
        finally:
            session.close()

if __name__ == "__main__":
    demo_db = DB()
    demo_db.add_students([
        {"name": "Demo One", "major": "Demo", "gpa": 3.2}
    ])
    rows = demo_db.get_students_with_min_gpa(3.0)
    for r in rows:
        print(r.id, r.name, r.major, r.gpa)
    
class Course(Base):
   __tablename__ = "Courses"
   id = Column(Integer, primary_key=True)
   title = Column(String(100))

   def list_courses(self):
       session = self.SessionLocal()
       try:
           return session.query(Course).order_by(Course.title).all()
       finally:
           session.close()
