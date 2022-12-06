from model import Model
from View import View
from array import *
import time
import os
class Controler():

    def __init__(self):
        self.model=Model()
        self.view=View()

    def insert_menu(self):
        table = self.view.output_table_names()
        print('='*70)
        table_data = self.model.get_table_data(table)
        table_data=list(table_data)
        tid = str(table+'id')
        if tid in table_data[0]:
            table_data[0].remove(tid)
        values = []
        for i in range(len(table_data[0])):
            values.append(input(f"Enter value for column {table_data[0][i]}: "))
        self.model.insert_data(table, values)
        if int(input("Type 1 to continue working")) == 1:
            print('|\n'*20)
            self.main_control()

    def delete_menu(self):
        table = self.view.output_table_names()
        print('='*70)
        table_data = self.model.get_table_data(table)
        self.view.output_table_data(table_data)
        try:
            self.model.delete_data(table, table_data[1][int(input('Choose number:')) - 1])
        except Exception as e:
            print(e)
        if int(input("Type 1 to continue working")) == 1:
            print('|\n'*20)
            self.main_control()

    def change_menu(self):
        table = self.view.output_table_names()
        print('='*70)
        table_data = self.model.get_table_data(table)
        id_name = table_data[0][0]
        try:
            num = table_data[1][int(input('Choose number:')) - 1][0]
        except Exception as e:
            print('*'*70)
            print(e)
            return 0
        tid = str(table+'id')
        if tid in table_data[0]:
            table_data[0].remove(tid)
        values = []
        for i in range(len(table_data[0])):
            values.append(input(f"Enter value for column {table_data[0][i]}: "))
        self.model.change_data(table, values, table_data[0], num, id_name)
        if int(input("Type 1 to continue working")) == 1:
            print('|\n'*20)
            self.main_control()

    def generate_menu(self):
        table = self.view.output_table_names()
        print('='*70)
        self.model.generate_data(table, int(input("Write how much to generate: ")))
        if int(input("Type 1 to continue working")) == 1:
            print('|\n'*20)
            self.main_control()

    def search_menu(self):
        self.view.search_menu()
        n = int(input("Choose what u want to find"))
        data = self.model.search_data(n) if 1 <= n <= 3 else print("Wrong parameter")
        if len(data) == 0: 
            print("Nothing found")
        else:
            self.view.output_table_data(data)
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
    model = Model()
    control = Controler()
    control.main_control()
