from django.urls import path
from CardFightRegis import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.index, name="home"),
    path('about', views.about, name="about"),
    path('register', views.register, name="register"),
    path('deckcreator/', views.create_deck, name="deckcreator"),
    path('decks/', views.deck_list, name="deck_list"),  # optional list view
    path('cardpool', views.cardData, name="cardpool"),
    path('login/', views.login_view, name="login"),   # use login_view
    path('cardpool/<int:pk>/', views.card_detail, name='card_detail'),  # detail page
    path('logout', views.logout_view, name="logout"),
    path('ranking', views.ranking, name="ranking"),
    path("password_reset/", auth_views.PasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('form', views.competition_list, name="form"),
    path("competitions/", views.competition_list, name="competition_list"),
    # Removed the separate register URL
    path("competitions/<int:pk>/", views.competition_detail, name="competition_detail"),
    path('decks/<int:deck_id>/edit/', views.edit_deck, name='edit_deck'),
    path('decks/<int:deck_id>/delete/', views.delete_deck, name='delete_deck'),
]
