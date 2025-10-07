from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Movie, Show, Booking
from .serializers import SignupSerializer, MovieSerializer, ShowSerializer, BookingSerializer
from .permissions import IsOwnerOrReadOnly
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


#Signup
class SignupView(APIView):
    permission_classes = (permissions.AllowAny,)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username'),
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='Email address'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password'),
            },
            required=['username', 'password']
        ),
        responses={201: 'User created successfully'}
    )
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)


#Movie List
class MovieListView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        movies = Movie.objects.all()
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)


#Shows for a Movie
class MovieShowsView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, movie_id):
        movie = get_object_or_404(Movie, id=movie_id)
        shows = movie.shows.all()
        serializer = ShowSerializer(shows, many=True)
        return Response(serializer.data)


#Book a Seat
class BookSeatView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, show_id):
        seat_number = request.data.get("seat_number")
        if seat_number is None:
            return Response({"detail": "seat_number is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            seat_number = int(seat_number)
        except ValueError:
            return Response({"detail": "seat_number must be an integer"}, status=status.HTTP_400_BAD_REQUEST)

        show = get_object_or_404(Show, id=show_id)

        if seat_number < 1 or seat_number > show.total_seats:
            return Response({"detail": f"seat_number must be between 1 and {show.total_seats}"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            already_booked = Booking.objects.filter(show=show, seat_number=seat_number, status='booked').exists()
            if already_booked:
                return Response({"detail": "This seat is already booked!"}, status=status.HTTP_400_BAD_REQUEST)

            booked_count = Booking.objects.filter(show=show, status='booked').count()
            if booked_count >= show.total_seats:
                return Response({"detail": "All seats are booked for this show!"}, status=status.HTTP_400_BAD_REQUEST)

            booking = Booking.objects.create(
                user=request.user,
                show=show,
                seat_number=seat_number,
                status='booked'
            )
            serializer = BookingSerializer(booking)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


#Cancel Booking
class CancelBookingView(APIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)

    def post(self, request, booking_id):
        booking = get_object_or_404(Booking, id=booking_id)
        self.check_object_permissions(request, booking)

        if booking.status == 'cancelled':
            return Response({"detail": "Booking is already cancelled"}, status=status.HTTP_400_BAD_REQUEST)

        booking.status = 'cancelled'
        booking.save()
        return Response({"detail": "Booking cancelled successfully"}, status=status.HTTP_200_OK)



#Bookings
class MyBookingsView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        bookings = Booking.objects.filter(user=request.user)
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
