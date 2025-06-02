from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Player(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='player_profile',
        verbose_name='Użytkownik'
    )
    balance = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1000.00,
        verbose_name='Saldo'
    )

    class Meta:
        verbose_name = 'Gracz'
        verbose_name_plural = 'Gracze'

    def __str__(self):
        return f"{self.user.username} (${self.balance})"


class GameHistory(models.Model):
    BET_TYPES = [
        ('number', 'Konkretny numer'),
        ('color', 'Kolor'),
        ('even_odd', 'Parzyste/Nieparzyste'),
        ('dozen', 'Tuzin'),
        ('column', 'Kolumna'),
        ('high_low', 'Wysokie/Niskie')
    ]

    player = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='game_history',
        verbose_name='Gracz'
    )
    bet_type = models.CharField(
        max_length=20,
        choices=BET_TYPES,
        verbose_name='Typ zakładu'
    )
    bet_value = models.CharField(
        max_length=50,
        verbose_name='Wartość zakładu'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Kwota zakładu'
    )
    result = models.CharField(
        max_length=50,
        verbose_name='Wynik'
    )
    payout = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        verbose_name='Wygrana'
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data i czas'
    )

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Historia gry'
        verbose_name_plural = 'Historie gier'

    def __str__(self):
        return f"{self.player.user.username} - {self.get_bet_type_display()} (${self.amount})"


# Automatyczne tworzenie profilu gracza przy rejestracji użytkownika
@receiver(post_save, sender=User)
def create_player_profile(sender, instance, created, **kwargs):
    if created:
        Player.objects.get_or_create(user=instance)


# Aktualizacja profilu przy zmianie danych użytkownika
@receiver(post_save, sender=User)
def save_player_profile(sender, instance, **kwargs):
    instance.player_profile.save()