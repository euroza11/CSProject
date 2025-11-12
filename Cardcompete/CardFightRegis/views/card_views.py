from django.shortcuts import render, get_object_or_404
from CardFightRegis.models import Card

def cardData(request):
    cards = Card.objects.all()

    # Use model choices instead of existing cards
    filter_nations = [n[0] for n in Card.NATION]
    filter_grades = [g[0] for g in Card.GRADE]
    filter_types = [t[0] for t in Card.TYPE]

    selected_nation = request.GET.get('nation')
    selected_grade = request.GET.get('grade')
    selected_type = request.GET.get('card_type')

    # Convert grade to int only if it is a valid number
    try:
        selected_grade = int(selected_grade)
    except (TypeError, ValueError):
        selected_grade = None

    if selected_nation:
        cards = cards.filter(nation=selected_nation)
    if selected_grade is not None:
        cards = cards.filter(grade=selected_grade)
    if selected_type:
        cards = cards.filter(card_type=selected_type)

    return render(request, 'cardData.html', {
        'cards': cards,
        'filter_nations': filter_nations,
        'filter_grades': filter_grades,
        'filter_types': filter_types,
        'selected_nation': selected_nation,
        'selected_grade': selected_grade,
        'selected_type': selected_type,
    })


def card_detail(request, pk):
    card = get_object_or_404(Card, pk=pk)
    return render(request, 'card_detail.html', {'card': card})
