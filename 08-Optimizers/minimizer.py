import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.optimize as opt

def f(X):
    #given a scalar x, return a real number y
    Y = (X - 1.5)**2 + 0.5
    print("X = ", X, " Y = ", Y)
    return Y

def test_run():
    guess = 2.0
    minresult = opt.minimize(f, guess, method='SLSQP', options={'disp': True})
    print("Minima found at:")
    print("X = ", minresult.x, " Y = ", minresult.fun)

    #plot function values, mark minia
    xplot = np.linspace(0.5, 2.5, 21)
    yplot = f(xplot)
    plt.plot(xplot, yplot)
    plt.plot(minresult.x, minresult.fun, 'ro')
    plt.title("Minima of an objective function f(x) y = (x - 1.5) * 2 + 0.5")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()

if __name__ == "__main__":
    test_run()    