from flask import Flask, render_template, request, flash, redirect
from flask_mail import Mail, Message
import re

app = Flask(__name__)
app.secret_key = 'KenStrem'
app.config['MAIL_SERVER']='smtp.office365.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'ken@fundingfastmoney.com'
app.config['MAIL_PASSWORD'] = '24Kobelakers'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/submit', methods=['POST'])
def handle_form():
    errors = False

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    phone_number = request.form['phone_number']
    email = request.form['email']
    loan_type = request.form['loan_type']
    extra = request.form['extra_info']

    print(loan_type)

    if len(first_name) == 0:
        errors = True
        flash(u'Please enter a first name.', 'error')

    if len(last_name) == 0:
        errors = True
        flash(u'Please enter a last name.', 'error')

    if (not re.match(r"^\D?(\d{3})\D?\D?(\d{3})\D?(\d{4})$", phone_number)) or len(phone_number) == 0:
        errors = True
        print("Phone Number Bad", phone_number)
        flash(u'Please enter a valid phone number.', 'error')
    else:
        phone_number = re.sub(r"[^0-9]", "", phone_number)
        print(re.sub(r"[^0-9]", "", phone_number))

    if (not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email)) or len(email) == 0:
        errors = True
        print("Email Bad")
        flash(u'Please enter a valid email.', 'error')

    print(first_name, last_name)

    if not errors:
        # Mail message

        msg = Message(
            "SYSTEM - " + first_name + " " + last_name,
            sender="ken@fundingfastmoney.com",
            recipients=["ken@fundingfastmoney.com"]
        )
        msg.body = "INFORMATION FROM SYSTEM:\nFIRST NAME: {}\nLAST NAME: {}\nPHONE NUMBER: {}\nEMAIL: {}\nLOAN TYPE: {}\nEXTRA (if any): {}".format(
            first_name,
            last_name,
            phone_number,
            email,
            loan_type,
            extra
        )

        mail.send(msg)

        flash(u'Information sent successfully.', 'success')

    return redirect('/#form_group')

app.run(debug=True)
