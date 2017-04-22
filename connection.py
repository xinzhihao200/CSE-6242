import sys, os
import recommender.py
from flask import Flask, request, session
from flaskext.mysql import MySQL
import ast

reload(sys)
sys.setdefaultencoding('utf-8')
application = Flask(__name__)
application.debug = True






@application.route('/welcome',method = ["GET","POST"])
    if request.method == "POST":
        string = request.form('search')
        data = easy_search(string)
        temp_show = {'name': 'none', 'city': 'none', 'stars': 0.0, 'address': 'none', 'categories': 'none'}
        show_result = []
        for element in data:
            temp_show['name'] = element['name']
            temp_show['categoires'] = element['categories']
            temp_show['city'] = element['city']
            temp_show['stars'] = element['stars']
            temp_show['address'] = element['address']

            show_result.append(temp_show)
