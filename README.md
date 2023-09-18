
# READ ME

A brief description of how this service works

# DESCRIPTION OF PROJECT
In this service there are two categories of users: (i) administrators, and (ii) ordinary users. Before performing the functions described below, ordinary users of the service must register in the system. The registration allows the introduction of new users in the system who will be classified in the "Simple User" category. The administrator is a user who already exists in the system.  
To register a simple user in the system, the following information is required:  
● Username  
● Username  
● Email  
● Login code  
● Date of birth  
● Country of origin  
● Passport Number  
Note: A new user can register in the system if and only if there is no other user with the same email, and the username is not used by another user. A simple user can perform the following functions:  

● Login to the system: The user enters his email and password and if the information is valid, he is successfully logged into the service. Otherwise, an appropriate message appears prompting the user to enter his data again. Only if a user has successfully logged in can he perform the following functions! Also, an ordinary user can only access the pages that concern ordinary users and NOT those that concern administrators of the service. If a user attempts to enter a page they do not have access to, an appropriate message is being displayed (including the relevant HTTP response code).

● Logout from the system: After the user exits, he does not have access to the functions described below.

● Search flights: A user can search the flights available in the system. The search can be made based on the following information:  
○ Airport of origin and airport of final destination, or  
○ Airport of origin, airport of final destination and date of operation, or  
○ By date, or  
○ Show all available flights  
A list of available flights, their unique codes (_id), date of departure, origin airport and final destination airport is displayed.  

● Show flight details (based on a unique code): For the flight, the date of departure, the airport of origin and the airport of final destination, the available tickets (economy and business), as well as the cost of the tickets for each of the two categories (economy and business) are being displayed.

● Book a ticket (using the unique code of the flight): The user provides the information described below and books a ticket for this flight:  
○ Name  
○ Surname  
○ Passport number  
○ Date of Birth  
○ Email  
○ If the ticket is for business or economy class  

● Show bookings: The bookings made by the specific user are being displayed.

● Display reservation details (based on unique reservation code): The details provided by the user for booking the ticket are being displayed, namely:  
○ Airport of origin  
○ Airport of final destination  
○ Date of the flight  
○ First and last name of person for whom the reservation has been made  
○ Passport number of person for whom the reservation has been made  
○ Date of birth of person booked  
○ Email of person for whom the reservation has been made  
○ If the ticket is for business or economy class  

● Cancellation of reservation (based on unique reservation code): The reservation is canceled and now the number of available tickets for the specific flight is renewed.

● Deletion of his account from the service: After deleting his account, the user can no longer access the service and his information. Reservations made by this user are not affected.

An administrator can perform the following functions:  
● Login to the system: The administrator enters his email, and his password and if the information is valid, he is successfully logged into the service. Otherwise, an appropriate message is being displayed prompting the administrator to enter the information again. Only if an administrator has successfully logged into the system can he perform the following functions!

● Logout: Once logged out, the administrator does not have access to the functions described below.

● Create a flight: The administrator can create a new flight by providing the following information:  
○ Airport of origin  
○ Airport of final destination  
○ Date of flight  
○ Tickets available and costs  
■ For business class  
■ For economy class  

● Update flight ticket prices: The administrator can change the cost of tickets for the two categories (economy and business).

● Flight deletion (based on unique flight code): The administrator can delete a flight only if there are no reservations for that flight.

● Search flights: An administrator can search the flights available in the system. The search can be made based on the following information:  
○ Airport of origin and airport of final destination, or  
○ Airport of origin, airport of final destination and date of operation, or  
○ By date, or  
○ Show all available flights  
A list of available flights, their unique codes (_id), date of departure, origin and final destination is displayed.  

● Display flight details (based on unique flight code): The following details for the specific flight are displayed:  
○ Airport of origin  
○ Airport of final destination  
○ Total number of tickets  
○ Total number of tickets per class (economy and business)  
○ Ticket cost per category  
○ Tickets available  
○ Available tickets per class (economy and business)  
○ For each reservation made on this flight, the first and last name of the person for whom the reservation has been made and the class of the seat reserved.  


The web service has been implemented using Python and the Microframework Flask, which provides the necessary endpoints to its users, so that they can perform the aforementioned functions. The web service that has been implemented is connected to a MongoDB container. Inside, exists the DigitalAirlines database, which stores the related collections, the users, the available flights and the reservations made. The web service has been containerized, while the exact steps to be followed by Docker are described in the Dockerfile to create the image. The docker-compose.yml file has also been created. It connects the two containers (ie the web service and MongoDB) to run together. The database container has a volume in a folder on the host called "data", so that in the event that the container is deleted, data loss is avoided.

Also, the following have been created:  
1. System data flow diagram  
2. Table of risks for the implementation of the system  
3. Proposed Gantt Chart for Information System Implementation Management  



## Database/Flask-Application Initialization
```python
from flask import Flask, request, jsonify, session
from pymongo import MongoClient
import json

client = MongoClient('mongodb://mongodb:27017/')

db = client['DigitalAirlines']

users = db['Users']
flights = db['Flights']
bookings = db['Bookings']

admin_emails = ['admin1@example.com']

app = Flask(__name__)
app.secret_key = 'secret_key'

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

users.delete_one({"User_code": "THIS_IS_TEMP_CODE"})
```
**1. Imports the necessary models from the flask and pymongo packages.  
2. Connects to MongoDB database on port 27017.  
3. Gets the "DigitalAirlines" database from the MongoDB instance.  
4. Gets the collections from the "DigitalAirlines" database.  
5. Creates a list of admin emails, which are banned for normal user registration.  
6. Starts a Flask application and sets a session secret.  
7. Temporarily adds a user to create the "users" collection. If the collection does not exist, this will result in an error and crash, so it creates the collection first.  
8. Creates the system administrator.  
9. If the administrator already exists, it displays a message.  
10. If the administrator does not exist, then it adds it to the database.  
11. Deletes the temporary user, because we don't want unnecessary items in the "users" collection.**

## Endpoints Creation
## /register
```python
@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Could not parse data as json"}), 400

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

    if email in admin_emails:
        print(f"Error: Privileged email cannot be used for user registration.")
        return jsonify({"Error": "Privileged email cannot be used for user registration."}), 403

    if users.find_one({"email": email}):
        print(f"Error: User exists already.")
        return jsonify({"Error": "User exists already."}), 409
    if users.find_one({"user_name": user_name}):
        print(f"Error: User does not exist but user_name is in use.")
        return jsonify({"Error": "Email is available but user_name is in use."}), 409

    user_count = users.count_documents({}) + 1
    user_code = user_name[0] + user_surname[0] + str(user_count).zfill(3)

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

    users.insert_one(new_user)
    
    success_message = f"User registered successfully. Details: Name: {user_name} {user_surname}, Email: {email}, " \
                  f"Date of Birth: {date_of_birth}, Country of Origin: {country_of_origin}, " \
                  f"Passport Number: {passport_number}, User Code: {user_code}"

    print(success_message)
    return jsonify({"Success": "User registered successfully."}), 201
```
**1. At first, on the '/register' endpoint, it receives an HTTP POST request with the new user's data in JSON format.  
2. It tries to parse this data and if it encounters an error, it returns an error message.  
3. Retrieves the user's information from the request data and, if any information is missing, returns an error message.  
4. Checks if the user's email exists in the list of administrators' emails and returns an error message if so.  
5. It then checks if the email or username already exists in the database and returns an error message if so.  
6. Computes a unique user code, creates a dictionary for the new user, and inserts it into the database.  
7. If everything goes well, it returns a success message.**


**Correct json input syntax:**  
```json
{
    "user_name": " ",
    "user_surname": " ",
    "email": " ",
    "login_code": " ",
    "date_of_birth": " ",
    "country_of_origin": " ",
    "passport_number": " "
}
```


## /login
```python
@app.route('/login', methods=['POST'])
def login():
    if 'user_code' in session:
        print(f"Error: A user is currently logged-in. Please log out first.")
        return jsonify({"Error": "A user is currently logged-in. Please log out first."}), 403
    
    try:
        data = request.get_json()
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Could not parse data as json"}), 400

    try:
        email = data['email']
        login_code = data['login_code']
    except:
        return jsonify(print("Error! Missing Field!")), 400

    if email in admin_emails:
        print("Error: Administrators should use the admin login endpoint  -->/admin/login")
        return jsonify({"Error": "Administrators should use the admin login endpoint -->/admin/login"}), 403

    user = users.find_one({"$and": [{"email": email}, {"login_code": login_code}]})
    if user:
        session['user_code'] = user['User_code']
        print(f"Success! User {user['user_name']} {user['user_surname']} Logged-in")
        return jsonify({"Success": f"User {user['user_name']} {user['user_surname']} logged in"}), 200
    else:
        if users.find_one({"email": email}):
            print(f"Error! Wrong login Code for email: {user['email']}. Please try again!")
            return jsonify({"Error": f"Wrong login Code for email: {user['email']}. Please try again!"}), 401
        else:
            print(f"Error: {email} does not exist. Please register first!")
            return jsonify({"Error": f"{email} does not exist. Please register first!"}), 404
```
**1. Checks if there is already a logged in user. If so, it returns an error message.  
2. If not, it tries to parse the HTTP POST request data containing the user's email and login code.  
3. If the user exists in the database and the password is correct, it creates a new session for the user and returns a success message.  
4. If the password is wrong but the email exists, it returns an error message.  
5. If the email does not exist, it returns another error message.**  


**Correct json input syntax:**  
```json
{
    "email": " ",
    "login_code": " "
}
```


## /logout
```python
@app.route('/logout', methods=['POST'])
def logout():
    if 'user_code' not in session:
        print(f"Error: No user is currently logged in.")
        return jsonify({"Error": "No user is currently logged in."}), 401

    user_code = session['user_code']
    user = users.find_one({"User_code": user_code})

    if user is not None and user['email'] in admin_emails:
        print("Error: Administrators should use the admin logout endpoint -->/admin/login")
        return jsonify({"Error": "Administrators should use the admin logout endpoint -->/admin/login"}), 403
    
    session.pop('user_code', None)

    if user is not None:
        print(f"Success! User {user['user_name']} {user['user_surname']} Logged-out")
        return jsonify({"Success": f"User {user['user_name']} {user['user_surname']} logged out"}), 200
    else:
        print(f"Error: The user does not exist in the database.")
        return jsonify({"Error": "The user does not exist in the database."}), 404
```
**1. Checks if there is a logged in user. If not, it returns an error message.  
2. If so, retrieves the user's password from the session and checks if the user is an administrator.  
3. If so, it returns an error message.  
4. If not, it removes the user's password from the session, thus logging the user out.  
5. If the user's details existed in the database, it returns a success message. If not, it returns an error message.**  



## /search_flights
```python
@app.route('/search_flights', methods=['GET'])
def search_flights():
    if 'user_code' not in session:
        print(f"Error: No administrator is currently logged-in.")
        return jsonify({"Error": "No administrator is currently logged-in."}), 401

    data = request.get_json(silent=True)

    if data is None:
        results = flights.find()
        return jsonify([flight for flight in results]), 200

    airport_of_origin = data.get('airport_of_origin')
    airport_destination = data.get('airport_destination')
    date_of_flight = data.get('date_of_flight')

    search_criteria = {}
    if airport_of_origin:
        search_criteria['airport_of_origin'] = airport_of_origin
    if airport_destination:
        search_criteria['airport_destination'] = airport_destination
    if date_of_flight:
        search_criteria['date_of_flight'] = date_of_flight

    results = flights.find(search_criteria)
    return jsonify([flight for flight in results]), 200
```
**1. Checks if an administrator is logged on. If not, it returns an error message.  
2. If so, it tries to parse the request data as JSON.  
3. If there is no request data, it returns all flights in MongoDB's "Flights" collection.  
4. If request data exists, retrieves the search criteria from the data and creates a search query.  
5. Uses the search query to find matching flights in MongoDB's "Flights" collection and returns those flights as a JSON array.**  


**Correct json input syntax (optional):**  
```json
{
    "airport_of_origin": " "
}
```
```json
{
    "airport_destination": " "
}
```
```json
{
    "date_of_flight": " "
}
```


## /display_flight_details/<_id>
```python
@app.route('/display_flight_details/<_id>', methods=['GET'])
def display_flight_details(_id):
    if 'user_code' not in session:
        print(f"Error: No user is currently logged-in.")
        return jsonify({"Error": "No user is currently logged-in."}), 401

    flight = flights.find_one({"_id": _id})

    if not flight:
        return jsonify({"Error": "Flight cannot be found."}), 404

    flight_details = {
        "Date of Departure": flight['date_of_flight'],
        "Airport of Origin": flight['airport_of_origin'],
        "Airport of Destination": flight['airport_destination'],
        "Available Tickets - Business Class": flight['business_class_tickets_availability'],
        "Available Tickets - Economy Class": flight['economy_class_tickets_availability'],
        "Ticket Price - Business Class": flight['business_class_tickets_price'],
        "Ticket Price - Economy Class": flight['economy_class_tickets_price'],
    }

    return jsonify(flight_details), 200
```
**1. Checks if a user is logged in. If not, it returns an error message.  
2. If so, it gets the flight details from the MongoDB "Flights" collection using the given flight ID.  
3. If no flight is found with the given ID, it returns an error message.  
4. Creates a JSON object representing the flight details and returns it.**  


## /book_ticket/<_id>
```python
@app.route('/book_ticket/<_id>', methods=['POST'])
def book_ticket(_id):
    if 'user_code' not in session:
        print(f"Error: No user is currently logged-in.")
        return jsonify({"Error": "No user is currently logged-in."}), 401

    user_code = session['user_code']
    user = users.find_one({"User_code": user_code})

    try:
        data = request.get_json()
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Could not parse data as JSON."}), 400

    try:
        user_name = data['user_name']
        user_surname = data['user_surname']
        passport_number = data['passport_number']
        date_of_birth = data['date_of_birth']
        email = data['email']
        seat_class = data['seat_class']
    except:
        return jsonify({"Error": "Missing Field(s)!"}), 400
    
    if user['user_name'] == user_name and user['user_surname'] == user_surname and user['passport_number'] == passport_number and user['date_of_birth'] == date_of_birth and user['email'] == email:
        print(f"Correct Credentials provided! Continuing with the booking...")
    else:
        return jsonify({"Error": "The credentials you provided the system with, do not match the info saved on your account!"}), 403

    flight = flights.find_one({"_id": _id})

    if not flight:
        return jsonify({"Error": "Flight cannot be found."}), 404

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

    booking_count = bookings.count_documents({}) + 1
    booking_code = user_name[0] + user_surname[0] + _id[0] + _id[1] + seat_class[0].capitalize() + str(booking_count).zfill(3)

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

    bookings.insert_one(new_booking)

    success_message = f"Ticket booked successfully. Details: Name - {user_name}, Surname - {user_surname}, Passport number - {passport_number}, " \
                    f"Date of Birth - {date_of_birth}, Email - {email}, Flight id - {_id}, " \
                    f"Seat Class - {seat_class.capitalize()}, User code - {user_code}, Booking code - {booking_code}"
    print(success_message)
    return jsonify({"Success": "Ticket booked successfully!"}), 201
```
**1. Checks if a user is logged in. If not, it returns an error message.  
2. If so, it gets the user details from MongoDB's "Users" collection.  
3. It tries to parse the request data as JSON. If these are not JSON, it returns an error message.  
4. Retrieves the booking details from the application data. If any detail is missing, it returns an error message.  
5. Verifies that the booking details match the user details. If not, it returns an error message.  
6. Gets the flight details from the MongoDB "Flights" collection using the given flight ID.  
7. Checks if there are tickets available for the category chosen by the user (business or economy). If there are, it decrements the number of available tickets by 1. If there are no tickets available, it returns an error message.  
8. Creates a unique reservation code and a new JSON object for the reservation.  
9. Inserts the new booking into MongoDB's "Bookings" collection.  
10. Returns a success message.**  


**Correct json input syntax:**  
```json
{
    "user_name": " ",
    "user_surname": " ",
    "email": " ",
    "country_of_origin": " ",
    "passport_number": " ",
    "seat_class": "economy"
}
```


## /bookings
```python
@app.route('/bookings', methods=['GET'])
def show_bookings():
    if 'user_code' not in session:
        print(f"Error: No user is currently logged-in.")
        return jsonify({"Error": "No user is currently logged-in."}), 401

    user_code = session['user_code']

    user_bookings = bookings.find({"user_code": user_code})

    if user_bookings is None:
        # In this case, a JSON message is sent back to the client indicating that no bookings were found.
        return jsonify({"Message": "No bookings found for the user."}), 200

    bookings_data = []

    for booking in user_bookings: from the booking.
        flight = flights.find_one({"_id": booking['flight_id']})

        data = {
            "booking_code": booking.get('booking_code', ''),
            "flight_id": booking.get('flight_id', ''),
            "user_name": booking.get('user_name', ''),
            "user_surname": booking.get('user_surname', ''),
            "passport_number": booking.get('passport_number', ''),
            "date_of_birth": booking.get('date_of_birth', ''),
            "email": booking.get('email', ''),
            "seat_class": booking.get('seat_class', ''),
            "flight_details": {
                "origin": flight.get('airport_of_origin', ''),
                "destination": flight.get('airport_destination', ''),
                "date": flight.get('date_of_flight', '')
            }
        }

        bookings_data.append(data)

    return jsonify({"Bookings": bookings_data}), 200
```
**1. Checks if a user is logged in. If not, it returns an error message.  
2. If so, it gets the user's password from the session variable.  
3. Performs a find operation on MongoDB's "bookings" collection to get all bookings where 'user_code' matches the logged in user's code.  
4. If no reservations were found for the user, it returns a JSON message indicating that no reservations were found.  
5. If reservations are found, an empty list is initialized to contain the reservation data.  
6. Gets each booking's details and flight details from the 'flights' collection using the flight ID from the booking.  
7. Combines reservation data and flight data into a single dictionary.  
8. Adds the single reservation and flight data dictionary to the reservation data list.  
9. Returns the list of booking data to the client in JSON format.**  
 


## /show_booking_details/<booking_code>
```python
@app.route('/show_booking_details/<booking_code>', methods=['GET'])
def show_booking_details(booking_code):
    if 'user_code' not in session:
        # If not, it logs an error and sends a 401 Unauthorized response with an error message.
        print(f"Error: No user is currently logged-in.")
        return jsonify({"Error": "No user is currently logged-in."}), 401

    user_code = session['user_code']
    user = users.find_one({"User_code": user_code})

    booking = bookings.find_one({"booking_code": booking_code})

    if not booking:
        return jsonify({"Error": "Booking cannot be found."}), 404

    if booking['email'] != user['email']:
        print(user['email'])
        print(booking['email'])
        print(f"Error: This booking was not made by the logged-in user.")
        return jsonify({"Error": "This booking was not made by the logged-in user."}), 403

    flight = flights.find_one({"_id": booking['flight_id']})

    if not flight:
        return jsonify({"Error": "Flight cannot be found."}), 404

    data = {
        "booking_code": booking['booking_code'],
        "flight_id": booking['flight_id'],
        "user_name": booking['user_name'],
        "user_surname": booking['surname'],
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
```
**1. Checks if a user is logged in. If not, it returns an error message.  
2. If so, it gets the user's password from the session variable.  
3. Performs a find operation on MongoDB's "bookings" collection to find the booking with the given code.  
4. If the reservation is not found, it returns an error message.  
5. If the reservation is found, it checks if it belongs to the logged in user. If not, it returns an error message.  
6. If the reservation belongs to the user, it finds the flight details from the 'flights' collection and joins them with the reservation details in a dictionary.  
7. Finally, it returns the dictionary to the user in JSON format.**  



## /cancel_flight/<booking_code>
```python
@app.route('/cancel_flight/<booking_code>', methods=['POST'])
def cancel_flight(booking_code):
    if 'user_code' not in session:
        print(f"Error: No user is currently logged-in.")
        return jsonify({"Error": "No user is currently logged-in."}), 401

    user_code = session['user_code']

    booking = bookings.find_one({"booking_code": booking_code})

    if not booking:
        return jsonify({"Error": "Booking cannot be found."}), 404

    if booking['user_code'] != user_code:
        print(f"Error: This booking was not made by the logged-in user.")
        return jsonify({"Error": "This booking was not made by the logged-in user."}), 403

    flight = flights.find_one({"_id": booking['flight_id']})

    if not flight:
        return jsonify({"Error": "Flight cannot be found."}), 404

    if booking['seat_class'] == 'economy':
        flight = flights.find_one({"_id": booking['flight_id']})
        economy_class_tickets_availability = int(flight['economy_class_tickets_availability']) + 1
        flights.update_one({"_id": booking['flight_id']}, {"$set": {"economy_class_tickets_availability": economy_class_tickets_availability}})
    elif booking['seat_class'] == 'business':
        flight = flights.find_one({"_id": booking['flight_id']})
        business_class_tickets_availability = int(flight['business_class_tickets_availability']) + 1
        flights.update_one({"_id": booking['flight_id']}, {"$set": {"business_class_tickets_availability": business_class_tickets_availability}})
    
    bookings.delete_one({"_id": booking_code})

    return jsonify({"Success": "Booking cancelled successfully."}), 202
```
**1. It follows a similar process to the '/show_booking_details/<booking_code>' endpoint.  
2. If the reservation is found and belongs to the user, it increases the number of available seats on the flight according to the ticket category of the reservation (economy or business).  
3. It then deletes the booking from the 'bookings' collection.  
4. Finally, it returns a success message to the user.**  



## /delete_account
```python
@app.route('/delete_account', methods=['DELETE'])
def delete_account():
    if 'user_code' not in session:
        print(f"Error: No user is currently logged-in.")
        return jsonify({"Error": "No user is currently logged-in."}), 401

    user_code = session['user_code']

    user = users.find_one({"User_code": user_code})

    if not user:
        return jsonify({"Error": "User cannot be found."}), 404
    users.delete_one({"User_code": user_code})

    session.pop('user_code', None)

    return jsonify({"Success": "Account deleted successfully."}), 204
```
**1. Checks if a user is logged in. If not, it returns an error message.  
2. If so, it finds the user in the 'users' collection and deletes it.  
3. Removes the user's password from the session variable, logging the user out.  
4. Finally, it returns a success message to the user.**  



## /admin/login
```python
@app.route('/admin/login', methods=['POST'])
def admin_login():
    if 'user_code' in session:
        print(f"Error: A user is currently logged-in. Please log out first.")
        return jsonify({"Error": "A user is currently logged-in. Please log out first."}), 403
    
    try:
        data = request.get_json()
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Could not parse data as json"}), 400

    try:
        email = data['email']
        login_code = data['login_code']
    except:
        return jsonify(print("Error! Missing Field!")), 400

    if email not in admin_emails:
        print("Error: Users should use the user login endpoint  -->/login")
        return jsonify({"Error": "Users should use the user login endpoint  -->/login"}), 403

    user = users.find_one({"$and": [{"email": email}, {"login_code": login_code}]})
    if user:
        session['user_code'] = user['User_code']
        print(f"Success! Administrator {user['user_name']} {user['user_surname']} Logged-in")
        return jsonify({"Success": f"Administrator {user['user_name']} {user['user_surname']} logged in"}), 200
    else:
        if users.find_one({"email": email}):
            print(f"Error! Wrong login Code for email: {email}. Please try again!")
            return jsonify({"Error": f"Wrong login Code for email: {email}. Please try again!"}), 401
        else:
            print(f"Error: {email} does not exist. Wrong Admin Credentials!")
            return jsonify({"Error": f"{email} does not exist. Wrong Admin Credentials!"}), 404
```
**1. Checks if a user is already logged in to the session. If so, it displays an error message and returns a 403 error.  
2. It tries to parse the request data as JSON. If it fails, it displays an error message and returns a 400 error.  
3. Extracts the email and login code from the application data. If any of these are missing, it returns an error message and a 400 error.  
4. Checks if the email does not belong to the administrator. If so, it displays an error message and returns a 403 error.  
5. Checks if the user exists with the given email and password. If so, it connects the user and creates a new session.  
6. If the input code is incorrect but the email exists in the database, it returns an error.  
7. If the email does not exist in the database, it returns an error.**  


**Correct json input syntax:**  
```json
{
    "email": "admin1@example.com",
    "login_code": "3364"
}
```


## /admin/logout
```python
@app.route('/admin/logout', methods=['POST'])
def admin_logout():
    if 'user_code' not in session:
        print(f"Error: No administrator is currently logged-in.")
        return jsonify({"Error": "No administrator is currently logged-in."}), 401

    user_code = session['user_code']
    
    user = users.find_one({"User_code": user_code})
    
    if user['email'] not in admin_emails:
        print(f"Error: The user currently logged-in is not an administrator.")
        return jsonify({"Error": "The user currently logged-in is not an administrator. Use request --> /logout instead"}), 403

    session.pop('user_code', None)
    
    print(f"Success! Administrator {user['user_name']} {user['user_surname']} logged-out")
    return jsonify({"Success": f"Administrator {user['user_name']} {user['user_surname']} logged-out"}), 200
```
**1. The admin_logout() function reacts to an HTTP POST request to the path /admin/logout.  
2. First, it checks if user_code exists in the current session. If not, no administrator is logged in, and a 401 error is returned.  
3. If user_code exists, retrieve it from the session.  
4. It then looks up the user from the users collection based on user_code.  
5. Checks if the user is an admin by checking if the user's email is in the admin_emails list.  
6. If the email is not in the list, the user is not an administrator, and a 403 error is returned.  
7. If the user is an administrator, then it is "logged out", removing the user_code from the session.  
8. Finally, a success message is returned indicating that the administrator has successfully logged out.**  



## /admin/create_flight
```python
@app.route('/admin/create_flight', methods=['POST'])
def create_flight():
    if 'user_code' not in session:
        print(f"Error: No administrator is currently logged-in.")
        return jsonify({"Error": "No administrator is currently logged-in."}), 401

    user_code = session['user_code']
    user = users.find_one({"User_code": user_code})
   
    if user['email'] not in admin_emails:
        print(f"Error: The user currently logged-in is not an administrator.")
        return jsonify({"Error": "The user currently logged-in is not an administrator. Cannot use /admin/* entrypoints"}), 403

    try:
        data = request.get_json()
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Could not parse data as JSON."}), 400

    try:
        airport_of_origin = data['airport_of_origin']
        airport_destination = data['airport_destination']
        date_of_flight = data['date_of_flight']
        business_class_tickets_availability = data['business_class_tickets_availability']
        economy_class_tickets_availability = data['economy_class_tickets_availability']
        business_class_tickets_price = data['business_class_tickets_price']
        economy_class_tickets_price = data['economy_class_tickets_price']
    except:
        return jsonify(print("Error! Missing Field(s)!")), 400

    flight_count = flights.count_documents({}) + 1
    _id = airport_of_origin[0] + airport_destination[0] + str(flight_count).zfill(3)

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

    flights.insert_one(new_flight)
    
    success_message = f"Flight registered successfully. Details: Flying from {airport_of_origin} to {airport_destination} at {date_of_flight}, " \
                  f"Business_class: {business_class_tickets_availability} available tickets priced at: {business_class_tickets_price} EUR each, " \
                  f"Economy_class: {economy_class_tickets_availability} available tickets priced at: {economy_class_tickets_price} EUR each," \
                  f"Unique flight id (_id): {_id}"

    print(success_message)
    return jsonify({"Success": "Flight Added Successfully."}), 201
```
**1. The create_flight() function responds to an HTTP POST request to the path /admin/create_flight.  
2. It first checks if user_code exists in the session, i.e. if a user is logged in. If user_code does not exist, it returns a 401 error, stating that no administrator is currently logged in.  
3. If user_code exists, retrieves it from the session and looks for the user in the users collection.  
4. Checks if the logged in user is an admin, i.e. if the user's email is in the admin_emails list. If not found, it returns a 403 error.  
5. It then tries to parse the request data as JSON. If the data is not formatted correctly, it returns a 400 error.  
6. If the request data is properly formatted as JSON, it tries to retrieve the necessary fields. If a field is missing, it returns a 400 error.  
7. Counts the flights in the flights collection and uses that number to generate a unique ID for the new flight.  
8. Creates a new flight document using the data retrieved from the request.  
9. Inserts the new flight into the flights collection.  
10. Returns a success message indicating that the flight has been created successfully.**  


**Correct json input syntax:**  
```json
{
  "airport_of_origin": " ",
  "airport_destination": " ",
  "date_of_flight": " ",
  "business_class_tickets_availability": " ",
  "economy_class_tickets_availability": " ",
  "business_class_tickets_price": " ",
  "economy_class_tickets_price": " "
}
```


## /admin/renew_ticket_prices/<_id>
```python
@app.route('/admin/renew_ticket_prices/<_id>', methods=['POST'])
def renew_ticket_prices(_id):
    if 'user_code' not in session:
        print(f"Error: No administrator is currently logged-in.")
        return jsonify({"Error": "No administrator is currently logged-in."}), 401

    user_code = session['user_code']

    user = users.find_one({"User_code": user_code})

    if user['email'] not in admin_emails:
        print(f"Error: The user currently logged-in is not an administrator.")
        return jsonify({"Error": "The user currently logged-in is not an administrator. Cannot use /admin/* entrypoints"}), 403

    try:
        data = request.get_json()
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"Error": "Could not parse data as JSON."}), 400

    try:
        new_business_class_ticket_price = data['business_class_tickets_price']
        new_economy_class_ticket_price = data['economy_class_tickets_price']
    except:
        return jsonify(print("Error! Missing Field(s)!")), 400

    flight = flights.find_one({"_id": _id})

    if not flight:
        return jsonify({"Error": "Flight cannot be found."}), 404

    flights.update_one({"_id": _id}, {"$set": {
        "business_class_tickets_price": new_business_class_ticket_price,
        "economy_class_tickets_price": new_economy_class_ticket_price,
    }})

    flight = flights.find_one({"_id": _id})
    
    success_message = f"Flight prices changed successfully. Details: Flying from {flight['airport_of_origin']} to {flight['airport_destination']} at {flight['date_of_flight']}, " \
                      f"Business_class: {flight['business_class_tickets_availability']} available tickets priced at: {flight['business_class_tickets_price']} EUR each, " \
                      f"Economy_class: {flight['economy_class_tickets_availability']} available tickets priced at: {flight['economy_class_tickets_price']} EUR each," \
                      f"Unique flight id (_id): {_id}"
    print(success_message)

    return jsonify({"Success": "Flight prices updated successfully."}), 200
```
**1. Checks if an administrator is logged in by checking the 'user_code' in the session. If not, it returns an error message.  
2. Checks if the logged in user is an administrator by checking their email in the list of administrators' emails. If not, it returns an error message.  
3. Tries to parse the request data as JSON. If it fails, it returns an error message.  
4. Extracts the new ticket prices from the request data.  
5. Checks if there is a flight with the given '_id'. If not, it returns an error message.  
6. If the flight exists, it updates its ticket prices in the database.  
7. Returns a success message to the administrator.**  


**Correct json input syntax:**  
```json
{
  "business_class_tickets_price": " ",
  "economy_class_tickets_price": " "
}
```

## /admin/delete_flight/<_id>
```python
@app.route('/admin/delete_flight/<_id>', methods=['DELETE'])
def delete_flight(_id):
    if 'user_code' not in session:
        print(f"Error: No administrator is currently logged-in.")
        return jsonify({"Error": "No administrator is currently logged-in."}), 401

    user_code = session['user_code']

    user = users.find_one({"User_code": user_code})

    if user['email'] not in admin_emails:
        print(f"Error: The user currently logged-in is not an administrator.")
        return jsonify({"Error": "The user currently logged-in is not an administrator. Cannot use /admin/* entrypoints"}), 403

    flight = flights.find_one({"_id": _id})

    if not flight:
        return jsonify({"Error": "Flight cannot be found."}), 404

    booking = bookings.find_one({"flight_id": _id})

    if booking:
        return jsonify({"Error": "Cannot delete this flight as there are existing ticket bookings."}), 409

    flights.delete_one({"_id": _id})

    success_message = f"Flight with id {_id} deleted successfully. Details: Flying from {flight['airport_of_origin']} to {flight['airport_destination']} at {flight['date_of_flight']}, " \
                      f"Business_class: {flight['business_class_tickets_availability']} available tickets priced at: {flight['business_class_tickets_price']} EUR each, " \
                      f"Economy_class: {flight['economy_class_tickets_availability']} available tickets priced at: {flight['economy_class_tickets_price']} EUR each."

    print(success_message)

    return jsonify({"Success": "Flight deleted successfully."}), 204
```
**1. Checks if an administrator is already logged in by checking for the existence of 'user_code' in the session. If not, it returns an error message.  
2. Checks if the logged in user's email is in the list of administrators' emails. If not, it returns an error message.  
3. Searches for the flight with the given '_id' in the database. If not found, it returns an error message.  
4. Checks if there are reservations for the flight. If so, it returns an error message and does not delete the flight.  
5. If there are no reservations, it deletes the flight from the database.  
6. Returns a success message.**  



## /admin/search_flights
```python
@app.route('/admin/search_flights', methods=['GET'])
def admin_search_flights():
    if 'user_code' not in session:
        print(f"Error: No administrator is currently logged-in.")
        return jsonify({"Error": "No administrator is currently logged-in."}), 401

    user_code = session['user_code']

    user = users.find_one({"User_code": user_code})

    if user['email'] not in admin_emails:
        print(f"Error: The user currently logged-in is not an administrator.")
        return jsonify({"Error": "The user currently logged-in is not an administrator. Cannot use /admin/* entrypoints"}), 403

    data = request.get_json(silent=True)

    if data is None:
        return jsonify([flight for flight in results]), 200

    airport_of_origin = data.get('airport_of_origin')
    airport_destination = data.get('airport_destination')
    date_of_flight = data.get('date_of_flight')

    search_criteria = {}

    if airport_of_origin:
        search_criteria['airport_of_origin'] = airport_of_origin
    if airport_destination:
        search_criteria['airport_destination'] = airport_destination
    if date_of_flight:
        search_criteria['date_of_flight'] = date_of_flight

    results = flights.find(search_criteria)
    return jsonify([flight for flight in results]), 200
```
**1. Checks if an administrator is logged on.  
2. Checks if the logged in user is an administrator.  
3. Searches for flights based on the request data (origin airport, destination airport, flight date).  
4. Returns flights matching the criteria.**  


**Correct json input syntax (optional):**  
```json
{
    "airport_of_origin": " "
}
```
```json
{
    "airport_destination": " "
}
```
```json
{
    "date_of_flight": " "
}
```


## /admin/flight_details/<_id>
```python
@app.route('/admin/flight_details/<_id>', methods=['GET'])
def flight_details(_id):
    if 'user_code' not in session:
        print(f"Error: No administrator is currently logged-in.")
        return jsonify({"Error": "No administrator is currently logged-in."}), 401

    user_code = session['user_code']

    user = users.find_one({"User_code": user_code})

    if user['email'] not in admin_emails:
        print(f"Error: The user currently logged-in is not an administrator.")
        return jsonify({"Error": "The user currently logged-in is not an administrator. Cannot use /admin/* entrypoints"}), 403

    flight = flights.find_one({"_id": _id})

    if not flight:
        return jsonify({"Error": "Flight not found"}), 404

    flight_bookings = list(bookings.find({"flight_id": _id}))

    economy_bookings = len([booking for booking in flight_bookings if booking['seat_class'] == 'economy'])
    business_bookings = len(flight_bookings) - economy_bookings

    total_tickets = int(economy_bookings) + int(business_bookings) + int(flight['business_class_tickets_availability']) + int(flight['economy_class_tickets_availability'])

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

    booking_details = []

    for booking in flight_bookings:
        user = users.find_one({"User_code": booking['user_code']})
        if user is not None:
            detail = {
                "User Name": user['user_name'] + " " + user['user_surname'],
                "Seat Class": booking['seat_class'],
            }
        else:
            detail = {
                "User Name": "Unknown (user may have been deleted)",
                "Seat Class": booking['seat_class'],
            }
        booking_details.append(detail)

    return jsonify({"Flight Information": flight_info, "Bookings": booking_details}), 200

```
**1. Checks if an administrator is logged on.  
2. Checks if the logged in user is an administrator.  
3. Searches for the flight with the given '_id' in the database. If not found, it returns an error message.  
4. Searches for flight reservations and returns flight and reservation details.**  



## Dockerfile
```bash
FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install flask pymongo
RUN mkdir /app
RUN mkdir -p /app/data
COPY Airline_Service.py /app/Airline_Service.py
ADD data /app/data
EXPOSE 5000
WORKDIR /app
ENTRYPOINT [ "python3","-u", "Airline_Service.py" ]
```
## docker-compose.yml
```bash
version: '3'
services:
  mongodb:
    image: mongo
    restart: always
    container_name: mongodb
    ports:
    - 27017:27017
    volumes:
    - ./mongodb/data:/data/db
  flask-service:
    build:
      context: .
    restart: always
    container_name: flask
    depends_on:
      - mongodb
    ports:
      - 5000:5000
    environment:
      - "MONGO_HOSTNAME=mongodb"
```
## How To Set Up

**Step 1:**
In the same folder we have the following:
| Airline_Service.py | Dockerfile | docker-compose.yml | data (κενός φάκελος) |
| :----------------- | :--------- | :----------------- | :------------------- |

**Step 2:**
We go to the correct PATH of the folder with the files and then run:  
```bash
$ sudo docker-compose build
```
```bash
$ sudo docker-compose up
```

**Step 3:**
After both containers are started, we send requests via POSTMAN to use the service.
In POSTMAN we send the requests to the address: **http://0.0.0.0:5000**


**Highly Reccomended:** Run the following commands 
```bash
$ sudo iptables -A INPUT -p tcp --dport 27017 -j ACCEPT
```
This command uses iptables, a user program that allows a system administrator to configure the IP packet filter rules of the Linux kernel firewall.

**-A INPUT adds a rule to the INPUT chain. The INPUT chain is used to control the behavior for incoming connections.
-p tcp specifies that the rule is applied to TCP traffic.
--dport 27017 specifies the destination port, which in this case is 27017.
-j ACCEPT means that if the packet matches the rule, it should be accepted and not checked against other rules in the chain.**

```bash
$ sudo ufw allow 27017
```
This command uses ufw (Uncomplicated Firewall), an interface to iptables that aims to simplify the process of setting up a firewall.
Adds a rule that allows inbound traffic on port 27017.

**Note**
I ran ``sudo docker-compose build'' and ``sudo docker-compose up'' with the files in an ``InfoSys'' folder on the desktop in my VM, and zipped the new ``InfoSys'' folder to **ALREADY_BUILT .zip** to see exactly what is produced. In the .zip are the files I had together with the ones created after successfully running docker-compose and creating the pair of containers.

## Run Locally
To run the code locally on your computer you need the following steps:   

**1. Change line 7 from:**
```python
client = MongoClient('mongodb://mongodb:27017/')
```
**to**  
```python
client = MongoClient('localhost:27017')
```

**2. Create a container using the commands:** 
```bash
docker pull mongo
```
```bash
docker run -d -p 27017:27017 --name mongodb mongo
```

**3. Run Airline_Services.py** 

**4. Send correct Requests via POSTMAN to the address: http://0.0.0.0:5000**
## Authors

- [@Vaioskn](https://github.com/Vaioskn)

