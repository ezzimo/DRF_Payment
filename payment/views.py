from account.models import User
from account.serializers import UsersSerializer
from django.db import transaction
from django.db.models import F
from django.db.models.query_utils import Q
from django.http.response import Http404
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from .models import Balance, Operation
from .serializers import (
    OperationCreateSerializer,
    OperationListSerializer,
    UserBalanceSerializer,
)


# Create your views here.
class BalanceView(generics.RetrieveAPIView):
    lookup_field = "user_id"
    lookup_value_regex = "[0-9a-f]{32}"
    serializer_class = UserBalanceSerializer

    def get_queryset(self, **kwargs):
        try:
            queryset = Balance.objects.all()
            return queryset
        except Balance.DoesNotExist:
            raise Http404


class UsersView(generics.ListAPIView):
    serializer_class = UsersSerializer
    queryset = User.objects.all()


class TransferView(generics.CreateAPIView):
    serializer_class = OperationCreateSerializer
    queryset = Operation.objects.all()

    def create(self, request, *args, **kwargs):
        serializer = OperationCreateSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            with transaction.atomic():
                sender = Balance.objects.filter(user_id=serializer.validated_data.get("sender"))
                if sender and sender[0].balance >= serializer.validated_data.get("amount"):
                    Balance.objects.filter(user_id=serializer.validated_data.get("sender")).update(
                        balance=F("balance") - serializer.validated_data.get("amount", 0)
                    )
                    Balance.objects.filter(user_id=serializer.validated_data.get("receiver")).update(
                        balance=F("balance") + serializer.validated_data.get("amount", None)
                    )
                    serializer.save(
                        sender=User.objects.get(uuid=serializer.validated_data.get("sender")),
                        receiver=User.objects.get(uuid=serializer.validated_data.get("receiver")),
                    )
                    return Response({"message": "transfer done successfully"}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class TransactionViewSet(generics.ListAPIView):
    serializer_class = OperationListSerializer
    queryset = Operation.objects.all()

    def get_queryset(self, **kwargs):
        """
        Restricting the returned purchased Operations to a given user,
        by filtering against a date range query parameter in the URL.
        """
        start = self.request.query_params.get("start_date")
        end = self.request.query_params.get("end_date")
        try:
            queryset = self.queryset.filter(Q(created_at__date__range=[start, end]))
            return queryset
        except Operation.DoesNotExist:
            raise Http404
