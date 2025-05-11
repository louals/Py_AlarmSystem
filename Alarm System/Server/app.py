from flask import Flask, request, render_template
import mysql.connector

app = Flask(__name__)


db = mysql.connector.connect(
    host="localhost",
    user="AlarmAdmin",
    password="syStempassword_678$",
    database="alarmsys",
    port=3308
)
cursor = db.cursor()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/update', methods=['POST'])
def update_alarm_system():
    try:
        zone1 = int(request.args.get('zone1'))
        zone2 = int(request.args.get('zone2'))
        zone3 = int(request.args.get('zone3'))
        zone4 = int(request.args.get('zone4'))
        system_status = int(request.args.get('system_status'))
        alarm_status = int(request.args.get('alarm_status'))

        # Insert into the database
        cursor.execute("""
            INSERT INTO status (zone1, zone2, zone3, zone4, system_status, alarm_status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (zone1, zone2, zone3, zone4, system_status, alarm_status))
        db.commit()
        
        return "Data received and updated successfully!"
    except ValueError:
        return "Invalid data received!", 400

@app.route('/status', methods=['GET'])
def get_status():
    cursor.execute("SELECT * FROM status ORDER BY id DESC LIMIT 1")
    result = cursor.fetchone()
    
    if result:
        response = f"{result[1]},{result[2]},{result[3]},{result[4]},{result[5]},{result[6]}"
        return response
    return "No data found"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)