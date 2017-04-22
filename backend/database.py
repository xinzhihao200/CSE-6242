import numpy as np
from sql import (MysqlPython, business_dataDict, config)


class Response(object):

    def __init__(self, sql):
        self.sql = sql
        self.exe = self.sql.exe

    def sign_up(self, name, password):
        """
        return 1: success
        return 0: user name exists
        """
        if not self.is_user_exist(name):
            return 0

        query = "insert into alldata.user (name, password) values ('{}','{}')".format(name, password)
        self.exe(query)

    def sign_in(self, name, password):
        """
        return 0: user name does not exist or password incorrect
        return name: success
        """
        if not self.is_user_exist(name):
            return 0

        if not self.is_password_correct(name, password):
            return 0

        return name

    def is_password_correct(self, name, password):
        query = "select exists (select 1 from alldata.user where name='{}' and password='{}')".format(name, password)
        self.exe(query)
        for i in self.sql.cursor:
            pass
        if i[0] == 0:
            return False
        else:
            return True

    def is_user_exist(self, name):
        query = "select exists (select 1 from alldata.user where name='{}')".format(
            name)
        self.exe(query)
        for i in self.sql.cursor:
            pass
        if i[0] == 0:
            return False
        else:
            return True

    def search(self, string):
        keys = []
        for key in business_dataDict.iterkeys():
            keys.append(key)
        query = "select {} from business where match (name, categories, city) against ('{}' in natural language mode) limit 100".format(
            ','.join(keys), string)
        self.exe(query)
        datum = self.sql.cursor.fetchall()
        res = []
        for data in datum:
            newDict = {}
            for key, val in zip(keys, data):
                if key == 'attributes':
                    newDict['price'] = self._get_price(val)
                else:
                    newDict['price'] = None
                if isinstance(val, unicode):
                    newDict[key] = val.split('-=-')
                else:
                    newDict[key] = val
            res.append(newDict)

        return res

    def _get_price(self, val):
        if 'RestaurantsPriceRange2' not in val:
            return None
        else:
            val_list = val.split('-=-')
            for string in val_list:
                if 'RestaurantsPriceRange2' in string:
                    string = string.replace('RestaurantsPriceRange2:', '')
                    return int(string)


def easy_search(string):
    sql = MysqlPython(config, "alldata")
    res = Response(sql)
    return res.search(string)
