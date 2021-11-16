from MenuClass import Menu

if __name__ == "__main__":
    flag = True
    while flag:
        menu = Menu()
        choice = input("Do you want to exit?[y/n]")
        if choice == "y":
            flag = False
