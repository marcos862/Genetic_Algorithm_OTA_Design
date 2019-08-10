#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      mibolano
#
# Created:     16/11/2018
# Copyright:   (c) mibolano 2018
# Licence:     <your licence>
#-------------------------------------------------------------------------------

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
        return 100 * (x2 - x1**2)**2 + (1 - x1)**2

    def getFitness(self, value):
        return 1.0 / (1.0 + value)

class StyblinskiTang(OptFunction):
    def getRangeX1(self):
        return [-5.0, 5.0]

    def getRangeX2(self):
        return [-5.0, 5.0]

    def getBestX(self):
        return [-2.903535,-2.903534]

    # 0.5 (x^4 - 16*x^2 + 5*x + x2^4 - 16*x2^2 + 5*x2)
    def evaluate(self, x1, x2):
        return 0.5 * (x1**4 - 16*x1**2 + 5*x1 + x2**4 - 16*x2**2 + 5*x2)

    def getFitness(self, value):
        #return 1.0 - (78.33233140752647 + value) / 1078.33233140752647
        return 1.0 - (100 + value) / 1100

def main():
    pass

if __name__ == '__main__':
    main()
