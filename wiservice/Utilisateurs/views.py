from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.utils import timezone
from django.contrib.auth import get_user_model
from wiservice import settings
from .models import OTP
from twilio.rest import Client
import random
from .models import Appel, Utilisateur, Solde
from .serializers import AppelSerializer, SoldeSerializer

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

User = get_user_model()
@api_view(['POST'])
def send_otp(request):
    phone = request.data.get('phone')
    if not phone:
        return Response({'error': 'Numéro requis'}, status=400)
    code = str(random.randint(100000, 999999))
    OTP.objects.create(phone=phone, code=code)
    print(f"📲 Requête reçue pour : {phone}")
    print(f"📩 Code OTP généré : {code}")
    try:
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        client.messages.create(
            body=f"Votre code de vérification est : {code}",
            from_=settings.TWILIO_PHONE_NUMBER,  
            to=phone
        )
        print("✅ SMS envoyé avec succès")
    except Exception as e:
        print("❌ Échec d’envoi Twilio :", e)
        return Response({'error': 'Échec d’envoi SMS'}, status=500)

    return Response({'message': f'Code envoyé à {phone}'})

@api_view(['POST'])
def verify_otp(request):
    phone = request.data.get('phone')
    code = request.data.get('code')
    if not phone or not code:
        return Response({'error': 'Téléphone et code requis'}, status=400)
    otp = OTP.objects.filter(phone=phone, code=code).order_by('-created_at').first()
    if otp and (timezone.now() - otp.created_at).seconds < 300:
        utilisateur, _ = Utilisateur.objects.get_or_create(phone=phone)
        token, _ = Token.objects.get_or_create(user=utilisateur)
        return Response({
            'token': token.key,
            'user': utilisateur.phone,
            'message': 'Connexion réussie ✅'
        })
    return Response({'error': 'Code invalide ou expiré'}, status=400)

# enregistrement d'un appel
@api_view(['POST'])
def enregistrer_appel(request):
    phone = request.data.get('phone') 
    numero = request.data.get('numero')
    type_appel = request.data.get('type', 'OUT')

    try:
        utilisateur = Utilisateur.objects.get(phone=phone)
    except Utilisateur.DoesNotExist:
        return Response({'error': 'Utilisateur non trouvé'}, status=404)

    Appel.objects.create(utilisateur=utilisateur, numero=numero, type_appel=type_appel)
    return Response({'message': 'Appel enregistré avec succès'})

# consulter l'historique des appels
@api_view(['GET'])
def historique_appels(request):
    phone = request.query_params.get('phone')

    try:
        utilisateur = Utilisateur.objects.get(phone=phone)
    except Utilisateur.DoesNotExist:
        return Response({'error': 'Utilisateur non trouvé'}, status=404)

    appels = Appel.objects.filter(utilisateur=utilisateur).order_by('-date_appel')
    serializer = AppelSerializer(appels, many=True)
    return Response(serializer.data)

# consulter le solde de l'utilisateur
@api_view(['GET'])
def consulter_solde(request):
    phone = request.query_params.get('phone')

    try:
        utilisateur = Utilisateur.objects.get(phone=phone)
        solde, _ = Solde.objects.get_or_create(utilisateur=utilisateur)
    except Utilisateur.DoesNotExist:
        return Response({'error': 'Utilisateur non trouvé'}, status=404)

    serializer = SoldeSerializer(solde)
    return Response(serializer.data)

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Utilisateur, Solde, Recharge

import traceback
from decimal import Decimal
@api_view(['POST'])
def recharger_solde(request):
    try:
        phone = request.data.get('phone')
        montant = request.data.get('montant')

        if not phone or not montant:
            return Response({'error': 'Téléphone et montant requis'}, status=400)

        montant = Decimal(str(montant).strip()) 

        utilisateur, _ = Utilisateur.objects.get_or_create(phone=phone)
        solde, _ = Solde.objects.get_or_create(utilisateur=utilisateur)

        solde.montant += montant
        solde.save()

        Recharge.objects.create(utilisateur=utilisateur, montant=montant)

        return Response({'message': '✅ Rechargement réussi', 'nouveau_solde': solde.montant})

    except Exception as e:
        import traceback
        traceback.print_exc()
        return Response({'error': 'Erreur interne : ' + str(e)}, status=500)




