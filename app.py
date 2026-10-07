from flask import Flask,render_template,request
from datetime import datetime
app=Flask(__name__)
parking_data={}
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/vehicle-entry",methods=["GET","POST"])
def vehicle_entry():
    if request.method=="POST":
        vehicle_number=request.form["vehicle_number"]
        vehicle_type = request.form["vehicle_type"]
        owner_name = request.form["owner_name"]
        entry_time=datetime.now().strftime("%d-%m-%Y %I:%M %p")
        parking_data[vehicle_number]={
            "vehicle_type":vehicle_type,
            "owner_name":owner_name,
            "entry_time":datetime.now()
        }
        print("Vehicle Number:", vehicle_number)
        print("Vehicle Type:", vehicle_type)
        print("Owner Name:", owner_name)
        print("Entry Time:",entry_time)
        return f"""
        Vehicle Registered Successfully!<br><br>
        Vehicle Number: {vehicle_number}<br>
        Vehicle Type: {vehicle_type}<br>
        Owner Name: {owner_name}<br>
        Entry Time: {entry_time}
        """
    return render_template("vehicle_entry.html")
@app.route("/vehicle-exit", methods=["GET", "POST"])
def vehicle_exit():
    if request.method == "POST":
        vehicle_number = request.form["vehicle_number"]
        if vehicle_number not in parking_data:
            return "Vehicle not found!"
        entry_time = parking_data[vehicle_number]["entry_time"]
        exit_time = datetime.now()
        duration = exit_time - entry_time
        hours = duration.total_seconds() / 3600
        if hours <= 1:
            amount = 20
        else:
            extra_hours = int(hours - 1) + 1
            amount = 20 + (extra_hours * 10)
        exit_time_display = exit_time.strftime("%d-%m-%Y %I:%M %p")
        return f"""
        Vehicle Exit Recorded Successfully!<br><br>
        Vehicle Number: {vehicle_number}<br>
        Entry Time: {entry_time.strftime("%d-%m-%Y %I:%M %p")}<br>
        Exit Time: {exit_time_display}<br>
        Parking Duration: {hours:.2f} hours<br>
        <br>
        <h2>Parking Bill: ₹{amount}</h2>
        """
    return render_template("vehicle_exit.html")
if __name__=="__main__":
    app.run(debug=True)