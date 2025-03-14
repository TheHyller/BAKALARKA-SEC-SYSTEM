from os import path
import json
import os

# Get the absolute path to the config file
BASE_DIR = path.dirname(path.dirname(path.abspath(__file__)))
CONFIG_FILE = path.join(BASE_DIR, "config.json")

# These will be set by load_config()
PIN_CODE = None
system_active = None

def load_config():
    global system_active, PIN_CODE
    # Default values only used if file doesn't exist
    defaults = {
        "PIN_CODE": "0000",
        "system_active": False
    }
    
    if path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                PIN_CODE = config.get("PIN_CODE", defaults["PIN_CODE"])
                system_active = config.get("system_active", defaults["system_active"])
                print(f"Loaded config from {CONFIG_FILE}: PIN={PIN_CODE}, state={system_active}")
        except Exception as e:
            print(f"Failed loading config from {CONFIG_FILE}: {e}")
            PIN_CODE = defaults["PIN_CODE"]
            system_active = defaults["system_active"]
    else:
        print(f"Config file not found at {CONFIG_FILE}, creating with defaults")
        PIN_CODE = defaults["PIN_CODE"]
        system_active = defaults["system_active"]
        # Create initial config file
        save_config()

def save_config(new_pin=None, new_state=None):
    global PIN_CODE, system_active
    
    if new_pin is not None:
        PIN_CODE = new_pin
    if new_state is not None:
        system_active = new_state
        
    config = {
        "PIN_CODE": PIN_CODE,
        "system_active": system_active
    }
    
    # Ensure the directory exists
    os.makedirs(path.dirname(CONFIG_FILE), exist_ok=True)
    
    try:
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
            print(f"Saved config to {CONFIG_FILE}: PIN={PIN_CODE}, state={system_active}")
    except Exception as e:
        print(f"Failed saving config to {CONFIG_FILE}: {e}")