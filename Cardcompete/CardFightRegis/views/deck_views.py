from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from CardFightRegis.models import Player, Deck, Card, DeckCard
from CardFightRegis.deck_forms import DeckForm

@login_required
def create_deck(request):
    player = request.user.player
    cards = Card.objects.all()

    # Filters from GET parameters
    selected_nation = request.GET.get('nation')
    selected_grade = request.GET.get('grade')
    selected_type = request.GET.get('card_type')

    if selected_nation:
        cards = cards.filter(nation=selected_nation)
    if selected_grade:
        try:
            selected_grade = int(selected_grade)
            cards = cards.filter(grade=selected_grade)
        except ValueError:
            selected_grade = None
    if selected_type:
        cards = cards.filter(card_type=selected_type)

    # All choices for filters
    filter_nations = [n[0] for n in Card.NATION]
    filter_grades = [g[0] for g in Card.GRADE if isinstance(g[0], int)]
    filter_types = [t[0] for t in Card.TYPE]

    if request.method == "POST":
        deck_form = DeckForm(request.POST)
        card_ids = request.POST.getlist('card')
        quantities = request.POST.getlist('quantity')

        if deck_form.is_valid():
            deck = deck_form.save(commit=False)
            deck.player = player
            deck.save()

            for card_id, qty in zip(card_ids, quantities):
                qty = int(qty)
                if qty > 0:
                    card = Card.objects.get(id=card_id)
                    DeckCard.objects.create(deck=deck, card=card, quantity=qty)

            messages.success(request, f"Deck '{deck.name}' created successfully!")
            return redirect('deck_list')
    else:
        deck_form = DeckForm()

    return render(request, 'deckcreator.html', {
        'deck_form': deck_form,
        'cards': cards,
        'filter_nations': filter_nations,
        'filter_grades': filter_grades,
        'filter_types': filter_types,
        'selected_nation': selected_nation,
        'selected_grade': selected_grade,
        'selected_type': selected_type,
        'is_edit': False,
    })


@login_required
def edit_deck(request, deck_id):
    player = request.user.player
    deck = get_object_or_404(Deck, id=deck_id, player=player)
    cards = Card.objects.all()

    selected_nation = request.GET.get('nation')
    selected_grade = request.GET.get('grade')
    selected_type = request.GET.get('card_type')

    if selected_nation:
        cards = cards.filter(nation=selected_nation)
    if selected_grade:
        try:
            selected_grade = int(selected_grade)
            cards = cards.filter(grade=selected_grade)
        except ValueError:
            selected_grade = None
    if selected_type:
        cards = cards.filter(card_type=selected_type)

    filter_nations = [n[0] for n in Card.NATION]
    filter_grades = [g[0] for g in Card.GRADE if isinstance(g[0], int)]
    filter_types = [t[0] for t in Card.TYPE]

    if request.method == "POST":
        deck_form = DeckForm(request.POST, instance=deck)
        card_ids = request.POST.getlist('card')
        quantities = request.POST.getlist('quantity')

        if deck_form.is_valid():
            deck_form.save()
            DeckCard.objects.filter(deck=deck).delete()
            for card_id, qty in zip(card_ids, quantities):
                qty = int(qty)
                if qty > 0:
                    card = Card.objects.get(id=card_id)
                    DeckCard.objects.create(deck=deck, card=card, quantity=qty)

            messages.success(request, f"Deck '{deck.name}' updated successfully!")
            return redirect('deck_list')
    else:
        deck_form = DeckForm(instance=deck)

    deck_cards = {dc.card.id: dc.quantity for dc in deck.deckcard_set.all()}

    return render(request, 'deckcreator.html', {
        'deck_form': deck_form,
        'cards': cards,
        'deck_cards': deck_cards,
        'filter_nations': filter_nations,
        'filter_grades': filter_grades,
        'filter_types': filter_types,
        'selected_nation': selected_nation,
        'selected_grade': selected_grade,
        'selected_type': selected_type,
        'is_edit': True,
    })


@login_required
def delete_deck(request, deck_id):
    player = request.user.player
    deck = get_object_or_404(Deck, id=deck_id, player=player)
    deck.delete()
    messages.success(request, f"Deck '{deck.name}' deleted successfully!")
    return redirect('deck_list')


@login_required
def deck_list(request):
    player = request.user.player
    decks = player.decks.all()
    return render(request, 'deck_list.html', {'decks': decks})
