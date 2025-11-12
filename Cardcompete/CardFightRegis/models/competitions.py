from django.db import models
from django.conf import settings
from CardFightRegis.models import Deck  # make sure Deck model is imported

class Competition(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=200, blank=True, null=True)
    max_players = models.IntegerField(default=32)

    def __str__(self):
        return self.name


class CompetitionRegistration(models.Model):
    PAYMENT_STATUS = [
        ('PENDING', 'Pending'),
        ('PAID', 'Paid'),
        ('CANCELLED', 'Cancelled'),
    ]

    player = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, related_name="registrations")
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, null=True, blank=True)
    fee_slip = models.FileField(upload_to='fee_slips/', null=True, blank=True)
    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS,
        default='PENDING'
    )
    registered_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("player", "competition")  # prevent double registration

    def __str__(self):
        return f"{self.player.username} → {self.competition.name}"
