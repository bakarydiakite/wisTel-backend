from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Utilisateur, Solde

@receiver(post_save, sender=Utilisateur)
def create_solde(sender, instance, created, **kwargs):
    if created:
        Solde.objects.create(utilisateur=instance)
