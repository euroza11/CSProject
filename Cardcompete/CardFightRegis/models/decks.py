from django.db import models
from .players import Player
from .cards import Card

class Deck(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name="decks")
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    cards = models.ManyToManyField(Card, blank=True, related_name="decks")

    def __str__(self):
        return self.name

class DeckCard(models.Model):
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('deck', 'card')
