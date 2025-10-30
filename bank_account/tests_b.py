import unittest
from main_b import BankAccount, InsufficientFunds
import json
from decimal import Decimal
from unittest.mock import MagicMock, patch

def mocked_get_call(url, heads=None):
    sample_data = json.load(open("some_result.json"))
    return sample_data

class A1:
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        sample_data = json.load(open("some_result.json"))
        return sample_data

class TestDeposits(unittest.TestCase):
    def test_deposit_positive(self):
        acc = BankAccount(0)
        acc.deposit(100)
        self.assertEqual(acc.get_balance(), 100)
        acc.deposit(50)
        self.assertEqual(acc.get_balance(), 150)
    @patch("main_b.external_tools.make_get_request",mocked_get_call)
    def test_deposit_zero(self):
        acc = BankAccount(100)
        with self.assertRaises(ValueError):
            acc.deposit(0)

    def test_deposit_negative(self):
        acc = BankAccount(100)
        with self.assertRaises(ValueError):
            acc.deposit(-50)


class TestWithdraw(unittest.TestCase):
    def test_withdraw_positive(self):
        acc = BankAccount(200)
        acc.withdraw(50)
        self.assertEqual(acc.get_balance(), 150)

    def test_withdraw_zero(self):
        acc = BankAccount(100)
        with self.assertRaises(ValueError):
            acc.withdraw(0)

    def test_withdraw_negative(self):
        acc = BankAccount(100)
        with self.assertRaises(ValueError):
            acc.withdraw(-10)

    def test_withdraw_too_much(self):
        acc = BankAccount(100)
        with self.assertRaises(InsufficientFunds):
            acc.withdraw(200)


class TestTransfer(unittest.TestCase):
    def test_transfer_success(self):
        acc1 = BankAccount(200)
        acc2 = BankAccount(100)
        acc1.transfer(acc2, 50)
        self.assertEqual(acc1.get_balance(), 150)
        self.assertEqual(acc2.get_balance(), 150)

    def test_transfer_insufficient_funds(self):
        acc1 = BankAccount(50)
        acc2 = BankAccount(100)
        with self.assertRaises(InsufficientFunds):
            acc1.transfer(acc2, 200)

    def test_transfer_invalid_account(self):
        acc1 = BankAccount(100)
        with self.assertRaises(TypeError):
            acc1.transfer("Not Account", 50)

class TestGetBalance(unittest.TestCase):
    def test_get_balance(self):
        acc = BankAccount(300)
        self.assertEqual(acc.get_balance(), 300)

if __name__ == '__main__':
    unittest.main()
