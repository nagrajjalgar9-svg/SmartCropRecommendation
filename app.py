from flask import Flask, render_template, request
import joblib

app = Flask(__name__)

# Load ML Model
model = joblib.load("crop_model.pkl")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/prediction", methods=["GET", "POST"])
def prediction_page():

    prediction = None
    crop_image = None
    crop_details = {}

    if request.method == "POST":

        N = float(request.form["Nitrogen"])
        P = float(request.form["Phosphorus"])
        K = float(request.form["Potassium"])
        temp = float(request.form["Temperature"])
        humidity = float(request.form["Humidity"])
        ph = float(request.form["Ph"])
        rainfall = float(request.form["Rainfall"])

        result = model.predict([[N, P, K, temp, humidity, ph, rainfall]])
        prediction = result[0].lower()

        crop_info = {
            "rice": {
                "season": "Kharif",
                "water": "High",
                "soil": "Clayey Soil",
                "description": "Rice is a major food crop."
            },
            "wheat": {
                "season": "Rabi",
                "water": "Medium",
                "soil": "Loamy Soil",
                "description": "Wheat is an important cereal crop."
            },
            "maize": {
                "season": "Kharif",
                "water": "Medium",
                "soil": "Well-drained Soil",
                "description": "Maize is widely cultivated."
            },
            "coffee": {
                "season": "Perennial",
                "water": "Medium",
                "soil": "Rich Organic Soil",
                "description": "Coffee is a commercial crop."
            }
        }

        crop_details = crop_info.get(prediction, {})

        crop_images = {
            "rice": "rice.jpg",
            "wheat": "wheat.jpg",
            "maize": "maize.jpg",
            "coffee": "coffee.jpg"
        }

        crop_image = crop_images.get(prediction, "default.jpg")

    return render_template(
        "prediction.html",
        prediction=prediction,
        crop_image=crop_image,
        crop_details=crop_details
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        mobile = request.form["mobile"]
        password = request.form["password"]
        print("Mobile:", mobile)
        print("Password:", password)

        try:
            with open("users.txt", "r") as f:
                users = f.readlines()

            for user in users:
                saved_mobile, saved_password = user.strip().split(",")

                if mobile == saved_mobile and password == saved_password:
                    return render_template(
                        "index.html",
                        username=mobile
                    )

        except FileNotFoundError:
            pass

        return render_template(
            "login.html",
            error="Incorrect Mobile Number or Password"
        )

    return render_template("login.html")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        mobile = request.form["mobile"].strip()
        password = request.form["password"].strip()

        import os
        print("Writing to:", os.path.abspath("users.txt"))

        with open("users.txt", "a", encoding="utf-8") as f:
            f.write(f"{mobile},{password}\n")

        print("Saved successfully!")

        return render_template("login.html")

    return render_template("register.html")


if __name__ == "__main__":
    app.run(debug=True)