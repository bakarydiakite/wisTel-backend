from rest_framework import serializers
from .models import Utilisateur, Appel, Solde

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = ['id', 'phone']

class AppelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appel
        fields = ['id', 'numero', 'type_appel', 'date_appel']

class SoldeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Solde
        fields = ['montant']
