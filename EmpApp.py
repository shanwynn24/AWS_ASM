from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__,template_folder="aws_asm",static_folder="static")

bucket = custombucket
region = customregion

db_conn = connections.Connection(
    host=customhost,
    port=3306,
    user=customuser,
    password=custompass,
    db=customdb

)
output = {}
table = 'employee'

def employee():
    select_sql = "SELECT * FROM employee"
    cursor = db_conn.cursor()
    cursor.execute(select_sql)
    db_conn.commit()

    empDB = cursor.fetchall()
    emp_id = 0
    
    for x in empDB:
        emp_id = x[0]

    return emp_id + 1


@app.route("/", methods=['GET', 'POST'])
@app.route("/index.html", methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route("/profile.html", methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')

@app.route("/viewEmployee.html", methods=['GET', 'POST'])
def viewEmployee():
    return render_template('viewEmployee.html', data = employee())
    
@app.route("/editEmployee.html", methods=['GET', 'POST'])
def editEmployee():
    return render_template('editEmployee.html')

@app.route("/leave.html", methods=['GET', 'POST'])
def leave():
    return render_template('leave.html')

@app.route("/payroll.html", methods=['GET', 'POST'])
def payroll():
    return render_template('payroll.html')

@app.route("/performance.html", methods=['GET', 'POST'])
def performance():
    return render_template('performance.html')

@app.route("/success.html", methods=['GET', 'POST'])
def success():
    return render_template('success.html')

@app.route("/addemp", methods=['GET', 'POST'])
def AddEmp():
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    position = request.form['position']
    location = request.form['location']
    emp_image_file = request.files['emp_image_file']

    insert_sql = "INSERT INTO employee (name,email,phone,position,location) VALUES (%s, %s, %s, %s, %s)"
    cursor = db_conn.cursor()

    if emp_image_file.filename == "":
        return "Please select a file"

    try:

        cursor.execute(insert_sql, (name, email, phone, position, location))
        db_conn.commit()
        emp_name = "" + position
        # Uplaod image file in S3 #
        emp_image_file_name_in_s3 = "emp-id-" + str(employee()) + "_image_file"
        s3 = boto3.resource('s3')

        try:
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])

            if s3_location is None:
                s3_location = ''
            else:
                s3_location = '-' + s3_location

            object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                s3_location,
                custombucket,
                emp_image_file_name_in_s3)

        except Exception as e:
            return str(e)

    finally:
        cursor.close()

    print("all modification done...")
    return render_template('viewEmployee.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
