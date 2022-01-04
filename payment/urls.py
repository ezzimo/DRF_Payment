from django.urls import path

from .views import BalanceView, TransactionViewSet, TransferView, UsersView

app_name = "payment"

urlpatterns = [
    path("users/<uuid:user_id>", BalanceView.as_view()),
    path("users/", UsersView.as_view()),
    path("operations/", TransactionViewSet.as_view()),
    path("transfert/", TransferView.as_view()),
]
