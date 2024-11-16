from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your_secret_key"


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/nhansu1'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Employee(db.Model):
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    department = db.Column(db.String(100), nullable=True)
    hire_date = db.Column(db.DateTime, default=datetime.utcnow)
    salary = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f'<Employee {self.name}, Position: {self.position}>'


with app.app_context():
    db.create_all()


@app.route("/")
def index():
    employees = Employee.query.all()
    return render_template("index.html", employees=employees)


@app.route('/employee/<int:employee_id>')
def employee_details(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    return render_template('employee_details.html', employee=employee)

@app.route("/add", methods=["GET", "POST"])
def add_employee():
    if request.method == "POST":
        name = request.form.get("name")
        position = request.form.get("position")
        department = request.form.get("department")
        salary = request.form.get("salary")
        
        if name and position:
            new_employee = Employee(
                name=name,
                position=position,
                department=department,
                salary=float(salary) if salary else None
            )
            db.session.add(new_employee)
            db.session.commit()
            flash("Đã thêm nhân viên thành công!", "success")
        else:
            flash("Tên và chức vụ không được để trống!", "error")
        return redirect(url_for("index"))
    return render_template("add.html")


@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_employee(id):
    employee = Employee.query.get_or_404(id)
    if request.method == "POST":
        employee.name = request.form.get("name")
        employee.position = request.form.get("position")
        employee.department = request.form.get("department")
        employee.salary = float(request.form.get("salary")) if request.form.get("salary") else None
        db.session.commit()
        flash("Cập nhật thông tin nhân viên thành công!", "success")
        return redirect(url_for("index"))
    return render_template("edit.html", employee=employee)

@app.route("/delete/<int:id>")
def delete_employee(id):
    employee = Employee.query.get_or_404(id)
    db.session.delete(employee)
    db.session.commit()
    flash("Đã xóa nhân viên thành công!", "success")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
