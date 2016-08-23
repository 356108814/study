# encoding: utf-8
"""

@author Yuriseus
@create 2016-8-18 22:52
"""

from multiprocessing import Pool

def f(x):
    print(x)
    return x*x

if __name__ == '__main__':
    with Pool(5) as p:
        p.map(f, [1, 2, 3])