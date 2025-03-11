from flask import Flask, render_template, request, jsonify, redirect, url_for, session
from state_manager import update_device_state, get_device_state
from schedule_manager import save_new_event, remove_event, get_schedule
from light_control import Light
from thermostat_control import Thermostat

app = Flask(__name__)
app.secret_key = '12345'

PASSWORD = "12345"

light, thermostat = "", ""

@app.route('/')
def home():
    if 'logged_in' in session and session['logged_in']:
        return render_template('index.html')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form['password']
        if password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/get_device/<device_name>', methods=['GET'])
def get_device(device_name):
    state = get_device_state(device_name)
    if not state:
        return jsonify({"error":f"No state found for {device_name}"}), 400

    death = get_device_state("death")
    if death['status'] == "on" and device_name != "death":
        return jsonify({"error":f"Death is active"}), 400

    return jsonify(state)

@app.route('/update_device', methods=['POST'])
def update_device():
    data = request.json
    if 'device' not in data or 'state' not in data:
        return jsonify({"error": "Invalid payload"}), 400

    device_name = data['device']
    new_state = data['state']

    death = get_device_state("death")
    if death['status'] == "on" and device_name != "death":
        return jsonify({"error":f"Death is active"}), 400

    update_device_state(device_name, new_state)

    if device_name == 'light':
        light.change_lights(new_state['status'], new_state['color'],new_state['brightness'], new_state['type'])
    elif device_name == 'thermostat':
        thermostat.change_thermostat(new_state['max_temperature'], new_state['min_temperature'], new_state['fan_status'], new_state['window_status'])

    return jsonify({"message":f"Updated {device_name} state"}), 200

@app.route('/update_temperature', methods=['POST'])
def update_temperature():
	data = request.json
	if 'temperature' in data and 'humidity' in data:
		thermostat.update_TH_state(data)
		return jsonify({"message": "Sensor data updated successfully"}), 200
	else:
		return jsonify({"error": "Invalid payload"}), 400

@app.route('/get_schedule', methods=['GET'])
def get_device_schedule():
    schedule = get_schedule()
    return jsonify(schedule)

@app.route('/add_schedule', methods=['POST'])
def add_schedule_event():
    data = request.json
    if not data or "device" not in data or "state" not in data or "start_time" not in data or "end_time" not in data or "repeat" not in data:
        return jsonify({"error": "Invalid event data"}), 400

    save_new_event(data)
    return jsonify({"message": "Event added successfully"}), 200

@app.route('/remove_schedule', methods=['POST'])
def remove_schedule_event():
    data = request.json
    if not data or "device" not in data or "start_time" not in data or "end_time" not in data:
        return jsonify({"error": "Invalid request data"}), 400

    device_name = data["device"]
    start_time = data["start_time"]
    end_time = data["end_time"]

    remove_event(device_name, start_time, end_time)
    return jsonify({"message": "Event removed successfully"}), 200

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    l = get_device_state('light')
    t = get_device_state('thermostat')

    light = Light(l['status'], l['color'], l['brightness'], l['type'])
    thermostat = Thermostat(t['max_temperature'], t['min_temperature'], t['fan_status'], t['window_status'])

    app.run(host='192.168.50.159', port=5000, debug=True)
