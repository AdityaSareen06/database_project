from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:Aditsar06@localhost/school_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define database models based on your schema
class Student(db.Model):
    __tablename__ = 'Student'
    student_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    dob = db.Column(db.Date)
    email = db.Column(db.String(100))
    phone = db.Column(db.String(15))

class Teacher(db.Model):
    __tablename__ = 'Teacher'
    teacher_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    email = db.Column(db.String(100))
    phone = db.Column(db.String(15))

class Course(db.Model):
    __tablename__ = 'Course'
    course_id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100))
    teacher_id = db.Column(db.Integer, db.ForeignKey('Teacher.teacher_id'))
    credits = db.Column(db.Integer)
    teacher = db.relationship('Teacher', backref='courses')

class Enrollment(db.Model):
    __tablename__ = 'Enrollment'
    enrollment_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('Student.student_id'))
    course_id = db.Column(db.Integer, db.ForeignKey('Course.course_id'))
    enrollment_date = db.Column(db.Date, default=datetime.utcnow)
    student = db.relationship('Student', backref='enrollments')
    course = db.relationship('Course', backref='enrollments')

# Route to display homepage
@app.route('/')
def index():
    return render_template('index.html')

# Route to show all students
@app.route('/students')
def students():
    students = Student.query.all()
    return render_template('students.html', students=students)

# Route to add a new student
@app.route('/students/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        dob = request.form['dob']
        email = request.form['email']
        phone = request.form['phone']
        
        new_student = Student(first_name=first_name, last_name=last_name, dob=datetime.strptime(dob, '%Y-%m-%d'), email=email, phone=phone)
        db.session.add(new_student)
        db.session.commit()
        return redirect(url_for('students'))
    
    return render_template('add_student.html')

# Route to show all teachers
@app.route('/teachers')
def teachers():
    teachers = Teacher.query.all()
    return render_template('teachers.html', teachers=teachers)

# Route to add a new teacher
@app.route('/teachers/add', methods=['GET', 'POST'])
def add_teacher():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        
        new_teacher = Teacher(first_name=first_name, last_name=last_name, email=email, phone=phone)
        db.session.add(new_teacher)
        db.session.commit()
        return redirect(url_for('teachers'))
    
    return render_template('add_teacher.html')

# Route to show all courses
@app.route('/courses')
def courses():
    courses = Course.query.all()
    return render_template('courses.html', courses=courses)

# Route to add a new course
@app.route('/courses/add', methods=['GET', 'POST'])
def add_course():
    teachers = Teacher.query.all()  # Get all teachers to associate with the course
    if request.method == 'POST':
        course_name = request.form['course_name']
        teacher_id = request.form['teacher_id']
        credits = request.form['credits']
        
        new_course = Course(course_name=course_name, teacher_id=teacher_id, credits=credits)
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for('courses'))
    
    return render_template('add_course.html', teachers=teachers)

# Route to show all enrollments
@app.route('/enrollments')
def enrollments():
    enrollments = Enrollment.query.all()
    return render_template('enrollments.html', enrollments=enrollments)

# Route to add a new enrollment
@app.route('/enrollments/add', methods=['GET', 'POST'])
def add_enrollment():
    students = Student.query.all()  # Get all students to associate with the enrollment
    courses = Course.query.all()    # Get all courses to associate with the enrollment
    if request.method == 'POST':
        student_id = request.form['student_id']
        course_id = request.form['course_id']
        
        new_enrollment = Enrollment(student_id=student_id, course_id=course_id)
        db.session.add(new_enrollment)
        db.session.commit()
        return redirect(url_for('enrollments'))
    
    return render_template('add_enrollment.html', students=students, courses=courses)

@app.route('/students/edit/<int:student_id>', methods=['GET', 'POST'])
def edit_student(student_id):
    student = Student.query.get_or_404(student_id)
    if request.method == 'POST':
        student.first_name = request.form['first_name']
        student.last_name = request.form['last_name']
        student.dob = datetime.strptime(request.form['dob'], '%Y-%m-%d')
        student.email = request.form['email']
        student.phone = request.form['phone']
        
        db.session.commit()
        return redirect(url_for('students'))
    
    return render_template('edit_student.html', student=student)
# Edit Teacher Route
@app.route('/teachers/edit/<int:teacher_id>', methods=['GET', 'POST'])
def edit_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    if request.method == 'POST':
        teacher.first_name = request.form['first_name']
        teacher.last_name = request.form['last_name']
        teacher.email = request.form['email']
        teacher.phone = request.form['phone']
        
        db.session.commit()
        return redirect(url_for('teachers'))
    
    return render_template('edit_teacher.html', teacher=teacher)

# Edit Course Route
@app.route('/courses/edit/<int:course_id>', methods=['GET', 'POST'])
def edit_course(course_id):
    course = Course.query.get_or_404(course_id)
    teachers = Teacher.query.all()
    if request.method == 'POST':
        course.course_name = request.form['course_name']
        course.teacher_id = request.form['teacher_id']
        course.credits = request.form['credits']
        
        db.session.commit()
        return redirect(url_for('courses'))
    
    return render_template('edit_course.html', course=course, teachers=teachers)

# Edit Enrollment Route
@app.route('/enrollments/edit/<int:enrollment_id>', methods=['GET', 'POST'])
def edit_enrollment(enrollment_id):
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    students = Student.query.all()
    courses = Course.query.all()
    if request.method == 'POST':
        enrollment.student_id = request.form['student_id']
        enrollment.course_id = request.form['course_id']
        
        db.session.commit()
        return redirect(url_for('enrollments'))
    
    return render_template('edit_enrollment.html', enrollment=enrollment, students=students, courses=courses)

@app.route('/students/delete/<int:student_id>', methods=['GET'])
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('students'))

@app.route('/teachers/delete/<int:teacher_id>', methods=['GET'])
def delete_teacher(teacher_id):
    teacher = Teacher.query.get_or_404(teacher_id)
    db.session.delete(teacher)
    db.session.commit()
    return redirect(url_for('teachers'))
@app.route('/courses/delete/<int:course_id>', methods=['GET'])
def delete_course(course_id):
    course = Course.query.get_or_404(course_id)
    db.session.delete(course)
    db.session.commit()
    return redirect(url_for('courses'))
@app.route('/enrollments/delete/<int:enrollment_id>', methods=['GET'])
def delete_enrollment(enrollment_id):
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    db.session.delete(enrollment)
    db.session.commit()
    return redirect(url_for('enrollments'))

# Run the Flask app
if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
