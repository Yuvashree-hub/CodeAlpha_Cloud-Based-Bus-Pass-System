from flask import Flask, render_template, request
import sqlite3
import random

app = Flask(__name__)


# Create database
def create_db():
    conn = sqlite3.connect("bookings.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id TEXT,
        name TEXT,
        phone TEXT,
        from_city TEXT,
        to_city TEXT,
        travel_date TEXT,
        bus TEXT,
        price INTEGER
    )
    """)

    conn.commit()
    conn.close()


create_db()



@app.route("/", methods=["GET","POST"])
def booking():

    if request.method == "POST":

        name = request.form["name"]
        phone = request.form["phone"]
        from_city = request.form["from_city"]
        to_city = request.form["to_city"]
        date = request.form["date"]
        bus = request.form["bus"]


        # price logic
        if bus == "AC Sleeper":
            price = 1200

        elif bus == "Non AC Sleeper":
            price = 800

        elif bus == "AC Seater":
            price = 600

        else:
            price = 400


        # unique ticket id
        ticket_id = "BUS" + str(random.randint(10000,99999))


        conn = sqlite3.connect("bookings.db")
        cursor = conn.cursor()


        cursor.execute("""
        INSERT INTO bookings
        (ticket_id,name,phone,from_city,to_city,travel_date,bus,price)
        VALUES(?,?,?,?,?,?,?,?)
        """,
        (
        ticket_id,
        name,
        phone,
        from_city,
        to_city,
        date,
        bus,
        price
        ))


        conn.commit()
        conn.close()



        return render_template(
            "confirmation.html",
            ticket=ticket_id,
            name=name,
            phone=phone,
            from_city=from_city,
            to_city=to_city,
            date=date,
            bus=bus,
            price=price
        )


    return render_template("index.html")




if __name__=="__main__":
    app.run(debug=True)