name = input('Enter your name ')
age = input('Enter your age ')

def getNameAge():
    print (' Your name is ' + name + ' and your age is ' + age)

def getAnyNameAndAge(name,age):
    print('Your name is ' + name + ' and age is ' + age)

getAnyNameAndAge(name,age)

def calculateDecadesLived(years):
    numOfDecades = int(years) // 10
    return numOfDecades

print(calculateDecadesLived(age))