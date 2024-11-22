from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

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

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


with app.app_context():
    existing_user = User.query.filter_by(username="admin").first()
    if not existing_user:
        admin_user = User(username="admin", password=generate_password_hash("123456"))
        db.session.add(admin_user)
        db.session.commit()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash("Vui lòng đăng nhập để truy cập!", "error")
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
@login_required
def index():
    employees = Employee.query.all()
    return render_template("index.html", employees=employees)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        action = request.form.get('action')  
        
        username = request.form.get('username')
        password = request.form.get('password')
        
        
        if action == 'login':
            user = User.query.filter_by(username=username).first()
            if user and check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['username'] = user.username
                flash("Đăng nhập thành công!", "success")
                return redirect(url_for('index'))
            else:
                flash("Tên đăng nhập hoặc mật khẩu không đúng!", "error")
        
        elif action == 'register':
            confirm_password = request.form.get('confirm_password')
            if password != confirm_password:
                flash("Mật khẩu không khớp!", "error")
            else:
                existing_user = User.query.filter_by(username=username).first()
                if existing_user:
                    flash("Tài khoản đã tồn tại!", "error")
                else:
                    hashed_password = generate_password_hash(password)
                    new_user = User(username=username, password=hashed_password)
                    db.session.add(new_user)
                    db.session.commit()
                    flash("Đăng ký thành công! Bạn có thể đăng nhập ngay.", "success")
                    return redirect(url_for('login'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("Bạn đã đăng xuất.", "success")
    return redirect(url_for('login'))


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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        


        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Tên tài khoản đã tồn tại. Vui lòng chọn tên khác.", "danger")
            return redirect(url_for('register'))
        
        
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Đăng ký thành công! Bạn có thể đăng nhập ngay.", "success")
        return redirect(url_for('login'))
    
    return render_template('register.html')



if __name__ == "__main__":
    app.run(debug=True, port=5000)
