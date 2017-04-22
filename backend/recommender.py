import numpy as np
import cPickle as pickle
from sql import (MysqlPython, business_dataDict, config)


class Data(object):

    def __init__(self, sql, per_train=0.7):
        with open('profile', 'rb') as f:
            profile = pickle.load(f)

        self.n_users = profile['n_users']
        self.n_items = profile['n_items']
        self.global_mean = profile['global_mean']
        self.total = profile['total']
        self.sql = sql
        self.per_train = per_train

    def fetch_data(self, mode='train', batch_size=5000):
        N = self.total
        a = int(self.per_train * N)
        b = int((1 - self.per_train) * N)
        if mode == 'train':
            query = "select u, i, stars from review limit {}".format(a)
        elif mode == 'test':
            query = "select u, i, stars from review limit {0},{1}".format(a, b)

        self.sql.exe(query)
        while True:
            data = self.sql.cursor.fetchmany(size=batch_size)
            if data == []:
                break
            else:
                idx = np.random.permutation(len(data))
                data = np.array(data)[idx]
                yield data

    def fetchTrain(self):
        return self.fetch_data(mode='train')

    def fetchTest(self):
        return self.fetch_data(mode='test')


class SVD(object):

    def __init__(self, n_factors=100, n_epochs=20, biased=True, lr_all=.005,
                 reg_all=.02, lr_bu=None, lr_bi=None, lr_pu=None, lr_qi=None,
                 reg_bu=None, reg_bi=None, reg_pu=None, reg_qi=None,
                 verbose=True):

        self.n_factors = n_factors
        self.n_epochs = n_epochs
        self.biased = biased
        self.lr_bu = lr_bu if lr_bu is not None else lr_all
        self.lr_bi = lr_bi if lr_bi is not None else lr_all
        self.lr_pu = lr_pu if lr_pu is not None else lr_all
        self.lr_qi = lr_qi if lr_qi is not None else lr_all
        self.reg_bu = reg_bu if reg_bu is not None else reg_all
        self.reg_bi = reg_bi if reg_bi is not None else reg_all
        self.reg_pu = reg_pu if reg_pu is not None else reg_all
        self.reg_qi = reg_qi if reg_qi is not None else reg_all
        self.verbose = verbose

    def load(self):
        with open('profile', 'rb') as f:
            profile = pickle.load(f)
        try:
            self.bu = profile['bu']
            self.bi = profile['bi']
            self.pu = profile['pu']
            self.qi = profile['qi']
        except:
            self.bu = np.zeros(profile['n_users'])
            self.bi = np.zeros(profile['n_items'])
            self.pu = np.zeros([profile['n_users'], self.n_factors]) + 0.1
            self.qi = np.zeros([profile['n_items'], self.n_factors]) + 0.1
        self.profile = profile

    def save(self):
        self.profile['bu'] = self.bu
        self.profile['bi'] = self.bi
        self.profile['pu'] = self.pu
        self.profile['qi'] = self.qi
        with open('profile', 'wb') as f:
            pickle.dump(self.profile, f)

    def train(self, data):
        self.load()
        self.data = data
        self.global_mean = data.global_mean

        batch_step = 0
        for epoch in range(self.n_epochs):
            for batch in data.fetchTrain():
                if self.verbose:
                    print(
                        "Processing epoch {}, batch {}".format(epoch, batch_step))
                batch_step += 1
                for u, i, r in batch:
                    dot = np.dot(self.qi[i], self.pu[u])
                    err = r - \
                        (self.global_mean + self.bu[u] + self.bi[i] + dot)

                    self.bu[u] += self.lr_bu * (err - self.reg_bu * self.bu[u])
                    self.bi[i] += self.lr_bi * (err - self.reg_bi * self.bi[i])

                    self.pu[u] += self.lr_pu * \
                        (err * self.qi[i] - self.reg_pu * self.pu[u])
                    self.qi[i] += self.lr_qi * \
                        (err * self.pu[u] - self.reg_qi * self.qi[i])

        self.save()

    def predict(self, testset=None):
        if testset is None:
            testset = self.data.fetchTest()

        res = []
        for u, i in testset:
            est = self.global_mean
            if u < self.bu.size and i < self.bi.size:
                est += self.bu[u] + self.bi[i]
                est += np.dot(self.qi[i], self.pu[u])
            else:
                raise Exception("Prediction Error!")
            res.append(est)

        return res
