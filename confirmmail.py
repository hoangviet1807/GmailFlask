from flask import Flask, request, url_for, render_template
from flask_mail import Mail,Message
from itsdangerous import URLSafeTimedSerializer, SignatureExpired

app = Flask(__name__, template_folder='template')
app.config.from_pyfile('config.cfg')

mail = Mail(app)

s = URLSafeTimedSerializer('thisisascrect!')

@app.route('/',methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return '<form action="/" method="POST"> <input name = "email" type="email"> <input type="submit"></form>'

    email = request.form['email']
    token = s.dumps(email, salt ='email-confirm')

    msg = Message('Confirm email', sender="hoangviet1807@gmail.com", recipients=[email])

    link = url_for('confirm_email', token = token, _external = True)

    msg.body = 'your link is {}'.format(link)

    mail.send(msg)

    return '<h1>The email you entered is {}. The token is {}</h1>'.format(email, token)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
         email = s.loads(token, salt='email-confirm', max_age=36000)
    except SignatureExpired:
        return '<h1> The token is expired </h1>' 
    return render_template("home.html", email = email)

if __name__ == '__main__':
    app.run(debug = True)
