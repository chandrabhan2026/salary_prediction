from flask import Flask, render_template, request, redirect, url_for, session
import pickle
import numpy as np

app = Flask(__name__)
app.secret_key = "salary_project_secret"

# Load model & encoders
model = pickle.load(open("models/salary_model.pkl", "rb"))
gender_encoder = pickle.load(open("models/gender_encoder.pkl", "rb"))
edu_encoder = pickle.load(open("models/edu_encoder.pkl", "rb"))
job_encoder = pickle.load(open("models/job_encoder.pkl", "rb"))

# ---------------- HOME ---------------- #
@app.route("/")
def home():
    return render_template("login.html")

# ---------------- LOGIN ---------------- #
@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    session["user"] = username
    return redirect(url_for("dashboard"))

# ---------------- DASHBOARD ---------------- #
@app.route("/dashboard")
def dashboard():
    if "user" in session:
        return render_template("dashboard.html")
    return redirect(url_for("home"))

# ---------------- PREDICT PAGE ---------------- #
@app.route("/predict_page")
def predict_page():
    if "user" in session:
        return render_template("predict.html",
                               genders=gender_encoder.classes_,
                               educations=edu_encoder.classes_,
                               jobs=job_encoder.classes_)
    return redirect(url_for("home"))

# ---------------- PREDICT ---------------- #
@app.route("/predict", methods=["POST"])
def predict():
    if "user" not in session:
        return redirect(url_for("home"))

    age = int(request.form["age"])
    gender = request.form["gender"]
    education = request.form["education"]
    job = request.form["job"]
    experience = float(request.form["experience"])

    gender = gender_encoder.transform([gender])[0]
    education = edu_encoder.transform([education])[0]
    job = job_encoder.transform([job])[0]

    input_data = np.array([[age, gender, education, job, experience]])

    prediction = round(model.predict(input_data)[0], 2)

    return render_template("predict.html",
                           prediction=prediction,
                           genders=gender_encoder.classes_,
                           educations=edu_encoder.classes_,
                           jobs=job_encoder.classes_)

# ---------------- ANALYTICS ---------------- #
@app.route("/analytics")
def analytics():
    if "user" in session:
        importance = pickle.load(open("models/feature_importance.pkl", "rb"))
        return render_template("analytics.html", importance=importance)
    return redirect(url_for("home"))

# ---------------- LOGOUT ---------------- #
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("home"))

# ---------------- RUN ---------------- #
if __name__ == "__main__":
    app.run(debug=True)