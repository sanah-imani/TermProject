#functions class
class Function(object):
    functions = ['Square Root', 'Linear', 'Quadratic', 'Cubic', 'Quartic']
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
    #https://stackoverflow.com/questions/6683690/making-a-list-of-evenly-spaced-numbers-in-a-certain-range-in-python
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
        y = []
        if self.degree == 0.5:
            for i in range(len(x)):
                y.append(15*self.coeffs[0]*(x[i])**(0.5))
            
        else:
            for i in range(len(x)):
                intermed = 0
                for j in range(len(self.coeffs)):
                    intermed += (self.coeffs[j]*(x[i])**(self.degree-j))
                y.append(15*intermed)
        allCoords = []
        for i in range(len(x)):
            allCoords.append([x[i],y[i]])
        return allCoords
    def getDerivative(self,pointX, frame):
        translation = self.pixelInterval[0] - self.finalCoords[0][0]
        transformedX = (pointX + (600*frame)) - translation
        finalAns = 0
        for j in range(len(self.coeffs)):
            finalAns += (self.degree-j)*(self.coeffs[j])*(transformedX**(self.degree-j-1))
        return finalAns

    def reflectH(self):
        for i in range(len(self.cartesianCoords)):
            self.cartesianCoords[i][1] *= -1
        return self.cartesianCoords
    def reflectV(self):
        for i in range(len(self.cartesianCoords)):
            self.cartesianCoords[i][0] *= -1
        reflectedCoords = self.getCoords(len(self.cartesianCoords))
        return reflectedCoords
        
            

