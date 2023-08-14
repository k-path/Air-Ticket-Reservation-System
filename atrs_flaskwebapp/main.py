from flask import Flask, render_template, request, session, url_for, redirect, jsonify
import pymysql
import pymysql.cursors # For database interfaceing
import hashlib # For md5
from hashlib import md5
import re # regex
import json # Parse json in python
import random
import datetime

# App initialization
app = Flask(__name__)
SESSION_TYPE = 'redis'
app.config['SECRET_KEY'] = "dontmatter" #
app.config['APP_HOST'] = "localhost"

# DB Information
app.config['DB_USER'] = "root"
app.config['DB_PASSWORD'] = ""
app.config['APP_DB'] = "atrs"
app.config['CHARSET'] = "utf8mb4"

conn = pymysql.connect(host=app.config['APP_HOST'],
                       user=app.config['DB_USER'],
                       password=app.config['DB_PASSWORD'],
                       db=app.config['APP_DB'],
                       charset=app.config['CHARSET'],
                       cursorclass=pymysql.cursors.DictCursor)

# Helper functions

def validateEmail(email):
  regex = r'\b[a-z0-9]+@[a-z]+\\b'
  return re.fullmatch(regex, email)

def hashPassword(password):
  output = hashlib.md5()
  output.update(password.encode())
  return output.hexdigest()

def validateAuthenticaiton(): # this function checks if you are signed in (validates whenever you passed authwall). we need to check this before going on pages that require sign in
  if session.get("email") or session.get("username"):
    return True
  return False

# Routes
@app.route('/') # default page
def index():
    #cur = conn.cursor()
    #cur.execute('select * from customer')
    #results = cur.fetchall()
    #print(results) 
    # we did this to check if mySQL was successfully connected
    #cur = conn.cursor()
    #cur.execute('SELECT email, password, type from SiteUser where email = "kjs10010@nyu.edu" or password = "ballislife2"')
    #results = cur.fetchall()
    #print(results)
   
    return render_template("index.html", name="Welcome to Air Ticket Reservation System")



@app.route('/logout') #logout page
def logout():
  session.clear()
  return render_template("login.html")

@app.route('/login', methods=['GET', 'POST']) #login page
def login():
  error = None
  if request.method == "GET":
    if(session.get("email")):
      return render_template("index.html")
    else:
      return render_template("login.html")
  elif request.method == "POST":
    email = request.form["userOrEmail"]
    username = request.form['userOrEmail']
    password = hashPassword(request.form["password"])
    # Login
    #doesUserExistQuery = "SELECT email, password from customer where email = %s AND password = %s"
    doesUserExistQuery = "SELECT email, password, type from SiteUser where email = %s AND password = %s"
    # doesStaffExistQuery = "SELECT username, airline_name FROM AirlineStaff where username = %s"
    email = request.form['userOrEmail']
    username = request.form['userOrEmail']
    password = hashPassword(request.form["password"])

    cursor = conn.cursor()
    cursor.execute(doesUserExistQuery, (email, password)) # execute the doesUserExistQuery such that % gets replaced with email and password variables
    data = cursor.fetchone()


    doesStaffUserExistQuery = "SELECT username, password, type from SiteUser where username = %s AND password = %s" # this query checks if the username and password combination 
                                                                                                                    # input matches a user and pass combo in our database's SiteUser table
    cursor4 = conn.cursor()
    cursor4.execute(doesStaffUserExistQuery, (username, password))
    data4 = cursor4.fetchone()

    #print(data)
    
    if data: # if data is not None then that means doesUserExistQuery told us that a user (staff or customer) exists. Note: staff or customer can login using email, but staff can also login using username (preferred way)
      session["email"] = data.get("email")
      session["user_type"] = data.get("type")
      if session["user_type"] == 1: # if the type of user is a staff
        getStaffNameQuery = "SELECT fname from AirlineStaff where email = %s AND password = %s"
        cursor2 = conn.cursor()
        cursor2.execute(getStaffNameQuery, (email, password))
        data2 = cursor2.fetchone()
        cursor2.close()
      else: # else; it is a customer
        getCusNameQuery = "SELECT name from Customer where email = %s AND password = %s"
        cursor3 = conn.cursor()
        cursor3.execute(getCusNameQuery, (email, password))
        data3 = cursor3.fetchone()
        cursor3.close()

      #session["password"] = data.get("password")


    elif data4: # if data4 is not None then that means that doesStaffUserExistQuery told us that the user (staff) exists. Here we are making it possible for staff to sign in using username
        session["username"] = data4.get("username")
        session["user_type"] = data4.get("type")

        getStaffNameQuery = "SELECT fname from AirlineStaff where username = %s AND password = %s"
        cursor2 = conn.cursor()
        cursor2.execute(getStaffNameQuery, (username, password))
        data2 = cursor2.fetchone()

    else:
      error = "Invalid username or password"
    # allow login using just username, this is only for staff so dont need to check type here


    cursor.close()
    #cursor2.close()
    #cursor3.close()
    cursor4.close()
    if error:
      return render_template("login.html", error=error)
    if session["user_type"] == 1:
        #return render_template("index.html", error=None, name = "Welcome " + data2.get("fname") + "!")
        return render_template("staffHome.html", error=None, name = "Welcome " + data2.get("fname") + "!")
    #return render_template("customerHome.html", error=None, name = "Welcome " + data3.get("name").split()[0] + "!")
    return render_template("customerHome.html", error=None, name = "Welcome " + data3.get("name").split()[0] + "!")
    

@app.route('/pretty', methods=["GET"])
def pretty():
  print(validateAuthenticaiton())
  if validateAuthenticaiton():
    return render_template("pretty.html", error=None)
  return redirect(url_for('index'))

@app.route('/register', methods=["GET", "POST"])
def chooseRegistry():
    return render_template("register.html", name = "Choose an option below")

@app.route('/registerCustomer', methods=["GET", "POST"])
def registerCus():
    if request.method == "POST":
        fname = request.form['fname']
        lname = request.form['lname']
        new_email = request.form["userEmail"]
        new_pass = hashPassword(request.form["password"])
        building_num = request.form['building_number']
        street = request.form['street']
        city = request.form['city']
        state = request.form['state']
        phone_num = request.form['phone_number']
        passport_num = request.form['passport_number']
        passport_exp = request.form['passport_exp']
        passport_country = request.form['passport_country']
        date_of_birth = request.form['dob']

        cursor = conn.cursor()
        checkEmailQuery = "SELECT * FROM Customer WHERE email = %s"
        cursor.execute(checkEmailQuery, new_email)
        data = cursor.fetchone()


        if data:
            error = "This email is already taken"
            cursor.close()
            return render_template('registerCus.html', error=error)
        else:
            regQuery = "INSERT INTO SiteUser VALUES(%s, '', %s, 2)"
            fillCustomerQuery = "INSERT INTO Customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            #cursor.execute(regQuery, (new_email, new_pass))
            cursor.execute(regQuery, (new_email, new_pass))
            conn.commit()
            cursor.close()
            cursor2 = conn.cursor()
            cursor2.execute(fillCustomerQuery, (new_email, new_pass, fname + ' ' + lname, building_num, street, city, state, phone_num, passport_num, passport_exp, passport_country, date_of_birth))
            conn.commit()
            cursor2.close()

            return render_template('regSuccess.html')
        
    return render_template("registerCus.html", name="Welcome to Airline Ticket Reservation System, create an account below")

@app.route('/registerStaff', methods=["GET", "POST"])
def registerStaff():
    if request.method == "POST":
        fname = request.form['fname']
        lname = request.form['lname']
        new_sEmail = request.form["userEmail"]
        new_username = request.form["username"]
        new_sPassword = hashPassword(request.form["password"])
        date_of_birth = request.form["dob"]
        airline_name = request.form["airline_name"]
        #cursor = conn.cursor()
        #checkEmailUserQuery = "SELECT * FROM AirlineStaff WHERE email = %s or username = %s"
        #cursor.execute(checkEmailUserQuery, (new_sEmail, new_username))
        #data = cursor.fetchone()

        cursor = conn.cursor()
        checkSiteUserQuery = "SELECT * FROM SiteUser WHERE email = %s or username = %s"
        cursor.execute(checkSiteUserQuery, (new_sEmail, new_username))
        data = cursor.fetchone()

        # (obsolete now) only allow registration if email already in database in AirlineStaff table
        if data:
            error = "This username or email is already associated with an account"
            cursor.close()
            return render_template('registerStaff.html', error=error)
        else:
            #if data2: # dont allow duplicate staff registration, so if in SiteUser already don't allow it!
            #    error2 = "This username or email is already associated with an account"
            #    cursor2.close()
            #    return render_template('registerStaff.html', error=error2)

            
            regQuery = "INSERT INTO SiteUser VALUES(%s, %s, %s, 1)"
            regStaffQuery = "INSERT INTO AirlineStaff VALUES(%s, %s, %s, %s, %s, %s)"
            regWorksAtQuery = "INSERT INTO Works_At VALUES (%s, %s)"
            cursor2 = conn.cursor()
            #cursor.execute(regQuery, (new_sEmail, new_username, new_sPassword))
            cursor.execute(regQuery, (new_sEmail, new_username, new_sPassword))
            conn.commit()
            cursor.close()
            cursor = conn.cursor()
            cursor.execute(regStaffQuery, (new_username, new_sPassword, fname, lname, date_of_birth, new_sEmail))
            conn.commit()
            cursor = conn.cursor()
            cursor.execute(regWorksAtQuery, (new_username, airline_name))
            conn.commit()


            return render_template('regSuccess.html')
           
        
    return render_template("registerStaff.html", name="Welcome to Airline Ticket Reservation System website, register for staff account below")

@app.route('/searchpage')
def searchPage():
    return render_template("searchpage.html")

@app.route('/searchflights', methods = ["GET", "POST"])
def searchflights():
    cursor = conn.cursor()
    if request.method == 'POST':
        d_airport = request.form['d_airport']
        a_airport = request.form['a_airport']
        d_city = request.form['d_city']
        a_city = request.form['a_city']
        d_date = request.form['d_date']
        return_date = request.form['return_date']
        
        # search for one way trip by airports
        if d_airport != "" and a_airport != "" and d_date != "" and return_date == "" and d_city == "" and a_city == "":
            #print('d_date is', d_date)
            query = 'SELECT flight_num, d_date, d_time, d_airport, a_date, a_time, a_airport, base_price FROM Flight WHERE d_date = %s AND d_airport = %s AND a_airport = %s AND %s > CURRENT_DATE()'
            cursor.execute(query, (d_date, d_airport, a_airport, d_date))
            go_flights = cursor.fetchall()	
            cursor.close()
            #print('go_flights is', go_flights)
            if(go_flights):
                return render_template('searchpage.html', go_flights = go_flights)
            else:
                noGoError = 'No trip found'
                return render_template('searchpage.html', noGoError = noGoError)
        # search for round trip by airports
        elif d_airport != "" and a_airport != "" and d_date != "" and return_date != "" and d_city == "" and a_city == "":
            if d_date > return_date:
                dateError = "Arrival date must be after departure date."
                return render_template('searchpage.html', dateError = dateError)
            # check if there is a return trip
            query = 'SELECT flight_num, d_date, d_time, d_airport, a_date, a_time, a_airport FROM Flight WHERE d_date = %s AND d_airport = %s AND a_airport = %s AND %s > CURRENT_DATE()'
            cursor.execute(query, (return_date, a_airport, d_airport, return_date))
            return_flights = cursor.fetchall()
            if (return_flights):
                query = 'SELECT flight_num, d_date, d_time, d_airport, a_date, a_time, a_airport FROM Flight WHERE d_date = %s AND d_airport = %s AND a_airport = %s AND %s > CURRENT_DATE()'
                cursor.execute(query, (d_date, d_airport, a_airport, d_date))
                go_flights = cursor.fetchall()	
                if(go_flights):
                    return render_template('searchpage.html', return_flights = return_flights, go_flights = go_flights)
                else:
                    noGoError = "No trip found"
                    return render_template('searchpage.html', noGoError = noGoError)
            else:
                noReturnError = 'No return trip found.'
                return render_template('searchpage.html', noReturnError = noReturnError)
        # search for round trip by city
        elif d_airport == "" and a_airport == "" and d_date != "" and return_date != "" and d_city != "" and a_city != "":
            if d_date > return_date:
                dateError = "Arrival date must be after departure date."
                return render_template('searchpage.html', dateError = dateError)
            # check if there is a return trip
            query = 'SELECT flight_num, d_date, d_time, d_airport, a_date, a_time, a_airport FROM Flight NATURAL JOIN Airport WHERE d_airport = airport_name AND a_airport = airport_name AND city = %s AND city = %s AND d_date = %s AND %s > CURRENT_DATE()'
            cursor.execute(query, (a_city, d_city, return_date, return_date))
            return_flights = cursor.fetchall()
            if (return_flights):
                query = 'SELECT flight_num, d_date, d_time, d_airport, a_date, a_time, a_airport FROM Flight NATURAL JOIN Airport WHERE d_airport = airport.name AND a_airport = airport.name AND airport.city = %s AND airport.city = %s AND d_date = %s AND %s > CURRENT_DATE()'
                cursor.execute(query, (d_city, a_city, d_date, d_date))
                go_flights = cursor.fetchall()
                if(go_flights):
                    return render_template('searchpage.html', return_flights = return_flights, go_flights = go_flights)
                else:
                    noGoError = "No trip found"
                    return render_template('searchpage.html', noGoError = noGoError)
            else:
                noReturnError = 'No return trip found'
                return render_template('searchpage.html', noReturnError = noReturnError)
        # search for one way by city
        elif d_airport == "" and a_airport == "" and d_date != "" and return_date == "" and d_city != "" and a_city != "":
            query = 'SELECT flight_num, d_date, d_time, d_airport, a_date, a_time, a_airport FROM Flight NATURAL JOIN Airport WHERE d_airport = airport_name AND a_airport = airport_name AND city = %s AND city = %s AND d_date = %s AND %s > CURRENT_DATE()'
            cursor.execute(query, (d_city, a_city, d_date, d_date))
            go_flights = cursor.fetchall()
            print("go flights is", go_flights)
            if(go_flights):
                return render_template('searchpage.html', go_flights = go_flights)
            else:
                noGoError = 'No trip found'
                return render_template('searchpage.html', noGoError = noGoError)
        elif d_airport != "" and a_airport != "" and d_city != "" and a_city != "":
            invalidSearchError = 'Please enter only departure/arrival city or departure/arrival airport'
            return render_template('searchpage.html', invalidSearchError = invalidSearchError)
        else:
            invalidSearchError = 'Invalid data'
            return render_template('searchpage.html', invalidSearchError = invalidSearchError)
    else:
        return render_template('searchpage.html')
    

@app.route('/checkstatus', methods = ["GET", "POST"])
def checkstatus():
    cursor = conn.cursor()
    if request.method == 'POST':
        airline = request.form['airline_name']
        flight_num = request.form['flight_num']
        d_date = request.form['d_date']
        a_date = request.form['a_date']
        if airline != "" and flight_num != "" and d_date != "" and a_date != "":
            query = 'SELECT airline_name, flight_num, d_date, a_date, status FROM Flight WHERE airline_name = %s AND flight_num = %s AND d_date = %s AND a_date = %s'
            #query = 'SELECT flight_num, d_date, a_date, status FROM Flight WHERE (SELECT airline_name from airline where airline_name = %s) = %s AND flight_num = %s AND d_date = %s AND a_date = %s'
            cursor.execute(query, (airline, flight_num, d_date, a_date))
            data = cursor.fetchall()
            cursor.close()
            if (data):
                return render_template('searchpage.html', status = data)
            else:
                invalidFlightError = 'Sorry, no flight found'
                return render_template('searchpage.html', invalidFlightError = invalidFlightError)
        else:
            invalidDataError = 'Invalid data'
            return render_template('searchpage.html', invalidDataError = invalidDataError)
    else:
        return render_template('searchpage.html')



def default30days():
	cursor = conn.cursor();
	username = session['username']
	# find which airline it is 
	query = 'SELECT airline_name FROM works_at WHERE username = %s'
	cursor.execute(query, (username))
	data = cursor.fetchone()
	airline = data['airline_name']
	query = 'SELECT flight_num, d_date, d_time, d_airport, a_date, a_time, a_airport FROM Flight WHERE d_date >= CURRENT_DATE() AND d_date <= DATE_ADD(CURRENT_DATE(), INTERVAL 30 DAY) AND airline_name = %s'
	cursor.execute(query, (airline))
	flights = cursor.fetchall()
	for i in range(len(flights)):
		flight_num = flights[i]['flight_num']
		d_date = flights[i]['d_date']
		d_time = flights[i]['d_time']
		query = 'SELECT email FROM Ticket WHERE flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s'
		cursor.execute(query, (flight_num, d_date, d_time, airline))
		customers = cursor.fetchall()
		customer_list = []
		for j in range(len(customers)):
			customer_list.append(customers[j]['email'])
		customer_email_str = ", ".join(customer_list)
		flights[i]['email'] = customer_email_str
	cursor.close()
	return flights


@app.route('/staffHomepage')
def staffHome():
  print(validateAuthenticaiton())
  if validateAuthenticaiton():
    username = session.get("username")

    getStaffNameQuery = "SELECT fname from AirlineStaff where username = %s"
    cursor = conn.cursor()
    cursor.execute(getStaffNameQuery, (username))
    data = cursor.fetchone()

    flights = default30days()
    return render_template("staffHome.html", name = "Welcome " + data.get("fname") + "!", flights = flights)
  return redirect(url_for('login'))


@app.route('/staffViewFlights', methods=['GET', 'POST'])
def staffViewFlights():
	cursor = conn.cursor();
	username = session['username']
	flights = default30days()
	if request.method == 'POST':
		start = request.form['start_date']
		end = request.form['end_date']
		d_airport = request.form['d_airport']
		a_airport = request.form['a_airport']
		d_city = request.form['d_city']
		a_city = request.form['a_city']
		# find which airline it is 
		query = 'SELECT airline_name FROM Works_at WHERE username = %s'
		cursor.execute(query, (username))
		data = cursor.fetchone()
		airline = data['airline_name']
		# if there are inputs from user that specifies start_date, end_date, departure_airport, departure_city, 
		# arrival_airport, and arrival_city
		if start == "" and end != "" and d_airport == "" and a_airport == "" and d_city == "" and a_city == "":
			return render_template('staffHome.html', username = username, flights = flights)
		elif start != "" and end != "" and d_airport != "" and a_airport != "" and d_city == "" and a_city == "":
			query = 'SELECT flight_num, d_date, d_time, d_airport, a_date, a_time, a_airport FROM Flight WHERE d_date >= %s AND d_date <= %s AND d_airport = %s AND a_airport = %s AND airline_name = %s'
			cursor.execute(query, (start, end, d_airport, a_airport, airline))
			flights = cursor.fetchall()
			for i in range(len(flights)):
				flight_num = flights[i]['flight_num']
				d_date = flights[i]['d_date']
				d_time = flights[i]['d_time']
				query = 'SELECT email FROM Ticket WHERE flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s'
				cursor.execute(query, (flight_num, d_date, d_time, airline))
				customers = cursor.fetchall()
				customer_list = []
				for j in range(len(customers)):
					customer_list.append(customers[j]['email'])
				customer_email_str = ", ".join(customer_list)
				flights[i]['email'] = customer_email_str
			cursor.close()
			return render_template('staffHome.html', username = username, flights = flights)
        # doesn't work needs fixing
		elif start != "" and end != "" and d_airport == "" and a_airport == "" and d_city != "" and a_city != "":
			query = 'SELECT flight_num, d_date, d_time, d_airport, a_date, a_time, a_airport FROM Flight NATURAL JOIN Airport WHERE d_airport = airport_name AND a_airport = airport_name AND city = %s AND city = %s AND d_date >= %s AND d_date <= %s AND airline_name = %s'
			cursor.execute(query, (d_city, a_city, start, end, airline))
			flights = cursor.fetchall()
			for i in range(len(flights)):
				flight_num = flights[i]['flight_num']
				dept_date = flights[i]['d_date']
				dept_time = flights[i]['d_time']
				query = 'SELECT email FROM Ticket WHERE flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s'
				cursor.execute(query, (flight_num, d_date, d_time, airline))
				customers = cursor.fetchall()
				customer_list = []
				for j in range(len(customers)):
					customer_list.append(customers[j]['email'])
				customer_email_str = ", ".join(customer_list)
				flights[i]['email'] = customer_email_str
			cursor.close()
			return render_template('staffHome.html', username = username, flights = flights)
		else:
			mismatchError = 'Please enter only departure/arrival city or departure/arrival airport.'
			return render_template('staffHome.html', username = username, mismatchError = mismatchError)

	else:
		return render_template('staffHome.html', username = username, flights = flights)




@app.route('/createflight', methods=['GET', 'POST'])
def createflight():
	cursor = conn.cursor();
	username = session['username']
	flights = default30days()
	if request.method == 'POST':
		flight_num = request.form['flight_num']
		d_airport = request.form['d_airport']
		d_date = request.form['d_date']
		d_time = request.form['d_time']
		a_airport = request.form['a_airport']
		a_date = request.form['a_date']
		a_time = request.form['a_time']
		a_id = request.form['a_id']
		base_price = request.form['base_price']
		# find which airline it is 
		query = 'SELECT airline_name FROM works_at WHERE username = %s'
		cursor.execute(query, (username))
		data = cursor.fetchone()
		airline = data['airline_name']
		# check if this is an existing flight
		query = 'SELECT * FROM Flight WHERE flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s'
		cursor.execute(query, (flight_num, d_date, d_time, airline))
		data = cursor.fetchone()
		if(data):
			flightExistError = "This is an existing flight, try another"
			return render_template('staffHome.html', username = username, flightExistError = flightExistError, flights = flights)
		else:
			# check if departure and arrival airports are the same
			if d_airport == a_airport:
				sameAirportError = 'Departure airport and arrival airport cannot be the same'
				return render_template('staffHome.html', username = username, sameAirportError = sameAirportError, flights = flights)
			# check if departure_date and time < arrival_date and time exist in the system
			dep_date = datetime.datetime.strptime(d_date, "%Y-%m-%d")
			dep_time = datetime.datetime.strptime(d_time, "%H:%M")
			com_date = datetime.datetime.combine(dep_date.date(), dep_time.time())
			arr_date = datetime.datetime.strptime(a_date, "%Y-%m-%d")
			arr_time = datetime.datetime.strptime(a_time, "%H:%M")
			com_date2 = datetime.datetime.combine(arr_date.date(), arr_time.time())
			now_date = datetime.datetime.now()
			if(com_date < now_date):
				pastFlightError = 'Cannot create a flight in the past'
				return render_template('staffHome.html', username = username, pastFlightError = pastFlightError, flights = flights)
			if(com_date < com_date2):
				# check if the airplane exist in the system
				query = 'SELECT * FROM Airplane WHERE a_id = %s AND airline_name = %s'
				cursor.execute(query, (a_id, airline))
				planeExist = cursor.fetchone()
				if (planeExist):
					query = 'INSERT INTO Flight (flight_num, d_airport, d_date, d_time, a_airport, a_date, a_time, a_id, base_price, airline_name, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)'
					cursor.execute(query, (flight_num, d_airport, d_date, d_time, a_airport, a_date, a_time, a_id, base_price, airline))
					conn.commit()
					cursor.close()
					addFlightSucc = "Sucessfully added a flight"
					flights = default30days()
					return render_template('staffHome.html', username = username, addFlightSucc = addFlightSucc, flights = flights)
				else:
					noPlaneError = 'No airplane found'
					return render_template('staffHome.html', username = username, noPlaneError = noPlaneError, flights = flights)
			else:
				departureDateError = 'Departure date time can not be greater than arrival date time. Please check again.'
				return render_template('staffHome.html', username = username, departureDateError = departureDateError, flights = flights)

	else:
		return render_template('staffHome.html', username = username, flights = flights)







@app.route('/updateStatus', methods=['GET', 'POST'])
def updateStatus():
	cursor = conn.cursor();
	username = session['username']
	flights = default30days()
	if request.method == 'POST':
		flight_num = request.form['flight_num']
		d_date = request.form['d_date']
		d_time = request.form['d_time']
		airline = request.form['airline_name']
		new_status = request.form['flight_status']
		query = 'SELECT * FROM Flight WHERE flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s'
		cursor.execute(query, (flight_num, d_date, d_time, airline))
		data = cursor.fetchone()
		if (data):
			query = 'UPDATE Flight SET status = %s WHERE flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s' 
			cursor.execute(query, (new_status, flight_num, d_date, d_time, airline))
			conn.commit()
			cursor.close()
			changeStatusSucc = "Successfully changed the flight status"
			return render_template('staffHome.html', username = username, changeStatusSucc = changeStatusSucc, flights = flights)
		else:
			changeStatusError = "Sorry, cannot find the flight"
			return render_template('staffHome.html', username = username, changeStatusError = changeStatusError, flights = flights)
	else:
		return render_template('staffHome.html', username = username, flights = flights)





@app.route('/addAirplane', methods=['GET', 'POST'])
def addAirplane():
	cursor = conn.cursor();
	username = session['username']
	flights = default30days()
	if request.method == 'POST':
		a_id = request.form['a_id']
		num_seats = request.form['num_seats']
		manufacturer = request.form['manufacturer']
		airplane_age = request.form['age']
		# find which airline it is 
		query = 'SELECT airline_name FROM works_at WHERE username = %s'
		cursor.execute(query, (username))
		data = cursor.fetchone()
		airline = data['airline_name']
		# check if an airplane already exist in the system
		query = 'SELECT * FROM Airplane WHERE a_id = %s AND airline_name = %s'
		cursor.execute(query, (a_id, airline))
		data = cursor.fetchone()
		if (data):
			planeExistError = "Sorry, this plane already exists. Please try another."
			return render_template('staffHome.html', username = username, planeExistError = planeExistError, flights = flights)
		else:
			query = 'INSERT INTO Airplane (a_id, num_seats, manufacturer, age, airline_name) VALUES (%s, %s, %s, %s, %s)'
			cursor.execute(query, (a_id, num_seats, manufacturer, airplane_age, airline))
			conn.commit()
			cursor.close()
			addPlaneSucc = 'Successfully added a plane'
			
			return render_template('staffHome.html', username = username, addPlaneSucc = addPlaneSucc, flights = flights)
	else:
		return render_template('staffHome.html', username = username, flights = flights)



@app.route('/addAirport', methods=['GET', 'POST'])
def addAirport():
	cursor = conn.cursor();
	username = session['username']
	
	flights = default30days()
	if request.method == 'POST':
		airport_name = request.form['airport_name']
		city = request.form['airport_city']
		country = request.form['airport_country']
		type = request.form['airport_type']
		if airport_name != None and city != None and country != None and type != None:
			query = 'SELECT * FROM Airport WHERE airport_name = %s'
			cursor.execute(query, (airport_name))
			data = cursor.fetchone()
			if (data):
				airportExistError = "Sorry, this airport already exist. Please try another one."
				return render_template('staffHome.html', username = username, airportExistError = airportExistError, flights = flights)
			else:
				query = 'INSERT INTO AIRPORT (airport_name, city, country, type) VALUES (%s, %s, %s, %s)'
				cursor.execute(query, (airport_name, city, country, type))
				conn.commit()
				cursor.close()
				addAirportSucc = 'Successfully added an airport'
				return render_template('staffHome.html', username = username , addAirportSucc = addAirportSucc, flights = flights)
	else:
		return render_template('staffHome.html', username = username)


@app.route('/viewRating', methods=['GET', 'POST'])
def viewRating():
	cursor = conn.cursor();
	username = session['username']
	flights = default30days()
	if request.method == 'POST':
		flight_num = request.form['flight_num']
		d_date = request.form['d_date']
		d_time = request.form['d_time']
		# find out which airline it is
		query = 'SELECT airline_name FROM works_at WHERE username = %s'
		cursor.execute(query, (username))
		data = cursor.fetchone()
		airline = data['airline_name']
		if flight_num != "" and d_date != "" and d_time != "":
			query = 'SELECT rating, comment FROM Review WHERE flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s'
			cursor.execute(query, (flight_num, d_date, d_time, airline))
			rating_comment = cursor.fetchall()
			if (rating_comment):
				query = 'SELECT AVG(rating) AS average_rating FROM Review WHERE flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s'
				cursor.execute(query, (flight_num, d_date, d_time, airline))
				avg_rating = cursor.fetchone()
				average_rating = avg_rating['average_rating']
				cursor.close()
				return render_template('staffHome.html', username = username, rating_comment = rating_comment, average_rating = average_rating, flights = flights)
			else:
				invalidFlightError = 'This flight either does not exist or has no ratings or comments yet.'
				return render_template('staffHome.html', username = username, invalidFlightError = invalidFlightError, flights = flights)
		else:
			noDataError = 'Please specify a flight'
			return render_template('staffHome.html', username = username, noDataError = noDataError, flights = flights)
	else:
		return render_template('staffHome.html', username = username)



@app.route('/frequentCustomer', methods=['GET', 'POST'])
def frequentCustomer():
	cursor = conn.cursor();
	username = session['username']
	flights = default30days()
	if request.method == 'POST':
		# find out which airline it is
		query = 'SELECT airline_name FROM works_at WHERE username = %s'
		cursor.execute(query, (username))
		data = cursor.fetchone()
		airline = data['airline_name']
		query = 'SELECT email, COUNT(t_ID) AS frequency FROM Customer NATURAL JOIN Ticket WHERE airline_name = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR) GROUP BY email ORDER BY frequency DESC LIMIT 1'
		cursor.execute(query, (airline))
		data = cursor.fetchone()
		freq_customer = data['email']
		cursor.close()
		return render_template('staffHome.html', username = username, freq_customer = freq_customer, flights = flights)
	else:
		return render_template('staffHome.html', username = username, flights = flights)


@app.route('/viewFlightsOf', methods=['GET', 'POST'])
def viewFlightsOf():
	cursor = conn.cursor();
	username = session['username']
	flights = default30days()
	if request.method == 'POST':
		email = request.form['email']
		# find out which airline it is
		query = 'SELECT airline_name FROM works_at WHERE username = %s'
		cursor.execute(query, (username))
		data = cursor.fetchone()
		airline = data['airline_name']
		if email != "":
			query = 'SELECT * FROM Customer NATURAL JOIN Ticket NATURAL JOIN Flight WHERE email = %s AND airline_name = %s'
			cursor.execute(query, (email, airline))
			customer_flights = cursor.fetchall()
			cursor.close()
			return render_template('staffHome.html', username = username, customer_flights = customer_flights, flights = flights)
		else:
			noEmailError = 'Please sepcify a customer email'
			return render_template('staffHome.html', username = username, noEmailError = noEmailError, flights = flights)
	else:
		return render_template('staffHome.html', username = username, flights = flights)



@app.route('/viewReports', methods=['GET', 'POST'])
def viewReports():
	cursor = conn.cursor()
	username = session['username']
	flights = default30days()
	if request.method == 'POST':
		start = request.form['start_date']
		end = request.form['end_date']
		query = 'SELECT airline_name FROM works_at WHERE username = %s'
		cursor.execute(query, (username))
		data = cursor.fetchone()
		airline = data['airline_name']
		if start != "" and end != "":
			query = 'SELECT COUNT(t_id) AS num_tickets FROM Ticket WHERE airline_name = %s AND purchase_date >= %s AND purchase_date <= %s'
			cursor.execute(query, (airline, start, end))
			data = cursor.fetchone()
			custom_num_tickets = data['num_tickets']
			cursor.close()
			return render_template('staffHome.html', username = username, custom_num_tickets = custom_num_tickets, start_date = start, end_date = end, flights = flights)
		elif start == "" and end == "":
			query = 'SELECT COUNT(ticket_id) AS num_tickets FROM Ticket WHERE airline_name = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR) AND purchase_date <= CURRENT_DATE()'
			cursor.execute(query, (airline))
			data = cursor.fetchone()
			last_year_num = data['num_tickets']
			query = 'SELECT COUNT(ticket_id) AS num_tickets FROM Ticket WHERE airline_name = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH) AND purchase_date <= CURRENT_DATE()'
			cursor.execute(query, (airline))
			data = cursor.fetchone()
			last_month_num = data['num_tickets']
			return render_template('staffHome.html', username = username, last_year_num = last_year_num, last_month_num = last_month_num, flights = flights)
		else:
			noDateError = 'Please specify a correct date range'
			return render_template('staffHome.html', username = username, noDateError = noDateError, flights = flights)
	else:
		return render_template('staffHome.html', username = username)



@app.route('/viewRevenue', methods=['GET', 'POST'])
def viewRevenue():
	cursor = conn.cursor()
	username = session['username']
	flights = default30days()
	if request.method == 'POST':
		# find out which airline it is
		query = 'SELECT airline_name FROM works_at WHERE username = %s'
		cursor.execute(query, (username))
		data = cursor.fetchone()
		airline = data['airline_name']
		query = 'SELECT SUM(sold_price) AS year_revenue FROM Ticket WHERE airline_name = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR) AND purchase_date <= CURRENT_DATE()'
		cursor.execute(query, (airline))
		data1 = cursor.fetchone()
		last_year_revenue = data1['year_revenue']
		query = 'SELECT SUM(sold_price) AS month_revenue FROM Ticket WHERE airline_name = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH) AND purchase_date <= CURRENT_DATE()'
		cursor.execute(query, (airline))
		data2 = cursor.fetchone()
		last_month_revenue = data2['month_revenue']
		return render_template('staffHome.html', username=username, last_year_revenue=last_year_revenue, last_month_revenue=last_month_revenue, flights = flights)
	else:
		return render_template('staffHome.html', username = username, flights = flights)


@app.route('/customerHomepage')
def customerHome():
  print(validateAuthenticaiton())
  if validateAuthenticaiton():
    email = session.get("email")

    getCusNameQuery = "SELECT name from Customer where email = %s"
    cursor = conn.cursor()
    cursor.execute(getCusNameQuery, (email))
    data = cursor.fetchone()
    cursor.close()

    return render_template("customerHome.html", error=None, name = "Welcome " + data.get("name").split()[0] + "!")
  return redirect(url_for('login'))









def pastYearSpending():
	cursor = conn.cursor();
	email = session['email']
	query = 'SELECT SUM(sold_price) AS total_last_year FROM Ticket NATURAL JOIN Customer WHERE email = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR) AND purchase_date <= CURRENT_DATE()'
	cursor.execute(query, (email))
	total_last_year = cursor.fetchone()
	if total_last_year == None:
		total_last_year = 0
	total_last_year = total_last_year['total_last_year']
	cursor.close()
	return total_last_year

# return customer's spending by month
def pastYearMonthlySpending():
	cursor = conn.cursor();
	email = session['email']
	spending = []
	# month 1
	q1 = 'SELECT DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH) AS start_date, DATE_SUB(CURRENT_DATE(), INTERVAL 5 MONTH) AS end_date, SUM(sold_price) AS total FROM Ticket NATURAL JOIN Customer WHERE email = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 6 MONTH) AND purchase_date <= DATE_SUB(CURRENT_DATE(), INTERVAL 5 MONTH)'
	cursor.execute(q1, (email))
	# stores purchase date, sold_price of that month
	month1 = cursor.fetchone()
	# month 2
	q2 = 'SELECT DATE_SUB(CURRENT_DATE(), INTERVAL 5 MONTH) AS start_date, DATE_SUB(CURRENT_DATE(), INTERVAL 4 MONTH) AS end_date, SUM(sold_price) AS total FROM Ticket NATURAL JOIN Customer WHERE email = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 5 MONTH) AND purchase_date <= DATE_SUB(CURRENT_DATE(), INTERVAL 4 MONTH)'
	cursor.execute(q2, (email))
	# stores purchase date, sold_price of that month
	month2 = cursor.fetchone()
	# month 3
	q3 = 'SELECT DATE_SUB(CURRENT_DATE(), INTERVAL 4 MONTH) AS start_date, DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH) AS end_date, SUM(sold_price) AS total FROM Ticket NATURAL JOIN Customer WHERE email = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 4 MONTH) AND purchase_date <= DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH)'
	cursor.execute(q3, (email))
	# stores purchase date, sold_price of that month
	month3 = cursor.fetchone()
	# month 4
	q4 = 'SELECT DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH) AS start_date, DATE_SUB(CURRENT_DATE(), INTERVAL 2 MONTH) AS end_date, SUM(sold_price) AS total FROM Ticket NATURAL JOIN Customer WHERE email = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 3 MONTH) AND purchase_date <= DATE_SUB(CURRENT_DATE(), INTERVAL 2 MONTH)'
	cursor.execute(q4, (email))
	# stores purchase date, sold_price of that month
	month4 = cursor.fetchone()
	# month 5
	q5 = 'SELECT DATE_SUB(CURRENT_DATE(), INTERVAL 2 MONTH) AS start_date, DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH) AS end_date, SUM(sold_price) AS total FROM Ticket NATURAL JOIN Customer WHERE email = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 2 MONTH) AND purchase_date <= DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH)'
	cursor.execute(q5, (email))
	# stores purchase date, sold_price of that month
	month5 = cursor.fetchone()
	# month 6
	q6 = 'SELECT DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH) AS start_date, CURRENT_DATE() AS end_date, SUM(sold_price) AS total FROM Ticket NATURAL JOIN Customer WHERE email = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH) AND purchase_date <= CURRENT_DATE()'
	cursor.execute(q6, (email))
	# stores purchase date, sold_price of that month
	month6 = cursor.fetchone()
	spending.append(month1)
	spending.append(month2)
	spending.append(month3)
	spending.append(month4)
	spending.append(month5)
	spending.append(month6)
	for item in spending:
		if item['total'] == None:
			item['total'] = 0
	cursor.close()
	return spending


@app.route('/customerViewFlights', methods=['GET', 'POST'])
def customerViewFlights():
	cursor = conn.cursor()
	email = session['email']
	total_last_year = pastYearSpending()
	spending = pastYearMonthlySpending()
	start = request.form['start_date']
	end = request.form['end_date']
	d_airport = request.form['d_airport']
	a_airport = request.form['a_airport']
	d_city = request.form['d_city']
	a_city = request.form['a_city']
	if request.method == 'POST':
		# default show all future flights
		if start == "" and end == "" and d_airport == "" and a_airport == "" and d_city == "" and a_city == "":
			query ='SELECT * FROM Ticket NATURAL JOIN Flight WHERE email = %s and d_date >= CURDATE()'
			cursor.execute(query, (session['email']))
			required_flights = cursor.fetchall()
			if(required_flights):
				return render_template('customerHome.html', required_flights = required_flights, email = email, total_last_year = total_last_year, spending = spending)
			else:
				no_future_error = 'No future flight'
				return render_template('customerHome.html', no_future_error = no_future_error, email = email, total_last_year = total_last_year, spending = spending)
		elif start != "" and end != "" and d_airport != "" and a_airport != "" and d_city == "" and a_city == "":
			query ='SELECT * FROM Ticket NATURAL JOIN Flight WHERE email = %s and d_date >= %s and d_date <= %s and d_airport = %s and a_airport = %s'
			cursor.execute(query, (session['email'], start, end, d_airport, a_airport))
			required_flights = cursor.fetchall()
			if(required_flights):
				return render_template('customerHome.html', required_flights = required_flights, email = email, total_last_year = total_last_year, spending = spending)
			else:
				no_flight_error = 'No flight found'
				return render_template('customerHome.html', no_flight_error = no_flight_error, email = email, total_last_year = total_last_year, spending = spending)
		elif start != "" and end != "" and d_airport == "" and a_airport == "" and d_city != "" and a_city != "":
			query = 'SELECT * FROM Ticket NATURAL JOIN Flight NATURAL JOIN Airport WHERE email = %s AND d_airport = airport_name AND a_airport = airport_name AND city = %s AND city = %s AND d_date >= %s AND d_date <= %s'
			cursor.execute(query, (session['email'], d_city, a_city, start, end))
			required_flights = cursor.fetchall()
			if(required_flights):
				return render_template('customerHome.html', required_flights = required_flights, email = email, total_last_year = total_last_year, spending = spending)
			else:
				no_flight_error = 'No flight found'
				return render_template('customerHome.html', no_flight_error = no_flight_error, email = email, total_last_year = total_last_year, spending = spending)
		else:
			invalid_error = 'Invalid data'
			return render_template('customerHome.html', invalid_error = invalid_error, email = email, total_last_year = total_last_year, spending = spending)
	else:
		return render_template('customerHome.html', email = email, total_last_year = total_last_year, spending = spending)





@app.route('/customerSearchFlights', methods=['GET', 'POST'])
def customerSearchDlights():
	cursor = conn.cursor()
	total_last_year = pastYearSpending()
	spending = pastYearMonthlySpending()
	if request.method == 'POST':
		d_airport = request.form['d_airport']
		a_airport = request.form['a_airport']
		d_date = request.form['d_date']
		return_date = request.form['return_date']
		d_city = request.form['d_city']
		a_city = request.form['a_city']
		email = session['email']
		# search one way by airport
		if d_airport != "" and a_airport != "" and d_date != "" and return_date == "" and d_city == "" and a_city == "":
			query = 'SELECT flight_num, d_date, d_time, d_airport, a_date, a_time, a_airport, airline_name, base_price FROM Flight WHERE d_date = %s AND d_airport = %s AND a_airport = %s AND %s > CURRENT_DATE()'
			cursor.execute(query, (d_date, d_airport, a_airport, d_date))
			go_flights = cursor.fetchall()	
			if (go_flights):
				return render_template('customerHome.html', go_flights = go_flights, email = email, total_last_year = total_last_year, spending = spending)
			else:
				noGoError = 'Sorry, no trip found.'
				return render_template('customerHome.html', noGoError = noGoError, email = email, total_last_year = total_last_year, spending = spending)
		# search round trip by airport
		elif d_airport != "" and a_airport != "" and d_date != "" and return_date != "" and d_city == "" and a_city == "":
			if d_date > return_date:
				dateError = "Arrival date must be after departure date."
				return render_template('customerHome.html', email = email, total_last_year = total_last_year, spending = spending, dateError = dateError)
			query = 'SELECT flight_num, d_date, d_time, d_airport, a_date, a_time, a_airport, airline_name, base_price FROM Flight WHERE d_date = %s AND d_airport = %s AND a_airport = %s AND %s > CURRENT_DATE()'
			cursor.execute(query, (return_date, a_airport, d_airport, return_date))
			return_flights = cursor.fetchall()
			if (return_flights):
				query = 'SELECT flight_num, d_date, d_time, d_airport, a_date, a_time, a_airport, airline_name, base_price FROM Flight WHERE d_date = %s AND d_airport = %s AND a_airport = %s AND %s > CURRENT_DATE()'
				cursor.execute(query, (d_date, d_airport, a_airport, d_date))
				go_flights = cursor.fetchall()
				if (go_flights):
					return render_template('customerHome.html', return_flights = return_flights, go_flights = go_flights, email = email, total_last_year = total_last_year, spending = spending)
				else:
					noGoError = 'Sorry, no trip found.'
					return render_template('customerHome.html', noGoError = noGoError, email = email, total_last_year = total_last_year, spending = spending)
			else:
				noReturnError = 'Sorry, no return trip found.'
				return render_template('customerHome.html', noReturnError = noReturnError, email = email, total_last_year = total_last_year, spending = spending)
		# search round trip by city
		elif d_airport == "" and a_airport == "" and d_date != "" and return_date != "" and d_city != "" and a_city != "":
			if d_date > return_date:
				dateError = "Arrival date must be after departure date."
				return render_template('customerHome.html', email = email, total_last_year = total_last_year, spending = spending, dateError = dateError)
			# check if there is a return trip
			query = 'SELECT flight_num, d_date, d_time, d_airport, a_date, a_time, a_airport, airline_name, base_price FROM Flight NATURAL JOIN Airport WHERE d_airport = airport_name AND a_airport = airport_name AND city = %s AND city = %s AND d_date = %s AND %s > CURRENT_DATE()'
			cursor.execute(query, (a_city, d_city, return_date, return_date))
			return_flights = cursor.fetchall()
			if (return_flights):
				query = 'SELECT flight_num, d_date, d_time, d_airport, a_date, a_time, a_airport, airline_name, base_price FROM Flight NATURAL JOIN Airport WHERE d_airport = airport_name AND a_airport = airport_name AND city = %s AND city = %s AND d_date = %s AND %s > CURRENT_DATE()'
				cursor.execute(query, (d_city, a_city, d_date, d_date))
				go_flights = cursor.fetchall()
				if (go_flights):
					return render_template('customerHome.html', return_flights = return_flights, go_flights = go_flights, email = email, total_last_year = total_last_year, spending = spending)
				else:
					noGoError = 'Sorry, no trip found.'
					return render_template('customerHome.html', noGoError = noGoError, email = email, total_last_year = total_last_year, spending = spending)
			else:
				noReturnError = 'Sorry, no return trip found.'
				return render_template('customerHome.html', noReturnError = noReturnError, email = email, total_last_year = total_last_year, spending = spending)
		# search one way by airport
		elif d_airport == "" and a_airport == "" and d_date != "" and return_date == "" and d_city != "" and a_city != "":
			query = 'SELECT flight_num, d_date, d_time, d_airport, a_date, a_time, a_airport, airline_name, base_price FROM Flight NATURAL JOIN Airport WHERE d_airport = airport_name AND a_airport = airport_name AND city = %s AND city = %s AND d_date = %s AND %s > CURRENT_DATE()'
			cursor.execute(query, (d_city, a_city, d_date, d_date))
			go_flights = cursor.fetchall()
			if(go_flights):
				return render_template('customerHome.html', go_flights = go_flights, email = email, total_last_year = total_last_year, spending = spending)
			else:
				noGoError = 'Sorry, no trip found.'
				return render_template('customerHome.html', noGoError = noGoError, email = email, total_last_year = total_last_year, spending = spending)
		elif d_airport != "" and a_airport != "" and d_city != "" and a_city != "":
			invalidSearchError = 'Please enter only departure/arrival city or departure/arrival airport'
			return render_template('customerHome.html', invalidSearchError = invalidSearchError, email = email, total_last_year = total_last_year, spending = spending)
		else:
			invalidSearchError = 'Invalid data'
			return render_template('customerHome.html', invalidSearchError = invalidSearchError, email = email, total_last_year = total_last_year, spending = spending)
	else:
		return render_template('customerHome.html', email = email, total_last_year = total_last_year, spending = spending)


@app.route('/purchaseTicket', methods=['GET', 'POST'])
def purchaseTicket():
	cursor = conn.cursor()
	total_last_year = pastYearSpending()
	spending = pastYearMonthlySpending()
	email = session['email']
	if request.method == 'POST':
		flight_num = request.form['flight_num']
		d_date = request.form['d_date']
		d_time = request.form['d_time']
		airline_name = request.form['airline_name']
		card_type = request.form['card_type']
		card_number = request.form['card_number']
		card_exp = request.form['card_exp']
		card_name = request.form['card_name']
		# check if the flight to purchase exists
		query = 'SELECT * FROM Flight WHERE flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s AND d_date > CURRENT_DATE()'
		cursor.execute(query, (flight_num, d_date, d_time, airline_name))
	
		new_data = cursor.fetchone()
		t_ID = str(random.randint(1000,9999))

		if (new_data):
			query = 'SELECT base_price FROM Flight WHERE flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s AND d_date > CURRENT_DATE()'
			cursor.execute(query, (flight_num, d_date, d_time, airline_name))
			data = cursor.fetchone()
			# The sold price may be different from the base price. Handle the price increase mechanism.
			query = 'SELECT COUNT(t_ID) FROM Ticket NATURAL JOIN Airplane NATURAL JOIN Flight WHERE flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s'
			cursor.execute(query, (flight_num, d_date, d_time, airline_name))
			count_num = cursor.fetchone()
			query = 'SELECT num_seats FROM Flight NATURAL JOIN Airplane WHERE flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s'
			cursor.execute(query, (flight_num, d_date, d_time, airline_name))
			num_seats = cursor.fetchone()
			sold_price = data['base_price']

			# Should return error message if the card expiration date has passed.
			if(datetime.datetime.now() > datetime.datetime.strptime(card_exp, "%Y-%m-%d")):
				card_exp_error = 'Sorry, the card expiration date has passed!'
				return render_template('customerHome.html', card_exp_error = card_exp_error, email = email, total_last_year = total_last_year, spending = spending)
			# Should return error message if the tickets of the flight is fully booked.
			if(count_num['COUNT(t_ID)'] == (int(num_seats['num_seats']))):
				no_ticket_error = 'Sorry, there is no ticket!'
				return render_template('customerHome.html', no_ticket_error = no_ticket_error, email = email, total_last_year = total_last_year, spending = spending)
			elif(count_num['COUNT(t_ID)'] >= (int(num_seats['num_seats']) * 0.6)):
				sold_price = float(data['base_price'])
				sold_price *= 1.2
			insertion = 'INSERT INTO Ticket VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIME(), CURRENT_TIME(), %s, %s)'
			cursor.execute(insertion, (t_ID, airline_name, sold_price, email, flight_num, card_type, card_number, card_name, card_exp, d_date, d_time))
			conn.commit()
			purchase = 'INSERT INTO Purchase VALUES(%s, %s)'
			cursor.execute(purchase, (email, t_ID))
			conn.commit()
			cursor.close()
			total_last_year = pastYearSpending()
			spending = pastYearMonthlySpending()
			purchase_message = 'Successfully purchased ticket'
			return render_template('customerHome.html', purchase_message = purchase_message, email = email, total_last_year = total_last_year, spending = spending)
		else:
			no_purchase_error = 'Invalid purchase. Please try again'
			return render_template('customerHome.html', no_purchase_error = no_purchase_error, email = email, total_last_year = total_last_year, spending = spending)
	else:
		return render_template('customerHome.html', email = email, total_last_year = total_last_year, spending = spending)



@app.route('/cancelTrip', methods=['GET', 'POST'])
def cancel_trip():
	cursor = conn.cursor()
	total_last_year = pastYearSpending()
	spending = pastYearMonthlySpending()
	if request.method == 'POST':
		flight_num = request.form['flight_num']
		d_date = request.form['d_date']
		d_time = request.form['d_time']
		airline_name = request.form['airline_name']
		email = session['email']
		query = 'SELECT t_ID FROM Ticket NATURAL JOIN Flight WHERE email = %s and d_date = %s and flight_num = %s and d_time = %s and airline_name = %s and d_date >= CURDATE()'
		cursor.execute(query, (session['email'], d_date, flight_num, d_time, airline_name))
		data = cursor.fetchone()
		if(data):
			dep_date = datetime.datetime.strptime(d_date, "%Y-%m-%d")
			dep_time = datetime.datetime.strptime(d_time, "%H:%M")
			com_date = datetime.datetime.combine(dep_date.date(), dep_time.time())
			now_date = datetime.datetime.now()
			now_date += datetime.timedelta(days=1)
			if(now_date < com_date):
				query = 'DELETE FROM Purchase WHERE t_ID = %s'
				cursor.execute(query, (data['t_ID']))
				conn.commit()
				query = 'DELETE FROM Ticket WHERE t_ID = %s'
				cursor.execute(query, (data['t_ID']))
				conn.commit()
				cursor.close()
				total_last_year = pastYearSpending()
				spending = pastYearMonthlySpending()
				cancel_message = 'Successfully cancelled the trip'
				return render_template("customerHome.html", cancel_message = cancel_message, email = email, total_last_year = total_last_year, spending = spending)
			else:
				no_cancel_error = 'Could not cancel the flight, since the date is less than 24 hour'
				return render_template('customerHome.html', no_cancel_error = no_cancel_error, email = email, total_last_year = total_last_year, spending = spending)
		else:
			no_cancel_error = 'Could not cancel the flight'
			return render_template('customerHome.html', no_cancel_error = no_cancel_error, email = email, total_last_year = total_last_year, spending = spending)
	else:
		return render_template('customerHome.html', email = email, total_last_year = total_last_year, spending = spending)


@app.route('/customerRating', methods=['GET', 'POST'])
def customerRating():
	cursor = conn.cursor();
	# display default data
	total_last_year = pastYearSpending()
	spending = pastYearMonthlySpending()
	email = session['email']
	if request.method == 'POST':
		flight_num = request.form['flight_num']
		d_date = request.form['d_date']
		d_time = request.form['d_time']
		airline = request.form['airline_name']
		rating = request.form['rating']
		comment = request.form['comment']
		# check if the flight is in the customer's past flights
		query = 'SELECT * FROM Customer NATURAL JOIN Ticket WHERE email = %s AND flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s AND %s < CURRENT_DATE()'
		cursor.execute(query, (email, flight_num, d_date, d_time, airline, d_date))
		data = cursor.fetchone()
		if(data):
			# check if the customer already commented the trip
			query = 'SELECT * FROM Review WHERE email = %s AND flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s'
			cursor.execute(query, (email, flight_num, d_date, d_time, airline))
			comment = cursor.fetchone()
			if(comment):
				commentExistError = 'Sorry, this flight has already been commented or rated. Please try another.'
				return render_template('customerHome.html', commentExistError = commentExistError, total_last_year = total_last_year, spending = spending, email = email)
			else:
				query = 'INSERT INTO Review VALUES(%s, %s, %s, %s, %s, %s, %s)'
				cursor.execute(query, (email, flight_num, rating, comment, airline_name, d_date, d_time))
				conn.commit()
				cursor.close()
				commentSucc = 'Thanks for your feedback!'
				return render_template('customerHome.html', commentSucc = commentSucc, total_last_year = total_last_year, spending = spending, email = email)
		else:
			noFlightError = 'There is no flight or past flight you are looking for. Please try again.'
			return render_template('customerHome.html', noFlightError = noFlightError, total_last_year = total_last_year, spending = spending, email = email)
	else: 
		return render_template('customerHome.html', email = email)


@app.route('/trackExpenses', methods=['GET', 'POST'])
def trackExpenses():
	cursor = conn.cursor();
	email = session['email']
	total_last_year = pastYearSpending()
	spending = pastYearMonthlySpending()
	if request.method == 'POST':
		start = request.form['start_date']
		end = request.form['end_date']
		if start != "" and end != "":
			if start > end:
				startEndError = 'End date should be after the start date'
				return render_template('customerHome.html', email = email, spending = spending, total_last_year = total_last_year, startEndError = startEndError)
			query = 'SELECT %s AS start_date, %s AS end_date, SUM(sold_price) AS total FROM Ticket NATURAL JOIN Customer WHERE email = %s AND purchase_date >= %s AND purchase_date <= %s'
			cursor.execute(query, (start, end, email, start, end))
			# stores purchase date, sold_price in a given date range
			spending = cursor.fetchall()
			cursor.close()
			return render_template('customerHome.html', email = email, spending = spending, total_last_year = total_last_year)
		else:
			emptyError = 'Invalid data'
			return render_template('customerHome.html', emptyError = emptyError, email = email, spending = spending, total_last_year = total_last_year)
	else:
		return render_template('customerHome.html', email = email, spending = spending, total_last_year = total_last_year)

# 127.0.0.1 is the equivalent of localhost
# Port 3000 can be any port
if __name__ == "__main__":
  app.run("127.0.0.1", 3000, debug = True)
