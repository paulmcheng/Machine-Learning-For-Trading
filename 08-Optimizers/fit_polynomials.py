import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as spo

def error_poly(c, data):
    """ 
    compute error between given polynomial and observed data 
    C: numpy.poly1d object representing polyomial coefficients
    data: 2d array where each row is a point (x, y)

    Returns error as a single real value

    """

    #Metric: Sum of squared y-axis differences
    err = np.sum((data[:,1] - np.polyval(c, data[:, 0])) ** 2)
    return err

def fit_poly(data, error_func, degree=4):
     """
     Fit a polynomial to given data, using supplied error function. 

     data: 2D array where each point is a point (x, y)
     error_func: function that computes the error between a polynomial and observed data 

    Returns polynomial that minimizes the error function. 

     """   

     # generate initial guss for polynomial model (all coeffs = 1)
     guess = np.poly1d(np.ones(degree + 1, dtype=np.float32))

     # plot intial guess
     x = np.linspace(-5, 5, 21)
     plt.plot(x, np.polyval(guess, x), 'm--', linewidth=2.0, label="Initial guess")

     # call optimizer to minimize error function
     result = spo.minimize(error_poly, guess, args=(data,), method='SLSQP', options={'disp':True})
     
     # convert optimal result into a poly1d object
     return np.poly1d(result.x)

def test_run():
    # define orginal polynomial curve 
    corig = np.poly1d([1.5, -10, -5, 60, 50])
    print("Orginal polynomial: {}*x^4 + {}*x^3 + {}*x^2 + {}*x + {}".format(corig[4], corig[3], corig[2], corig[1], corig[0]))
    xorig = np.linspace(-5, 5, 21)
    yorig = np.polyval(corig, xorig)
    plt.plot(xorig, yorig, 'b--', linewidth=2.0, label="Orginal polynomial")

    # generate noisy data points
    noise_sigma = 30.0
    noise = np.random.normal(0, noise_sigma, yorig.shape)
    # convert input into an array, then transpose 
    data = np.asarray([xorig, yorig + noise]).T
    plt.plot(data[:, 0], data[:,1], 'go', label='Data points')

    #try to fit a polynominal to this data
    cfit = fit_poly(data, error_poly)

    print("Orginal polynomial: {}*x^4 + {}*x^3 + {}*x^2 + {}*x + {}".format(cfit[4], cfit[3], cfit[2], cfit[1], cfit[0]))
    plt.plot(data[:, 0], np.polyval(cfit, data[:,0]), 'r--', linewidth=2.0,label="Fitted polynomial")
    
    # add a legend and show plot
    plt.title("Polynomial curve fitting optimization")
    plt.legend()
    plt.show()

if __name__ == "__main__":
     test_run()   