from flask import Flask, request, render_template, redirect, url_for, abort, session,Blueprint, flash
import bcrypt
import pymysql
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
import socket
import smtplib
import random
from email.mime.text import MIMEText
from flask import current_app as current_app


app = Flask(__name__)
app.config['MYSQL_HOST'] = 'school.mingky.me'
app.config['MYSQL_USER'] = 'team02'
app.config['MYSQL_PASSWORD'] = 'KIT'
app.config['MYSQL_DB'] = 'team02'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'




conn = pymysql.connect(host = 'school.mingky.me', user='team02', password='KIT', db = 'team02', charset='utf8')



@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template("index.html")
    else:
        return render_template("index.html")


@app.route('/board_duo')
def board_duo():
    name2 = select_user3(session['user'])
    name = select_user2(session['user'])
    print(name[0])
    return render_template("duo.html", data=name, data2=name2) #data2=name2)

@app.route('/duo', methods=['GET','POST'])
def duo():
    if request.method == 'GET':
        return render_template('matching.html')
    else:
        connectedUser = select_user2(session['user'])
        title = request.form['title']
        #line = request.form.get('matching_line_select1')
        #teer = request.form['matching_line_select2']
        #gender = request.form['matching_line_select3']
        #mic = request.form['matching_line_select4']
        content = request.form['content']
        email = connectedUser[0] # 멤버에서 가져오기
        user_name = connectedUser[1] # 멤버에서 가져오기
        

        #sql = "INSERT INTO qna (title, content, line, teer, gender, mic, created) \
                #VALUE('%s', '%s', '%s', '%s', '%s', '%s', now())" % (title, content, line, teer, gender, mic)
        sql = "INSERT INTO duo (title, content, user_name, email) \
                VALUE('%s', '%s', '%s', '%s')" % (title, content, user_name, email)

       

       #sql="INSERT INTO duo (title, content, line, created, teer, gender, mic) VALUE(%s, %s, %s, now(), %s, %s,%s)",(title,content,line,teer,gender,mic)

       # sql = "INSERT INTO qna (user_name, title, content, created, deleteflag, hit, email) \
               # VALUE('%s', '%s', '%s', now(), %d, %d, '%s')" % (user_name, title, content, deleteflag, hit, email)
        db = conn.cursor()
        db.execute(sql)
        conn.commit()
        db.close()
        
        

        return redirect(url_for('board_duo'))

@app.route('/dema')
def dema():
    return render_template("index2.html")

@app.route('/pro', methods=['GET','POST'])
def pro():
    
    if request.method == 'GET':
        return render_template("profile2.html")
    else:
        teer = request.form['teer']
        line = request.form['line']
        gender = request.form['gender']
        mic = request.form['mic']
        ptime = request.form['ptime']
        pnickname = request.form['pnickname']

        sql= """UPDATE usertbl SET teer='%s', line='%s',gender= '%s',mic= '%s', ptime= '%s', pnickname= '%s'
         WHERE email='%s' """ % (teer,line,gender,mic,ptime,pnickname,session['user'])
          



        db = conn.cursor()
        print(session['user'])
        db.execute(sql)
        conn.commit()
        db.close()
        return render_template("index.html")
            
            


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password'].encode('utf-8')
    
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM usertbl WHERE email = '"+email+"'")

        user = cursor.fetchone()

        if user != None:
            session['user'] = email
            return render_template("index.html")
        else:
            return render_template("Login.html")
    else:
        return render_template("Login.html")

@app.route('/logout')
def logout():
    session.pop('user', None)
    return render_template("index.html")

@app.route('/fin')
def fin():
     return render_template('finPassword.html')

@app.route('/cer', methods=["GET", "POST"])
def cer():
    ret = ()
    if request.method == 'GET':
        return render_template('Certification.html')
    else:
        cer = request.form['cernum']
        
        db = conn.cursor()
        db.execute("SELECT cer_num FROM usertbl WHERE cer_num = %s",(int(cer)))
        
        conn.commit()
        ret = db.fetchone()
        db.close()
        if len(ret) is 1:    
            return '''
            <script>
                alert("회원가입 완료 되었습니다.")
                location.href="/login"
            </script>
          ''' 
        else:
            return render_template("Certification.html")
        

@app.route('/sign', methods=["GET","POST"])
def sign():
    if request.method == 'GET':
        return render_template('Signup.html')
    else:
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        session['email'] = request.form['email']
        session['name'] = request.form['name']
        session['password'] = request.form['password']
        
        
        num = random_num()
        contents = "Certification Number is :{}".format(num)
        message = MIMEText(contents, _charset='euc-kr')
        message['Subject'] = "Demacia 인증번호"
        message['From'] = 'evanpark333@gmail.com'
        message['To'] = email
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login("evanpark333@gmail.com", "seulhyun7070")
        server.sendmail("evanpark333@gmail.com", email, message.as_string())
        server.quit()

        db = conn.cursor()
        db.execute("INSERT INTO usertbl (email,pw,nickname,cer_num) VALUES (%s,%s,%s,%s)",(email,password,name,int(num)))
        conn.commit()
        db.close()

        return render_template("Certification.html", testdata = email)



        #token = s.dumps(email, salt='email-confirm')
        #msg = Message('Confirm Email', sender='evanpark333@gmail.com', recipients=[email])

        #link = url_for('confirm_email', token=token, _external=True)

        #msg.body = 'Your link is {}'.format(link)

        
        #mail.send(msg)

        #return '<h1> The email you entered is {}. The token is {}<h1>'.format(email, token)
      
    
        
        
main = Blueprint('main', __name__, url_prefix='/')

#@app.route('/confirm_email/<token>')
#def confirm_email(token):
    
def select_user2(id): 
    ret = () 
    setdata = (id,) 
    db = conn.cursor()
    db.execute('SELECT email,nickname,pnickname, teer, line, ptime, mic, gender FROM usertbl WHERE email = %s', (setdata)) 
        
    conn.commit()
    ret = db.fetchone()
    db.close()
    return ret

def select_user3(id): 
    ret = () 
    setdata = (id,) 
    db = conn.cursor()
    db.execute('SELECT user_name, title, content FROM duo WHERE email = %s', (setdata)) 
        
    conn.commit()
    ret = db.fetchone()
    db.close()
    return ret

@app.route('/board_qna', methods=['GET'])
def board_qna():
    if request.method == 'GET':
        return render_template("board_qna.html")
    else:
        selet_results = {}

        sql = "SELECT * \
                    FROM team02.qna \
                        WHERE deleteflag = 0"

        db = conn.cursor()
        selet_results = db.execute(sql)
        conn.commit()
        db.close()
        
        return render_template('/board_qna.html',
                            selet_results=selet_results)

@app.route('/board_qna_fwrite_page')
def board_qna_fwrite_page():
    return render_template('/board_qna_fwrite.html')

@app.route('/fwrite', methods=['GET', 'POST'])
def fwrite():
    connectedUser = select_user2(session['user'])

    email = connectedUser[0] # 멤버에서 가져오기
    user_name = connectedUser[1] # 멤버에서 가져오기
    title = request.form['title']
    content = request.form['content']
    deleteflag = 0
    hit = 0
    #lock_password = request.form['lock_password'] # 비밀번호추가
    lock_password = ""
    #attach = request.form['attach']
    attach = ""

    sql = "INSERT INTO qna (user_name, title, content, created, deleteflag, hit, email) \
                VALUE('%s', '%s', '%s', now(), %d, %d, '%s')" % (user_name, title, content, deleteflag, hit, email)
    db = conn.cursor()
    db.execute(sql)
    conn.commit()
    db.close()

    return redirect('/board_qna')

@app.route('/delete', methods=['POST'])
def delete():
    sql = "UPDATE team02.qna \
                SET deleteflag = 1 \
                WHERE `idx` = %s" % request.values.get('idx')

    db = conn.cursor()
    db.execute(sql)
    conn.commit()
    db.close()

    return '''
            <script>
                alert("삭제되었습니다")
                location.href="/board_qna"
            </script>
          ''' 










   


def random_num():

    ran_num = random.randrange(000000,999999)

    return ran_num

if __name__ == '__main__':
    app.config['SECRET_KEY'] = '1651dfdf5461af561ad321-reg561efgr6g51_fewf3651'
    app.run(debug=True)
    





