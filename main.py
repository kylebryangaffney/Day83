from datetime import datetime
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_bootstrap import Bootstrap5
import smtplib
import os

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
bootstrap = Bootstrap5(app)

@app.route('/')
def home():
    cur_year = datetime.now().year
    return render_template("index.html", year=cur_year)

@app.route('/about')
def about():
    cur_year = datetime.now().year
    return render_template("about.html", year=cur_year)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    cur_year = datetime.now().year

    if request.method == 'POST':
        contact_data = request.form
        name = contact_data.get("name")
        email = contact_data.get("email")
        message = contact_data.get("message")

        if name and email and message:
            full_message = f"{name}\n{email}\n{message}"
            send_mail(full_message)
            return render_template("contact.html", msg_sent=True, year=cur_year)
        else:
            flash("Missing information. Please fill out each field.")
            return redirect(url_for('contact'))
    return render_template("contact.html", msg_sent=False, year=cur_year)

def send_mail(full_message):
    send_gmail = os.getenv('MAIL_APP_ADDRESS')
    gmail_password = os.getenv('MAIL_APP_PW')
    receive_email = os.getenv("MAIL_REC_ADDRESS")

    with smtplib.SMTP("smtp.gmail.com", 587) as connection:
        connection.starttls()
        connection.login(user=send_gmail, password=gmail_password)
        connection.sendmail(
            from_addr=send_gmail, 
            to_addrs=receive_email,
            msg=f"Subject: New Message From Site\n\n{full_message}"
        )
    return 'Email sent'

if __name__ == '__main__':
    app.run(debug=True)
