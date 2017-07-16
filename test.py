import numpy as np
from pandas import Series 
from hurst import Hurst

def main():
    series = Series(np.random.randn(5), index=['a', 'b', 'c', 'd', 'e'])
    hurst = Hurst(series)
    print(hurst.exponent())

if __name__ == '__main__':
    main()
