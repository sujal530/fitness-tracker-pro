#fitnss tracker app
#developed by sujal jadhav 


from flask import Flask, render_template, request, redirect, session
from models.db import create_tables, connect_db

app = Flask(__name__)
app.secret_key = "secret123"

# Create tables
create_tables()


# Home
@app.route("/")
def home():
    return redirect("/login")


# Register
@app.route("/register", methods=["GET", "POST"])
def register():
    if (request.method == "POST"):
        username = request.form["username"]
        password = request.form["password"]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    if (request.method == "POST"):
        username = request.form["username"]
        password = request.form["password"]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            return redirect("/dashboard")
        else:
            return "Invalid Credentials ❌"

    return render_template("login.html")


#  Dashboard
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    conn = connect_db()
    cursor = conn.cursor()

    
    cursor.execute("SELECT goal FROM users WHERE id=?", (user_id,))
    result = cursor.fetchone()
    goal = result[0] if result and result[0] else 0

    
    cursor.execute("SELECT steps FROM fitness_data WHERE user_id=? AND date=date('now')", (user_id,))
    data = cursor.fetchone()
    today_steps = data[0] if data else 0

    conn.close()

    return render_template("dashboard.html", goal=goal, today_steps=today_steps)



# Add Fitness Data
@app.route("/add", methods=["GET", "POST"])
def add_data():
    if "user_id" not in session:
        return redirect("/login")

    if (request.method == "POST"):
        steps = request.form["steps"]
        calories = request.form["calories"]
        water = request.form["water"]

        user_id = session["user_id"]

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO fitness_data (user_id, steps, calories, water, date) VALUES (?, ?, ?, ?, date('now'))",
            (user_id, steps, calories, water)
        )
        conn.commit()
        conn.close()

        return "Data Saved Successfully ✅"

    return render_template("add_data.html")
    
 
@app.route("/progress")
def progress():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fitness_data WHERE user_id=?", (user_id,))
    data = cursor.fetchall()
    conn.close()

    return render_template("progress.html", data=data) 

# Smart Mode
@app.route("/smart", methods=["GET", "POST"])
def smart():
    if "user_id" not in session:
        return redirect("/login")

    if (request.method == "POST"):
        weight = float(request.form["weight"])
        height = float(request.form["height"])
        goal_type = request.form["goal"]

        
        protein = weight * 2
        water = weight * 0.04

        if goal_type == "bulking":
            calories = weight * 30 + 500
            foods = ["Chicken", "Rice", "Eggs", "Milk", "Banana", "Peanut Butter"]
        else:
            calories = weight * 30 - 500
            foods = ["Boiled Chicken", "Egg Whites", "Oats", "Vegetables", "Fruits", "Low-fat Paneer"]

        return render_template(
            "result.html",
            protein=protein,
            calories=calories,
            water=round(water, 2),
            foods=foods
        )

    return render_template("smart.html")

@app.route("/graph")
def graph():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT date, steps, calories FROM fitness_data WHERE user_id=?", (user_id,))
    rows = cursor.fetchall()
    conn.close()

    dates = []
    steps = []
    calories = []

    for row in rows:
        dates.append(row[0])
        steps.append(row[1])
        calories.append(row[2])

    return render_template("graph.html", dates=dates, steps=steps, calories=calories)


@app.route("/delete/<int:id>")
def delete(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM fitness_data WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/progress")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if "user_id" not in session:
        return redirect("/login")

    if "chat_history" not in session:
        session["chat_history"] = []

    if request.method == "POST":
        message = request.form["message"].lower()

        if "protein" in message:
            reply = "For protein, eat eggs, chicken, paneer, milk, soy, and pulses. Try 1.5–2g protein per kg body weight 💪"

        elif "weight loss" in message or "fat loss" in message:
            reply = "For weight loss, maintain calorie deficit, do cardio regularly, and eat low-fat high-protein foods 🔥"

        elif "muscle" in message or "bulking" in message:
            reply = "For muscle gain, focus on strength training, eat more calories, and include high protein foods 🏋️"

        elif "diet" in message:
            reply = "A balanced diet includes protein, carbs, healthy fats, and enough water. Avoid junk food 💯"

        elif "workout" in message or "exercise" in message:
            reply = "Do a mix of strength training and cardio. Workout at least 4-5 times per week 🏃‍♂️"

        elif "water" in message or "hydration" in message:
            reply = "Drink at least 3-4 liters of water daily. Hydration is important 💧"

        elif "abs" in message:
            reply = "For abs, focus on fat loss and core exercises like planks and crunches 🔥"

        elif "chest" in message:
            reply = "For chest, do bench press, push-ups, and chest fly 🏋️"

        elif "biceps" in message:
            reply = "For biceps, do curls like dumbbell curls and hammer curls 💪"

        elif "triceps" in message:
            reply = "For triceps, include dips and pushdowns 💪"

        elif "legs" in message:
            reply = "For legs, do squats, lunges, and leg press. Don't skip leg day 🦵"

        elif "shoulder" in message:
            reply = "For shoulders, do overhead press and lateral raises 🏋️"

        elif "sleep" in message:
            reply = "Sleep at least 7-8 hours daily for recovery 😴"

        elif "supplement" in message or "whey" in message:
            reply = "Supplements help, but whole foods should be your priority 🍗"

        elif "cardio" in message:
            reply = "Cardio helps in fat loss. Try running, cycling, or skipping 🏃"

        elif "motivation" in message:
            reply = "Stay consistent, trust the process, and results will come 💯🔥"

        else:
            reply = "Maintain a balanced diet, regular workouts, and proper sleep 👍"

        session["chat_history"].append({
            "user": message,
            "bot": reply
        })

    return render_template("chat.html", chats=session["chat_history"])


@app.route("/clear_chat")
def clear_chat():
    session.pop("chat_history", None)
    return redirect("/chat")

#  Logout
@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/login")




import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)