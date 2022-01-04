from account.models import User
from django.test import TestCase

from payment.models import Balance, Operation


class Test_Create_Balance(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_user1 = User.objects.create(
            uuid="da739912-b671-4093-934a-f5b5b3de2429",
            first_name="user1",
            last_name="user1",
            email="a@a.com",
            password="123456789",
        )
        test_user2 = User.objects.create(
            uuid="da739912-b671-4093-934a-f5b5b3de2430",
            first_name="user2",
            last_name="user2",
            email="b@a.com",
            password="123456789",
        )
        test_balance_user1 = Balance.objects.create(
            user_id="da739912-b671-4093-934a-f5b5b3de2429", balance=99345.38, is_active=True
        )
        test_balance_user2 = Balance.objects.create(
            user_id="da739912-b671-4093-934a-f5b5b3de2430", balance=789348.27, is_active=True
        )
        test_transfer = Operation.objects.create(sender=test_user1, receiver=test_user2, amount=1000.45)

    def test_balance_content(self):
        # Balance tests
        balance1 = Balance.objects.get(id=1)
        balance2 = Balance.objects.get(id=2)
        user_1 = f"{balance1.user}"
        balance1 = f"{balance1.balance}"
        user2 = f"{balance2.user}"
        balance2 = f"{balance2.balance}"
        self.assertEqual(user_1, "user1, user1")
        self.assertEqual(balance1, "99345.38")
        self.assertEqual(user2, "user2, user2")
        self.assertEqual(balance2, "789348.27")
        # Transfert tests
        transfert = Operation.objects.get(id=1)
        sender = f"{transfert.sender}"
        receiver = f"{transfert.receiver}"
        amount = f"{transfert.amount}"
        self.assertEqual(sender, "user1, user1")
        self.assertEqual(receiver, "user2, user2")
        self.assertEqual(amount, "1000.45")


# Create your tests here.
