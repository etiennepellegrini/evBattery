# ======================================================================
#
# evBattery - main.py
#
# ----------------------------------------------------------------------
# Current architecture:
# - Login provides access code, is exchanged for access token which is saved to
# DB
# - Call to `vehicle` (can be made through app or programmatically) calls API
# for battery status
#     - Try to load access token from database
#         - If none found, go to login
#     - Check token validity
#         - Exchange if expired
#
# ======================================================================

"""Get EV battery status with Smartcar."""

__version__ = "0.1"
__author__ = "Etienne Pellegrini (392M)"

# ======================================================================
# Place all imports after here.
#
import datetime
import json
import os
from flask import Flask, redirect, request, jsonify
from flask_cors import CORS

import smartcar
#
# Place all imports before here.
# ======================================================================

# Data
database = "../data/.access.db"

# Global variables/settings
mode = "live"
units = "imperial"
scope = [
    "read_compass",      # Read the compass direction your vehicle is facing
    "read_engine_oil",   # Read vehicle engine oil health
    "read_battery",      # Read EV battery"s capacity and state of charge
    "read_charge",       # Read whether vehicle is charging
    "control_charge",    # Start or stop your vehicle"s charging
    "read_thermometer",  # Read temperatures from inside and outside the vehicle
    "read_fuel",         # Read fuel tank level
    "read_location",     # Access location
    "control_security",  # Lock or unlock your vehicle
    "read_odometer",     # Retrieve total distance traveled
    "read_speedometer",  # Know your vehicle"s speed
    "read_tires",        # Read vehicle tire pressure
    "read_vehicle_info", # Know make, model, and year
    "read_vin",          # Read VIN
]

# ======================================================================
#                              UTILITIES
# ======================================================================

# --- Authorization Step 1: Launch Smartcar authorization dialog
client = smartcar.AuthClient(mode=mode)


# ----------------------------------------------------------------------
# Load access token from database
def load_access_from_database():
    """Read access database to return a smartcar.types.Access object."""
    # Read json dictionary
    with open(database, "r") as db:
        access_dict = json.load(db)

        # Convert datetime objects
        access_dict["expiration"] = datetime.datetime.fromisoformat(
            access_dict["expiration"]
        )
        access_dict["refresh_expiration"] = datetime.datetime.fromisoformat(
            access_dict["refresh_expiration"]
        )

    # Make and return Access object
    return smartcar.types.make_access_object(access_dict)


# ----------------------------------------------------------------------
# Save access token to database
def save_access_to_database(access: smartcar.types.Access):
    """Save Access object as a json dictionary to access database."""
    # Create dict from Access object
    access_dict = {
        "access_token": access.access_token,
        "token_type": access.token_type,
        "expires_in": access.expires_in,
        "expiration": access.expiration.isoformat(),
        "refresh_token": access.refresh_token,
        "refresh_expiration": access.refresh_expiration.isoformat(),
    }
    # Write to access.db
    with open(database, "w") as db:
        json.dump(access_dict, db)


# ----------------------------------------------------------------------
# Get fresh access token (because they expire every 2 hours)
def get_fresh_access():
    # TODO: replace global with a database access
    try:
        access = load_access_from_database()
    except:
        return redirect("/login")

    # Check access expiration date
    # BUG: is_expired somehow doesn't work, don't get it
    # if smartcar.is_expired(access["expiration"]):
    if datetime.datetime.utcnow() > access.expiration:
        new_access = client.exchange_refresh_token(access.refresh_token)
        save_access_to_database(new_access)
        return new_access

    # Access in database is valid
    else:
        return access


# ======================================================================
#                                 APP
# ======================================================================
app = Flask(__name__)
CORS(app)

# ----------------------------------------------------------------------
# login: provide login to car manufacturer's website
@app.route("/login", methods=["GET"])
def login():
    # --- Authorization Step 2: Launch Smartcar authorization dialog
    auth_url = client.get_auth_url(scope)
    return redirect(auth_url)


# ----------------------------------------------------------------------
# Exchange manufacturer's access code for a Smartcar Access object
@app.route("/exchange", methods=["GET"])
def exchange():
    # --- Authorization Step 3: Handle Smartcar response, get access code
    code = request.args.get("code")

    # --- Request Step 1: Obtain an access token
    # Exchange access code for an access token
    access = client.exchange_code(code)
    save_access_to_database(access)

    return redirect("/vehicle")


# ----------------------------------------------------------------------
# vehicle: Get vehicle info
@app.route("/vehicle", methods=["GET"])
def vehicle():
    fresh_access = get_fresh_access()

    # --- Request Step 2: Get vehicle ids
    # Send a request to get a list of vehicle ids
    vehicles = smartcar.get_vehicles(fresh_access.access_token)
    vehicle_ids = vehicles.vehicles

    # --- Request Step 3: Create a vehicle
    # Instantiate the first vehicle in the vehicle id list
    vehicle = smartcar.Vehicle(
        vehicle_ids[0],
        fresh_access.access_token,
        options={"unit_system": units},
    )

    # --- Request Step 4: Make a request to Smartcar API
    odometer = vehicle.odometer()
    battery = vehicle.battery()

    # --- Output
    # Create output dict
    stats_dict = {
        "date": datetime.datetime.now().isoformat(),
        "odometer": odometer.distance,
        "battery_level": battery.percent_remaining,
        "battery_range": battery.range,
    }

    # Jsonify depends on a Flask app being active.
    # For general use, return a dict and handle it differently depending on
    # whether the app is active or not
    # return jsonify(stats_dict)

    return stats_dict


# ======================================================================
#                                 MAIN
# ======================================================================
if __name__ == "__main__":
    app.run(port=8000)
