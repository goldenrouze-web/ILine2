from sqlalchemy import Column, Integer, String, Date, Numeric, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()


class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    position = Column(String(50), nullable=False)
    hire_date = Column(Date, nullable=False)
    salary = Column(Numeric(10, 2), nullable=False)
    manager_id = Column(Integer, ForeignKey("employees.id"), nullable=True)

    manager = relationship(
        "Employee",
        remote_side=[id],
        backref="subordinates"
    )

    def __repr__(self):
        return f"<Employee {self.full_name}>"
