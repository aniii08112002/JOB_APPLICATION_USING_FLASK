from flask import Flask, request,flash
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime  # Import datetime module
from flask_mail import Mail,Message
app = Flask(__name__)
app.config["SECRET_KEY"] = 'GENETRATE THE KEY'  # security
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///data.db'
app.config["MAIL_USERNAME"]="anirudhloveshismotheralot@gmail.com"
app.config["MAIL_SERVER"]="smtp.gmail.com"
app.config["MAIL_PORT"]=465
app.config["MAIL_USE_SSL"]=True
app.config["MAIL_PASSWORD"]="FIND THE KEY IN GMAIL SECURITY AND PRIVECY SECTION"

db = SQLAlchemy(app)

mail=Mail(app)
class Form(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80))
    last_name = db.Column(db.String(80))
    email = db.Column(db.String(80))
    date = db.Column(db.Date)
    occupation = db.Column(db.String(80))


@app.route("/", methods=['GET', 'POST'])
def index():

    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        email = request.form["email"]
        date_str = request.form["date"]  # Get date string
        occupation = request.form["occupation"]

        # Convert date string to Python date object
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')

        form = Form(first_name=first_name, last_name=last_name,
                    email=email, date=date_obj, occupation=occupation)
        db.session.add(form)
        db.session.commit()

        message_body=f"Thank you for your submission,{first_name}."\
        f"Here are your data.{first_name}\n{last_name}\n{date_obj}\n Thank YOU"


        message=Message("NEW Job Post Application form",sender=app.config["MAIL_USERNAME"],recipients=[email],body=message_body)
        mail.send(message)
        flash(f"{first_name} Your form was submitted  successfully","success")

    return render_template("index.html")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=5006)
