from Model import *
from View import View
import time
import os

table_names = list(["publisher","owner","game","tag","gametags"])

class Controler():

    def __init__(self):
        self.view=View()

    def insert_menu(self):
        table_name = self.view.output_table_names()
        data = list()
        for i in columns[table_name]:
            data.append(input(f"Enter {i}"))
        insert(table_name,data)

    def delete_menu(self):
        table_name = self.view.output_table_names()
        dataid = input("Enter ID")
        delete(table_name,dataid)

    def change_menu(self):
        table_name = self.view.output_table_names()
        data = list()
        dataid = input("Enter ID")
        for i in columns[table_name]:
            data.append(input(f"Enter {i}"))
        update(table_name,dataid,data)

    def search_menu(self):
        View.search_menu()
        n = int(input("Choose what u want to find"))
        data = search_data(n) if 1 <= n <= 3 else print("Wrong parameter")
        if len(data) == 0: 
            print("Nothing found")
        else:
            self.view.output_table_data(data)
        if int(input("Type 1 to continue working")) == 1:
            print('|\n'*20)
            self.main_control()

    def generate_menu(self):
        table = View.output_table_names()
        print('='*70)
        generate_data(table, int(input("Write how much to generate: ")))
        if int(input("Type 1 to continue working")) == 1:
            print('|\n'*20)
            self.main_control()

    def main_control(self):
        flag = self.view.main_menu()
        if flag == 1:
            print('='*70)
            self.insert_menu()
        elif flag == 2:
            print('='*70)
            self.delete_menu()
        elif flag == 3:
            print('='*70)
            self.change_menu()
        elif flag == 4:
            print('='*70)
            self.generate_menu()
        elif flag == 5:
            print('='*70)
            self.search_menu()
        elif flag ==-1:
            print('*'*70)
            print("invalid input")
            time.sleep(3)
            print('*'*70)
            self.main_control()


if __name__ == '__main__':
    controller = Controler()
    controller.main_control()

