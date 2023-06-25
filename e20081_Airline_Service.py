# Importing necessary modules from flask and pymongo packages
from flask import Flask, request, jsonify, session
from pymongo import MongoClient
import json

# Establishing a connection with MongoDB running at port 27017
client = MongoClient('mongodb://mongodb:27017/')

# Getting the "DigitalAirlines" database from the MongoDB instance.
db = client['DigitalAirlines']

# Getting collections from the "DigitalAirlines" database
users = db['Users']
flights = db['Flights']
bookings = db['Bookings']

# Admin Emails List: This is a  list of admins to disallow these emails for normal user registration.
admin_emails = ['admin1@example.com']

# Initiating a Flask app and setting a secret key for sessions.
app = Flask(__name__)
app.secret_key = 'secret_key'

#Temporarly adding a user in order to ensure the creaiton of the collection "users" for the successfull execution of line --> users.find_one({"email": "admin1@example.com"})  IF the collection is non-existent this will result in an error and a crash, so we first create the collection.
temp = {
    "user_name": "TEMP",
    "user_surname" : "TEMP",
    "email" : "TEMP",
    "login_code" : "TEMP",
    "date_of_birth" : "TEMP",
    "country_of_origin" : "TEMP",
    "passport_number" : "TEMP",
    "User_code" : "THIS_IS_TEMP_CODE"
}
users.insert_one(temp)

#Create the admin of the system. This is hard-coded
admin = {
    "user_name": "Admin",
    "user_surname" : "Admin",
    "email" : "admin1@example.com",
    "login_code" : "3364",
    "date_of_birth" : "31-02-2002",
    "country_of_origin" : "Greece",
    "passport_number" : "AM553988",
    "User_code" : "THIS_IS_A_UNIQUE_ADMIN_CODE"
}
if users.find_one({"email": "admin1@example.com"}):
    print(f"Admin exists already.\nUSE EMAIL: admin1@example.com\nAND LOGIN_CODE:3364")
else:
    users.insert_one(admin)
    print(f"Added Admin successfully.\nUSE EMAIL: admin1@example.com\nAND LOGIN_CODE:3364")


#Delete the temporary user because we dont want unnecessary elements in the "users" collection
users.delete_one({"User_code": "THIS_IS_TEMP_CODE"})


# Register Route: This is an endpoint for user registration. It is only accessible by HTTP POST request.
@app.route('/register', methods=['POST'])
def register():
    # Try block to catch any error while parsing the JSON data in the request.
    try:
        data = request.get_json()
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Could not parse data as json"}), 400

    # Extracting user data from the request. If any data is missing, it will return an error message.
    try:
        user_name = data['user_name']
        user_surname = data['user_surname']
        email = data['email']
        login_code = data['login_code']
        date_of_birth = data['date_of_birth']
        country_of_origin = data['country_of_origin']
        passport_number = data['passport_number']
    except:
        return jsonify(print("Error! Missing Field(s)!")), 400

    # Check if the user email exists in the admin email list. If yes, then it should return an error.
    if email in admin_emails:
        print(f"Error: Privileged email cannot be used for user registration.")
        return jsonify({"Error": "Privileged email cannot be used for user registration."}), 403

    # Check if the user email or username exists in the database. If yes, then it should return an error.
    if users.find_one({"email": email}):
        print(f"Error: User exists already.")
        return jsonify({"Error": "User exists already."}), 409
    if users.find_one({"user_name": user_name}):
        print(f"Error: User does not exist but user_name is in use.")
        return jsonify({"Error": "Email is available but user_name is in use."}), 409

    # Counting the number of users in the database to generate a unique user_code.
    user_count = users.count_documents({}) + 1
    user_code = user_name[0] + user_surname[0] + str(user_count).zfill(3)

    # Creating a dictionary to represent the new user.
    new_user = {
        "user_name": user_name,
        "user_surname" : user_surname,
        "email" : email,
        "login_code" : login_code,
        "date_of_birth" : date_of_birth,
        "country_of_origin" : country_of_origin,
        "passport_number" : passport_number,
        "User_code" : user_code,
    }

    # Inserting the new user data into the "Users" collection in MongoDB.
    users.insert_one(new_user)
    
    # Preparing the success message.
    success_message = f"User registered successfully. Details: Name: {user_name} {user_surname}, Email: {email}, " \
                  f"Date of Birth: {date_of_birth}, Country of Origin: {country_of_origin}, " \
                  f"Passport Number: {passport_number}, User Code: {user_code}"

    print(success_message)
    return jsonify({"Success": "User registered successfully."}), 201

# Login Route: This is an endpoint for user login. It is only accessible by HTTP POST request.
@app.route('/login', methods=['POST'])
def login():
    # Checking if a user is already logged in the session.
    if 'user_code' in session:
        print(f"Error: A user is currently logged-in. Please log out first.")
        return jsonify({"Error": "A user is currently logged-in. Please log out first."}), 403
    
    # Try block to catch any error while parsing the JSON data in the request.
    try:
        data = request.get_json()
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Could not parse data as json"}), 400

    # Extracting email and login code from the request data. If either is missing, it will return an error message.
    try:
        email = data['email']
        login_code = data['login_code']
    except:
        return jsonify(print("Error! Missing Field!")), 400

    # If an admin tries to log in from the user login endpoint, an error message is returned.
    if email in admin_emails:
        print("Error: Administrators should use the admin login endpoint  -->/admin/login")
        return jsonify({"Error": "Administrators should use the admin login endpoint -->/admin/login"}), 403

    # Check if the user exists with the given email and login code. If yes, log-in the user and create a new session.
    user = users.find_one({"$and": [{"email": email}, {"login_code": login_code}]})
    if user:
        session['user_code'] = user['User_code']
        print(f"Success! User {user['user_name']} {user['user_surname']} Logged-in")
        return jsonify({"Success": f"User {user['user_name']} {user['user_surname']} logged in"}), 200
    else:
        # If the login code is incorrect but the email exists in the database, returns an error.
        if users.find_one({"email": email}):
            print(f"Error! Wrong login Code for email: {email}. Please try again!")
            return jsonify({"Error": f"Wrong login Code for email: {email}. Please try again!"}), 401
        else:
            # If the email does not exist in the database, returns an error.
            print(f"Error: {email} does not exist. Please register first!")
            return jsonify({"Error": f"{email} does not exist. Please register first!"}), 404

# The "/logout" endpoint is a POST route that logs out a user.
@app.route('/logout', methods=['POST'])
def logout():
    # Check if a user is currently logged in. If not, return an error.
    if 'user_code' not in session:
        print(f"Error: No user is currently logged in.")
        return jsonify({"Error": "No user is currently logged in."}), 401

    # If a user is logged in, get the user's code from the session.
    user_code = session['user_code']
    # Fetch the user details from MongoDB using the user code.
    user = users.find_one({"User_code": user_code})

    # Check if an administrator is trying to logout from the user logout endpoint. If so, return an error.
    if user is not None and user['email'] in admin_emails:
        print("Error: Administrators should use the admin logout endpoint -->/admin/login")
        return jsonify({"Error": "Administrators should use the admin logout endpoint -->/admin/login"}), 403
    
    # If it's not an admin, remove the 'user_code' from the session, effectively logging out the user.
    session.pop('user_code', None)

    # If the user details were found in MongoDB, return a successful logout message.
    if user is not None:
        print(f"Success! User {user['user_name']} {user['user_surname']} Logged-out")
        return jsonify({"Success": f"User {user['user_name']} {user['user_surname']} logged out"}), 200
    else:
        # If the user details were not found in MongoDB, return an error.
        print(f"Error: The user does not exist in the database.")
        return jsonify({"Error": "The user does not exist in the database."}), 404

# The "/search_flights" endpoint is a GET route that allows admins to search for flights.
@app.route('/search_flights', methods=['GET'])
def search_flights():
    # Check if an admin is logged in. If not, return an error.
    if 'user_code' not in session:
        print(f"Error: No administrator is currently logged-in.")
        return jsonify({"Error": "No administrator is currently logged-in."}), 401

    # Attempt to parse the request data as JSON. If the request data is empty, this will return None.
    data = request.get_json(silent=True)

    if data is None:
        # If no request data is provided, return all flights in the MongoDB "Flights" collection.
        results = flights.find()
        return jsonify([flight for flight in results]), 200

    # Extract the search criteria from the request data. If a certain criterion is not provided, its corresponding
    # variable will be None.
    airport_of_origin = data.get('airport_of_origin')
    airport_destination = data.get('airport_destination')
    date_of_flight = data.get('date_of_flight')

    # Construct the search query. If a certain criterion is None, it will not be included in the query.
    search_criteria = {}
    if airport_of_origin:
        search_criteria['airport_of_origin'] = airport_of_origin
    if airport_destination:
        search_criteria['airport_destination'] = airport_destination
    if date_of_flight:
        search_criteria['date_of_flight'] = date_of_flight

    # Use the search query to find matching flights in the MongoDB "Flights" collection.
    results = flights.find(search_criteria)
    # Return the matching flights as a JSON array.
    return jsonify([flight for flight in results]), 200

# The "/display_flight_details/<_id>" endpoint is a GET route that shows the details of a flight.
@app.route('/display_flight_details/<_id>', methods=['GET'])
def display_flight_details(_id):
    # Check if a user is logged in. If not, return an error.
    if 'user_code' not in session:
        print(f"Error: No user is currently logged-in.")
        return jsonify({"Error": "No user is currently logged-in."}), 401

    # Fetch the flight details from the MongoDB "Flights" collection using the provided flight ID.
    flight = flights.find_one({"_id": _id})

    # If no flight with the provided ID was found, return an error.
    if not flight:
        return jsonify({"Error": "Flight cannot be found."}), 404

    # Construct a JSON object that represents the flight details.
    flight_details = {
        "Date of Departure": flight['date_of_flight'],
        "Airport of Origin": flight['airport_of_origin'],
        "Airport of Destination": flight['airport_destination'],
        "Available Tickets - Business Class": flight['business_class_tickets_availability'],
        "Available Tickets - Economy Class": flight['economy_class_tickets_availability'],
        "Ticket Price - Business Class": flight['business_class_tickets_price'],
        "Ticket Price - Economy Class": flight['economy_class_tickets_price'],
    }

    # Return the flight details as a JSON object.
    return jsonify(flight_details), 200

# The "/book_ticket/<_id>" endpoint is a POST route that allows users to book a ticket for a flight.
@app.route('/book_ticket/<_id>', methods=['POST'])
def book_ticket(_id):
    # Check if a user is logged in. If not, return an error.
    if 'user_code' not in session:
        print(f"Error: No user is currently logged-in.")
        return jsonify({"Error": "No user is currently logged-in."}), 401

    # If a user is logged in, get the user's code from the session.
    user_code = session['user_code']
    # Fetch the user details from the MongoDB "Users" collection using the user code.
    user = users.find_one({"User_code": user_code})

    # Attempt to parse the request data as JSON. If the request data is not JSON, return an error.
    try:
        data = request.get_json()
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Could not parse data as JSON."}), 400

    # Extract the booking details from the request data. If a certain detail is not provided, return an error.
    try:
        user_name = data['user_name']
        user_surname = data['user_surname']
        passport_number = data['passport_number']
        date_of_birth = data['date_of_birth']
        email = data['email']
        seat_class = data['seat_class']
    except:
        return jsonify({"Error": "Missing Field(s)!"}), 400
    
    # Verify that the booking details match the user's details. If they don't, return an error.
    if user['user_name'] == user_name and user['user_surname'] == user_surname and user['passport_number'] == passport_number and user['date_of_birth'] == date_of_birth and user['email'] == email:
        print(f"Correct Credentials provided! Continuing with the booking...")
    else:
        return jsonify({"Error": "The credentials you provided the system with, do not match the info saved on your account!"}), 403

    # Fetch the flight details from the MongoDB "Flights" collection using the provided flight ID.
    flight = flights.find_one({"_id": _id})

    # If no flight with the provided ID was found, return an error.
    if not flight:
        return jsonify({"Error": "Flight cannot be found."}), 404

    # Depending on the user's chosen class (business or economy), check if there are any available tickets.
    # If there are, decrement the number of available tickets by 1.
    # If there are no tickets available, return an error.
    if seat_class == "business":
        current_tickets = int(flight['business_class_tickets_availability'])
        if current_tickets < 1:
            return jsonify({"Error": "No business class tickets available for this flight."}), 409
        else:
            flights.update_one({"_id": _id}, {"$set": {"business_class_tickets_availability": str(current_tickets - 1)}})
    elif seat_class == "economy":
        current_tickets = int(flight['economy_class_tickets_availability'])
        if current_tickets < 1:
            return jsonify({"Error": "No economy class tickets available for this flight."}), 400
        else:
            flights.update_one({"_id": _id}, {"$set": {"economy_class_tickets_availability": str(current_tickets - 1)}})
    else:
        return jsonify({"Error": "Invalid seat class. Please choose 'business' or 'economy'."}), 400

    # Generate a unique booking code.
    booking_count = bookings.count_documents({}) + 1
    booking_code = user_name[0] + user_surname[0] + _id[0] + _id[1] + seat_class[0].capitalize() + str(booking_count).zfill(3)

    # Construct a new booking JSON object.
    new_booking = {
        "user_code": user_code,
        "flight_id": _id,
        "user_name": user_name,
        "user_surname": user_surname,
        "passport_number": passport_number,
        "date_of_birth": date_of_birth,
        "email": email,
        "seat_class": seat_class,
        "booking_code": booking_code
    }

    # Insert the new booking into the MongoDB "Bookings" collection.
    bookings.insert_one(new_booking)

    # Construct and print a success message.
    success_message = f"Ticket booked successfully. Details: Name - {user_name}, Surname - {user_surname}, Passport number - {passport_number}, " \
                    f"Date of Birth - {date_of_birth}, Email - {email}, Flight id - {_id}, " \
                    f"Seat Class - {seat_class.capitalize()}, User code - {user_code}, Booking code - {booking_code}"
    print(success_message)
    # Return a success message.
    return jsonify({"Success": "Ticket booked successfully!"}), 201

# "/bookings" endpoint with a GET method is used to get all the bookings of the currently logged in user.
@app.route('/bookings', methods=['GET'])
def show_bookings():
    # The session variable 'user_code' is used to check if a user is logged in. If 'user_code' is not in the session, it means no user is currently logged in.
    if 'user_code' not in session:
        # If no user is logged in, an error message is printed to the server log, and an error message is sent back to the client in JSON format.
        print(f"Error: No user is currently logged-in.")
        return jsonify({"Error": "No user is currently logged-in."}), 401

    # If a user is logged in, the user's code is retrieved from the session variable.
    user_code = session['user_code']

    # A MongoDB find operation is performed on the "bookings" collection to get all the bookings where the 'user_code' matches the logged in user's code.
    # The returned value is a cursor object that can be iterated to get each individual booking.
    user_bookings = bookings.find({"user_code": user_code})

    # If the cursor object is None, it means no bookings were found for the user.
    if user_bookings is None:
        # In this case, a JSON message is sent back to the client indicating that no bookings were found.
        return jsonify({"Message": "No bookings found for the user."}), 200

    # If bookings were found, an empty list is initialized to hold the booking data.
    bookings_data = []

    # The cursor object is iterated to get each individual booking.
    for booking in user_bookings:
        # For each booking, the flight details are fetched from the 'flights' collection using the flight ID from the booking.
        flight = flights.find_one({"_id": booking['flight_id']})

        # The booking data and flight data are combined into a single dictionary.
        data = {
            "booking_code": booking.get('booking_code', ''),
            "flight_id": booking.get('flight_id', ''),
            "user_name": booking.get('user_name', ''),
            "user_surname": booking.get('user_surname', ''),
            "passport_number": booking.get('passport_number', ''),
            "date_of_birth": booking.get('date_of_birth', ''),
            "email": booking.get('email', ''),
            "seat_class": booking.get('seat_class', ''),
            # Flight details are embedded within the booking data as a nested dictionary.
            "flight_details": {
                "origin": flight.get('airport_of_origin', ''),
                "destination": flight.get('airport_destination', ''),
                "date": flight.get('date_of_flight', '')
            }
        }

        # The combined booking and flight data dictionary is appended to the bookings data list.
        bookings_data.append(data)

    # The bookings data list is sent back to the client in JSON format.
    return jsonify({"Bookings": bookings_data}), 200

# "/show_booking_details/<booking_code>" endpoint with a GET method is used to get the details of a specific booking using its booking_code.
@app.route('/show_booking_details/<booking_code>', methods=['GET'])
def show_booking_details(booking_code):
    # As before, it checks if a user is logged in by checking for 'user_code' in the session.
    if 'user_code' not in session:
        # If not, it logs an error and sends a 401 Unauthorized response with an error message.
        print(f"Error: No user is currently logged-in.")
        return jsonify({"Error": "No user is currently logged-in."}), 401

    # If a user is logged in, their 'user_code' is retrieved from the session and used to fetch their details from the 'users' collection.
    user_code = session['user_code']
    user = users.find_one({"User_code": user_code})

    # The booking related to the provided booking_code is fetched from the 'bookings' collection.
    booking = bookings.find_one({"booking_code": booking_code})

    # If the booking is not found (i.e., 'booking' is None), it sends a 404 Not Found response with an error message.
    if not booking:
        return jsonify({"Error": "Booking cannot be found."}), 404

    # It checks if the booking belongs to the currently logged-in user by comparing the email in the booking to the email of the user.
    # If they don't match, it logs an error and sends a 403 Forbidden response with an error message.
    if booking['email'] != user['email']:
        print(user['email'])
        print(booking['email'])
        print(f"Error: This booking was not made by the logged-in user.")
        return jsonify({"Error": "This booking was not made by the logged-in user."}), 403

    # The flight details related to the booking are fetched from the 'flights' collection.
    flight = flights.find_one({"_id": booking['flight_id']})

    # If the flight is not found (i.e., 'flight' is None), it sends a 404 Not Found response with an error message.
    if not flight:
        return jsonify({"Error": "Flight cannot be found."}), 404

    # If the flight and booking are found and the booking belongs to the user, the details are combined into a dictionary.
    # This dictionary is sent in a 200 OK response.
    data = {
        "booking_code": booking['booking_code'],
        "flight_id": booking['flight_id'],
        "user_name": booking['user_name'],
        "user_surname": booking['user_surname'],
        "passport_number": booking['passport_number'],
        "date_of_birth": booking['date_of_birth'],
        "email": booking['email'],
        "seat_class": booking['seat_class'],
        "flight_details": {
            "origin": flight['airport_of_origin'],
            "destination": flight['airport_destination'],
            "date": flight['date_of_flight']
        }
    }
    return jsonify({"Booking": data}), 200

# "/cancel_flight/<booking_code>" endpoint with a POST method is used to cancel a booking using its booking_code.
@app.route('/cancel_flight/<booking_code>', methods=['POST'])
def cancel_flight(booking_code):
    # It starts by checking if a user is logged in by checking for 'user_code' in the session.
    if 'user_code' not in session:
        # If not, it logs an error and sends a 401 Unauthorized response with an error message.
        print(f"Error: No user is currently logged-in.")
        return jsonify({"Error": "No user is currently logged-in."}), 401

    # If a user is logged in, their 'user_code' is retrieved from the session.
    user_code = session['user_code']

    # The booking related to the provided booking_code is fetched from the 'bookings' collection.
    booking = bookings.find_one({"booking_code": booking_code})

    # If the booking is not found (i.e., 'booking' is None), it sends a 404 Not Found response with an error message.
    if not booking:
        return jsonify({"Error": "Booking cannot be found."}), 404

    # It checks if the booking belongs to the currently logged-in user by comparing the user_code in the booking to the user_code of the user.
    # If they don't match, it logs an error and sends a 403 Forbidden response with an error message.
    if booking['user_code'] != user_code:
        print(f"Error: This booking was not made by the logged-in user.")
        return jsonify({"Error": "This booking was not made by the logged-in user."}), 403

    # The flight details related to the booking are fetched from the 'flights' collection.
    flight = flights.find_one({"_id": booking['flight_id']})

    # If the flight is not found (i.e., 'flight' is None), it sends a 404 Not Found response with an error message.
    if not flight:
        return jsonify({"Error": "Flight cannot be found."}), 404

    # If the flight and booking are found and the booking belongs to the user, the number of available seats in the flight is incremented.
    # This depends on the seat class of the booking. The seat class is either 'economy' or 'business'.
    # It fetches the flight details again to ensure that it is working with the most recent data. It then increments the relevant field and updates the flight in the 'flights' collection.
    if booking['seat_class'] == 'economy':
        flight = flights.find_one({"_id": booking['flight_id']})
        economy_class_tickets_availability = int(flight['economy_class_tickets_availability']) + 1
        flights.update_one({"_id": booking['flight_id']}, {"$set": {"economy_class_tickets_availability": economy_class_tickets_availability}})
    elif booking['seat_class'] == 'business':
        flight = flights.find_one({"_id": booking['flight_id']})
        business_class_tickets_availability = int(flight['business_class_tickets_availability']) + 1
        flights.update_one({"_id": booking['flight_id']}, {"$set": {"business_class_tickets_availability": business_class_tickets_availability}})
    
    # After the flight has been updated, the booking is deleted from the 'bookings' collection using its '_id'.
    # This is done using the 'delete_one' method which deletes the first document that matches the filter (in this case, the booking_code).
    bookings.delete_one({"_id": booking_code})

    # If the booking was successfully cancelled, it sends a 202 Accepted response with a success message.
    return jsonify({"Success": "Booking cancelled successfully."}), 202

# '/delete_account' endpoint handles deletion of a user's account
@app.route('/delete_account', methods=['DELETE'])
def delete_account():
    # Check if a user is logged in by checking the session for 'user_code'
    # This 'user_code' is unique to each user and is set in the session when they log in
    if 'user_code' not in session:
        # If 'user_code' is not found in the session, no user is logged in
        # Log the error and return a 401 Unauthorized status code
        print(f"Error: No user is currently logged-in.")
        return jsonify({"Error": "No user is currently logged-in."}), 401

    # If a user is logged in, get their 'user_code' from the session
    user_code = session['user_code']

    # Search the 'users' collection in the MongoDB database for a user document that has the same 'user_code'
    user = users.find_one({"User_code": user_code})

    # If no user document is found, the 'user' variable will be None
    # If 'user' is None, the user does not exist in the database
    # Return a 404 Not Found status code
    if not user:
        return jsonify({"Error": "User cannot be found."}), 404

    # If a user document is found in the database, delete it
    # 'delete_one' method deletes the first document that matches the filter
    # In this case, the filter is the 'user_code' of the logged-in user
    users.delete_one({"User_code": user_code})

    # After deleting the user document, remove 'user_code' from the session
    # This effectively logs out the user
    session.pop('user_code', None)

    # If the user document was deleted successfully and the 'user_code' was removed from the session
    # Return a 204 No Content status code, which is standard for a successful DELETE request
    return jsonify({"Success": "Account deleted successfully."})


# Define admin endpoints
@app.route('/admin/login', methods=['POST'])
def admin_login():
    # Checking if a user is already logged in the session.
    if 'user_code' in session:
        print(f"Error: A user is currently logged-in. Please log out first.")
        return jsonify({"Error": "A user is currently logged-in. Please log out first."}), 403
    
    # Try block to catch any error while parsing the JSON data in the request.
    try:
        data = request.get_json()
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Could not parse data as json"}), 400

    # Extracting email and login code from the request data. If either is missing, it will return an error message.
    try:
        email = data['email']
        login_code = data['login_code']
    except:
        return jsonify(print("Error! Missing Field!")), 400

    # If a user tries to log in from the admin login endpoint, an error message is returned.
    if email not in admin_emails:
        print("Error: Users should use the user login endpoint  -->/login")
        return jsonify({"Error": "Users should use the user login endpoint  -->/login"}), 403

    # Check if the user exists with the given email and login code. If yes, log-in the user and create a new session.
    user = users.find_one({"$and": [{"email": email}, {"login_code": login_code}]})
    if user:
        session['user_code'] = user['User_code']
        print(f"Success! Administrator {user['user_name']} {user['user_surname']} Logged-in")
        return jsonify({"Success": f"Administrator {user['user_name']} {user['user_surname']} logged in"}), 200
    else:
        # If the login code is incorrect but the email exists in the database, returns an error.
        if users.find_one({"email": email}):
            print(f"Error! Wrong login Code for email: {email}. Please try again!")
            return jsonify({"Error": f"Wrong login Code for email: {email}. Please try again!"}), 401
        else:
            # If the email does not exist in the database, returns an error.
            print(f"Error: {email} does not exist. Wrong Admin Credentials!")
            return jsonify({"Error": f"{email} does not exist. Wrong Admin Credentials!"}), 404

@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    # The session should contain 'user_code', signifying a user is logged in.
    # If 'user_code' not in session, it means no user is currently logged in. 
    # In that case, we return an error.
    if 'user_code' not in session:
        print(f"Error: No administrator is currently logged-in.")
        return jsonify({"Error": "No administrator is currently logged-in."}), 401

    # If 'user_code' is present in the session, we extract it.
    user_code = session['user_code']
    
    # Then, we try to find the user from our 'users' collection based on 'user_code'.
    user = users.find_one({"User_code": user_code})

    # Check if the user exists in the database.
    if user is None:
        print(f"Error: No user associated with the current session.")
        return jsonify({"Error": "No user associated with the current session."}), 401
    
    # We need to make sure the logged-in user is an administrator.
    # We do that by checking if the user's email is in the list of admin emails.
    # If the email is not in the list, it means the logged-in user is not an admin.
    # In that case, we return an error.
    if user['email'] not in admin_emails:
        print(f"Error: The user currently logged-in is not an administrator.")
        return jsonify({"Error": "The user currently logged-in is not an administrator. Use request --> /logout instead"}), 403

    # If the user is an admin, we log them out by removing 'user_code' from the session.
    session.pop('user_code', None)
    
    # Finally, we return a success message indicating that the admin has been logged out.
    print(f"Success! Administrator {user['user_name']} {user['user_surname']} logged-out")
    return jsonify({"Success": f"Administrator {user['user_name']} {user['user_surname']} logged-out"}), 200

@app.route('/admin/create_flight', methods=['POST'])
def create_flight():
    # Check if a user is logged in
    if 'user_code' not in session:
        print(f"Error: No administrator is currently logged-in.")
        return jsonify({"Error": "No administrator is currently logged-in."}), 401

    # Retrieve the user code from the session
    user_code = session['user_code']
    # Query the database to find the user associated with the user code
    user = users.find_one({"User_code": user_code})

    # Check if a user exists
    if user is None:
        print(f"Error: No user found with the provided user_code.")
        return jsonify({"Error": "No user found with the provided user_code."}), 404

    # Check if the logged-in user is an admin
    if user['email'] not in admin_emails:
        print(f"Error: The user currently logged-in is not an administrator.")
        return jsonify({"Error": "The user currently logged-in is not an administrator. Cannot use /admin/* entrypoints"}), 403

    # Try to get JSON data from request
    try:
        data = request.get_json()
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Could not parse data as JSON."}), 400

    # Extract the necessary fields from the request data
    try:
        airport_of_origin = data['airport_of_origin']
        airport_destination = data['airport_destination']
        date_of_flight = data['date_of_flight']
        business_class_tickets_availability = data['business_class_tickets_availability']
        economy_class_tickets_availability = data['economy_class_tickets_availability']
        business_class_tickets_price = data['business_class_tickets_price']
        economy_class_tickets_price = data['economy_class_tickets_price']
    except:
        print("Error! Missing Field(s)!")
        return jsonify({"Error": "Missing Field(s)!"}), 400

    # Generate a unique ID for the flight
    flight_count = flights.count_documents({}) + 1
    _id = airport_of_origin[0] + airport_destination[0] + str(flight_count).zfill(3)

    # Create a dictionary for the new flight
    new_flight = {
        "airport_of_origin": airport_of_origin,
        "airport_destination" : airport_destination,
        "date_of_flight" : date_of_flight,
        "business_class_tickets_availability" : business_class_tickets_availability,
        "economy_class_tickets_availability" : economy_class_tickets_availability,
        "business_class_tickets_price" : business_class_tickets_price,
        "economy_class_tickets_price" : economy_class_tickets_price,
        "_id" : _id,
    }

    # Insert the new flight into the database
    flights.insert_one(new_flight)

    # Create a success message detailing the new flight's information
    success_message = f"Flight registered successfully. Details: Flying from {airport_of_origin} to {airport_destination} at {date_of_flight}, " \
                  f"Business_class: {business_class_tickets_availability} available tickets priced at: {business_class_tickets_price} EUR each, " \
                  f"Economy_class: {economy_class_tickets_availability} available tickets priced at: {economy_class_tickets_price} EUR each," \
                  f"Unique flight id (_id): {_id}"

    print(success_message)
    return jsonify({"Success": success_message}), 201

@app.route('/admin/renew_ticket_prices/<_id>', methods=['POST'])
def renew_ticket_prices(_id):
    # Check if an admin is logged in by checking the 'user_code' key in the session
    if 'user_code' not in session:
        print(f"Error: No administrator is currently logged-in.")
        return jsonify({"Error": "No administrator is currently logged-in."}), 401

    # Extract the logged in admin's 'user_code'
    user_code = session['user_code']

    # Look up the admin user details by 'user_code' in the users collection
    user = users.find_one({"User_code": user_code})

    # Check if the logged-in user is an admin by verifying if their email is present in the admin_emails list.
    # If not an admin, return an error message
    if user['email'] not in admin_emails:
        print(f"Error: The user currently logged-in is not an administrator.")
        return jsonify({"Error": "The user currently logged-in is not an administrator. Cannot use /admin/* entrypoints"}), 403

    # Try to parse the request data as JSON. If this fails, catch the exception and return a 400 Bad Request status code.
    try:
        data = request.get_json()
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Could not parse data as JSON."}), 400

    # Extract the new ticket prices from the request data. If any of these fields are missing, return a 400 Bad Request status code.
    try:
        new_business_class_ticket_price = data['business_class_tickets_price']
        new_economy_class_ticket_price = data['economy_class_tickets_price']
    except:
        return jsonify(print("Error! Missing Field(s)!")), 400

    # Try to find a flight in the flights collection with the '_id' provided in the URL parameters.
    flight = flights.find_one({"_id": _id})

    # If a flight with the provided '_id' does not exist, return a 404 Not Found status code.
    if not flight:
        return jsonify({"Error": "Flight cannot be found."}), 404

    # If the flight exists, update its ticket prices in the database
    flights.update_one({"_id": _id}, {"$set": {
        "business_class_tickets_price": new_business_class_ticket_price,
        "economy_class_tickets_price": new_economy_class_ticket_price,
    }})

    # Find the updated flight document in the database to confirm the price changes
    flight = flights.find_one({"_id": _id})
    
    # Print a success message detailing the updated flight information
    success_message = f"Flight prices changed successfully. Details: Flying from {flight['airport_of_origin']} to {flight['airport_destination']} at {flight['date_of_flight']}, " \
                      f"Business_class: {flight['business_class_tickets_availability']} available tickets priced at: {flight['business_class_tickets_price']} EUR each, " \
                      f"Economy_class: {flight['economy_class_tickets_availability']} available tickets priced at: {flight['economy_class_tickets_price']} EUR each," \
                      f"Unique flight id (_id): {_id}"
    print(success_message)

    # Return a success message with a 200 OK status code to the client
    return jsonify({"Success": "Flight prices updated successfully."}), 200

# Define a new route that handles HTTP DELETE requests to delete a flight
@app.route('/admin/delete_flight/<_id>', methods=['DELETE'])
def delete_flight(_id):
    # Check if a session key 'user_code' exists, indicating a user is logged in
    # If not, return a 401 Unauthorized status code
    if 'user_code' not in session:
        print(f"Error: No administrator is currently logged-in.")
        return jsonify({"Error": "No administrator is currently logged-in."}), 401

    # Get the session 'user_code' key's value
    user_code = session['user_code']

    # Query the 'users' collection in the database for a document with a matching 'User_code'
    user = users.find_one({"User_code": user_code})

    # If the email of the user retrieved is not in the list of admin_emails
    # Return a 403 Forbidden status code
    if user['email'] not in admin_emails:
        print(f"Error: The user currently logged-in is not an administrator.")
        return jsonify({"Error": "The user currently logged-in is not an administrator. Cannot use /admin/* entrypoints"}), 403

    # Query the 'flights' collection for a document with a matching '_id'
    flight = flights.find_one({"_id": _id})

    # If no matching flight is found, return a 404 Not Found status code
    if not flight:
        return jsonify({"Error": "Flight cannot be found."}), 404

    # Query the 'bookings' collection for a document with a matching 'flight_id'
    booking = bookings.find_one({"flight_id": _id})

    # If a booking is found, return a 409 Conflict status code indicating the flight cannot be deleted
    if booking:
        return jsonify({"Error": "Cannot delete this flight as there are existing ticket bookings."}), 409

    # If no bookings are found, delete the flight from the 'flights' collection
    flights.delete_one({"_id": _id})

    # Construct a success message string with the details of the deleted flight
    success_message = f"Flight with id {_id} deleted successfully. Details: Flying from {flight['airport_of_origin']} to {flight['airport_destination']} at {flight['date_of_flight']}, " \
                      f"Business_class: {flight['business_class_tickets_availability']} available tickets priced at: {flight['business_class_tickets_price']} EUR each, " \
                      f"Economy_class: {flight['economy_class_tickets_availability']} available tickets priced at: {flight['economy_class_tickets_price']} EUR each."

    # Print the success message to the console
    print(success_message)

    return jsonify({"Success": "Flight deleted successfully."})

# Define a new route that handles HTTP GET requests to search flights
@app.route('/admin/search_flights', methods=['GET'])
def admin_search_flights():
    # Again, check if a session key 'user_code' exists
    # If not, return a 401 Unauthorized status code
    if 'user_code' not in session:
        print(f"Error: No administrator is currently logged-in.")
        return jsonify({"Error": "No administrator is currently logged-in."}), 401

    # Get the session 'user_code' key's value
    user_code = session['user_code']

    # Query the 'users' collection in the database for a document with a matching 'User_code'
    user = users.find_one({"User_code": user_code})

    # If the email of the user retrieved is not in the list of admin_emails
    # Return a 403 Forbidden status code
    if user['email'] not in admin_emails:
        print(f"Error: The user currently logged-in is not an administrator.")
        return jsonify({"Error": "The user currently logged-in is not an administrator. Cannot use /admin/* entrypoints"}), 403

    # Retrieve the request data sent by the client
    # If there's no JSON data, it will return None
    data = request.get_json(silent=True)

    # If no data is provided, fetch and return all flights in the database
    if data is None:
        # Fetch all documents in the 'flights' collection
        results = flights.find()
        # Convert the result to a list of dictionaries and return it as a JSON response with a 200 OK status code
        return jsonify([flight for flight in results]), 200

    # If data is provided, retrieve the airport_of_origin, airport_destination and date_of_flight from the data
    airport_of_origin = data.get('airport_of_origin')
    airport_destination = data.get('airport_destination')
    date_of_flight = data.get('date_of_flight')

    # Initialize an empty dictionary to hold search criteria
    search_criteria = {}

    # If airport_of_origin, airport_destination or date_of_flight is provided, add it to the search criteria
    if airport_of_origin:
        search_criteria['airport_of_origin'] = airport_of_origin
    if airport_destination:
        search_criteria['airport_destination'] = airport_destination
    if date_of_flight:
        search_criteria['date_of_flight'] = date_of_flight

    # Fetch documents in the 'flights' collection that match the search criteria
    results = flights.find(search_criteria)
    # Convert the result to a list of dictionaries and return it as a JSON response with a 200 OK status code
    return jsonify([flight for flight in results]), 200

# Define a new route that handles HTTP GET requests to get the details of a specific flight
@app.route('/admin/flight_details/<_id>', methods=['GET'])
def flight_details(_id):
    # Similar to the previous endpoints, we first verify the user's admin status
    if 'user_code' not in session:
        print(f"Error: No administrator is currently logged-in.")
        return jsonify({"Error": "No administrator is currently logged-in."}), 401

    # Get the session 'user_code' key's value
    user_code = session['user_code']

    # Query the 'users' collection in the database for a document with a matching 'User_code'
    user = users.find_one({"User_code": user_code})

    # Check if the email of the user is present in the list of admin_emails
    # If it's not, return a 403 Forbidden status code
    if user['email'] not in admin_emails:
        print(f"Error: The user currently logged-in is not an administrator.")
        return jsonify({"Error": "The user currently logged-in is not an administrator. Cannot use /admin/* entrypoints"}), 403

    # Get the flight details by querying the 'flights' collection for a document with a matching '_id'
    flight = flights.find_one({"_id": _id})

    # If the flight is not found in the collection, return a 404 Not Found status code
    if not flight:
        return jsonify({"Error": "Flight not found"}), 404

    # Find the bookings for this flight by querying the 'bookings' collection for documents with a matching 'flight_id'
    flight_bookings = list(bookings.find({"flight_id": _id}))

    # Calculate the number of economy class bookings by filtering the bookings based on 'seat_class'
    economy_bookings = len([booking for booking in flight_bookings if booking['seat_class'] == 'economy'])
    # Subtract the number of economy bookings from the total to get the number of business class bookings
    business_bookings = len(flight_bookings) - economy_bookings

    # Calculate the total number of tickets for the flight
    total_tickets = int(economy_bookings) + int(business_bookings) + int(flight['business_class_tickets_availability']) + int(flight['economy_class_tickets_availability'])

    # Construct a dictionary containing the flight's information
    flight_info = {
        "Airport of Origin": flight['airport_of_origin'],
        "Airport of Destination": flight['airport_destination'],
        "Total Number of Tickets": total_tickets,
        "Business Class Tickets": int(flight['business_class_tickets_availability']) + int(business_bookings),
        "Economy Class Tickets": int(flight['economy_class_tickets_availability']) + int(economy_bookings),
        "Business Class Ticket Price": flight['business_class_tickets_price'],
        "Economy Class Ticket Price": flight['economy_class_tickets_price'],
        "Business Class Available Tickets": flight['business_class_tickets_availability'],
        "Economy Class Available Tickets": flight['economy_class_tickets_availability'],
    }

    # Initialize an empty list to store the booking details
    booking_details = []

    # Loop through each booking for this flight
    for booking in flight_bookings:
        # Query the 'users' collection for a document with a matching 'User_code'
        user = users.find_one({"User_code": booking['user_code']})
        if user is not None:
            # If the user is found, add their name and seat class to the booking details
            detail = {
                "User Name": user['user_name'] + " " + user['user_surname'],
                "Seat Class": booking['seat_class'],
            }
        else:
            # If the user is not found, use a placeholder string
            detail = {
                "User Name": "Unknown (user may have been deleted)",
                "Seat Class": booking['seat_class'],
            }
        booking_details.append(detail)

    # Return the flight information and booking details as a JSON response with a 200 OK status code
    return jsonify({"Flight Information": flight_info, "Bookings": booking_details}), 200

# Run the Flask application
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

