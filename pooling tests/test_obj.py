import time
from multiprocessing import Pool

def f(x):
    return x*x

class Test_obj:
    def __init__(self):
        self.pool = Pool()

    # this doesn't work in grid.py, no clue why it does here!
    # def f(self, x):
    #     return x*x

    def calc(self):
        t1 = time.time()
        self.pool.map(f, [1, 2, 3])
        t2 = time.time()
        print("total time: " + str(t2 - t1) + "s")
        # t3 = time.time()
        # print("calculated pools: " + str(round(t3 - t2, 2)) + "s")

        # p.close()
        # t4 = time.time()
        # print("closed pools: " + str(round(t4 - t3, 10)) + "s")
        # p.join()
        # t5 = time.time()
        # print("joined pools: " + str(round(t5 - t4, 2)) + "s")

        # print("total time: " + str(round(t3 - t1, 2)) + "s")
        print()