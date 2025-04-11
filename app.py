from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Configure MySQL connection
db_config = {
    'host': 'suranardsdemo.cdtqd6jgia7i.ap-south-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'test1234',
    'database': 'mysqldemo'
}


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/students')
def view_students():
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM students")
            students = cursor.fetchall()
    finally:
        connection.close()
    return render_template('view_students.html', students=students)


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        Email = request.form['Email']
        contact_number = request.form['contact_number']
        section = request.form['section']
        collage = request.form['collage']

        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO students (name, Email, contact_number, section, collage) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(sql, (name, Email, contact_number, section, collage))
            connection.commit()
        finally:
            connection.close()

        return redirect(url_for('view_students'))
    return render_template('add_student.html')


@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    connection = pymysql.connect(**db_config)

    if request.method == 'GET':
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
            student = cursor.fetchone()
        return render_template('edit_student.html', student=student)

    try:
        with connection.cursor() as cursor:
            if request.method == 'POST':
                name = request.form['name']
                Email = request.form['Email']
                contact_number = request.form['contact_number']
                section = request.form['section']
                collage = request.form['collage']
                sql = "UPDATE students SET name=%s, Email=%s, contact_number=%s, section=%s, collage=%s WHERE id=%s"
                cursor.execute(sql, (name, Email, contact_number, section, collage, id))
                connection.commit()
                return redirect(url_for('view_students'))
    finally:
        connection.close()
    return render_template('edit_student.html', student=student)


@app.route('/delete_student/<int:id>', methods=['GET', 'POST'])
def delete_student(id):
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM students WHERE id=%s", (id,))
            connection.commit()
    finally:
        connection.close()
    return redirect(url_for('add_student'))


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')

