Air Ticket Reservation System

This document lists each use case and the SQL query(s) used to execute that use case


Use cases for when not login in (homepage):

1. View Public Info:
a. Search for future flights based on source city/airport name, destination city/airport name,
departure date for one way (departure and return dates for round trip).

By airport:
SELECT flight_num, d_date, d_time, d_airport, a_date, a_time, a_airport, base_price FROM Flight WHERE d_date = %s AND d_airport = %s AND a_airport = %s AND %s > CURRENT_DATE()

By city: (may be bugged)
SELECT flight_num, d_date, d_time, d_airport, a_date, a_time, a_airport FROM Flight NATURAL JOIN Airport WHERE d_airport = airport_name AND a_airport = airport_name AND city = %s AND city = %s AND d_date = %s AND %s > CURRENT_DATE()



b. Will be able to see the flights status based on airline name, flight number, arrival/departure
date.

SELECT airline_name, flight_num, d_date, a_date, status FROM Flight WHERE airline_name = %s AND flight_num = %s AND d_date = %s AND a_date = %s



2. Register: 2 types of user registrations (Customer, and Airline Staff) option via forms as mentioned in
the part 1 of the project.


Customer queries:
checkEmailQuery = "SELECT * FROM Customer WHERE email = %s"
fillCustomerQuery = "INSERT INTO Customer VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

Staff queries:
checkSiteUserQuery = "SELECT * FROM SiteUser WHERE email = %s or username = %s"
regQuery = "INSERT INTO SiteUser VALUES(%s, %s, %s, 1)"
regStaffQuery = "INSERT INTO AirlineStaff VALUES(%s, %s, %s, %s, %s, %s)"
regWorksAtQuery = "INSERT INTO Works_At VALUES (%s, %s)"


3. Login: 2 types of user login (Customer, and Airline Staff).

Customer queries:
doesUserExistQuery = "SELECT email, password, type from SiteUser where email = %s AND password = %s"
getCusNameQuery = "SELECT name from Customer where email = %s AND password = %s"

Staff queries:
doesStaffUserExistQuery = "SELECT username, password, type from SiteUser where username = %s AND password = %s"
getStaffNameQuery = "SELECT fname from AirlineStaff where email = %s AND password = %s"






Customer Use Cases (operations Customer can perform when they are logged in):

1. View My flights: Provide various ways for the user to see flights information which he/she purchased.
The default should be showing for the future flights. Optionally you may include a way for the user to
specify a range of dates, specify destination and/or source airport name or city name etc.

getFlightQuery ='SELECT * FROM Ticket NATURAL JOIN Flight WHERE email = %s and d_date >= CURDATE()'
getFlightQuery2 = 'SELECT * FROM Ticket NATURAL JOIN Flight WHERE email = %s and d_date >= %s and d_date <= %s and d_airport = %s and a_airport = %s'
getFlightQuery3 (might be bugged) = 'SELECT * FROM Ticket NATURAL JOIN Flight NATURAL JOIN Airport WHERE email = %s AND d_airport = airport_name AND a_airport = airport_name AND city = %s AND city = %s AND d_date >= %s AND d_date <= %s'




2. Search for flights: Search for future flights (one way or round trip) based on source city/airport name,
destination city/airport name, dates (departure or return).

see 'View Public Info'



3. Purchase tickets: Customer chooses a flight and purchase ticket for this flight, providing all the
needed data, via forms. You may find it easier to implement this along with a use case to search for
flights.

checkFlightExists = SELECT * FROM Flight WHERE flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s AND d_date > CURRENT_DATE()
getPrice= 'SELECT base_price FROM Flight WHERE flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s AND d_date > CURRENT_DATE()'
getCount= 'SELECT COUNT(t_ID) FROM Ticket NATURAL JOIN Airplane NATURAL JOIN Flight WHERE flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s'
getCapacity = 'SELECT num_seats FROM Flight NATURAL JOIN Airplane WHERE flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s'
insertIntoTicket = 'INSERT INTO Ticket VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, CURRENT_TIME(), CURRENT_TIME(), %s, %s)'
purchase = 'INSERT INTO Purchase VALUES(%s, %s)'

4. Cancel Trip: Customer chooses a purchased ticket for a flight that will take place more than 24 hours
in the future and cancel the purchase. After cancellation, the ticket will no longer belong to the
customer. The ticket will be available again in the system and purchasable by other customers.

getTicket = 'SELECT t_ID FROM Ticket NATURAL JOIN Flight WHERE email = %s and d_date = %s and flight_num = %s and d_time = %s and airline_name = %s and d_date >= CURDATE()'
deletionPur = 'DELETE FROM Purchase WHERE t_ID = %s'
deletionTick = 'DELETE FROM Ticket WHERE t_ID = %s'


5. Give Ratings and Comment on previous flights: Customer will be able to rate and comment on their
previous flights (for which he/she purchased tickets and already took that flight) for the airline they
logged in.



checkFlight = 'SELECT * FROM Customer NATURAL JOIN Ticket WHERE email = %s AND flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s AND %s < CURRENT_DATE()'
checkifComment= 'SELECT * FROM Review WHERE email = %s AND flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s'
insertReview = 'INSERT INTO Review VALUES(%s, %s, %s, %s, %s, %s, %s)'



6.Track My Spending: Default view will be total amount of money spent in the past year and a bar
chart/table showing month wise money spent for last 6 months. He/she will also have option to specify
a range of dates to view total amount of money spent within that range and a bar chart/table showing
month wise money spent within that range.

calcExpenses = 'SELECT %s AS start_date, %s AS end_date, SUM(sold_price) AS total FROM Ticket NATURAL JOIN Customer WHERE email = %s AND purchase_date >= %s AND purchase_date <= %s'


7.Logout: The session is destroyed and a “goodbye” page or the login page is displayed.
 session.clear()





Staff Use Cases (operations Staff can perform when they are logged in):
1. View flights: Defaults will be showing all the future flights operated by the airline he/she works for
the next 30 days. He/she will be able to see all the current/future/past flights operated by the airline
he/she works for based range of dates, source/destination airports/city etc. He/she will be able to see
all the customers of a particular flight.

whereWorksQuery = 'SELECT airline_name FROM Works_at WHERE username = %s'
getFlightDetails = 'SELECT flight_num, d_date, d_time, d_airport, a_date, a_time, a_airport FROM Flight WHERE d_date >= %s AND d_date <= %s AND d_airport = %s AND a_airport = %s AND airline_name = %s'
getWhichCustomers = 'SELECT email FROM Ticket WHERE flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s'
getFlightDetails (by city (might be bugged)) = 'SELECT flight_num, d_date, d_time, d_airport, a_date, a_time, a_airport FROM Flight NATURAL JOIN Airport WHERE d_airport = airport_name AND a_airport = airport_name AND city = %s AND city = %s AND d_date >= %s AND d_date <= %s AND airline_name = %s'


2. Create new flights: He or she creates a new flight, providing all the needed data, via forms. The
application should prevent unauthorized users from doing this action. Defaults will be showing all the
future flights operated by the airline he/she works for the next 30 days.

whereWorksQuery = 'SELECT airline_name FROM works_at WHERE username = %s'
checkExists = 'SELECT * FROM Flight WHERE flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s'
airplaneExists = 'SELECT * FROM Airplane WHERE a_id = %s AND airline_name = %s'
insertion = 'INSERT INTO Flight (flight_num, d_airport, d_date, d_time, a_airport, a_date, a_time, a_id, base_price, airline_name, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NULL)'

3. Change Status of flights: He or she changes a flight status (from on-time to delayed or vice versa) via
forms.

getFlights = 'SELECT * FROM Flight WHERE flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s'
updateStatusfield = 'UPDATE Flight SET status = %s WHERE flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s' 




4. Add airplane in the system: He or she adds a new airplane, providing all the needed data, via forms.
The application should prevent unauthorized users from doing this action. In the confirmation page,
she/he will be able to see all the airplanes owned by the airline he/she works for.

whichAirline = 'SELECT airline_name FROM works_at WHERE username = %s'
airplaneExists ='SELECT * FROM Airplane WHERE a_id = %s AND airline_name = %s'
insertion = 'INSERT INTO Airplane (a_id, num_seats, manufacturer, age, airline_name) VALUES (%s, %s, %s, %s, %s)'


5. Add new airport in the system: He or she adds a new airport, providing all the needed data, via
forms. The application should prevent unauthorized users from doing this action.

airportExists = 'SELECT * FROM Airport WHERE airport_name = %s'
insertion = 'INSERT INTO AIRPORT (airport_name, city, country, type) VALUES (%s, %s, %s, %s)'



6. View flight ratings: Airline Staff will be able to see each flight’s average ratings and all the comments
and ratings of that flight given by the customers.

getAirline = 'SELECT airline_name FROM works_at WHERE username = %s'
getReview= 'SELECT rating, comment FROM Review WHERE flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s'
avg = 'SELECT AVG(rating) AS average_rating FROM Review WHERE flight_num = %s AND d_date = %s AND d_time = %s AND airline_name = %s'

7. View frequent customers: Airline Staff will also be able to see the most frequent customer within
the last year. In addition, Airline Staff will be able to see a list of all flights a particular Customer has
taken only on that particular airline.


whichAirline = 'SELECT airline_name FROM works_at WHERE username = %s'
getfreqCusEmail= 'SELECT email, COUNT(t_ID) AS frequency FROM Customer NATURAL JOIN Ticket WHERE airline_name = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR) GROUP BY email ORDER BY frequency DESC LIMIT 1'



8. View reports: Total amounts of ticket sold based on range of dates/last year/last month etc. Month
wise tickets sold in a bar chart/table.

whichAirline= 'SELECT airline_name FROM works_at WHERE username = %s'
getnumTickets = 'SELECT COUNT(t_id) AS num_tickets FROM Ticket WHERE airline_name = %s AND purchase_date >= %s AND purchase_date <= %s'
       1 yr     'SELECT COUNT(ticket_id) AS num_tickets FROM Ticket WHERE airline_name = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR) AND purchase_date <= CURRENT_DATE()'
       1 month	'SELECT COUNT(ticket_id) AS num_tickets FROM Ticket WHERE airline_name = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH) AND purchase_date <= CURRENT_DATE()'

9. View Earned Revenue: Show total amount of revenue earned from ticket sales in the last month and
last year.


whichAirline = 'SELECT airline_name FROM works_at WHERE username = %s'
getYrRev= 'SELECT SUM(sold_price) AS year_revenue FROM Ticket WHERE airline_name = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 YEAR) AND purchase_date <= CURRENT_DATE()'
getMonthRev = 'SELECT SUM(sold_price) AS month_revenue FROM Ticket WHERE airline_name = %s AND purchase_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 MONTH) AND purchase_date <= CURRENT_DATE()'


10. Logout: The session is destroyed and a “goodbye” page or the login page is displayed.
session.clear()