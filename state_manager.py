import json

STATE_FILE = "device_states.json"

def load_state():
    try:
        with open(STATE_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_state(state):
    with open(STATE_FILE, 'w') as file:
        json.dump(state, file, indent=4)

def update_device_state(device_name, new_state):
    state = load_state()
    if device_name not in state:
        state[device_name] = {}
    state[device_name].update(new_state)
    save_state(state)

def get_device_state(device_name):
    state = load_state()
    return state.get(device_name, {})
