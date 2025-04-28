from django.urls import path
from .views import *

urlpatterns = [
    path('send-otp/', send_otp, name='send_otp'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('appels/', enregistrer_appel, name='enregistrer_appel'),
    path('appels/historique/', historique_appels, name='historique_appels'),
    path('solde/', consulter_solde, name='consulter_solde'),
    path('solde/recharger/', recharger_solde, name='recharger_solde'),
    # path('solde/transactions/', consulter_transactions, name='consulter_transactions'),
    # path('solde/transactions/<int:transaction_id>/', consulter_transaction_detail, name='consulter_transaction_detail'),
]
