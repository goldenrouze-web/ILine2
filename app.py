import os
from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import date, datetime
from models import Base, Employee

DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    "mysql+pymysql://crmuser:crm123@localhost:3306/employees_db"
)

app = Flask(__name__, template_folder="templates")
app.secret_key = os.environ.get("SECRET_KEY", "secret_key_for_flask_flash")

engine = create_engine(DATABASE_URL, echo=False)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

positions = ["CEO", "Manager", "Team Lead", "Senior Developer", "Developer"]


@app.route("/employees")
def employees():
    sort_field = request.args.get("sort", "id")
    search_query = request.args.get("q", "")

    try:
        query = session.query(Employee)
        if search_query:
            query = query.filter(Employee.full_name.ilike(f"%{search_query}%"))

        if sort_field in [
            "id", "full_name", "position", "hire_date", "salary"
        ]:
            query = query.order_by(getattr(Employee, sort_field))
        else:
            query = query.order_by(Employee.id)

        employees_list = query.all()
    except Exception as e:
        flash(f"Ошибка получения сотрудников: {e}", "error")
        employees_list = []

    return render_template(
        "employees.html",
        employees=employees_list,
        search_query=search_query,
        sort_field=sort_field
    )


@app.route("/add_employee", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        try:
            name = request.form.get("full_name")
            position = request.form.get("position")
            salary = float(request.form.get("salary"))
            hire_date_str = (
                request.form.get("hire_date") or date.today().isoformat()
            )
            hire_date = datetime.fromisoformat(hire_date_str).date()
            manager_id = request.form.get("manager_id")
            manager_id = int(manager_id) if manager_id else None

            emp = Employee(
                full_name=name,
                position=position,
                salary=salary,
                hire_date=hire_date,
                manager_id=manager_id
            )
            session.add(emp)
            session.commit()
            flash("Сотрудник добавлен", "success")
            return redirect(url_for("employees"))
        except Exception as e:
            session.rollback()
            flash(f"Ошибка добавления: {e}", "error")

    all_employees = session.query(Employee).all()
    return render_template(
        "add_employee.html",
        positions=positions,
        employees=all_employees
    )


@app.route("/employee/<int:employee_id>/update_manager", methods=["POST"])
def update_manager(employee_id):
    new_manager_id = request.form.get("manager_id", type=int)
    emp = session.query(Employee).get(employee_id)

    if not emp:
        flash("Сотрудник не найден", "error")
        return redirect(url_for("employees"))

    if new_manager_id == emp.id:
        flash(
            "Сотрудник не может быть своим начальником", "error"
        )
        return redirect(url_for("employees"))

    if new_manager_id:
        new_manager = session.query(Employee).get(new_manager_id)
        if not new_manager:
            flash("Указанный начальник не существует", "error")
            return redirect(url_for("employees"))

        temp = new_manager
        while temp:
            if temp.id == emp.id:
                flash(
                    "Нельзя назначить подчиненного начальником (цикл)", "error"
                )
                return redirect(url_for("employees"))
            temp = temp.manager

    try:
        emp.manager_id = new_manager_id
        session.commit()
        flash("Начальник обновлен", "success")
    except Exception as e:
        session.rollback()
        flash(f"Ошибка обновления: {e}", "error")

    return redirect(url_for("employees"))


if __name__ == "__main__":
    app.run(debug=True)
