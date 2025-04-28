from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
    phone = models.CharField(max_length=20, unique=True)
    date_inscription = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone
class OTP(models.Model):
    phone = models.CharField(max_length=20)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone} - {self.code}"
class Appel(models.Model):
    TYPE_CHOICES = [
        ('OUT', 'Sortant'),
        ('IN', 'Entrant'),
    ]

    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    numero = models.CharField(max_length=20)
    type_appel = models.CharField(max_length=10, choices=TYPE_CHOICES, default='OUT')
    date_appel = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur.phone} → {self.numero}"

class Solde(models.Model):
    utilisateur = models.OneToOneField(Utilisateur, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.utilisateur.phone} - {self.montant} GNF"

class Recharge(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    montant = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur.phone} - {self.montant} GNF"