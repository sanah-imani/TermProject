#functions class
import numpy as np
class Function(object):
    functions = ['Square Root', 'Linear', 'Quadratic', 'Cubic', 'Quartic','']
    def __init__(self, key, category, startCoords, endCoords, showCoords):
        self.startCoords = startCoords
        self.endCoords = endCoords
        self.showCoords = showCoords
        self.key = key
        self.category = category
        self.move = True
    def setPixelInterval(self, pixelInterval):
        self.pixelInterval = pixelInterval
    def setTransformedCoords(self, transformedCoords):
        self.finalCoords = transformedCoords
    def setCartesianCoords(self, cartesianCoords):
        self.cartesianCoords = cartesianCoords
    def getFunctions(self):
        return self.functions
    def applyTransformation(self, transformation):
        for i in range(len(self.finalCoords)):
            self.finalCoords[i][0] += transformation[0]
            self.finalCoords[i][1] += transformation[1]
    @staticmethod
    def getInterval(st, end, n):
        return [st + x*(end-st)/n for x in range(n)]
    

#polynomial
class polynomial(Function):
    params = {'Square Root': ['A'],
              'Linear': ['A','B'],
              'Quadratic': ['A','B','C'],
              'Cubic': ['A','B','C','D'],
              'Quartic': ['A','B','C','D']}
    
    degrees = {'Square Root': 0.5,
              'Linear': 1,
              'Quadratic': 2,
              'Cubic': 3,
              'Quartic': 4}
    def __init__(self, key, category, startCoords, endCoords, showCoords, coeffs, transformation, degree):
        super().__init__(key, category, startCoords, endCoords, showCoords)
        self.degree = degree
        self.coeffs = coeffs
        self.transformation = transformation
        
    @staticmethod
    def getExpression(category, degree):
        exp = ""
        coeffs = polynomial.params[category]
        for i in range(len(coeffs)):
            exp += f"{coeffs[i]}x**{degree-i} +"
        exp = exp[:-2]
        return exp
        
    def getCoords(self, samples):
        x = Function.getInterval(self.startCoords, self.endCoords,samples)
        print(x)
        y = []
        if self.degree == 0.5:
            for i in range(len(x)):
                y.append(self.coeffs[0]*(x[i])**(0.5))
            
        else:
            for i in range(len(x)):
                intermed = 0
                for j in range(len(self.coeffs)):
                    intermed += (self.coeffs[j]*(x[i])**(self.degree-j))
                y.append(15*intermed)
        print(y)
        allCoords = []
        for i in range(len(x)):
            allCoords.append([x[i],y[i]])
        print(allCoords)
        return allCoords
    def getDerivative(self,pointX):
        finalAns = 0
        for i in range(len(self.coeffs)+1):
            finalAns += (self.degree-j)*(self.coeffs[j])*(pointX**(self.degree-j-1))
        return finalAns

