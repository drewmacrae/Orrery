import math

def normalize(vector):
    sumOfSquares = 0
    result = [0]*(len(vector))
    for eachComponent in vector:
        sumOfSquares = sumOfSquares+eachComponent**2
    magnitude = math.sqrt(sumOfSquares)
    for eachIndex in range(len(vector)):
        result[eachIndex]=vector[eachIndex]/magnitude
    return result

def sub(vectorA,vectorB):
    return add(scale(-1,vectorB),vectorA)

def add(vectorA,vectorB):
    assert len(vectorA)==len(vectorB)
    result = [0]*(len(vectorA))
    for eachIndex in range(len(vectorA)):
        result[eachIndex] = vectorA[eachIndex]+vectorB[eachIndex]
    return result

def magnitude(vector):
    #print("computingMagnitude of")
    #print(vector)
    sumOfSquares = 0
    for eachComponent in vector:
        sumOfSquares = sumOfSquares+eachComponent**2
    magnitude = math.sqrt(sumOfSquares)
    #print(magnitude)
    return magnitude

def scale(scalar,vectorA):
    result = [0]*(len(vectorA))
    for eachIndex in range(len(vectorA)):
        result[eachIndex] = vectorA[eachIndex]*scalar
    return result
