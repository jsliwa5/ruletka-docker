from django.contrib import admin
from .models import Player, GameHistory

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['user', 'balance']
    search_fields = ['user__username']

@admin.register(GameHistory)
class GameHistoryAdmin(admin.ModelAdmin):
    list_display = ['player', 'bet_type', 'result', 'payout', 'timestamp']
    list_filter = ['bet_type']
    search_fields = ['player__user__username']