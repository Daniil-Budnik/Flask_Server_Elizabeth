
# ----------------------------------------------------------------- -----------------------------------------------------------------

# Импортируем нужные библиотеки
import MyDataBase as MySQL
import flask as FL
import csv as CSV

# ----------------------------------------------------------------- -----------------------------------------------------------------

# Глобальные переменные

app = FL.Flask(__name__, static_url_path='/static')     # Экземпляр сервера
ProfileDB = MySQL.DataBaseProfile()                     # Экземпляр данных
FileSQL = "Profile.db"                                  # Файл базы данных
B1,B2 = 'Авторизация', 'Регистрация'                    # Текст для кнопок
Login = 0

# ----------------------------------------------------------------- -----------------------------------------------------------------

# Проверка авторизации для кнопок
def Cheack():
    global B1; global B2
    if('userLogin' in FL.session): B1 = FL.session['userLogin']; B2 = 'Выход'     
    else: B1 = 'Авторизация'; B2 = 'Регистрация'
     
# ----------------------------------------------------------------- -----------------------------------------------------------------

# Запись в базу данных
def setBD(ITEM): ProfileDB.addProfile(ITEM[0],ITEM[1],ITEM[2],ITEM[3]); ProfileDB.SaveDB(FileSQL)

# Получение база данных
def getBD():

    Profile = []
    for ID in range(ProfileDB.getLenProfiles()):
        Profile.append([ProfileDB.getLogin(ID),ProfileDB.getPass(ID),ProfileDB.getName(ID),ProfileDB.getTest1(ID)])
    return Profile

# -----------------------------------------------------------------

# Главная страница
@app.route('/')
@app.route('/index')
def Index(): Cheack(); return FL.render_template("index.html",B1 = B1, B2 = B2)

# ----------------------------------------------------------------- -----------------------------------------------------------------

# Регистрация
@app.route('/Registration')
@app.route('/Registration', methods=['post'])
def Regis(): 
    Cheack();
    if('userLogin' in FL.session): 
        global B1; global B2 
        B1 = 'Авторизация'; B2 = "Регистрация"; Login = 0
        
        FL.session.clear()
        FL.session.pop('userLogin', None)
        FL.session.pop('userName', None)
        FL.session.pop('userNum', None)

        return FL.redirect(FL.url_for('Autoriz'))
        
    else:
        if(FL.request.method == 'POST'): 

            CSS_G = "p-3 mb-2 bg-success text-white"
            CSS_R = "p-3 mb-2 bg-danger text-white"

            Arr = FL.request.form
            MyBD = getBD()
            EnableRegistr = True
            
            if(len(Arr['login']) < 4):          EnableRegistr = False; FL.flash("Ваш логин слишком маленький!!!",CSS_R);
            if(len(Arr['name']) < 2):           EnableRegistr = False; FL.flash("Ваше имя слишком маленькое!!!",CSS_R);
            if(len(Arr['pass1']) < 4):          EnableRegistr = False; FL.flash("Ваш пароль слишком простой!!!",CSS_R);
            if(Arr['pass1'] != Arr['pass2']):   EnableRegistr = False; FL.flash("Пароли не совпадают!!!",CSS_R);

            if(EnableRegistr):
                for i in range(len(MyBD)):
                    if(MyBD[i][0] == Arr['login'] ): 
                        EnableRegistr = False
                        break

                if(EnableRegistr): 
                    ArrN = [ Arr['login'], Arr['pass1'],  Arr['name'], 0 ]
                    Login = Arr['login']
                    setBD(ArrN)
                    FL.flash("Поздравляю, вы успешно зарегестировались!!! Теперь вы можете авторизоваться!!!", CSS_G);
                    
                else: FL.flash("Данный логин занят!!!", CSS_R);
        Cheack();           
        return FL.render_template("Reg.html", B1 = B1, B2 = B2)

# ----------------------------------------------------------------- -----------------------------------------------------------------

# Авторизация
@app.route('/Authorization')
@app.route('/Authorization', methods=['post'])
def Autoriz(): 

    Cheack(); 

    if('userLogin' in FL.session):
        return FL.redirect(FL.url_for("Profile", userLogin=FL.session["userLogin"]))
    else:
        if(FL.request.method == 'POST'):

            CSS_G = "p-3 mb-2 bg-success text-white"
            CSS_R = "p-3 mb-2 bg-danger text-white"

            Arr = FL.request.form
            MyBD = getBD()

            EnableLogin, N = False, 0

            for i in range(len(MyBD)):
                if(MyBD[i][0] == Arr['Login'] ): 
                    EnableLogin = True
                    N = i
                    
            if(EnableLogin):
               if(Arr['Pass'] == MyBD[N][1]):
                   FL.flash("Авторизация прошла успешно",CSS_G);

                   FL.session.pop('userLogin', None)
                   FL.session.pop('userName', None)
                   FL.session.pop('userNum', None)

                   FL.session["userLogin"] =    str(MyBD[N][0])
                   FL.session["userName"] =     str(MyBD[N][2])
                   FL.session["userNum"] =      str(MyBD[N][3])

                   global B1; global B2
                   B1 = FL.session["userName"]; B2 = "Выход"
                   
                   return FL.redirect("/" + FL.session["userLogin"] )

               else: FL.flash("Вы неправильно ввели ваш пароль!!!",CSS_R);
            else: FL.flash("Вы неправильно ввели ваш логин!!!",CSS_R);

    Cheack();
    return FL.render_template("Aut.html", B1 = B1, B2 = B2)

# ----------------------------------------------------------------- -----------------------------------------------------------------

# Страница профиля
@app.route('/<path:userLogin>')
def Profile(userLogin): 
    if( False == ('userLogin' in FL.session)): return FL.render_template("403.html", B1 = B1, B2 = B2), 403
    Cheack(); 
    return FL.render_template("Profile.html", B1 = B1, B2 = B2)

# ----------------------------------------------------------------- -----------------------------------------------------------------

# Страница профиля
@app.route('/Result', methods=['post'])
def Res(): 
    Cheack(); 
    if(FL.request.method == 'POST'):
        ArrMy = [ FL.request.form[i] for i in FL.request.form]
        with open("Test_1/Test_1.csv") as FileBD: BD = [ Line[0].split(";") for Line in CSV.reader(FileBD) ]
        ArrOt = [ BD[i][6] for i in range(1,len(BD))]
        N = 0
        for i in range(len(ArrOt)):
            if(ArrMy[i] == ArrOt[i]): N+=1
        FL.session["userNum"] = N
        ID = ProfileDB.getIndexByLogin(FL.session["userLogin"])
        ProfileDB.setTest1(ID,N)
        ProfileDB.SaveDB(FileSQL)
    return FL.render_template("Result.html", RES = ArrMy, OTV = ArrOt , B1 = B1, B2 = B2)

# ----------------------------------------------------------------- -----------------------------------------------------------------

# Страница теста 
@app.route('/Test_Cat')
def Test_Cat(): 
    Cheack(); 
    with open("Test_1/Test_1.csv") as FileBD: BD = [ Line[0].split(";") for Line in CSV.reader(FileBD) ]
    return FL.render_template("Test_Cat.html", TEST = BD, B1 = B1, B2 = B2)


# ----------------------------------------------------------------- -----------------------------------------------------------------

# Страница ошибки 404 ( Ой, а тут ничего нет :) )
@app.errorhandler(404)
def Error_404(error): Cheack(); return FL.render_template("404.html", B1 = B1, B2 = B2), 404

# Страница ошибки 403 ( А сюда вам низя !!! )
@app.errorhandler(403)
def Error_403(error): Cheack(); return FL.render_template("403.html", B1 = B1, B2 = B2), 403

# ----------------------------------------------------------------- -----------------------------------------------------------------

# Главный метод
def main(): 

    # Загружаем базу данных
    ProfileDB.LoadDB(FileSQL)
    
    # Вывод базы данных 
    for ID in range(ProfileDB.getLenProfiles()): print(ProfileDB.findProfileID(ID))

    # Ключ шифрования
    app.config["SECRET_KEY"] = "e2h223hljk3lbnsiheilruhil35l35h3k4hjnar"
    
    # Старт сервера
    app.run(debug=True)

    #app.run(debug=True, host='192.168.0.131', port=25565)


# ----------------------------------------------------------------- -----------------------------------------------------------------

# Проверка запуска
if __name__ == "__main__": main()

# ----------------------------------------------------------------- -----------------------------------------------------------------