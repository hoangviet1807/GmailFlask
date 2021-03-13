from flask import Flask, render_template, request
from flask_mail import Message, Mail
import random


app = Flask(__name__,template_folder='template')

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "hoangviet1807@gmail.com"
app.config['MAIL_PASSWORD'] = "hoangviet01"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)


@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/send_message', methods=['POST','GET'])
def send_message():
    if request.method == 'POST':
        email = request.form['email']
        subject = request.form['subject']
        msg = request.form['message']
        n = random.random()
        message = Message(subject, sender="hoangviet1807@gmail.com", recipients=[email])

        message.body = n

        mail.send(message)

        success = "Mess sended"

        return render_template("result.html", success = success)

if __name__ == '__main__':
    app.run(debug=True)
