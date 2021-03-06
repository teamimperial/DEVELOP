from setting.config import mysql
from flask import Blueprint, render_template, session, redirect
from users.get_company import GetCompany


class OneCourse:
    @classmethod
    def api_get_one_course(cls, id_course, id_company):
        connect = mysql.connect()
        cursor = connect.cursor()

        query = 'SELECT * FROM courses WHERE idCourse = %s AND idCompany = %s'
        param = (id_course, id_company)

        cursor.execute(query, param)

        result_course = cursor.fetchall()[0]

        query_company_name = 'SELECT CompanyName FROM company WHERE idCompany = %s'
        param_company_name = (id_company)
        cursor.execute(query_company_name, param_company_name)
        company = cursor.fetchone()[0]

        query_company_login = 'SELECT CompanyLogin FROM company WHERE idCompany = %s'
        param_company_login = (id_company)
        cursor.execute(query_company_login, param_company_login)
        login = cursor.fetchone()[0]

        course = {
            "id_course": id_course,
            "company_name": company,
            "course_name": result_course[2],
            "amount": result_course[3],
            "city": result_course[4],
            "country": result_course[5],
            "date_of_start": result_course[6],
            "date_of_end": result_course[7],
            "info": result_course[8],
            "status": result_course[9],
            "link": '/company/review/' + login
        }
        connect.commit()
        cursor.close()
        return course

    @classmethod
    def api_get_status_course(cls, id_course, id_company):
        connect = mysql.connect()
        cursor = connect.cursor()

        query = 'SELECT CoursesStatus FROM courses WHERE idCourse = %s AND idCompany = %s'
        param = (id_course, id_company)

        cursor.execute(query, param)

        status = cursor.fetchone()[0]

        connect.commit()
        cursor.close()

        return status

    @classmethod
    def get_review_about_course(cls, course_id):
        connect = mysql.connect()
        cursor = connect.cursor()

        query = 'SELECT students.StudentsName, students.StudentsLastName, coursereviews.review, coursereviews.time, coursereviews.id_course_reviews FROM students, coursereviews WHERE students.idStudents = coursereviews.idStudents AND coursereviews.idCourse = %s ORDER BY coursereviews.id_course_reviews DESC '
        param = (course_id)

        cursor.execute(query, param)

        result = cursor.fetchall()

        connect.commit()
        cursor.close()

        return result

    @classmethod
    def get_students_list_on_course(cls, course_id):
        connect = mysql.connect()
        cursor = connect.cursor()

        query = 'SELECT students.StudentsName, students.StudentsLastName, students.StudentsLogin FROM student_apply, students WHERE students.idStudents = student_apply.idStudents AND student_apply.idCourse = %s'
        param = (course_id)

        cursor.execute(query, param)

        result = cursor.fetchall()

        connect.commit()
        cursor.close()

        return result

    @classmethod
    def check_company_course(cls, id_company, id_course):
        connect = mysql.connect()
        cursor = connect.cursor()

        query = 'select exists(select * from courses where courses.idCompany=%s and courses.idCourse=%s)'
        param = (id_company, id_course)
        cursor.execute(query, param)

        result = cursor.fetchone()[0]

        connect.commit()
        cursor.close()

        return result


get_one_course = Blueprint('get_one_course', __name__)


@get_one_course.route('/course/!<id_course>/!<id_company>', methods=['GET'])
def api_get_one_course(id_course, id_company):
    if 'student' in session or 'company' in session:
        status = OneCourse.api_get_status_course(id_course, id_company)
        if 'student' in session and status == "Started" or status == "Not started" and 'company' not in session:
            global list_of_student
            course = OneCourse.api_get_one_course(id_course, id_company)
            students = OneCourse.get_students_list_on_course(id_course)
            photo = GetCompany.get_photo_company(id_company)
            if photo is None:
                photo = 'http://placehold.it/500x500'
            else:
                photo = photo
            list_of_student = []
            for student in students:
                student = {
                    'student_name': student[0],
                    'student_last_name': student[1],
                    'link': '/student/review/' + student[2]
                }
                list_of_student.append(student)
            return render_template('course-apply.html', course=course, list_of_student=list_of_student, photo=photo)

        if 'student' in session and status == "Finished":
            global comments
            course = OneCourse.api_get_one_course(id_course, id_company)
            reviews = OneCourse.get_review_about_course(id_course)
            photo = GetCompany.get_photo_company(id_company)
            if photo is None:
                photo = 'http://placehold.it/500x500'
            else:
                photo = photo
            comments = []
            for review in reviews:
                comment = {
                    'student_name': review[0],
                    'student_last_name': review[1],
                    'review': review[2],
                    'time': review[3],
                    'id_comment': review[4]
                }
                comments.append(comment)
            return render_template('course-reviews.html', course=course, course_id=id_course, comments=comments,
                                   photo = photo)

        if 'company' in session:
            login_company_in_session = session['company']
            id_company_in_session = GetCompany.get_company_id_from_db(login_company_in_session)
            if int(id_company) == int(id_company_in_session):
                if status == "Started" or status == "Not started":
                    course = OneCourse.api_get_one_course(id_course, id_company)
                    list_link = '/list_of_statement/' + id_course
                    students = OneCourse.get_students_list_on_course(id_course)
                    photo = GetCompany.get_photo_company(id_company)
                    if photo is None:
                        photo = 'http://placehold.it/500x500'
                    else:
                        photo = photo
                    list_of_student = []
                    for student in students:
                        student = {
                            'student_name': student[0],
                            'student_last_name': student[1],
                            'link': '/student/review/' + student[2]
                        }
                        list_of_student.append(student)
                    return render_template('course-company-list-of-student.html', course=course, list_link=list_link,
                                           list_of_student=list_of_student, photo=photo, id_course=id_course)
                if status == "Finished":
                    course = OneCourse.api_get_one_course(id_course, id_company)
                    reviews = OneCourse.get_review_about_course(id_course)
                    photo = GetCompany.get_photo_company(id_company)
                    if photo is None:
                        photo = 'http://placehold.it/500x500'
                    else:
                        photo = photo
                    comments = []
                    for review in reviews:
                        comment = {
                            'student_name': review[0],
                            'student_last_name': review[1],
                            'review': review[2],
                            'time': review[3],
                            'id_comment': review[4]
                        }
                        comments.append(comment)
                    students = OneCourse.get_students_list_on_course(id_course)
                    list_of_student = []
                    for student in students:
                        student = {
                            'student_name': student[0],
                            'student_last_name': student[1],
                            'link': '/student/review/' + student[2]
                        }
                        list_of_student.append(student)
                    return render_template('course-company-review-finished.html', course=course, comments=comments,
                                           list_of_student=list_of_student, photo=photo, id_course=id_course)

            if int(id_company) != int(id_company_in_session):
                if status == "Finished":
                    course = OneCourse.api_get_one_course(id_course, id_company)
                    reviews = OneCourse.get_review_about_course(id_course)
                    photo = GetCompany.get_photo_company(id_company)
                    if photo is None:
                        photo = 'http://placehold.it/500x500'
                    else:
                        photo = photo
                    comments = []
                    for review in reviews:
                        comment = {
                            'student_name': review[0],
                            'student_last_name': review[1],
                            'review': review[2],
                            'time': review[3]
                        }
                        comments.append(comment)
                    return render_template('course-company-review-finished-without-student.html',
                                           course=course, comments=comments, photo=photo)

                if status == "Started" or status == "Not started":
                    course = OneCourse.api_get_one_course(id_course, id_company)
                    students = OneCourse.get_students_list_on_course(id_course)
                    photo = GetCompany.get_photo_company(id_company)
                    if photo is None:
                        photo = 'http://placehold.it/500x500'
                    else:
                        photo = photo
                    list_of_student = []
                    for student in students:
                        student = {
                            'student_name': student[0],
                            'student_last_name': student[1]
                        }
                        list_of_student.append(student)
                    return render_template('course-company-review-student.html', course=course,
                                           list_of_student=list_of_student, photo=photo)
    else:
        return redirect('/'), 200
