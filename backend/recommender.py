import numpy as np
import cPickle as pickle


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

    def fetch_data(self, mode='train'):
        N = self.total
        a = int(self.per_train * N)
        b = int((1 - self.per_train) * N)
        if mode == 'train':
            query = "select u, i, stars from review limit {}".format(a)
        elif mode == 'test':
            query = "select u, i, stars from review limit {0},{1}".format(a, b)

        self.sql.exe(query)
        while True:
            data = self.cursor.fetchmany(size=1)
            if data == []:
                break
            else:
                yield data

    def fetchTrain(self):
        return self.fetch_data(mode='train')

    def fetchTest(self):
        return self.fetch_data(mode='test')


class SVD(object):

    def __init__(self, n_factors=100, n_epochs=20, biased=True, lr_all=.005,
                 reg_all=.02, lr_bu=None, lr_bi=None, lr_pu=None, lr_qi=None,
                 reg_bu=None, reg_bi=None, reg_pu=None, reg_qi=None,
                 verbose=False):

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

    def train(self, data):
        self.data = data
        bu = np.zeros(data.n_users)
        bi = np.zeros(data.n_items)
        pu = np.zeros([data.n_users, self.n_factors]) + 0.1
        qi = np.zeros([data.n_items, self.n_factors]) + 0.1
        self.global_mean = data.global_mean

        for epoch in range(self.n_epochs):
            if self.verbose:
                print("Processing epoch {}".format(epoch))
            for u, i, r in data.fetchTrain():
                dot = np.dot(qi[i], pu[u])
                err = r - (self.global_mean + bu[u] + bi[i] + dot)

                bu[u] += self.lr_bu * (err - self.reg_bu * bu[u])
                bi[i] += self.lr_bi * (err - self.reg_bi * bi[i])

                pu[u] += self.lr_pu * (err * qi[i] - self.reg_pu * pu[u])
                qi[i] += self.lr_qi * (err * pu[u] - self.reg_qi * qi[i])

        self.bu, self.bi, self.pu, self.qi = bu, bi, pu, qi

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
