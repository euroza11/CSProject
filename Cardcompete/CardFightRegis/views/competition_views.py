from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from CardFightRegis.models import Competition, CompetitionRegistration, Deck

def competition_list(request):
    competitions = Competition.objects.all().order_by("date")
    user_registrations = {}

    if request.user.is_authenticated:
        # Create a dict: competition.id -> registration object
        regs = CompetitionRegistration.objects.filter(player=request.user)
        user_registrations = {reg.competition.id: reg for reg in regs}

    return render(request, "competition_list.html", {
        "competitions": competitions,
        "user_registrations": user_registrations,
    })


@login_required
def competition_detail(request, pk):
    competition = get_object_or_404(Competition, pk=pk)
    current_registrations = competition.registrations.count()
    user_registration = CompetitionRegistration.objects.filter(
        player=request.user, competition=competition
    ).first()

    # Get the player's decks for the registration form
    player_decks = request.user.player.decks.all() if hasattr(request.user, 'player') else []

    if request.method == "POST":
        selected_deck_id = request.POST.get('deck')
        fee_slip = request.FILES.get('fee_slip')

        if user_registration:
            messages.warning(request, "You are already registered for this competition.")
        else:
            if competition.registrations.count() >= competition.max_players:
                messages.error(request, "Registration is full.")
            else:
                # Get selected deck
                deck = None
                if selected_deck_id:
                    deck = get_object_or_404(Deck, pk=selected_deck_id, player=request.user.player)

                # Create registration
                CompetitionRegistration.objects.create(
                    player=request.user,
                    competition=competition,
                    deck=deck,
                    fee_slip=fee_slip,
                    payment_status='PENDING'
                )
                messages.success(request, f"You have registered for {competition.name}!")

        return redirect('competition_detail', pk=competition.id)

    return render(request, 'competition_detail.html', {
        'competition': competition,
        'current_registrations': current_registrations,
        'user_registration': user_registration,
        'player_decks': player_decks,
    })
