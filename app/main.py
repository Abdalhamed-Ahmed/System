import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
    basedir, "database.db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
func.localtimestamp


class paper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fileName = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=True)
    outgoingNum = db.Column(db.String(80))
    date = db.Column(db.DateTime(timezone=True), server_default=func.now())
    # date = db.Column(db.Time(100), server_default=func.localtime())
    incomingNum = db.Column(db.String(80))
    senderName = db.Column(db.String(80))
    subject = db.Column(db.Text, nullable=False)
    receiver = db.Column(db.String(80))
    archiveNumber = db.Column(db.String(80), nullable=True)

    def __repr__(self):
        return f"<مكاتبة {self.fileName}>"


categories = [
    "مباحث",
    "جهات",
    "قطاع الشمال",
    "قطاع الجنوب",
    "قطاع شرق",
    "قطاع غرب",
    "قطاع القاهرة الجديدة",
    "قطاع العاصمة الادارية",
    "قطاع المجلس القومي",
]
fileNames = [
    "حقوق الانسان",
    "مدة ميعاد",
    "اعمال لجان",
    "مباحث داخلى",
    "قطاع الاعلام والعلاقات",
]


@app.route("/", methods=("GET",))
def home():
    params_fileName = request.args.get("fileName")
    params_archiveNumber = request.args.get("archiveNumber")
    papers = []
    if params_fileName or params_archiveNumber:
        if params_fileName:
            papers = paper.query.filter_by(fileName=params_fileName)
        if params_archiveNumber:
            if params_archiveNumber == "on":
                papers = paper.query.filter(paper.archiveNumber != "")
                print("مطلوب غير")
            else:
                papers = paper.query.filter(paper.archiveNumber == "")
                print("مطلوب ")

        print(params_archiveNumber)
    else:
        papers = paper.query.all()

    return render_template(
        "index.html", papers=papers, categories=categories, fileNames=fileNames
    )


@app.route("/create/", methods=("GET", "POST"))
def create_paper():
    if request.method == "POST":
        # Retrieve form data
        # file = request.files["file"]
        fileName = request.form["fileName"]
        category = request.form["category"]
        outgoingNum = request.form["outgoingNum"]
        senderName = request.form["senderName"]
        incomingNum = request.form["incomingNum"]
        subject = request.form["subject"]
        receiver = request.form["receiver"]
        archiveNumber = request.form["archiveNumber"]

        # Save the uploaded file
        # file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))

        # Create a new paper object
        new_paper = paper(
            fileName=fileName,
            category=category,
            outgoingNum=outgoingNum,
            senderName=senderName,
            incomingNum=incomingNum,
            subject=subject,
            receiver=receiver,
            archiveNumber=archiveNumber,
        )

        # Add the paper object to the database
        db.session.add(new_paper)
        db.session.commit()

        return redirect(url_for("home"))
    return render_template("create.html", categories=categories, fileNames=fileNames)


if __name__ == "__main__":
    app.run(debug=True)
