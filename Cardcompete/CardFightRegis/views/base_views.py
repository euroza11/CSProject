from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from CardFightRegis.models import Player, CompetitionRegistration

def index(request):
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def ranking(request):
    # Exclude admins
    players = Player.objects.filter(user__is_staff=False, user__is_superuser=False).order_by('-point')

    player_data = []
    for idx, player in enumerate(players, start=1):
        registration_count = CompetitionRegistration.objects.filter(player=player.user).count()
        player_data.append({
            'order': idx,
            'username': player.user.username,
            'tel': player.tel,
            'registrations': registration_count,
            'point': player.point,
        })

    return render(request, 'ranking.html', {'player_data': player_data})