from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt
from .models import Player, GameHistory
import json
from django.contrib.auth.forms import UserCreationForm
from decimal import Decimal


def home(request):
    return render(request, 'index.html')


def check_auth(request):
    if request.user.is_authenticated:
        return JsonResponse({'status': 'authenticated'})
    return JsonResponse({'status': 'unauthorized'}, status=401)


def get_balance(request):
    if request.user.is_authenticated:
        try:
            player = Player.objects.get(user=request.user)
            return JsonResponse({'balance': player.balance})
        except Player.DoesNotExist:
            return JsonResponse({'error': 'Player not found'}, status=404)
    return JsonResponse({'status': 'unauthorized'}, status=401)


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = authenticate(username=data['username'], password=data['password'])
        if user:
            login(request, user)
            player, _ = Player.objects.get_or_create(user=user)
            return JsonResponse({
                'status': 'success',
                'balance': player.balance
            })
        return JsonResponse({'status': 'error'}, status=401)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def update_balance(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = request.user
        if user.is_authenticated:
            player = Player.objects.get(user=user)
            player.balance = data['balance']
            player.save()

            GameHistory.objects.create(
                player=player,
                amount=data.get('amount', 0),
                bet_type=data.get('bet_type', ''),
                bet_value=data.get('bet_value', ''),
                result=data.get('result', ''),
                payout=data.get('payout', 0)
            )
            return JsonResponse({'status': 'OK'})
        return JsonResponse({'status': 'unauthorized'}, status=401)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def get_game_history(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            try:
                player = Player.objects.get(user=request.user)
                history = GameHistory.objects.filter(player=player).order_by('-timestamp')[:10]
                return JsonResponse({
                    'history': [
                        {
                            'bet_type': h.bet_type,
                            'bet_value': h.bet_value,
                            'result': h.result,
                            'payout': h.payout,
                            'timestamp': h.timestamp.strftime("%Y-%m-%d %H:%M:%S")
                        } for h in history
                    ]
                })
            except Player.DoesNotExist:
                return JsonResponse({'error': 'Player profile does not exist'}, status=404)
        return JsonResponse({'status': 'unauthorized'}, status=401)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = UserCreationForm({
                'username': data.get('username'),
                'password1': data.get('password1'),
                'password2': data.get('password2')
            })
            if form.is_valid():
                user = form.save()
                return JsonResponse({'status': 'success'})
            return JsonResponse({'errors': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def add_funds(request):
    if request.method == 'POST':
        try:
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Unauthorized'}, status=401)

            data = json.loads(request.body)
            amount = Decimal(str(data['amount']))

            player = Player.objects.get(user=request.user)
            player.balance += amount
            player.save()

            return JsonResponse({
                'status': 'success',
                'new_balance': float(player.balance)
            })

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except (KeyError, ValueError):
            return JsonResponse({'error': 'Invalid amount'}, status=400)
        except Player.DoesNotExist:
            return JsonResponse({'error': 'Player not found'}, status=404)
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def user_logout(request):
    if request.method == 'POST':
        logout(request)
        return JsonResponse({'status': 'success'})
    return JsonResponse({'error': 'Method not allowed'}, status=405)
