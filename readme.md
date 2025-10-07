                                              Backend Developer Intern Assignment


Tech Stack: Python, Django, Django REST Framework, JWT, Swagger
Platform: Linux


Objective
The goal of this assignment is to evaluate your ability to design and implement a backend
system using Django and Django REST Framework. You will build a Movie Ticket Booking
System that includes authentication, movie/show management, seat booking, and API
documentation.

Requirements
1. Authentication
●Implement Signup and Login functionality.
● Use JWT authentication (e.g., djangorestframework-simplejwt).
● All booking-related APIs should require a valid JWT token.
2. Models
Create the following models in Django:
●Movie: title, duration_minutes
● Show: movie (FK), screen_name, date_time, total_seats
● Booking: user (FK), show (FK), seat_number, status
(booked/cancelled), created_at
3. APIs
Implement the following endpoints:
●POST /signup → Register a user
●POST /login → Authenticate and return JWT token
● GET /movies/ → List all movies
● GET /movies/<id>/shows/ → List all shows for a movie
● POST /shows/<id>/book/ → Book a seat (input: seat_number)
● POST /bookings/<id>/cancel/ → Cancel a booking
● GET /my-bookings/ → List all bookings for the logged-in user
4. Swagger Documentation
●Integrate Swagger (via drf-yasg or drf-spectacular).
● API docs should be available at /swagger/.
● JWT authentication should be clearly documented.
● Each endpoint must display proper request/response schemas.
 Business Rules
●Prevent double booking: a seat cannot be booked twice.
● Prevent overbooking: bookings should not exceed the show’s capacity.
● Cancelling a booking should free up the seat.
Deliverables
1.A GitHub repository containing:
○Django project code
○ requirements.txt file
 A well-documented README.md with:
■ Setup instructions (how to run the project)
■ How to generate JWT tokens and call APIs
■ Link to Swagger docs (/swagger/)
 Evaluation Criteria
● Django/DRF fundamentals → models, serializers, views, urls.
● Correctness of booking logic → seat/booking rules are followed.
● Swagger documentation → complete and usable.
●Code quality & structure → clean, modular, readable code.
●README quality → clear instructions.
 
Expected API Flow
1. User registers → /signup
2. User logs in → /login → gets JWT
3. User views movies → /movies/
4. User views shows → /movies/<id>/shows/
5. User books a seat → /shows/<id>/book/
6. User views their bookings → /my-bookings/
7. User cancels a booking → /bookings/<id>/cancel/
✦ Submission:
https://github.com/tejal2102/movie-ticket-booking-backend
