from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask import current_app as current_app
from random import *

from app.module import dbModule

main = Blueprint('main', __name__, url_prefix='/')

@app.route('/board_qna', methods=['GET'])
def board_qna():
    selet_results = {}

    sql = "SELECT * \
                FROM team02.qna \
                    WHERE deleteflag = 0"

    db = conn.cursor()
    selet_results = db.executeAll(sql)
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


@app.route('/', methods=['GET'])
def index():
    return render_template('/board_free.html')

# INSERT 함수 예제
@app.route('/insert', methods=['GET'])
def insert():
    db_class = dbModule.Database()

    sql = "INSERT INTO board_qna (board_id, user_name, title, content, created, deleteflag, hit, lock_password, attach) \
                VALUE(%d, '%s', '%s', '%s', now(), %d, %d, '%s' ,'%s')" % (12345, '테스터', '제목입니다', '내용아입니다', 0, 1, '' ,'')
    db_class.execute(sql)
    db_class.commit()

    return render_template('/main/index.html',
                           result='insert is done!',
                           resultData=None,
                           resultUPDATE=None)


# SELECT 함수 예제
@app.route('/select', methods=['GET'])
def select():
    db_class = dbModule.Database()

    sql = "SELECT * \
                FROM team02.board_qna"
    row = db_class.executeAll(sql)

    return render_template('/main/index.html',
                           result=None,
                           resultDatas=row, # 해당 지점에서 전송
                           resultUPDATE=None)


# UPDATE 함수 예제
@app.route('/update', methods=['GET'])
def update():
    db_class = dbModule.Database()

    sql = "UPDATE testDB.testTable \
                SET test='%s' \
                WHERE test='testData'" % ('update_Data')
    db_class.execute(sql)
    db_class.commit()

    sql = "SELECT idx, test \
                FROM testDB.testTable"
    row = db_class.executeAll(sql)

    return render_template('/main/index.html',
                           result=None,
                           resultData=None,
                           resultUPDATE=row[0])
