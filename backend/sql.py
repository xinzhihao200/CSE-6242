import mysql
from mysql.connector import errorcode
import json
import pandas as pd
from sqlalchemy import create_engine
from itertools import islice
import sys
import cPickle as pickle
import numpy as np

DB_NAME = "alldata"

config = {
    'user': 'root',
    'password': ' ',
    'host': '127.0.0.1',
    'raise_on_warnings': True,
}
FILEPATH = "/home/zhangzimou/Downloads/ChromeDownload/cse6242_data/"
business_dataDict = {
    'address': None,
    'attributes': None,
    'business_id': None,
    'categories': None,
    'city': None,
    'hours': None,
    'is_open': None,
    'latitude': None,
    'longitude': None,
    'name': None,
    'neighborhood': None,
    'postal_code': None,
    'review_count': None,
    'stars': None,
    'state': None,
}


class MysqlPython(object):

    def __init__(self, config, db_name, mode='simple'):
        self.cnx = mysql.connector.connect(**config)
        self.cursor = self.cnx.cursor()
        try:
            self.cnx.database = db_name
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database(db_name)

        self.db_name = db_name
        self.exe("use {}".format(db_name))

        if mode != 'simple':
            try:
                with open('profile', 'rb') as f:
                    self.profile = pickle.load(f)
            except:
                self.profile = {}

    def exe(self, query):
        self.cursor.execute(query)

    def create_database(self, db_name):
        try:
            self.cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))

    def create_table(self, tb_name, dataType):
        query = "create table {}(".format(tb_name)
        var = []
        for key, val in dataType.iteritems():
            if key != 'primary_key' and key != 'foreign_key':
                var.append("{0} {1}".format(key, val))

        if 'primary_key' in dataType:
            var.append("primary key ({})".format(dataType['primary_key']))

        query += ','.join(var) + ');'
        # print query
        self.exe(query)

    def drop_table(self, tb_name):
        query = "drop table {};".format(tb_name)
        self.exe(query)

    def insert_table(self, tb_name, df):
        query = "insert into {}".format(tb_name)
        cols = list(df.columns)
        query += "(" + ",".join(cols) + ") values"

        def to_str(x):
            if isinstance(x, str) or isinstance(x, unicode):
                if x == "":
                    return 'NULL'
                x = x.replace('\"', '\'').replace('\\', '')
                return unicode(u'\"{}\"'.format(x))
            elif str(x.__class__) == "<class 'pandas.tslib.Timestamp'>":
                x = str(x)
                return unicode(u'\"{}\"'.format(x))
            else:
                return unicode(x)

        data = df.applymap(to_str)
        data = data.apply(lambda x: ','.join(x), axis=1)
        query += "(" + "),(".join(data) + ");"
        try:
            self.exe(query)
        except:
            print query
            sys.exit()

    def _create_insert(self, tb_name, filepath, dataType):
        for i, df in enumerate(self.process_json(filepath, N=50)):
            if i == 0:
                self.create_table(tb_name, dataType)

            self.insert_table(tb_name, df)
        self.cnx.commit()

    def create_review(self):
        filepath = FILEPATH + "yelp_academic_dataset_review.json"
        tb_name = 'review'
        dataType = {
            'business_id': 'varchar(100)',
            'cool': 'int',
            'date': 'varchar(100)',
            'funny': 'int',
            'review_id': 'varchar(100)',
            'stars': 'int',
            'text': 'text',
            'type': 'varchar(10)',
            'useful': 'int',
            'user_id': 'varchar(100)',
        }
        self._create_insert(tb_name, filepath, dataType)

    def create_business(self):
        filepath = FILEPATH + "yelp_academic_dataset_business.json"
        tb_name = 'business'
        dataType = {
            'address': 'varchar(100)',
            'attributes': 'text',
            'business_id': 'varchar(100)',
            'categories': 'varchar(500)',
            'city': 'varchar(50)',
            'hours': 'text',
            'is_open': 'int',
            'latitude': 'float',
            'longitude': 'float',
            'name': 'varchar(100)',
            'neighborhood': 'varchar(100)',
            'postal_code': 'varchar(40)',
            'review_count': 'int',
            'stars': 'float',
            'state': 'varchar(30)',
            'type': 'varchar(10)',
            'primary_key': 'business_id'
        }
        self._create_insert(tb_name, filepath, dataType)

    def get_business_info(self, business_id):
        dataDict = business_dataDict
        keys = []
        for key in dataDict.iterkeys():
            keys.append(key)
        query = "select {0} from business where business_id=\"{1}\"".format(",".join(keys), business_id)
        self.exe(query)
        for data in self.cursor:
            for key, val in zip(dataDict.iterkeys(), data):
                if isinstance(val, str) or isinstance(val, unicode):
                    dataDict[key] = val.split('-=-')
                else:
                    dataDict[key] = val
        try:
            return dataDict
        except NameError:
            return None
        else:
            raise Exception("error!")

    def process_json(self, filepath, N=1000):
        with open(filepath, 'r') as f:
            while True:
                next_n_lines = list(islice(f, N))
                if not next_n_lines:
                    break
                else:
                    df = "[" + ','.join(next_n_lines) + "]"
                    df = pd.read_json(df)
                    df = df.applymap(self.process_df)
                    df.fillna('NULL', inplace=True)
                    yield df

    def process_df(self, x, sep='-=-'):
        if isinstance(x, list):
            return sep.join(x)
        else:
            return x

    def json2csv(self, filepath, target_name, N=1000):
        df = pd.DataFrame()
        with open(filepath, 'r') as f:
            while True:
                next_n_lines = list(islice(f, N))
                if not next_n_lines:
                    break
                else:
                    data = "[" + ','.join(next_n_lines) + "]"
                    data = pd.read_json(data)
                    data = data.applymap(self.process_df)
                    df = df.append(data, ignore_index=True)

        df.to_csv(target_name + '.csv', encoding='utf-8', index=False)

    def process_review_data(self, N=3000):
        def a():
            query = ("create table business_hash("
                     "business_id varchar(100),"
                     "num int auto_increment unique,"
                     "primary key (business_id));")
            try:
                self.drop_table("business_hash")
            except:
                pass
            self.exe(query)

        def b():
            query = ("create table user_hash("
                     "user_id varchar(100),"
                     "num int auto_increment unique,"
                     "primary key (user_id));")
            try:
                self.drop_table("user_table")
            except:
                pass
            self.exe(query)

        def c():
            query = "alter table review add idx int auto_increment primary key"
            self.exe(query)
            query = "alter table review add (u int, i int)"
            self.exe(query)

        # a()
        # b()
        global_mean = 0
        step, i_max, u_max = 0, 0, 0
        readTimes = 0
        while True:
            query = "select business_id, user_id, stars, idx, u from review limit {},{}".format(readTimes*N, N)
            self.exe(query)
            readTimes += 1
            print readTimes
            data = self.cursor.fetchall()
            if data == []:
                break
            else:
                for b_id, u_id, r, idx, u_ in data:
                    if u_ is None:
                        i = self.id2num('business_hash', b_id)
                        u = self.id2num('user_hash', u_id)
                        i_max = max(i, i_max)
                        u_max = max(u, u_max)
                        query = "update review set i={0}, u={1} where idx={2}".format(
                            i, u, idx)
                        self.exe(query)

                    global_mean = step / \
                        (step + 1.0) * global_mean + 1.0 / (step + 1) * r
                    step += 1

        self.profile['global_mean'] = global_mean
        self.profile['n_users'] = u_max
        self.profile['n_items'] = i_max
        self.profile['total'] = idx
        with open('profile', 'wb') as f:
            pickle.dump(self.profile, f)

        self.cnx.commit()

    def id2num(self, tb_name, item):
        if tb_name == 'business_hash':
            col = 'business_id'
        elif tb_name == 'user_hash':
            col = 'user_id'
        query = "select * from {0} where {1}=\"{2}\"".format(tb_name, col, item)
        self.exe(query)
        num, id = None, None
        for id, num in self.cursor:
            pass
        if num is None:
            query = "insert into {0}({1}) values (\"{2}\")".format(
                tb_name, col, item)
            self.exe(query)
            return self.id2num(tb_name, item)
        else:
            return num

    def business_categories(self):
        query = "select categories from business where categories like '%restaurant%'"
        self.exe(query)
        cats = []
        for item in self.cursor:
            cat = item[0].split('-=-')
            cats.extend(cat)

        cat, count = np.unique(cats, return_counts=True)
        return cat[np.argsort(count)[::-1]]

    def setup_database(self):
        self.create_business()
        self.create_review()
        self.process_review_data()

    def reset(self):
        self.exe("drop table business_hash")
        self.exe("drop table user_hash")
        self.exe("alter table review drop idx")
        self.exe("alter table review drop u, drop i")


if __name__ == '__main__':
    a = MysqlPython(config, DB_NAME)
    # a.create_business()
    # a.create_review()
    # a.create_test()
    # data = a.fetch_review_data(N=2)
    # a.process_review_data()
