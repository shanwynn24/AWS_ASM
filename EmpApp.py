from re import template
from sqlite3 import Cursor
from tkinter.tix import Form
from urllib import response
from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
import pyautogui
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
tableEmp = 'employee'
tableLeave = 'leave'
tablePRoll = 'payroll'
tablePFM = 'performance'

select_sql = "SELECT * FROM "

def opSQL(statement):
    cursor = db_conn.cursor()
    cursor.execute(select_sql + statement)
    db_conn.commit()
    return cursor.fetchall()
def calEmpId():
    cursor = db_conn.cursor()
    cursor.execute(select_sql + tableEmp)
    db_conn.commit()

    empDB = cursor.fetchall()
    emp_id = 0
    
    for x in empDB:
        emp_id = x[0]

    cursor.close()

    return emp_id + 1
def retrivedEmp(empId):

    dataExist = False
    cursor = db_conn.cursor()
    cursor.execute(select_sql + tableEmp)
    db_conn.commit()

    empDB = cursor.fetchall()

    for x in empDB:
        if str(x[0]) == empId:
            
            dataExist = True
            break

    cursor.close()
    return dataExist    
#def retrivedImg():
#    boto3.resource('s3').Bucket(custombucket).Object(custombucket+profilebucket)
#    file_stream = io.StringIO()
#    object.download_fileobj(file_stream)
#    return mpimg.imread(file_stream)


@app.route("/", methods=['GET', 'POST'])
@app.route("/index.html", methods=['GET', 'POST'])
def home():
    return render_template('index.html',open= opSQL(tableEmp))

@app.route("/leave.html", methods=['GET', 'POST'])
def leave():
    return render_template('leave.html')

@app.route("/payroll.html", methods=['GET', 'POST'])
def payroll():
    return render_template('payroll.html')

@app.route("/viewEmployee.html", methods=['GET', 'POST'])
def AddEmp():
    try:
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        position = request.form['position']
        location = request.form['location']
        emp_image_file = request.files['emp_image_file']

        insert_sql = """INSERT INTO employee (name,email,phone,position,location) 
                        VALUES (%s, %s, %s, %s, %s)"""
        cursor = db_conn.cursor()

        if emp_image_file.filename == "":
            return "Please select a file"

        try:

            cursor.execute(insert_sql, (name, email, phone, position, location))
            db_conn.commit()
            emp_name = "" + position
            # Uplaod image file in S3 #
            emp_image_file_name_in_s3 = "emp-id-" + str(calEmpId()) + "_image_file.jpg"
            s3 = boto3.resource('s3')

            try:
                print("Data inserted in MySQL RDS... uploading image to S3...")
                s3.Bucket(custombucket).put_object(Key=profilebucket + emp_image_file_name_in_s3, 
                                                   Body=emp_image_file)
                bucket_location = boto3.client('s3').get_bucket_location(
                                                     Bucket=custombucket)
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
        return render_template('success.html', name = emp_name)
    except:
        return render_template('viewEmployee.html', data = calEmpId(),open= opSQL(tableEmp))

@app.route("/editEmployee.html", methods=['GET', 'POST'])
def EditEmp():
    try:
        id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        position = request.form['position']
        location = request.form['location']
        emp_image_file = request.files['image']

        if retrivedEmp(id) == True:
            modifydata = """UPDATE employee SET name = %s, email = %s ,phone = %s, 
                            position = %s, location = %s WHERE emp_id = %s"""
            cursor = db_conn.cursor()

            if emp_image_file.filename == "":
                return "Please select a file"

            try:
                cursor.execute(modifydata, (name, email, phone, position, location, id))
                db_conn.commit()
                emp_name = "" + position
                # Uplaod image file in S3 #
                emp_image_file_name_in_s3 = "emp-id-" + str(id) + "_image_file.jpg"
                s3 = boto3.resource('s3')

                try:
                    try:
                        #che the S3 Bucket got file or not, If not execute this, 
                        # else direct finally
                        boto3.client('s3').get_object(Bucket=custombucket,
                                                      Key=profilebucket + emp_image_file_name_in_s3)
                        print("Exist Data Deleting...")
                        boto3.client('s3').delete_object(Bucket=custombucket,
                                                         Key=profilebucket + emp_image_file_name_in_s3)
                    except:
                        pass
                    finally:
                        print("Data inserted in MySQL RDS... updating image to S3...")
                        s3.Bucket(custombucket).put_object(Key=profilebucket + emp_image_file_name_in_s3, 
                                                           Body=emp_image_file)
                        bucket_location = boto3.client('s3').get_bucket_location(
                                                             Bucket=custombucket)
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

        else:
            pyautogui.alert("Employee ID didn't exist")
            return render_template('editEmployee.html')

        return render_template('success.html')

    except:
        return render_template("editEmployee.html")

@app.route("/profile.html", methods=['GET', 'POST'])
def profile():
    return render_template('profile.html')

@app.route("/performance.html", methods=['GET', 'POST'])
def editPerformance():
    try:
        name = request.form["name"]
        reviewDate = request.form['reviewDate']
        cSalary = request.form['cSalary']
        knowledge = request.form['knowledge-SkillSet']
        qow = request.form['qualityofWork']
        atd = request.form['attitude']

        insert_sql = """
                     INSERT INTO performance (emp_name,review_date,salary,knowledge,qow,attitude) 
                     VALUES (%s, %s, %s, %s, %s,%s)
                     """
        cursor = db_conn.cursor()

        cursor.execute(insert_sql, (name, reviewDate, cSalary, knowledge, qow,atd))
        db_conn.commit()

        cursor.close()
        print("all modification done...")
        return render_template('success.html', name = name)
    except:
        return render_template('/performance.html',open=opSQL(tablePFM))

@app.route("/delEmp", methods=['GET', 'POST'])
def delEMP():
    emp_id = request.form['delItem']
    
    delete_sql = "DELETE FROM " + tableEmp + " WHERE emp_id = " + emp_id

    cursor = db_conn.cursor()
    cursor.execute(delete_sql)
    db_conn.commit()

    cursor.close()
    print("Record have been delete")
    return render_template('success.html', name = "Delete " + emp_id)



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
