# ----------------------------------------------------------------- -----------------------------------------------------------------

import os
import sqlite3 as SQL

# ----------------------------------------------------------------- -----------------------------------------------------------------

# Класс хранения данных о профилях
class Profile:
    
    def __init__(self, Login, Pass, Name, Test1 ):

        self.Login  = Login
        self.Pass   = Pass
        self.Name   = Name
        self.Test1  = Test1

    def setLogin(self,value):   self.Login  = value
    def setPass(self,value):    self.Pass   = value
    def setName(self,value):    self.Name   = value
    def setTest1(self,value):   self.Test1  = value
 
    def getLogin(self):         return self.Login 
    def getPass(self):          return self.Pass  
    def getName(self):          return self.Name  
    def getTest1(self):         return self.Test1 

    def __str__(self): return "\nLogin: {}\nPass: {}\nName: {}\nTest1: {}\n".format(self.Login, self.Pass, self.Name, self.Test1)
   
 # ----------------------------------------------------------------- -----------------------------------------------------------------

# База данных
class DataBaseProfile:
    
    # ----------------------------------------------------------------- 

    def __init__(self): self.ListProfile = []       # Список хранения профилей

    # ----------------------------------------------------------------- 


    # Добавляем профиль
    def addProfile(self,Login, Pass, Name, Test1):
        NewProfile = Profile(Login,Pass,Name,Test1)
        self.ListProfile.append(NewProfile)
    
    # ----------------------------------------------------------------- 

    # Возращает весь список профилей
    def getListProfile(self):       return self.ListProfile

    # Кол-во профилей
    def getLenProfiles(self):       return len(self.ListProfile)

    # Получить профиль по ID
    def findProfileID(self,ID):     return self.ListProfile[ID]

    # ----------------------------------------------------------------- 

    # Очистить базу данных
    def Clear(self): self.ListProfile.clear(); print(" >>> Clear Data Base !!!")

    # ----------------------------------------------------------------- 

    # Изменяем параметры профиля по ID

    def setLogin(self,ID,value):    self.ListProfile[ID].setLogin(value)
    def setPass(self,ID,value):     self.ListProfile[ID].setPass(value)
    def setName(self,ID,value):     self.ListProfile[ID].setName(value)
    def setTest1(self,ID,value):    self.ListProfile[ID].setTest1(value); print(self.ListProfile[ID])

    # ----------------------------------------------------------------- 
    
    # Узнаем параметры профиля по ID

    def getLogin(self,ID):          return self.ListProfile[ID].getLogin()
    def getPass(self,ID):           return self.ListProfile[ID].getPass() 
    def getName(self,ID):           return self.ListProfile[ID].getName() 
    def getTest1(self,ID):          return self.ListProfile[ID].getTest1() 

    # ----------------------------------------------------------------- 

    # Поиск ID профиля по его логину
    def getIndexByLogin(self,Login):
        for ID in range(self.getLenProfiles()):
            if(self.ListProfile[ID].getLogin() == Login): return ID
        return False

    # ----------------------------------------------------------------- 
    # Сохраняем базу данных
    def SaveDB(self,FileName):

        print(" >>> Save Data Base File: ",  FileName)

        # Удаляем файл перед его перезаписыванием
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), FileName)
        os.remove(path)

        # Подключаем файл базы данных
        MyDataBase = SQL.connect(FileName)
        SQLite = MyDataBase.cursor()

        # Создаем таблицу базы данных, если ее не существет
        SQLite.execute("""CREATE TABLE IF NOT EXISTS Profile (Login TEXT, Pass TEXT, Name TEXT, Test1 INT)""")

        # Подтверждение
        MyDataBase.commit()

        # Получаем списки данных профилей
        MyProfile    = [ [
            self.ListProfile[I].getLogin(),
            self.ListProfile[I].getPass(),
            self.ListProfile[I].getName(), 
            self.ListProfile[I].getTest1()
            ] for I in range(len(self.ListProfile)) ]
        
        for ID in range(len(MyProfile)): 
            SQLite.execute(f"SELECT Login FROM Profile WHERE Login = '{MyProfile[ID][0]}'")
            if SQLite.fetchone() is None:
                print(" >>> Save Name Profile: ", MyProfile[ID][2])
                SQLite.execute(f"INSERT INTO Profile VALUES ( '{MyProfile[ID][0]}', '{MyProfile[ID][1]}', '{MyProfile[ID][2]}', {MyProfile[ID][3]})")
            MyDataBase.commit()

        # Повторное подтверждение
        print(" >>> Save Data Base Complete")
        MyDataBase.commit()

    # ----------------------------------------------------------------- 

    # Загружаем базу данных
    def LoadDB(self,FileName):

        print(" >>> Load Data Base File: ",  FileName)

        # Подключаем файл базы данных
        MyDataBase = SQL.connect(FileName)
        SQLite = MyDataBase.cursor()

        # Получаем данные из базы данных
        for ITEM in SQLite.execute("SELECT * FROM Profile"): 
            print(" >>> Load Name Profile: ", ITEM[2])
            self.addProfile(ITEM[0],ITEM[1],ITEM[2],ITEM[3]) 

        print(" >>> Load Data Base Complete")
    
    # ----------------------------------------------------------------- 