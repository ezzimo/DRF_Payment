from account.models import User
from django.db import models


class Balance(models.Model):

    user = models.ForeignKey(User, related_name="Owner", on_delete=models.PROTECT)
    balance = models.DecimalField(max_digits=9, decimal_places=2, default=0.0, verbose_name=("Balance"))
    is_active = models.BooleanField("Is Active", default=False)
    created_at = models.DateTimeField("Created at", auto_now_add=True, editable=False)
    updated_at = models.DateTimeField("Updated at", auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Balance"
        verbose_name_plural = "Balances"

    def __str__(self):
        return f"{self.user.first_name}, {self.user.last_name}"


class Operation(models.Model):
    sender = models.ForeignKey(User, related_name=("Sender"), on_delete=models.PROTECT)
    receiver = models.ForeignKey(User, related_name=("Receiver"), on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=9, decimal_places=2, default=0.0, verbose_name=("Amount"))
    created_at = models.DateTimeField("Created at", auto_now_add=True, editable=False)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Operation"
        verbose_name_plural = "Operations"

    def __str__(self):
        return f"{self.sender}, {self.created_at}"
