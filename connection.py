import sys
import os
from recommender import easy_search
from database import Response
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from flaskext.mysql import MySQL
import ast

reload(sys)
sys.setdefaultencoding('utf-8')
application = Flask(__name__)
application.debug = True

# refers to application_top
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
APP_STATIC = os.path.join(APP_ROOT, 'static')

res = Response()


@application.route('/', methods=['GET', 'POST'])
def welcome():
    if request.method == "POST":
        messages = str(request.form['search'])
#        session['messages'] = messages
        return redirect(url_for('search_result', messages=messages))
    else:
        return render_template('welcome.htm')


@application.route('/searchresult', methods=['GET', 'POST'])
def search_result():
    #    string = request.form['request']
    #    string = request.form('search')
    string = request.args['messages']
    data = easy_search(string)

    show_result = []
    for element in data:
        temp_show = []
        temp_show.append(element['name'][0])
        temp_show.append(element['categories'][1])
        temp_show.append(element['stars'])
        temp_show.append(element['city'][0])
        temp_show.append(element['state'][0])

        show_result.append(temp_show)

    # return render_template('search_result.html', result=show_result)

    if request.method == "POST":
        messages = str(request.form['search'])
#        session['messages'] = messages

        return redirect(url_for('search_result', messages=messages))
    else:
        return render_template('search_result.html', result=show_result)


@application.route('/signup', methods=['GET', 'POST'])
def sign_up():
    error = "wrong"
    message = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['userpass']
        result = res.sign_up(email, password)

        if result == 1:
            return redirect(url_for('welcome', email=email))
        elif result == 0:
            return render_template('sign_up.html', error=error)

    else:
        return render_template('sign_up.html')


@application.route('/restaurantpage', methods=['GET', 'POST'])
def restaurant_page():
    restaurant = request.form['restaurant']
    return render_template('Restaurant_page.html', restaurant=restaurant)


@application.route('/signin', methods=['GET', 'POST'])
def sign_in():
    error = "wrong"
    message = None

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['userpass']

        try:
            #email = email
            result = res.sign_in(email, password)
            if result == 1:
                session["logged_in"] = True
                session["email"] = email

                return redirect(url_for('welcome'))

            elif result == 0:
                return render_template('sign_in.html', error=error)

        except Exception, e:
            error = e
            return render_template('sign_in.html', error=error)
    else:
        return render_template('sign_in.html')

if __name__ == '__main__':
    application.run()
