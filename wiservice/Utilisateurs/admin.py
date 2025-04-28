from django.contrib import admin

from .models import Utilisateur, Appel, Solde, OTP, Recharge
from django.utils.translation import gettext_lazy as _

# class AdminCategories(admin.ModelAdmin):
#     list_display = ('nom_categorie', 'date_ajout')
# @admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = ('phone', 'date_inscription')
    search_fields = ('phone',)

# class adminUtilisateur(admin.ModelAdmin):
#     list_display = ('phone', 'date_inscription')

admin.site.register(Utilisateur)
admin.site.register(Appel)
admin.site.register(Solde)
admin.site.register(OTP)
admin.site.register(Recharge)
