from MatrixClass import Matrix
import sys

class Menu:

    def __init__(self):
        self.__delete()

    def __loop(self):
        while True:
            self.__select_menu()

    def __selection_matrix(self):
        self.__condition1 = "3"
        str_name = ["Do you want to enter another matrix?[y/n]"]
        list_select = ["y", "n"]
        select = Menu.input_menu(str_name, list_select)
        if select == "n":
            str_name = ["Do you want to transporting or multiplication at number matrix? [t/m]"]
            list_select = ["t", "m"]
            select = Menu.input_menu(str_name, list_select)
            if select == "t":
                self.menu_action("5")
            elif select == "m":
                self.menu_action("4")
            self.condition = "0"

    def __select_menu(self):
        if self.counter == 1 and self.__condition1 == "2":
            self.__selection_matrix()
        if self.counter == 2:
            self.menu_action()
        elif self.condition == "100":
            self.main_menu()
        elif self.condition == "200":
            self.menu_read()
        elif self.condition == "300":
            self.menu_write()

    def __exit_main_menu(self):
        self.condition = "100"
        self.counter += 1
        self.__select_menu()

    def main_menu(self):
        str_name = ["Choose an action", "1 Add data", "2 Read data", "3 Exit"]
        list_select = ["1", "2", "3"]
        param = Menu.input_menu(str_name, list_select)
        if param == "1":
            self.condition = "300"
        elif param == "2":
            self.condition = "200"
        elif param == "3":
            sys.exit()
        self.__select_menu()

    def menu_read(self):
        str_name = ["Choose an action", "1 Read Matrix from file", "2 Read Matrix from Database"]
        list_select = ["1", "2"]
        param = Menu.input_menu(str_name, list_select)
        if param == "1":
            self.__matrixList[self.counter].read_matrix_file()
        elif param == "2":
            self.__matrixList[self.counter].read_data_base()
        self.__exit_main_menu()

    def menu_write(self):
        str_name = ["Choose an action", "1 Add new Matrix", "2 Write Matrix to file", "3 Write Matrix to Database"]
        list_select = ["1", "2", "3"]
        param = Menu.input_menu(str_name, list_select)
        if param == "1":
            self.__matrixList[self.counter].init_matrix()
        elif param == "2":
            self.__matrixList[self.counter].write_matrix_file()
        elif param == "3":
            self.__matrixList[self.counter].add_data_data_base()
        self.__exit_main_menu()

    def menu_action(self, param="0"):
        if param == "0":
            str_name = ["Choose an action", "1 Summa Matrix", "2 Difference Matrix", "3 Multiplication Matrix"]
            list_select = ["1", "2", "3"]
            param = Menu.input_menu(str_name, list_select)
        if param == "1":
            self.__matrixList[0] += self.__matrixList[1]
        elif param == "2":
            self.__matrixList[0] -= self.__matrixList[1]
        elif param == "4":
            number = Menu.input_value()
            self.__matrixList[0] *= number
        elif param == "3":
            self.__matrixList[0] *= self.__matrixList[1]
        elif param == "5":
            self.__matrixList[0] = self.__matrixList[0].transporting_matrix()
        self.__matrixList[0].show_matrix()
        self.__delete()

    def __delete(self):
        self.__matrixList = [Matrix() for i in range(2)]
        self.condition = "100"
        self.__condition1 = "2"
        self.counter = 0
        self.__loop()

    @staticmethod
    def input_menu(str_name, list_name):
        for index in str_name:
            print(index)
        param = input()
        try:
            if param in list_name:
                return param
            else:
                raise ValueError
        except ValueError:
            return Menu.input_menu(str_name, list_name)

    @staticmethod
    def input_value():
        param = input("Enter your value ")
        try:
            param = float(param)
            return param
        except ValueError:
            return Menu.input_value()
