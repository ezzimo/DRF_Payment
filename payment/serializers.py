from account.models import User
from rest_framework import serializers

from .models import Balance, Operation


class UserBalanceSerializer(serializers.ModelSerializer):
    balance = serializers.DecimalField(max_digits=9, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = Balance
        fields = ["balance"]


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["uuid", "email", "first_name", "last_name", "mobile", "balance"]


class OperationCreateSerializer(serializers.ModelSerializer):
    sender = serializers.UUIDField(format="hex_verbose")
    receiver = serializers.UUIDField(format="hex_verbose")
    amount = serializers.DecimalField(max_digits=9, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = Operation
        fields = ["sender", "receiver", "amount"]


class OperationListSerializer(serializers.ModelSerializer):
    amount = serializers.DecimalField(max_digits=9, decimal_places=2, coerce_to_string=False)

    class Meta:
        model = Operation
        fields = ["sender", "receiver", "amount", "created_at"]
