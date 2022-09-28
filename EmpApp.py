from flask import Flask, render_template, request
from pymysql import connections
import os
import boto3
<<<<<<< Updated upstream
=======
from tkinter import * 
from tkinter import messagebox
>>>>>>> Stashed changes
from config import *

app = Flask(__name__,template_folder='aws_asm')

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


@app.route("/", methods=['GET', 'POST'])
def home():
    return render_template('viewEmployee.html')


@app.route("/about", methods=['POST'])
def about():
    return render_template('www.intellipaat.com')

<<<<<<< Updated upstream
=======
            try:
                # Uplaod image file in S3 #
                emp_image_file_name_in_s3 = "emp-id-" + \
                    str(id) + "_leave_document.pdf"
                s3 = boto3.resource('s3')

                try:
                    try:
                        # che the S3 Bucket got file or not, If not execute this,
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

                        object_url = "https://{0}.s3.amazonaws.com/{1}{2}".format(
                            custombucket,
                            profilebucket,
                            emp_image_file_name_in_s3)
                        cursor.execute(
                            modifydata, (name, email, phone, position, location, id, object_url))
                        db_conn.commit()

                except Exception as e:
                    return str(e)

            finally:
                cursor.close()

        else:
            messagebox.showwarning('Warning',"Employee ID didn't exist")
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

        cursor.execute(insert_sql, (name, reviewDate,
                       cSalary, knowledge, qow, atd))
        db_conn.commit()

        cursor.close()
        print("all modification done...")
        return render_template('success.html', name=name)
    except:
        return render_template('/performance.html', open=opSQL(tablePFM))


@app.route("/delEmp", methods=['GET', 'POST'])
def delEMP():
    emp_id = request.form['delItem']

    delete_sql = "DELETE FROM " + tableEmp + " WHERE emp_id = " + emp_id
>>>>>>> Stashed changes

@app.route("/addemp", methods=['POST'])
def AddEmp():
    emp_id = request.form['emp_id']
    name = request.form['name']
    email = request.form['email']
    phone = request.form['phone']
    position = request.form['position']
    location = request.form['location']
    emp_image_file = request.files['emp_image_file']

    insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s,%s)"
    cursor = db_conn.cursor()

    if emp_image_file.filename == "":
        return "Please select a file"

    try:

        cursor.execute(insert_sql, (emp_id, name, email, phone, position, location))
        db_conn.commit()
        emp_name = "" + position
        # Uplaod image file in S3 #
        emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
        s3 = boto3.resource('s3')

        try:
<<<<<<< Updated upstream
            print("Data inserted in MySQL RDS... uploading image to S3...")
            s3.Bucket(custombucket).put_object(Key=emp_image_file_name_in_s3, Body=emp_image_file)
            bucket_location = boto3.client('s3').get_bucket_location(Bucket=custombucket)
            s3_location = (bucket_location['LocationConstraint'])
=======
            # Uplaod image file in S3 #
            emp_image_file_name_in_s3 = "leave_" + id + leaveStart + ".jpg"
            s3 = boto3.resource('s3')

            try:
                print("Data inserted in MySQL RDS... uploading image to S3...")
                s3.Bucket(custombucket).put_object(Key=leavebucket + emp_image_file_name_in_s3,
                                                   Body=empLeave_image_file)

                object_url = "https://{0}.s3.amazonaws.com/{1}{2}".format(
                    custombucket,
                    profilebucket,
                    emp_image_file_name_in_s3)
                cursor.execute(
                    insert_sql, (id, name, leaveStart, leaveEnd, object_url))
                db_conn.commit()

            except Exception as e:
                return str(e)

        except:
            messagebox.showwarning('Warning',"Employee ID didn't exist")
            return render_template('index.html', open=opSQL(tableEmp))
>>>>>>> Stashed changes

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
    return render_template('viewEmployee.html', name=emp_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
