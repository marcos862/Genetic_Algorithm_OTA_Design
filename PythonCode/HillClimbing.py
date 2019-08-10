#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mibolano
#
# Created:     13/11/2018
# Copyright:   (c) mibolano 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import random as r

class OptFunction():
    def getRangeX1(self):
        pass

    def getRangeX2(self):
        pass

    def getBestX(self):
        pass

    def evaluate(self, x1, x2):
        pass

    def getFitness(self, value):
        pass

class Rosenbrock(OptFunction):
    def getRangeX1(self):
        return [-5.0, 5.0]

    def getRangeX2(self):
        return [-5.0, 5.0]

    def getBestX(self):
        return [1.0, 1.0]

    def evaluate(self, x1, x2):
        return 100*(x2-x1**2)**2 + (1 - x1)**2

    def getFitness(self, value):
        return 1.0 / (1.0 + value)

class StyblinskiTang(OptFunction):
    def getRangeX1(self):
        return [-5.0, 5.0]

    def getRangeX2(self):
        return [-5.0, 5.0]

    def getBestX(self):
        return [-2.903535,-2.903534]

    def evaluate(self, x1, x2):
        return 0.5 * (x1**4 - 16*x1**2 + 5*x1 + x2**4 - 16*x2**2 + 5*x2)

    def getFitness(self, value):
        return 1.0 - (100 + value) / 1000

def rand(min, max):
    return (max - min) * r.random() + min

def norm(x1, x2):
    return (x1**2 + x2**2)**0.5

def hillClimbing(fn, G, minDx):
    x1 = rand(fn.getRangeX1()[0], fn.getRangeX1()[1])
    x2 = rand(fn.getRangeX2()[0], fn.getRangeX2()[1])
    r = fn.evaluate(x1, x2)
    f = fn.getFitness(r)

    Dx1 = (fn.getRangeX1()[1] - fn.getRangeX1()[0]) * (1 - f)
    Dx2 = (fn.getRangeX2()[1] - fn.getRangeX2()[0]) * (1 - f)

    g = 0
    while (g < G) and (norm(Dx1, Dx2) > minDx):
        dx1 = rand(-Dx1 / 2, Dx1 / 2)
        dx2 = rand(-Dx2 / 2, Dx2 / 2)
        r1 = fn.evaluate(x1 + dx1, x2 + dx2)
        if r1 < r:
            r = r1
            f = fn.getFitness(r)
            x1 += dx1;
            x2 += dx2;
            Dx1 = (fn.getRangeX1()[1] - fn.getRangeX1()[0]) * (1 - f)
            Dx2 = (fn.getRangeX2()[1] - fn.getRangeX2()[0]) * (1 - f)
        g += 1
    print "\tBest Solution: f({},{}) = {}".format(x1, x2, r)
    print "\tGenerations = {}, Fitness = {}".format(g + 1, f)
    print "\tDistant to the Optimal: {}".format(norm(x1 - fn.getBestX()[0], x2 - fn.getBestX()[1]))

def main():
    print "Rosenbrock Function:"
    f = Rosenbrock()
    hillClimbing(f, 1000000, 0.00001)

    print "\nStyblinskiTang Function:"
    f = StyblinskiTang()
    hillClimbing(f, 1000000, 0.00001)


if __name__ == '__main__':
    main()
