import math
import numpy as np
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt

class Hurst(object):

    def __init__(self, data_list):
        self.data_list = data_list 
        self.n_list = []
        self.rs_list = []
        self.__prepare_data()

    def exponent(self):
        log_rs = np.log(self.rs_list)
        log_n = np.log(self.n_list)
        hurst = np.polyfit(log_n,log_rs,1)
        print("The Hurst Exponent is: ")
        print(hurst[0])
        return hurst[0]

    def circle(self):
        plt.plot(np.log(self.n_list), np.log(self.rs_list))
        Vn = np.divide(self.rs_list, np.sqrt(self.n_list))
        plt.plot(np.log(self.n_list), np.log(self.rs_list))
#        plt.ylabel("ln(R/S)")
#        plt.show()
        plt.plot(np.log(self.n_list), Vn)
#        plt.ylabel("Vn")
        plt.show()

    def expected_hurst(self):
        e_list = []
        n_list = self.n_list
        for n in self.n_list:
            lst = []
            for r in range(1,n):
                lst.append(np.sqrt((n-r)/float(r)))
            result = np.sum(lst)
            e_rs = ((n-0.5)/n)*np.power((n*(np.pi/2)), -0.5)*result
            e_list.append(e_rs)
        log_n = np.log(n_list)
        log_e = np.log(e_list)
        return np.polyfit(log_n, log_e, 1)[0]

    def local_hurst(self):
        pass
        
    def __prepare_data(self):
        subtracted = self.__get_subtracted()
        length = len(subtracted)

        #rg = range(4, math.floor(len(subtracted)/4)+1)
        rg = range(8, math.floor(len(subtracted)/2)+1)

        index = []
        
        # independent variable
        i_var = [] 
        # dependent variable
        d_var = []
        for i in rg:
            reshaped = self.__reshape_list(subtracted, i)

            lst_r_per_s = []
            for item in reshaped:
                if len(item) == i:
                    r_per_s = self.__calulate_rs(item)
                    lst_r_per_s.append(r_per_s)
            
            i_var.append(i)
            d_var.append(np.mean(lst_r_per_s))

        self.n_list = i_var
        self.rs_list = d_var

    def __calulate_rs(self, sublist):
        e = np.mean(sublist)
        d = [x-e for x in sublist]
        x = np.cumsum(d) 
        R = np.max(x) - np.min(x)
        S = np.std(sublist)

        return R/S

    def __get_subtracted(self):
        return np.subtract(np.log(self.data_list[1:]), np.log(self.data_list[:-1]))

    def __reshape_list(self, values, n):
        return [values[i:i+n] for i in range(0, len(values), n)]
        
