from setting.config import mysql
from flask import Blueprint, render_template, session
from users.get_company import GetCompany


class OneCourse:
    @classmethod
    def api_get_one_course(cls, id_course, id_company):
        connect = mysql.connect()
        cursor = connect.cursor()

        query = 'select * from courses where idCourse = %s and idCompany = %s'
        param = (id_course, id_company)

        cursor.execute(query, param)

        result_course = cursor.fetchall()[0]

        query_company_name = 'select CompanyName from company where idCompany = %s'
        param_company_name = (id_company)
        cursor.execute(query_company_name,param_company_name)
        company = cursor.fetchone()[0]

        query_company_login = 'select CompanyLogin from company where idCompany = %s'
        param_company_login = (id_company)
        cursor.execute(query_company_login, param_company_login)
        login = cursor.fetchone()[0]

        course = {
            "company_name": company,
            "course_name": result_course[2],
            "amount": result_course[3],
            "city": result_course[4],
            "country": result_course[5],
            "date_of_start": result_course[6],
            "date_of_end": result_course[7],
            "info": result_course[8],
            "link": '/company/review/' + login
        }
        connect.commit()
        cursor.close()

        return course


get_one_course = Blueprint('get_one_course', __name__)


@get_one_course.route('/course/<id_course>/<id_company>', methods=['GET'])
def api_get_one_course(id_course, id_company):
    if 'student' in session or 'company' in session:
        course = OneCourse.api_get_one_course(id_course, id_company)
        return render_template('course-reviews.html', course=course)
    else:
        return 'Please login'