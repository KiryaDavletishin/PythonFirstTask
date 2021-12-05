import sqlite3 as data
import os
import random

class Matrix:

    def __init__(self, line=0, column=0):
        self.line = line
        self.column = column
        self.matrix = []

    @staticmethod
    def __input_number(str_name):
        print(str_name)
        param = input()
        try:
            param = int(param)
            return param
        except ValueError:
            return Matrix.__input_number(str)

    @staticmethod
    def __set_matrix_size():
        string = input("Enter the matrix size under space ")
        try:
            list_size = string.split()
            list_size = [int(list_size[0]), int(list_size[1])]
            return list_size
        except ValueError or IndexError:
            return Matrix.__set_matrix_size()

    @staticmethod
    def __string_list_to_int(list1):
        if isinstance(list1, list):
            for index in range(len(list1)):
                list1[index] = int(list1[index])
        return list1


    @staticmethod
    def __set_matrix_index(size1, size2):
        matrix = []
        try:
            for counterLine in range(size1):
                string = input(f"Enter though a space {size2} number ")
                list_index = string.split()
                if len(list_index) == size2:
                    matrix.append(Matrix.__string_list_to_int(list_index))
                else:
                    print("You have introduced a wrong line")
                    raise ValueError
        except ValueError:
            matrix = Matrix.__set_matrix_index(size1, size2)
        return matrix

    def init_matrix(self):
        size = Matrix.__set_matrix_size()
        self.line = size[0]
        self.column = size[1]
        self.matrix = Matrix.__set_matrix_index(self.line, self.column)

    def show_matrix(self):
        for index in self.matrix:
            print(index)

    def __compare_size(self, other):
        if self.line == other.line and self.column == other.column:
            return True
        else:
            return False

    def __add__(self, other):
        if isinstance(other, Matrix) and self.__compare_size(other):
            self.matrix = [[self.matrix[i][j] + other.matrix[i][j] for j in range(self.column)] for i in
                           range(self.line)]
            return self

    def __sub__(self, other):
        if isinstance(other, Matrix) and self.__compare_size(other):
            self.matrix = [[self.matrix[i][j] - other.matrix[i][j] for j in range(self.column)] for i in
                           range(self.line)]
            return self

    def __multiplication_number(self, number):
        self.matrix = [[self.matrix[i][j] * number for j in range(self.column)] for i in range(self.line)]
        return self

    def transporting_matrix(self):
        self.matrix = [[self.matrix[j][i] for j in range(self.column)] for i in range(self.line)]
        return self

    def __multiplication_matrix(self, other):
        if self.column == other.line:
            self.matrix = [[0 * i * j for i in range(other.column)] for j in range(self.line)]
            for i in range(self.line):
                for j in range(other.column):
                    for k in range(self.column):
                        self.matrix[i][j] = self.matrix[i][k] * other.matrix[k][j]
        return self

    def __mul__(self, other):
        if isinstance(other, Matrix):
            return self.__multiplication_matrix(other)
        elif isinstance(other, int) or isinstance(other, float):
            return self.__multiplication_number(other)

    def write_matrix_file(self):
        self.init_matrix()
        name = f"{random.randint(0, 50)}{random.randint(0, 50)}"
        try:
            self.__write_file(name)
        except FileNotFoundError:
            os.mkdir("File")
            self.__write_file(name)

    def __write_file(self, name):
        with open(f"File/{name}.txt", "w") as file:
            for i in range(self.line):
                for j in range(self.column):
                    file.write(str(self.matrix[i][j]) + " ")
                file.write("\n")

    def read_matrix_file(self):
        str_name = "Enter file's name"
        name = Matrix.__input_number(str_name)
        try:
            with open(f"File/{name}.txt") as file:
                for line in file:
                    self.matrix.append(Matrix.__string_list_to_int(line.split()))
                    self.column = len(line.split())
                    self.line += 1
        except FileNotFoundError:
            print("You enter wrong file's name")
            self.read_matrix_file()

    @staticmethod
    def delete_data_base():
        with data.connect("Matrix.db") as table:
            cur = table.cursor()
            cur.execute("DROP TABLE IF EXISTS matrix")
            cur.execute("DROP TABLE IF EXISTS matrix_table")

    @staticmethod
    def add_data_base():
        with data.connect("Matrix.db") as table:
            cur = table.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS matrix(
            matrix_id INTEGER PRIMARY KEY,
            line INTEGER,
            column INTEGER
            )""")
            cur.execute("""CREATE TABLE IF NOT EXISTS matrix_table(
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

    @staticmethod
    def __check_value():
        with data.connect("Matrix.db") as table:
            cur = table.cursor()
            value = cur.execute(
                "SELECT matrix_number FROM matrix_table"
                " WHERE matrix_number =(SELECT MAX(matrix_number) FROM matrix_table)")
            value = value.fetchone()
            try:
                value = value[0]
            except TypeError:
                value = 0
            return value

    def add_data_data_base(self):
        Matrix.add_data_base()
        self.init_matrix()
        with data.connect("Matrix.db") as table:
            cur = table.cursor()
            cur.execute(f"INSERT INTO matrix(line, column) VALUES({self.line},{self.column})")
            value = Matrix.__check_value()
            counter = 1
            for index in range(len(self.matrix)):
                for sub_index in range(len(self.matrix[index])):
                    if counter != 1:
                        cur.execute(
                            f"UPDATE matrix_table SET number{counter} = {self.matrix[index][sub_index]}"
                            f" WHERE matrix_number = {value + 1}")
                    else:
                        cur.execute(f"INSERT INTO matrix_table(number{counter})"
                                    f" VALUES({self.matrix[index][sub_index]})")
                    counter += 1

    def read_data_base(self):
        str_name = "Enter number matrix"
        identifier = Matrix.__input_number(str_name)
        with data.connect("Matrix.db") as table:
            cur = table.cursor()
            counter = 4
            value = cur.execute(f"SELECT * FROM matrix JOIN matrix_table"
                                f" ON matrix_table.matrix_number =  {identifier}")
            value = value.fetchone()
            self.line = value[1]
            self.column = value[2]
            for i in range(self.line):
                self.matrix.append(list(value[counter: counter + self.column]))
                counter += self.column
