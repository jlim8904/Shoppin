import os
from flask import Flask, redirect, request, render_template, url_for, session
from flask_bcrypt import Bcrypt
from datetime import datetime
import MySQLdb
from flask_socketio import SocketIO
import random, time, datetime

app = Flask(__name__) 
app.config['SECRET_KEY'] = os.urandom(24)
bcrypt = Bcrypt()

# socketio = SocketIO(app)  # 加上這行

conn = MySQLdb.connect(host="127.0.0.1",user="root", passwd='',db="shoppin")
cursor = conn.cursor()

userid = None

@app.route('/')
def start(): 
    return redirect(url_for('home'))

#首頁
@app.route('/home',methods=['GET','POST'])
def home(): 
    query = "Select * from products where ProductType = 'Books';"
    cursor.execute(query)
    books = cursor.fetchall()
    userid = session.get('userid')
    if userid == None:
        return render_template("Home.html",books=books,guest='guest')
    return render_template("Home.html",books=books)

#登入頁面
@app.route('/login',methods=['GET','POST'])
def login():
    if session.get('userid') and session.get('password'):
        userid = session.get('userid')
        query = "Select UserName From Users Where UserName = '{}';".format(userid)
        cursor.execute(query)
        userid_check = cursor.fetchone()
        if userid_check == None:
            return render_template('ErrorMessage.html',status=(("賬號輸入錯誤!","login","重新登入"),))
        query = "Select UserPassword From Users Where UserName = '{}';".format(userid)
        cursor.execute(query)
        password_check = cursor.fetchone()
        if not bcrypt.check_password_hash(session.get('password'),password_check[0]):
            session['password'] = None
            return render_template('ErrorMessage.html',status=(("請重新登入!","login","重新登入"),))
        return redirect(url_for('home'))
    session['userid'] = None
    session['password'] = None
    return render_template("Login.html")

#檢查登入
@app.route('/login_check',methods=['GET','POST'])
def login_check():
    global userid
    if not session.get('userid'):
        #檢查學號
        session['userid']=request.form.get('userid')
        userid = session.get('userid')
        if userid == '':
            return render_template('ErrorMessage.html',status=(("請輸入帳號!","login","重新登入"),))
        elif userid == None:
            return redirect(url_for('login'))
        
        query = "Select UserName From Users Where UserName = '{}';".format(userid)
        cursor.execute(query)
        userid_check = cursor.fetchone()
        if userid_check == None:
            return render_template('ErrorMessage.html',status=(("帳號輸入錯誤!","login","重新登入"),))
        
        #檢查密碼
        password=request.form.get('password')
        if password == '':
            return render_template('ErrorMessage.html',status=(("請輸入密碼!","login","重新登入"),))
        elif password == None:
            return redirect(url_for('login'))
        #密碼加密
        password = bcrypt.generate_password_hash(password=password)
        session['password']=password
        query = "Select UserPassword From Users Where UserName = '{}';".format(userid)
        cursor.execute(query)
        password_check = cursor.fetchone()
        if not bcrypt.check_password_hash(session.get('password'),password_check[0]):
            session['password'] = None
            return render_template('ErrorMessage.html',status=(("密碼錯誤!","login","重新登入"),))
        session.permanent=True
    
    return redirect(url_for('home'))

#登出頁面
@app.route('/logout')
def logout(): 
    global userid
    userid = None
    session['userid'] = None
    session['password'] = None
    return redirect(url_for('login'))

#搜尋
@app.route('/search',methods=['POST'])
def search_result():
    keyword = request.form.get('keyword')
    
    query = "Select * from products where ProductName like '%{}%'".format(keyword)
    cursor.execute(query)
    products = cursor.fetchall()
    userid = session.get('userid')
    if userid == None:
        return render_template("SearchResult.html",products=products,keyword=keyword,guest='guest')
    return render_template("SearchResult.html",products=products,keyword=keyword)

# 個別商品資訊頁面
@app.route('/productDetail',methods=['POST', 'GET'])
def product_detail():
    id = request.form.get('productid')
    userid = session.get('userid')
    if id == None:
        if userid == None:
            return render_template("Product.html",product=[['dvd-cover-mockup-template','CD Name','CD Shop','CD','CD Description',300,9999]],guest='guest')
        return render_template("Product.html",product=[['dvd-cover-mockup-template','CD Name','CD Shop','CD','CD Description',300,9999]])
    query = "Select * from products where ProductID = '{}'".format(id)
    cursor.execute(query)
    product = cursor.fetchall()
    if userid == None:
        return render_template("Product.html",product=product,guest='guest')
    return render_template("Product.html",product=product)

#書籍
@app.route('/books')
def book():
    query = "Select * from products where ProductType = 'Books';"
    cursor.execute(query)
    books = cursor.fetchall()
    userid = session.get('userid')
    if userid == None:
        return render_template("Books.html",books=books,guest='guest')
    return render_template("Books.html",books=books)

#CD
@app.route('/cd')
def cd(): 
    userid = session.get('userid')
    if userid == None:
        return render_template("CD.html",guest='guest')
    return render_template("CD.html")

#購物車
@app.route('/cart',methods=['POST', 'GET'])
def cart(): 
    userid = session.get('userid')
    if userid == None:
        return render_template('ErrorMessage.html',status=(("請先登入","login","登入"),))
    else:
        query = "Select UserName from Users where UserName = '{}';".format(userid)
        cursor.execute(query)
        name = cursor.fetchone()
        if request.method == "POST":
            if request.form.get("productAmount") != None:
                productAmount = request.form.get("productAmount")
                productId = request.form.get("productid")
                print("get amount")
                addProduct = "INSERT INTO cartitems(ProductID, TimeAdded, BuyerName, Quantity) VALUE('{}','{}', '{}', '{}')".format(productId, datetime.datetime.today(), name[0], productAmount)
                cursor.execute(addProduct)
                conn.commit()
            elif request.form.get('delete') != None:
                print("delete")
                deleteId = request.form.get('delete')
                query = "delete FROM cartitems where cartitems.ProductID = '{}';".format(deleteId)
                cursor.execute(query)
                conn.commit()
                return redirect(url_for('cart'))
            elif request.form.get('buy') != None:
                query = "SELECT ProductID, Quantity FROM cartitems WHERE BuyerName = '{}'".format(userid)
                cursor.execute(query)
                findProduct = cursor.fetchall()
                print(findProduct)

                time = datetime.datetime.today()
                for i in findProduct:
                    addProduct = "INSERT INTO orders(ProductID, OrderDate, BuyerName, Quantity, SellerName) VALUE('{}','{}', '{}', '{}', '{}')".format(i[0], datetime.datetime.today(), name[0], i[1], name[0])
                    cursor.execute(addProduct)
                    deleteProduct = "delete FROM cartitems where cartitems.ProductID = '{}';".format(i[0])
                    cursor.execute(deleteProduct)
                    conn.commit()
                    
                print("save")
                return redirect(url_for('cart'))
            return redirect(url_for('cart'))
        elif request.method == "GET":
            query =   "SELECT cartitems.ProductID, products.ProductName, Price, Quantity  FROM cartitems LEFT JOIN products on cartitems.ProductID = products.ProductID WHERE cartitems.BuyerName = '{}'".format(name[0])
            cursor.execute(query)
            products = cursor.fetchall()
    return render_template("Cart.html", products=products)
    # return render_template("Cart.html")/

#賬號
@app.route('/profile')
def profile():
    userid = session.get('userid')
    if userid == None:
        return render_template('ErrorMessage.html',status=(("請先登入","login","登入"),))
    query = "Select UserName,Email,Phone from Users where UserName = '{}';".format(userid)
    cursor.execute(query)
    userdetail = cursor.fetchone()
    
    return render_template("Profile.html",name=userdetail[0],mail=userdetail[1],phone=userdetail[2])

#訂單管理
@app.route('/order_management')
def order_management(): 
    userid = session.get('userid')
    if userid == None:
        return render_template('ErrorMessage.html',status=(("請先登入","login","登入"),))
    return render_template("OrderManagement.html")

# @socketio.on('send')
# def chat(data):
#     socketio.emit('get', data)


# @socketio.on('test')
# def test():
#     socketio.send("test")

@app.route('/work')
def work():
    return render_template("work.html", guest='guest')

@app.route('/applyAccount')
def applyAccount():
    return render_template("applyAccount.html")

@app.route('/ForgetPassword',methods=['GET','POST'])
def forget_password():
    if request.method == 'GET':
        return render_template("Forgetpassword.html")
    elif request.method== 'POST':
        if request.form.get('password'):
            password = request.form.get('password')
            repassword = request.form.get('repassword')
            mail = request.form.get('mail')
            if password != repassword:
                return render_template('ErrorMessage.html',status=(("密碼輸入錯誤!","ForgetPassword","重新輸入"),))
            query = "update users set UserPassword = '{}' where Email = '{}'".format(password,mail)
            cursor.execute(query)
            conn.commit()
            return render_template('ErrorMessage.html',status=(("密碼設定成功!","login","登入"),))
        else:
            mail = request.form.get('mail')
            query = "select Username,Email from Users Where Email ='{}'".format(mail)
            cursor.execute(query)
            userdetail = cursor.fetchone()
            if userdetail:
                return render_template("Forgetpassword.html",name=userdetail[0],mail=userdetail[1])
            else:
                return render_template('ErrorMessage.html',status=(("郵箱輸入錯誤!","ForgetPassword","重新輸入"),))

@app.route('/register',methods=['GET','POST'])
def register():
    global userid
    if not session.get('userid'):
        session['userid']=request.form.get('userid')
        userid = session.get('userid')
        if userid == '':
            return render_template('ErrorMessage.html',status=(("請輸入賬號!","applyAccount","重新註冊"),))
        elif userid == None:
            return redirect(url_for('applyAccount.html'))

        password = request.form.get('password')
        if password == '':
            return render_template('ErrorMessage.html',status=(("密碼輸入錯誤!","applyAccount","重新註冊"),))
        elif password == None:
            return redirect(url_for('applyAccount.html'))

        email = request.form.get('email')
        if email == '':
            return render_template('ErrorMessage.html',status=(("信箱輸入錯誤!","applyAccount","重新註冊"),))
        elif email == None:
            return redirect(url_for('applyAccount.html'))

        phone = request.form.get('phone')
        if phone == '':
            return render_template('ErrorMessage.html',status=(("電話輸入錯誤!","applyAccount","重新註冊"),))
        elif phone == None:
            return redirect(url_for('applyAccount.html'))

        register = f"""insert into Users values(\'{userid}\',\'{password}\',\'{email}\',\'{phone}\',1)"""
        cursor.execute(register)
        conn.commit()
    
    return redirect(url_for('login'))

@app.route('/Chatroom')
def Chatroom():
    return render_template("Chatroom.html", guest='guest')

if __name__ == "__main__":
    # socketio.run(app)
    app.run(debug=True)