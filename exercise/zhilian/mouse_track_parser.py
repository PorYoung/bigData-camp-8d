import pylab
import numpy as np
from scipy.optimize import curve_fit


class mouseTrackParser:
    time = []
    track = []

    def __init__(self, time, track):
        self.time = time
        self.track = track

    def myPolyfit(self, xx, exp):
        # 用多项式拟合
        fit3 = np.polyfit(self.time, self.track, exp)
        formula3 = np.poly1d(fit3)

        yy = np.zeros(len(xx))
        for idx, x in enumerate(xx):
            li = np.zeros(exp+1)
            for i in range(0, exp+1):
                li[i] = fit3[exp-i]*x**i
            yy[idx] = np.sum(li)
        return yy, fit3

    def expFit(self, xx):
        def func(x, a, b):
            return a*np.exp(b/x)
        popt, pcov = curve_fit(func, self.time, self.track)
        # popt里面是拟合系数，读者可以自己help其用法
        a = popt[0]
        b = popt[1]
        return func(xx, a, b)


if __name__ == '__main__':
    timeData = [0, 7, 23, 32, 39, 43, 56, 63, 71, 80, 88, 96, 103, 111, 119, 128, 136, 147, 151, 159, 167, 171, 180, 187, 196, 203, 211, 219, 227, 235, 243, 251, 263, 271, 279, 287,
                295, 299, 308, 320, 327, 335, 343, 351, 360, 368, 375, 383, 391, 400, 407, 415, 424, 428, 435, 444, 451, 460, 467, 475, 483, 492, 499, 510, 516, 524, 533, 638, 646, 732]
    trackData = [0, 1, 3, 4, 5, 8, 8, 10, 11, 13, 16, 17, 20, 23, 27, 30, 32, 34, 36, 38, 40, 41, 44, 47, 49, 52, 54, 57, 59, 63, 66, 69, 72, 76, 78, 82, 88, 93, 99,
                 103, 104, 108, 112, 117, 123, 128, 133, 136, 140, 145, 152, 158, 165, 173, 181, 189, 196, 204, 211, 217, 224, 231, 237, 243, 248, 254, 258, 264, 265, 265]
    mouseTrackParser = mouseTrackParser(timeData, trackData)
    pylab.plot(timeData, trackData, '.')
    pylab.plot(timeData, trackData, '-')
    xx = np.arange(0, 1000)
    yy, fits = mouseTrackParser.myPolyfit(xx, 3)
    # yy = expFit(xx, time, track)
    pylab.plot(xx, yy, 'r')
    pylab.show()
