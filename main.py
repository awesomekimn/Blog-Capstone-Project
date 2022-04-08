from flask import Flask, render_template, request
import requests
import smtplib

my_email = MY_EMAIL
password = MY_PASSWORD

posts = requests.get("https://api.npoint.io/2b75de17c055f76690b5").json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template('index.html', all_posts=posts)


@app.route('/post/<int:index>')
def post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template('post.html', post=requested_post)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == 'POST':
        data = request.form
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template('contact.html', msg_sent=True)
    return render_template('contact.html', msg_sent=False)


def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMassage: {message}"
    with smtplib.SMTP("smtp.mail.yahoo.com") as connection:
        connection.starttls()
        connection.login(my_email, password)
        connection.sendmail(my_email, my_email, email_message)


if __name__ == "__main__":
    app.run(debug=True)
