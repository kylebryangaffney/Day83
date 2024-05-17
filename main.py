from datetime import datetime
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap5
import smtplib
import requests
import os


app = Flask(__name__)
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
        name = contact_data["name"]
        email = contact_data["email"]
        message = contact_data["message"]
        full_message = f"{name}\n{email}\n{message}"

        send_gmail = os.environ.get('MAIL_APP_ADDRESS')
        gmail_password = os.environ.get('MAIL_APP_PW')
        receive_email = os.environ.get("MAIL_REC_ADDRESS")

        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=send_gmail, password=gmail_password)
            connection.sendmail(
                from_addr=send_gmail, 
                to_addrs=receive_email,
                msg=f"Subject: New Message\n\n{full_message}"
                )
        return render_template("contact.html", msg_sent=True, year=cur_year)
    return render_template("contact.html", msg_sent=False, year=cur_year)




if __name__ == "__main__":
    app.run()