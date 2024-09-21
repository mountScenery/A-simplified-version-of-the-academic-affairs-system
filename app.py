from sqlalchemy import create_engine
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column,Integer,String
from sqlalchemy.sql.elements import and_
from sqlalchemy import and_
from sqlalchemy.orm import sessionmaker

#app=Flask(__name__)
#创建一个对象，设置名为db
#class Config:
    #SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:root@127.0.0.1:3306/xscj"
   # SQLALCHEMY_TRACK_MODIFICATIONS = True
# mysql://账号：密码@数据库ip地址：端口号/数据库名
#app.config['SQLALCHEMY_DATABASE_URI'] ="mysql+pymysql://root:root@127.0.0.1:3306/xscj"
# 连接数据库
#app.config.from_object(Config)
# 关闭数据库修改跟踪操作[提高性能]，可以设置为True，这样可以跟踪操作：
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 开启输出底层执行的sql语句
#app.config['SQLALCHEMY_ECHO'] = True

# 开启数据库的自动提交功能[一般不使用]
#app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app=Flask(__name__,static_url_path="")
app.config['SECRET_KEY']='ABCDE'
app.config['SQLALCHEMY_DATABASE_URI'] ="mysql+pymysql://root:root@127.0.0.1:3306/xscj?charset=utf8mb4"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)

class Consumer(db.Model): #创建模型
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128))
    password = db.Column(db.String(128), nullable=False)
    def __init__(self,username, password):
        self.username = username
        self.password = password
        print(username)
        print(password)
    def __repr__(self):
        return '<User {}>'.format(self.username)
    def save(self):#添加用户
        db.session.add(self)
        db.session.commit()
        db.session.close()

    def getdata(self):
        sql='select * from xs'
        self.cursor.excute(sql)
        result=self.cursor.fetchall()
        return result




# 创建表
with app.app_context():
    db.create_all()
    # 插入数据
    #user = Consumer(username='小詹', password='888')
    #user.save()

@app.route("/page",methods=['GET','POST'])
def student_list():
    """
    显示班级列表
    """
    if request.method == 'GET':
        # 查询第几页的数据
        page = int(request.args.get('page',1))
        # 每页的条数是多少,默认为5条
        page_num = int(request.args.get('page_num',10))
        # 查询当前第几个的多少条数据
        paginate = xs.query.order_by('id').paginate(page,page_num)
        # 获取某也的具体数据
        grades = paginate.items
        # 返回获取到的班级信息给前端页面
        return render_template('studentScore.html', grades=grades,paginate=paginate)

#添加学生数据
@app.route("/add",methods=['GET','POST'])
def add_stu():
    """添加学生"""
    #if request.method == 'GET':
     #   grades = xs.query.all()
     #   return render_template('studentScore.html', grades=grades)
    if request.method == 'POST':
        add_name = request.form.get('name')
        add_id = request.form.get('id')
        add_specilized = request.form.get('specilized')
        add_gender = request.form.get('gender')
        add_birth = request.form.get('birth')
        add_courge = request.form.get('courge')
        add_remark = request.form.get('remark')
        stu = xs.query.filter(xs.name == add_name).first()
        if stu:
            msg = '* 学习姓名不能重复'
            grades = xs.query.all()
            return render_template('addstu.html', grades=grades, msg=msg)
        stu = xs(add_name=add_name, add_id=add_id,add_specilized=add_specilized,add_gender=add_gender,add_remark=add_remark,add_birth=add_birth,add_courge=add_courge)
        stu.save()
        return redirect(url_for('student_list'))


#登入页面
@app.route("/",methods=['GET','POST'])
def enter():
    return render_template("login.html")

#点击注册跳转页面
@app.route("/en",methods=["GET","POST"])
def en():
    return render_template("registry.html")

#用户登入
@app.route("/in",methods=['GET','POST'])
def getHtml():
    print(request.form)
    username=request.form.get("username")
    password = request.form.get("password")
    print(username)
    print(password)
    if username:
        user_list=db.session.query(Consumer.username).all()
        print(user_list)
        user_exists=db.session.query(Consumer.password).filter(Consumer.username==username).first()
        if user_exists:
            print(username)
            pass_one=db.session.query(Consumer.password).filter(Consumer.username==username).first()
            if password in pass_one:
                return render_template("mainInterface.html")
            else:
                return "密码输入错误"
        else:
            return "账号错误"



#注册用户
@app.route("/enroll",methods=["GET","POST"])
def logon():
    print(request.form)
    en_username=request.form.get("enrollusername")
    en_password=request.form.get("enrollpassword")
    en_pwd1=request.form.get("enrollpwd1")
    if en_password == en_pwd1:
        with app.app_context():
            # 插入数据
            con = Consumer(username=en_username, password=en_password)
            con.save()
            db.session.add(con)
            db.session.commit()
            db.session.close()
            return "注册成功！"
    else:
        return "请重新输入"


@app.route("/mess",methods=['GET',"POST"])
def login():#浏览器中传入参数
    username=request.form.get("username")
    password=request.form.get('password')
    user=Consumer(username=username,password=password)
    db.session.add(user)
    db.session.commit()
    return render_template("stu.html",username=username,password=password)

#点击跳转修改密码页面
@app.route("/rePassword.html",methods=["GET","POST"])
def re():
    return render_template("rePassword.html")

#点击跳转个人信息页面
@app.route("/selfMessage.html",methods=["GET","POST"])
def sel():
    return render_template("selfMessage.html")

#点击跳转课程页面
@app.route("/courge.html",methods=["GET","POST"])
def cour():
    return render_template("courge.html")

#点击跳转学生成绩页面
@app.route("/studentScore.html",methods=["GET","POST"])
def xscj():
    return render_template("studentScore.html")


#修改密码
@app.route("/revise",methods=['GET',"POST"])
def alter():
    password=request.form.get("repassword")
    pwd=request.form.get("repwd")
    if password==pwd:
        return "修改成功"
        with app.app_context():
            results = request.form
            db.updatadata(results)
            db.session.commit()
            db.session.close()
            return render_template("login.html",results=results)
    else:
        return "两次密码不同"

if __name__ == '__main__':
    app.run(debug=True)
