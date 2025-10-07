from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

class Movie(models.Model):
    title = models.CharField(max_length=255)
    duration_minutes = models.PositiveIntegerField()

    def __str__(self):
        return self.title


class Show(models.Model):
    movie = models.ForeignKey(Movie, related_name='shows', on_delete=models.CASCADE)
    screen_name = models.CharField(max_length=100)
    date_time = models.DateTimeField()
    total_seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.movie.title} - {self.screen_name} @ {self.date_time}"


class Booking(models.Model):
    STATUS_CHOICES = (
        ('booked', 'Booked'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE)
    show = models.ForeignKey(Show, related_name='bookings', on_delete=models.CASCADE)
    seat_number = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='booked')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('show', 'seat_number')
        ordering = ('-created_at',)

    def __str__(self):
        return f"{self.user} - {self.show} - seat {self.seat_number} ({self.status})"
