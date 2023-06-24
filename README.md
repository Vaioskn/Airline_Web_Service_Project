
# READ ME

A brief description of how this service works


## Read By

This file will be read by the following parties:

**- csymvoul**

**- jdtotow**


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
**1. Εισάγει τα απαραίτητα μοντέλα από τα πακέτα flask και pymongo.  
2. Συνδέεται με τη βάση δεδομένων MongoDB στη θύρα 27017.  
3. Λαμβάνει τη βάση δεδομένων "DigitalAirlines" από την παρουσία MongoDB.  
4. Λαμβάνει τις συλλογές από τη βάση δεδομένων "DigitalAirlines".  
5. Δημιουργεί μια λίστα με τα email των διαχειριστών, οι οποίοι απαγορεύονται για την κανονική εγγραφή χρηστών.  
6. Εκκινεί μια εφαρμογή Flask και ορίζει ένα μυστικό κλειδί για τις συνεδρίες.  
7. Προσωρινά προσθέτει έναν χρήστη για να δημιουργήσει τη συλλογή "users". Αν η συλλογή δεν υπάρχει, αυτό θα οδηγήσει σε σφάλμα και κατάρρευση, επομένως πρώτα δημιουργεί τη συλλογή.  
8. Δημιουργεί τον διαχειριστή του συστήματος.  
9. Αν ο διαχειριστής υπάρχει ήδη, εμφανίζει ένα μήνυμα.  
10. Αν ο διαχειριστής δεν υπάρχει, τότε τον προσθέτει στη βάση δεδομένων.  
11. Διαγράφει τον προσωρινό χρήστη, επειδή δεν θέλουμε περιττά στοιχεία στη συλλογή "users".**

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
**1. Στην αρχή, στο τερματικό σημείο '/register', λαμβάνει μια αίτηση HTTP POST με τα δεδομένα του νέου χρήστη σε μορφή JSON.  
2. Προσπαθεί να αναλύσει τα δεδομένα αυτά και εάν συναντήσει κάποιο σφάλμα, επιστρέφει ένα μήνυμα λάθους.  
3. Ανακτά τα στοιχεία του χρήστη από τα δεδομένα της αίτησης και, εάν λείπει κάποιο στοιχείο, επιστρέφει ένα μήνυμα λάθους.  
4. Ελέγχει αν το email του χρήστη υπάρχει στη λίστα των email των διαχειριστών και, αν ναι, επιστρέφει μήνυμα λάθους.  
5. Έπειτα, ελέγχει αν το email ή το όνομα χρήστη υπάρχει ήδη στη βάση δεδομένων και, αν ναι, επιστρέφει μήνυμα λάθους.  
6. Υπολογίζει έναν μοναδικό κωδικό χρήστη, δημιουργεί ένα λεξικό για τον νέο χρήστη και τον εισάγει στη βάση δεδομένων.  
7. Εάν όλα πάνε καλά, επιστρέφει ένα μήνυμα επιτυχίας.**


**Σωστή σύνταξη json input:**
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
**Παραδείγματα:**

![1](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/16463cc6-c6f1-4b29-8e0f-90ca05b3ef63)

![2](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/e717f902-5467-4f59-848b-279fb2c75656)


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
**1. Ελέγχει αν υπάρχει ήδη συνδεδεμένος χρήστης. Αν ναι, επιστρέφει μήνυμα λάθους.  
2. Αν όχι, προσπαθεί να αναλύσει τα δεδομένα της αίτησης HTTP POST που περιέχουν το email και τον κωδικό σύνδεσης του χρήστη.  
3. Εάν ο χρήστης υπάρχει στη βάση δεδομένων και ο κωδικός είναι σωστός, δημιουργεί νέα σύνοδο για τον χρήστη και επιστρέφει μήνυμα επιτυχίας.  
4. Αν ο κωδικός είναι λάθος αλλά το email υπάρχει, επιστρέφει μήνυμα λάθους.  
5. Αν το email δεν υπάρχει, επιστρέφει ένα άλλο μήνυμα λάθους.**


**Σωστή σύνταξη json input:**
```json
{
    "email": " ",
    "login_code": " "
}
```
**Παραδείγματα:**

![1](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/19388a52-2878-4741-8fb8-806d3ac13240)

![2](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/38c89b21-f6ab-4c70-aa62-91d90caaf89b)

![3](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/1be05d7a-e886-4cf5-9bca-f0b6844f8e2c)

![4](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/1baec856-b211-4091-9536-880d3b886f71)


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
**1. Ελέγχει αν υπάρχει συνδεδεμένος χρήστης. Αν όχι, επιστρέφει μήνυμα λάθους.  
2. Αν ναι, ανακτά τον κωδικό του χρήστη από τη σύνοδο και ελέγχει αν ο χρήστης είναι διαχειριστής.  
3. Αν ναι, επιστρέφει μήνυμα λάθους.  
4. Αν όχι, αφαιρεί τον κωδικό του χρήστη από τη σύνοδο, αποσυνδέοντας έτσι τον χρήστη.  
5. Αν τα στοιχεία του χρήστη υπήρχαν στη βάση δεδομένων, επιστρέφει μήνυμα επιτυχίας. Αν όχι, επιστρέφει μήνυμα λάθους.**


**Παραδείγματα:**

![3](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/7c1f74a1-163e-4adc-807d-d62ae7d3d81b)


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
**1. Ελέγχει αν ένας διαχειριστής είναι συνδεδεμένος. Αν όχι, επιστρέφει μήνυμα λάθους.  
2. Αν ναι, προσπαθεί να αναλύσει τα δεδομένα της αίτησης ως JSON.  
3. Εάν δεν υπάρχουν δεδομένα αίτησης, επιστρέφει όλες τις πτήσεις στη συλλογή "Flights" της MongoDB.  
4. Αν υπάρχουν δεδομένα αίτησης, ανακτά τα κριτήρια αναζήτησης από τα δεδομένα και δημιουργεί μια ερώτηση αναζήτησης.  
5. Χρησιμοποιεί την ερώτηση αναζήτησης για να βρει τις αντίστοιχες πτήσεις στη συλλογή "Flights" της MongoDB και επιστρέφει αυτές τις πτήσεις ως έναν πίνακα JSON.**


**Σωστή σύνταξη json input (προαιρετική):**
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
**Παραδείγματα:**

![4](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/9080b2b2-b826-4808-8406-4eede3413731)

![5](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/cd9ca724-125f-4d8b-aba4-e953747da1af)

![6](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/c8762e8c-9ded-4757-bfbd-db0517bcb463)

![7](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/4a798a45-6729-425e-8430-a429473c155a)

![8](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/6235799f-4344-44b8-822c-57121b143415)


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
**1. Ελέγχει αν ένας χρήστης είναι συνδεδεμένος. Αν όχι, επιστρέφει μήνυμα λάθους.  
2. Αν ναι, παίρνει τις λεπτομέρειες της πτήσης από τη συλλογή "Flights" της MongoDB χρησιμοποιώντας το δοθέν ID της πτήσης.  
3. Αν δεν βρέθηκε πτήση με το δοθέν ID, επιστρέφει μήνυμα λάθους.  
4. Δημιουργεί ένα αντικείμενο JSON που αναπαριστά τις λεπτομέρειες της πτήσης και το επιστρέφει.**


**Παραδείγματα:**

![9](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/755621b8-19f9-4b7d-9554-27b1453ecb8e)

![10](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/351891e2-e27c-4a60-953f-5612ad688545)


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
**1. Ελέγχει αν ένας χρήστης είναι συνδεδεμένος. Αν όχι, επιστρέφει μήνυμα λάθους.  
2. Αν ναι, παίρνει τις λεπτομέρειες του χρήστη από τη συλλογή "Users" της MongoDB.  
3. Προσπαθεί να αναλύσει τα δεδομένα της αίτησης ως JSON. Αν αυτά δεν είναι JSON, επιστρέφει μήνυμα λάθους.  
4. Ανακτά τις λεπτομέρειες της κράτησης από τα δεδομένα της αίτησης. Αν λείπει κάποια λεπτομέρεια, επιστρέφει μήνυμα λάθους.  
5. Επαληθεύει ότι οι λεπτομέρειες της κράτησης ταιριάζουν με τις λεπτομέρειες του χρήστη. Αν όχι, επιστρέφει μήνυμα λάθους.  
6. Παίρνει τις λεπτομέρειες της πτήσης από τη συλλογή "Flights" της MongoDB χρησιμοποιώντας το δοθέν ID της πτήσης.  
7. Ελέγχει αν υπάρχουν διαθέσιμα εισιτήρια για την κατηγορία που επέλεξε ο χρήστης (business ή economy). Αν υπάρχουν, μειώνει τον αριθμό των διαθέσιμων εισιτηρίων κατά 1. Αν δεν υπάρχουν διαθέσιμα εισιτήρια, επιστρέφει μήνυμα λάθους.  
8. Δημιουργεί ένα μοναδικό κωδικό κράτησης και ένα νέο αντικείμενο JSON για την κράτηση.  
9. Εισάγει τη νέα κράτηση στη συλλογή "Bookings" της MongoDB.  
10. Επιστρέφει ένα μήνυμα επιτυχίας.**


**Σωστή σύνταξη json input:**
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
**Παραδείγματα:**

![11](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/c8567ed3-90cd-45a6-9c75-9c79c21b1142)

![12](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/ae9fe115-8ce7-483d-ab6b-82a59b8343e8)

![13](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/d0abfac3-92fa-47ab-9b15-57d5ad3d21af)

![14](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/494f35f3-1bc5-4189-be0b-811fadf7aa23)


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
**1. Ελέγχει αν ένας χρήστης είναι συνδεδεμένος. Αν όχι, επιστρέφει μήνυμα λάθους.  
2. Αν ναι, παίρνει τον κωδικό του χρήστη από τη μεταβλητή session.  
3. Εκτελεί μια λειτουργία εύρεσης στη συλλογή "bookings" της MongoDB για να πάρει όλες τις κρατήσεις όπου ο 'user_code' ταιριάζει με τον κωδικό του συνδεδεμένου χρήστη.  
4. Αν δεν βρέθηκαν κρατήσεις για τον χρήστη, επιστρέφει ένα μήνυμα JSON που υποδηλώνει ότι δεν βρέθηκαν κρατήσεις.  
5. Αν βρέθηκαν κρατήσεις, αρχικοποιείται μια κενή λίστα για να περιέχει τα δεδομένα των κρατήσεων.  
6. Παίρνει τα στοιχεία κάθε κράτησης και τα στοιχεία της πτήσης από τη συλλογή 'flights' χρησιμοποιώντας το ID της πτήσης από την κράτηση.  
7. Συνδυάζει τα δεδομένα της κράτησης και τα δεδομένα της πτήσης σε ένα ενιαίο λεξικό.  
8. Προσθέτει το ενιαίο λεξικό κρατήσεων και δεδομένων πτήσεων στη λίστα δεδομένων κρατήσεων.  
9. Επιστρέφει τη λίστα δεδομένων κρατήσεων στον πελάτη σε μορφή JSON.**


**Παραδείγματα:**

![15](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/615ab49a-112b-4ed0-b2a9-6d61be9685b6)


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
**1. Ελέγχει αν ένας χρήστης είναι συνδεδεμένος. Αν όχι, επιστρέφει μήνυμα λάθους.  
2. Αν ναι, παίρνει τον κωδικό του χρήστη από τη μεταβλητή session.  
3. Εκτελεί μια λειτουργία εύρεσης στη συλλογή "bookings" της MongoDB για να βρει την κράτηση με τον κωδικό που δόθηκε.  
4. Αν η κράτηση δεν βρεθεί, επιστρέφει μήνυμα λάθους.  
5. Αν βρεθεί η κράτηση, ελέγχει αν ανήκει στον συνδεδεμένο χρήστη. Αν όχι, επιστρέφει μήνυμα λάθους.  
6. Αν η κράτηση ανήκει στον χρήστη, βρίσκει τα στοιχεία της πτήσης από τη συλλογή 'flights' και τα ενώνει με τα στοιχεία της κράτησης σε ένα λεξικό.  
7. Τέλος, επιστρέφει το λεξικό στον χρήστη σε μορφή JSON.**



**Παραδείγματα:**

![16](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/ed320482-c814-446d-95fa-7c9ee4fe7299)

![17](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/a6dad0e8-3dc9-4e62-a64c-2b05eefd7fc0)


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
**1. Ακολουθεί παρόμοια διαδικασία με το τερματικό σημείο '/show_booking_details/<booking_code>'.  
2. Αν βρεθεί η κράτηση και ανήκει στον χρήστη, αυξάνει τον αριθμό των διαθέσιμων θέσεων της πτήσης ανάλογα με την κατηγορία των εισιτηρίων της κράτησης (οικονομική ή επιχειρηματική).  
3. Στη συνέχεια, διαγράφει την κράτηση από τη συλλογή 'bookings'.  
4. Τέλος, επιστρέφει μήνυμα επιτυχίας στον χρήστη.**


**Παραδείγματα:**

![18](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/2733d57f-9465-45e3-ade9-bc842d29a467)

![19](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/50c4fd62-1e0b-4484-b2e3-ac28fdcec54a)


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
**1. Ελέγχει αν ένας χρήστης είναι συνδεδεμένος. Αν όχι, επιστρέφει μήνυμα λάθους.  
2. Αν ναι, βρίσκει τον χρήστη στη συλλογή 'users' και τον διαγράφει.  
3. Αφαιρεί τον κωδικό του χρήστη από τη μεταβλητή session, αποσυνδέοντας τον χρήστη.  
4. Τέλος, επιστρέφει μήνυμα επιτυχίας στον χρήστη.**


**Παραδείγματα:**

![20](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/63d36da5-a2ef-4701-a31e-d9f33150b7d9)

![21](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/47874057-71bb-410b-95f4-4745e230d66a)


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
**1. Ελέγχει αν υπάρχει ήδη χρήστης συνδεδεμένος στη συνεδρία. Αν ναι, εμφανίζει ένα μήνυμα λάθους και επιστρέφει ένα σφάλμα 403.  
2. Προσπαθεί να αναλύσει τα δεδομένα της αίτησης ως JSON. Αν αποτύχει, εμφανίζει ένα μήνυμα λάθους και επιστρέφει ένα σφάλμα 400.  
3. Εξάγει το email και τον κωδικό εισόδου από τα δεδομένα της αίτησης. Αν λείπει κάποιο από αυτά, επιστρέφει ένα μήνυμα λάθους και ένα σφάλμα 400.  
4. Ελέγχει αν το email δεν ανήκει στον διαχειριστή. Αν ναι, εμφανίζει ένα μήνυμα λάθους και επιστρέφει ένα σφάλμα 403.  
5. Ελέγχει αν ο χρήστης υπάρχει με το δοσμένο email και τον κωδικό εισόδου. Αν ναι, συνδέει τον χρήστη και δημιουργεί μια νέα συνεδρία.  
6. Εάν ο κωδικός εισόδου είναι λανθασμένος αλλά το email υπάρχει στη βάση δεδομένων, επιστρέφει ένα σφάλμα.  
7. Αν το email δεν υπάρχει στη βάση δεδομένων, επιστρέφει ένα σφάλμα.**


**Σωστή σύνταξη json input:**
```json
{
    "email": "admin1@example.com",
    "login_code": "3364"
}
```
**Παραδείγματα:**

![1](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/014abe2a-4fc9-4d0d-8f43-0f0048080d64)

![2](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/3d6c0f92-5e1e-47c0-bbb3-baabb5234058)

![4](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/34107cf6-75aa-444b-9817-a07c0af9f96e)

![admin4](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/71264208-8672-46d7-8c83-6b9e865fe8b1)

![admin5](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/f56f98c7-de58-4e90-a34a-b377192da388)

![new1](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/07587123-8acf-410b-b1bb-de33d6d31617)


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
**1. Η συνάρτηση admin_logout() αντιδρά σε ένα HTTP POST αίτημα στο διαδρομή /admin/logout.  
2. Αρχικά, ελέγχει αν υπάρχει user_code στην τρέχουσα συνεδρία. Αν δεν υπάρχει, κανένας διαχειριστής δεν είναι συνδεδεμένος, και επιστρέφεται ένα σφάλμα 401.  
3. Αν υπάρχει user_code, ανακτά τον από τη συνεδρία.  
4. Στη συνέχεια, αναζητά τον χρήστη από τη συλλογή users με βάση το user_code.  
5. Ελέγχει αν ο χρήστης είναι διαχειριστής, ελέγχοντας αν το email του χρήστη βρίσκεται στη λίστα admin_emails.  
6. Αν το email δεν βρίσκεται στη λίστα, ο χρήστης δεν είναι διαχειριστής, και επιστρέφεται ένα σφάλμα 403.  
7. Αν ο χρήστης είναι διαχειριστής, τότε "αποσυνδέεται", αφαιρώντας το user_code από τη συνεδρία.  
8. Τέλος, επιστρέφεται ένα μήνυμα επιτυχίας που δηλώνει ότι ο διαχειριστής έχει αποσυνδεθεί επιτυχώς.**


**Παραδείγματα:**

![3](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/f3443327-4401-4a03-9ddb-4b8c05fe8a01)

![9](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/9c67e910-b74e-4551-9ae6-3c2249e8ef48)

![10](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/2e6a481a-498a-40b6-b440-d036c48a2d77)


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
**1. Η συνάρτηση create_flight() ανταποκρίνεται σε ένα HTTP POST αίτημα στη διαδρομή /admin/create_flight.  
2. Ελέγχει αρχικά εάν υπάρχει user_code στη συνεδρία, δηλαδή εάν ένας χρήστης είναι συνδεδεμένος. Εάν δεν υπάρχει user_code, επιστρέφει ένα σφάλμα 401, δηλώνοντας ότι κανένας διαχειριστής δεν είναι επί του παρόντος συνδεδεμένος.  
3. Εάν υπάρχει user_code, τον ανακτά από τη συνεδρία και αναζητά τον χρήστη στη συλλογή users.  
4. Ελέγχει εάν ο συνδεδεμένος χρήστης είναι διαχειριστής, δηλαδή αν το email του χρήστη βρίσκεται στη λίστα admin_emails. Αν δεν βρίσκεται, επιστρέφει ένα σφάλμα 403.  
5. Στη συνέχεια, προσπαθεί να αναλύσει τα δεδομένα του αιτήματος ως JSON. Εάν τα δεδομένα δεν έχουν διαμορφωθεί σωστά, επιστρέφει ένα σφάλμα 400.  
6. Αν τα δεδομένα του αιτήματος είναι σωστά διαμορφωμένα ως JSON, προσπαθεί να ανακτήσει τα απαραίτητα πεδία. Αν λείπει κάποιο πεδίο, επιστρέφει ένα σφάλμα 400.  
7. Μετράει τις πτήσεις στη συλλογή flights και χρησιμοποιεί αυτόν τον αριθμό για να δημιουργήσει ένα μοναδικό ID για τη νέα πτήση.  
8. Δημιουργεί ένα νέο έγγραφο πτήσης χρησιμοποιώντας τα δεδομένα που ανακτήθηκαν από το αίτημα.
9. Εισάγει τη νέα πτήση στη συλλογή flights.  
10. Επιστρέφει ένα μήνυμα επιτυχίας που δηλώνει ότι η πτήση έχει δημιουργηθεί επιτυχώς.**


**Σωστή σύνταξη json input:**
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
**Παραδείγματα:**

![2](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/805403c1-01b0-478f-8a1b-dd49a142c53f)

![3](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/b8696198-6c4d-4b7c-b1f4-a1cc0a056a59)

![5](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/6bb97fab-3979-4e19-9e66-0702515d925b)

![6](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/a850b886-5c79-4893-b82d-4e4f2537e22f)


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
**1. Ελέγχει αν ένας διαχειριστής είναι συνδεδεμένος, ελέγχοντας το 'user_code' στην session. Εάν όχι, επιστρέφει μήνυμα λάθους.  
2. Ελέγχει αν ο συνδεδεμένος χρήστης είναι διαχειριστής, ελέγχοντας το email του στη λίστα των emails των διαχειριστών. Εάν όχι, επιστρέφει μήνυμα λάθους.  
3. Προσπαθεί να αναλύσει τα δεδομένα του αιτήματος ως JSON. Εάν αποτύχει, επιστρέφει μήνυμα λάθους.  
4. Εξάγει τις νέες τιμές για τα εισιτήρια από τα δεδομένα του αιτήματος.  
5. Ελέγχει αν υπάρχει πτήση με το '_id' που έχει δοθεί. Εάν όχι, επιστρέφει μήνυμα λάθους.  
6. Αν υπάρχει η πτήση, ενημερώνει τις τιμές των εισιτηρίων της στη βάση δεδομένων.  
7. Επιστρέφει μήνυμα επιτυχίας στον διαχειριστή.**


**Σωστή σύνταξη json input:**
```json
{
  "business_class_tickets_price": " ",
  "economy_class_tickets_price": " "
}
```
**Παραδείγματα:**

![7](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/e2c08cb9-2c80-4a60-bb48-8c912f94d901)

![8](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/e3769999-f080-4a81-99e6-3cb50defd8be)

![new8](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/d40b5fac-e815-412d-8b7a-da7e85d5e696)


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
**1. Ελέγχει αν υπάρχει ήδη συνδεδεμένος διαχειριστής, ελέγχοντας την ύπαρξη του 'user_code' στην session. Εάν όχι, επιστρέφει μήνυμα λάθους.  
2. Ελέγχει αν το email του συνδεδεμένου χρήστη υπάρχει στη λίστα των emails των διαχειριστών. Αν όχι, επιστρέφει μήνυμα λάθους.  
3. Αναζητά την πτήση με το δεδομένο '_id' στη βάση δεδομένων. Αν δεν βρεθεί, επιστρέφει μήνυμα λάθους.  
4. Ελέγχει αν υπάρχουν κρατήσεις για την πτήση. Αν ναι, επιστρέφει μήνυμα λάθους και δεν διαγράφει την πτήση.   
5. Αν δεν υπάρχουν κρατήσεις, διαγράφει την πτήση από τη βάση δεδομένων.  
6. Επιστρέφει μήνυμα επιτυχίας.**


**Παραδείγματα:**

![12](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/25dcdf36-0d1d-4443-a9b2-faea701133e7)

![13](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/ec1b7d46-b47a-43f8-ba1b-e94993448a26)

![admin1](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/630b22f4-a3cf-4599-847e-cb9faf5faab1)

![admin2](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/2cbd68f7-315e-489a-a513-b2be185608ac)

![admin3](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/3688e5fc-ecc6-42ba-8094-2604b4454a8b)


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
**1. Ελέγχει αν υπάρχει συνδεδεμένος διαχειριστής.  
2. Ελέγχει αν ο συνδεδεμένος χρήστης είναι διαχειριστής.  
3. Αναζητά πτήσεις με βάση τα δεδομένα του αιτήματος (αιρμπόρτικος σταθμός προέλευσης, αεροδρόμιο προορισμού, ημερομηνία πτήσης).  
4. Επιστρέφει τις πτήσεις που ταιριάζουν στα κριτήρια.**


**Σωστή σύνταξη json input (προαιρετική):**
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
**Παραδείγματα:**

![4](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/ef162a82-ea86-4532-8285-eba04d91f5f5)

![5](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/56345566-71c7-4184-b9c0-5c2285745597)

![6](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/88df7cb1-01da-49fc-a35c-dc6aed419e5b)

![7](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/9030178b-04cf-4c3c-993d-b5a5ea97b7aa)

![9](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/3b24a2ae-5328-4ed8-8360-f6b663267c4e)


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
**1. Ελέγχει αν υπάρχει συνδεδεμένος διαχειριστής.  
2. Ελέγχει αν ο συνδεδεμένος χρήστης είναι διαχειριστής.  
3. Αναζητά την πτήση με το δεδομένο '_id' στη βάση δεδομένων. Αν δεν βρεθεί, επιστρέφει μήνυμα λάθους.  
4. Αναζητά τις κρατήσεις για την πτήση και επιστρέφει λεπτομέρειες για την πτήση και τις κρατήσεις.**


**Παραδείγματα:**

![10](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/f3957484-34e7-4811-92d0-cd5ec2be9573)

![11](https://github.com/Vaioskn/YpoxreotikiErgasia23_E20081_KONSTANTOPOULOS_VAIOS/assets/77112171/67b1aa0a-36f6-4943-91ca-d5b65f4b5e57)


## Dockerfile
```bash
FROM ubuntu:20.04
RUN apt-get update
RUN apt-get install -y python3 python3-pip
RUN pip3 install flask pymongo
RUN mkdir /app
RUN mkdir -p /app/data
COPY e20081_Airline_Service.py /app/e20081_Airline_Service.py
ADD data /app/data
EXPOSE 5000
WORKDIR /app
ENTRYPOINT [ "python3","-u", "e20081_Airline_Service.py" ]
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

**Βήμα 1:**   
Στον Ίδιο φάκελο έχουμε τα εξής:
| e20081_Airline_Service | Dockerfile | docker-compose.yml | Requirements.txt | data (κενός φάκελος) |
| :--------------------- | :--------- | :----------------- | :--------------- | :------------------- |

**Βήμα 2:**  
Πηγαίνουμε στο σωστό PATH του φακέλου με τα αρχεία και μετά εκτελούμε:  
```bash
$ sudo docker-compose build
```
```bash
$ sudo docker-compose up
```

**Βήμα 3:**   
Αφού ξεκινήσουν και τα 2 containers, στέλνουμε requests μέσω POSTMAN για να χρησιμοποιήσουμε την υπηρεσία.  
Στο POSTMAN στέλνουμε τα requests στην διεύθυνση:  **http://0.0.0.0:5000**


**Highly Reccomended:** Εκτέλεση των παρακάτω εντολών 
```bash
$ sudo iptables -A INPUT -p tcp --dport 27017 -j ACCEPT
```
Αυτή η εντολή χρησιμοποιεί το iptables, ένα πρόγραμμα χρήστη που επιτρέπει σε έναν διαχειριστή συστήματος να ρυθμίσει τους κανόνες φίλτρων πακέτων IP του τείχους προστασίας του πυρήνα του Linux.

**-A INPUT προσθέτει έναν κανόνα στην αλυσίδα INPUT. Η αλυσίδα INPUT χρησιμοποιείται για τον έλεγχο της συμπεριφοράς για τις εισερχόμενες συνδέσεις.  
-p tcp καθορίζει ότι ο κανόνας εφαρμόζεται στην κίνηση TCP.  
--dport 27017 καθορίζει τη θύρα προορισμού, που σε αυτή την περίπτωση είναι 27017.  
-j ACCEPT σημαίνει ότι αν το πακέτο ταιριάζει με τον κανόνα, πρέπει να γίνει αποδεκτό και να μην ελεγχθεί έναντι άλλων κανόνων στην αλυσίδα.**

```bash
$ sudo ufw allow 27017
```
Αυτή η εντολή χρησιμοποιεί το ufw (Uncomplicated Firewall), μια διεπαφή στο iptables που στοχεύει στην απλοποίηση της διαδικασίας ρύθμισης ενός τείχους προστασίας.  
Προσθέτει έναν κανόνα που επιτρέπει την εισερχόμενη κίνηση στη θύρα 27017.

**2ος Τρόπος**  
Χρησιμοποιείτε το **ALREADY_BUILT.zip** στο οποίο έχω ήδη κάνει το ``sudo docker-compose build`` και μένει μόνο η εκτέλεση της εντολής ``sudo docker-compose up`` από το κατάλληλο PATH
## Run Locally
Για την εκτέλεση του κώδικα τοπικά στον υπολογιστή σας χρειάζονται τα παρακάτω βήματα:   

**1. Αλλαγή της γραμμής 7 από:**  
```python
client = MongoClient('mongodb://mongodb:27017/')
```
**σε**  
```python
client = MongoClient('localhost:27017')
```

**2. Δημιουργία ενός container μέσω των εντολών:**  
```bash
docker pull mongo
```
```bash
docker run -d -p 27017:27017 --name mongodb mongo
```

**3. Εκτέλεση του e20081_Airline_Services.py**  

**4. Αποστολή σωστών Requests μέσω POSTMAN στην διεύθυνση: http://0.0.0.0:5000**
## Authors

- [@Vaioskn](https://github.com/Vaioskn)

