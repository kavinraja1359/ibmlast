import ibm_db
from flask import Flask, render_template, redirect, url_for, request

app = Flask(__name__)
conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=31321;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=mbs42408;PWD=hMYQwnOc2bfI674f",'','')
@app.route('/', methods=['GET', 'POST'])
def register():
    error=None
    if request.method == 'POST':
        error=None
        check=False
        cheex=False
        uname=request.form['name']
        passw=request.form['password']
        r_no=request.form['r_no']
        email=request.form['email']
        print(uname+'   '+passw+'  '+r_no+'  '+email)
        if (len(uname)>0 and len(passw)>0 and len(r_no)>0 and len(email)>0):
            check=True
            sql1=ibm_db.prepare(conn,'select * from user where username=\''+uname+'\' or email=\''+email+'\' or roll_number=\''+r_no+'\';')
            sql2=ibm_db.prepare(conn,'INSERT INTO user(email, username, roll_number, password) VALUES (\''+email+'\', \''+uname+'\','+r_no+', \''+passw+'\');')
            ibm_db.execute(sql1)
            s=ibm_db.fetch_assoc(sql1)
            ds={}
            if (not isinstance(s,dict)):
                cheex=True
                print(ibm_db.execute(sql2))

        if check and cheex:
            error=error
            return redirect(url_for('login'))
        else:
            if not check:
                error = 'ENTER ALL DATA.'
            elif not cheex:
                error = 'DATA ALREADY exist.'
            else:
                error = 'TRY AFTER SOME TIME'
    return render_template('index.html', error=error)



@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    print("ffqqqqqqqqqqf")
    if request.method == 'POST':

        sql1=ibm_db.prepare(conn,'select * from user;')
        ibm_db.execute(sql1)
        s=ibm_db.fetch_both(sql1)
        username=request.form['username']
        password=request.form['password']
        check=False
        while s!=False:

            if( (s['EMAIL']==username or s['USERNAME']==username) and s['PASSWORD']==password):
                check=True
                error='WELCOME '+s['USERNAME']+' you are LOGINED'
                break
            s=ibm_db.fetch_both(sql1)


        if check:
            error=error

            return render_template('welcome.html',error=error)
        else:
            error = 'Invalid Credentials. Please try again.'

    return render_template('login.html', error=error)
if __name__ == "__main__":
    app.run(debug=True)
