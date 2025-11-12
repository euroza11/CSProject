from django.contrib import admin
from django.utils.html import format_html
from .models import Player, Deck, DeckCard
from .models import Competition, CompetitionRegistration
from django import forms
from .models import Card

# Inline Deck editing
class DeckInline(admin.TabularInline):
    model = Deck
    extra = 1
    fields = ("name", "created_at")
    readonly_fields = ("created_at",)

# Custom Player admin
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("username_display", "tel", "rank_badge", "point_badge", "deck_count")
    search_fields = ("user__username", "tel")
    list_filter = ("rank",)
    ordering = ("-point",)
    list_per_page = 20
    inlines = [DeckInline]

    # Username display
    def username_display(self, obj):
        return obj.user.username
    username_display.short_description = "Player"

    # Colored rank badge
    def rank_badge(self, obj):
        color = "gold" if obj.rank >= 10 else "silver" if obj.rank >= 5 else "gray"
        # Highlight top 3 players
        if obj.rank >= 15:
            return format_html('<b>👑<span style="color:{}">{}</span></b>', color, obj.rank)
        return format_html('<span style="color:{}; font-weight:bold;">{}</span>', color, obj.rank)
    rank_badge.short_description = "Rank"

    # Points badge
    def point_badge(self, obj):
        return format_html('<span style="color:blue; font-weight:bold;">{}</span>', obj.point)
    point_badge.short_description = "Points"

    # Count of decks
    def deck_count(self, obj):
        return obj.decks.count()
    deck_count.short_description = "Decks"

# Register models
admin.site.register(Player, PlayerAdmin)
admin.site.register(Deck)

# Admin branding
admin.site.site_header = "CardFight Admin Dashboard"
admin.site.site_title = "CardFight Admin Portal"
admin.site.index_title = "Welcome to CardFight Administration"

# Optional: Show which decks use this card
class DeckInlineForCard(admin.TabularInline):
    model = Deck.cards.through
    extra = 0
    verbose_name = "Deck using this card"
    verbose_name_plural = "Decks using this card"

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('name', 'card_type', 'nation', 'grade', 'power', 'shield')
    list_filter = ('card_type', 'nation', 'grade')
    search_fields = ('name', 'skill', 'description')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:50px;"/>', obj.image.url)
        return "-"
    image_tag.short_description = "Image"



@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ("name", "date", "location", "max_players")

@admin.register(CompetitionRegistration)
class CompetitionRegistrationAdmin(admin.ModelAdmin):
    list_display = ("player", "competition", "deck", "payment_status", "registered_at")
    list_filter = ("competition", "payment_status")
    search_fields = ("player__username", "competition__name")
    readonly_fields = ("deck_card_list", "registered_at")

    fieldsets = (
        (None, {
            "fields": ("player", "competition", "deck", "fee_slip", "payment_status", "registered_at")
        }),
        ("Deck Details", {
            "fields": ("deck_card_list",),
            "classes": ("collapse",),
        }),
    )

    def deck_card_list(self, obj):
        """Show all cards in the player's deck, with quantity and image if available."""
        if not obj.deck:
            return "No deck selected"

        # FIX: Iterate directly over the DeckCard intermediate model.
        # This provides direct access to both the Card object and the quantity.
        # .select_related('card') is used for efficient database querying.
        deck_cards = DeckCard.objects.filter(deck=obj.deck).select_related('card')
        
        if not deck_cards.exists():
            # Clearly indicate that the linked deck is empty.
            return format_html('<span style="color:red; font-weight:bold;">This deck has no cards.</span>')

        html = "<ul style='list-style:none; padding-left:0;'>"
        
        # Iterate over the DeckCard objects (dc)
        for dc in deck_cards:
            card = dc.card  # Access the related Card object
            quantity = dc.quantity # Access the quantity directly from the DeckCard object
            
            qty_text = f" × {quantity}"
            
            img_html = ""
            if card.image and hasattr(card.image, 'url'):
                img_html = f"<img src='{card.image.url}' style='height:50px; margin-right:10px; vertical-align:middle;'/>"
            
            html += f"<li style='margin-bottom:5px;'>{img_html}<strong>{card.name}</strong>{qty_text}</li>"
        
        html += "</ul>"
        return format_html(html)

    deck_card_list.short_description = "Cards in Deck"
