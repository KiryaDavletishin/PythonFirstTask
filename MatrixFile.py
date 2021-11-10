#блок импорта
import sqlite3 as data
import os
import random
#блок глобальных переменных
#блок функций
class Menu:

    def __init__(self):
        self.counter = 0
        self.__matrixList = [Matrix() for i in range(2)]
        self.condition = "100"
        self.__condition1 = "2"
        self.__selectMenu()

    def __selectoneMatrix(self):
        self.__condition1 = "3"
        str = ["Do you want to enter another matrix?[y/n]"]
        list = ["y", "n"]
        choice = inputMenu(str, list)
        if choice == "n":
            str = ["Do you want to transporting or multiplication at number matrix? [t/m]"]
            list = ["t", "m"]
            choice = inputMenu(str, list)
            if choice == "t":
                self.menuAction("5")
            elif choice == "m":
                self.menuAction("4")
            self.condition = "0"

    def __selectMenu(self):
        if self.counter == 1 and self.__condition1 == "2":
            self.__selectoneMatrix()
        if self.counter == 2:
            self.menuAction()
        elif self.condition == "100":
            self.mainMenu()
        elif self.condition == "200":
            self.menuRead()
        elif self.condition == "300":
            self.menuWrite()

    def __exitMainMenu(self):
        self.condition = "100"
        self.counter += 1
        self.__selectMenu()

    def mainMenu(self):
        str = ["Choose an action", "1 Add data", "2 Read data"]
        listchoices = ["1", "2"]
        param = inputMenu(str, listchoices)
        if param == "1":
            self.condition = "300"
        elif param == "2":
            self.condition = "200"
        self.__selectMenu()

    def menuRead(self):
        str = ["Choose an action", "1 Read Matrix from file", "2 Read Matrix from Database"]
        listchoices = ["1", "2"]
        param = inputMenu(str, listchoices)
        if param == "1":
            self.__matrixList[self.counter].readMatrixFromFile()
        elif param == "2":
            self.__matrixList[self.counter].readFromDB()
        self.__exitMainMenu()

    def menuWrite(self):
        str = ["Choose an action", "1 Add new Matrix", "2 Write Matrix to file", "3 Write Matrix to Database"]
        listchoices = ["1", "2", "3"]
        param = inputMenu(str, listchoices)
        if param == "1":
            self.__matrixList[self.counter].inizializationMatrix()
        elif param == "2":
            self.__matrixList[self.counter].writeMatrixatFile()
        elif param == "3":
            self.__matrixList[self.counter].addDataIntoDB()
        self.__exitMainMenu()

    def menuAction(self, param = "0"):
        if param == "0":
            str = ["Choose an action", "1 Summa Matrix", "2 Difference Matrix", "3 Multiplication Matrix"]
            list = ["1", "2", "3"]
            param = inputMenu(str, list)
        if param == "1":
            self.__matrixList[0] += self.__matrixList[1]
        elif param == "2":
            self.__matrixList[0] -= self.__matrixList[1]
        elif param == "4":
            number = inputValue()
            self.__matrixList[0] *= number
        elif param == "3":
            self.__matrixList[0] *= self.__matrixList[1]
        elif param == "5":
            self.__matrixList[0] = self.__matrixList[0].transprocessingMatrix()
        self.__matrixList[0].showMatrix()

def inputMenu(str, list1):
    for index in str:
        print(index)
    param = input()
    try:
        if param in list1:
            return param
        else: raise ValueError
    except ValueError:
        return inputMenu(str, list1)

def inputValue():
    param = input("Enter your value ")
    try:
        param = float(param)
        return param
    except ValueError:
        return inputValue()

def inputNumber(str):
    print(str)
    param = input()
    try:
        param = int(param)
        return param
    except ValueError:
        return inputValue()

def setMatrixSize():
    string = input("Enter the matrix size under space ")
    listSize = string.split()
    try:
        listSize = [int(listSize[0]), int(listSize[1])]
        return listSize
    except ValueError or IndexError:
        return setMatrixSize()

def StringListToInt(list1):
    if isinstance(list1, list):
        for index in range(len(list1)):
            list1[index] = int(list1[index])
    return list1

def nullList(size2):
    list1 = [0 for i in range(0, size2, 1)]
    return list1

def setMatrixIndex(size1, size2):
    matrix = []
    for counterLine in range(size1):
        string = input(f"Enter though a space {size2} number ")
        ListIndex = string.split()
        if len(ListIndex) == size2:
            try:
                matrix.append(StringListToInt(ListIndex))
            except ValueError:
                matrix.append(nullList(size2))
        else:
            print("Error number values")
            matrix.append(nullList(size2))
    return matrix

#блок классов
class Matrix:

    def __init__(self):
        self.line = 0
        self.column = 0
        self.matrix = []

    def inizializationMatrix(self):
        size = setMatrixSize()
        self.line = size[0]
        self.column = size[1]
        self.matrix = setMatrixIndex(self.line, self.column)

    def showMatrix(self):
        for index in range (len(self.matrix)):
            for jndex in range(len(self.matrix[index])):
                print(self.matrix[index][jndex], end = " ")
            print()

    def __compareSize(self, object):
        if self.line == object.line and self.column == object.column: return True
        else: return False

    def __add__(self, object):
        if isinstance(object, Matrix) and self.__compareSize(object):
            self.matrix = [[self.matrix[i][j]+object.matrix[i][j] for j in range(self.column)] for i in range(self.line)]
            return self

    def __sub__(self, object):
        if isinstance(object, Matrix) and self.__compareSize(object):
            self.matrix = [[self.matrix[i][j]-object.matrix[i][j] for j in range(self.column)] for i in range(self.line)]
            return self

    def __mul__(self, number: int):
        self.matrix = [[self.matrix[i][j] * number for j in range(self.column)] for i in range(self.line)]
        return self

    def transprocessingMatrix(self):
        self.matrix = [[self.matrix[j][i] for j in range(self.column)] for i in range(self.line)]
        return self

    def __mul__(self, other: object):
        if self.column == other.line and isinstance(other, Matrix):
            self.matrix = [[0 for j in range(other.column)] for i in range(self.line)]
            for i in range(self.line):
                for j in range(self.column):
                    for k in range(other.line):
                        self.matrix[i][j] += self.matrix[i][k] * other.matrix[k][j]
        return self

    def writeMatrixatFile(self):
        self.inizializationMatrix()
        name = f"{random.randint(0,50)}{random.randint(0,50)}"
        try:
            self.__writeFile(name)
        except FileNotFoundError:
            os.mkdir("File")
            self.__writeFile(name)

    def __writeFile(self, name):
        with open(f"File/{name}.txt", "w") as file:
            for i in range(self.line):
                for j in range(self.column):
                    file.write(str(self.matrix[i][j]) + " ")
                file.write("\n")

    def readMatrixFromFile(self):
        str = "Enter file's name"
        name = inputNumber(str)
        with open(f"File/{name}.txt") as file:
            for line in file:
                self.matrix.append(StringListToInt(line.split()))
                self.column = len(line.split())
                self.line +=1

    def deleteFile(self):
        str = "Enter file's name"
        name = inputNumber(str)
        os.remove(f"File/{name}.txt")

    def deleteDB(self):
        with data.connect("Matrix.db") as table:
            cur = table.cursor()
            cur.execute("DROP TABLE IF EXISTS matrix")
            cur.execute("DROP TABLE IF EXISTS matrixnumber")

    def addDB(self):
        with data.connect("Matrix.db") as table:
            cur = table.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS matrix(
            matrix_id INTEGER PRIMARY KEY,
            line INTEGER,
            column INTEGER
            )""")
            cur.execute("""CREATE TABLE IF NOT EXISTS matrixnumber(
            matrix_number INTEGER PRIMARY KEY,
            number1 INTEGER,
            number2 INTEGER,
            number3 INTEGER,
            number4 INTEGER,
            number5 INTEGER,
            number6 INTEGER,
            number7 INTEGER,
            number8 INTEGER,
            number9 INTEGER
            )""")

    def __checkValue(self, value):
        with data.connect("Matrix.db") as table:
            cur = table.cursor()
            value = cur.execute("SELECT matrix_number FROM matrixnumber WHERE matrix_number =(SELECT MAX(matrix_number) FROM matrixnumber)")
            value = value.fetchone()
            try:
                value = value[0]
            except TypeError:
                value = 0
            return value

    def addDataIntoDB(self):
        self.addDB()
        self.inizializationMatrix()
        with data.connect("Matrix.db") as table:
            cur = table.cursor()
            cur.execute(f"INSERT INTO matrix(line, column) VALUES({self.line},{self.column})")
            value = self.__checkValue()
            counter = 1
            for index in range(len(self.matrix)):
                for jndex in range(len(self.matrix[index])):
                    if counter != 1:
                        cur.execute(f"UPDATE matrixnumber SET number{counter} = {self.matrix[index][jndex]} WHERE matrix_number = {value+1}")
                    else:
                        cur.execute(f"INSERT INTO matrixnumber(number{counter}) VALUES({self.matrix[index][jndex]})")
                    counter +=1

    def readFromDB(self):
        str = "Enter number matrix"
        id = inputNumber(str)
        with data.connect("Matrix.db") as table:
            cur = table.cursor()
            counter = 4
            value = cur.execute(f"SELECT * FROM matrix JOIN matrixnumber ON matrixnumber.matrix_number =  {id}")
            value = value.fetchone()
            self.line = value[1]
            self.column = value[2]
            for i in range(self.line):
                self.matrix.append(list(value[counter : counter+self.column]))
                counter +=self.column

if __name__ =="__main__":
    matrix = Matrix()
    matrix.deleteDB()
    flag = True
    while flag:
        menu = Menu()
        choice = input("Do you want to exit?[y/n]")
        if choice == "y":
            flag = False

