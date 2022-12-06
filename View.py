from model import Model

class View():

    def __init__(self):
        self.table_names=''

    def main_menu(self):
        print("Choose a task:")
        print("1.Insert data")
        print("2.Remove data")
        print("3.Edit data")
        print("4.Generate data")
        print("5.Search data")
        task_number=int(input("Enter number of choosen table:"))
        if 0 < task_number < 6:
            return task_number 
        else:
            return -1

    def search_menu(self):
        print("Choose data to search:")
        print("1. Search games with price lower than N")
        print("2. Search tag")
        print("3. Search publisher company")

    def output_table_names(self):
        model = Model()
        table_names = model.get_table_names()
        print("Choose table to work with:")
        i=0
        while i<len(table_names):
            print(str(i+1)+'.'+ table_names[i])
            i+=1
        return table_names[int(input("Enter number of choosen table:"))-1]

    def output_table_data(self,values):
        if type(values) is list:
            for i in values:
                print(i)
        else:
            print(values[0])
            for i in range(len(values[1])):
                print(values[1][i])