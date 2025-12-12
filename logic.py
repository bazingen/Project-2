from __future__ import annotations
import csv
from typing import List, Dict


class BankLogic:
    """
    A class to manage bank account data stored in a CSV file
    """
    def __init__(self, filename: str = "accounts.csv") -> None:
        """
        Method to create BankLogic object
        :param filename: Path to the CSV file containing accounts
        """
        self.filename: str = filename

    def _read_accounts(self) -> List[Dict[str, str]]:#Got help from google
        """
        Method to read all account records from the file
        :return: list of accounts
        """
        accounts: List[Dict[str, str]] = []

        try:
            with open(self.filename, newline="") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    accounts.append(row)
        except FileNotFoundError:
            pass

        return accounts

    def _write_accounts(self, accounts: List[Dict[str, str]]) -> None:#Got help from google
        """
        Method to write account balance back to csv file
        :param accounts: List of account dictionaries to save
        """
        fieldnames: List[str] = ["first_name", "last_name", "pin", "balance"]

        with open(self.filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(accounts)

    def _find_account_index(
        self,
        accounts: List[Dict[str, str]],
        first_name: str,
        last_name: str,
        pin: str,
    ) -> int:
        """
        Method to find the index of an account
        :param accounts: List of account dictionaries to search
        :param first_name: Persons first name
        :param last_name: Persons last name
        :param pin: Account PIN
        :return: Index of the matching account
        """
        first_name = first_name.strip().lower()
        last_name = last_name.strip().lower()
        pin = pin.strip()

        if first_name == "" or last_name == "" or pin == "":
            raise ValueError("First name, last name, and PIN are required.")

        for index, account in enumerate(accounts):
            if (
                account.get("first_name", "").strip().lower() == first_name
                and account.get("last_name", "").strip().lower() == last_name
                and account.get("pin", "").strip() == pin
            ):
                return index

        raise ValueError("Account not found")

    def get_balance(self, first_name: str, last_name: str, pin: str) -> float:
        """
        Method to get the current balance for account
        :param first_name: Persons first name
        :param last_name: Persons last name
        :param pin: Account PIN
        :return: The current balance as a float
        """
        accounts = self._read_accounts()
        index = self._find_account_index(accounts, first_name, last_name, pin)
        balance_text = accounts[index].get("balance", "0")

        try:
            return float(balance_text)
        except ValueError:
            raise ValueError("Invalid balance")

    def deposit(
        self,
        first_name: str,
        last_name: str,
        pin: str,
        amount: float,
    ) -> float:
        """
        Method to deposit money and return new balance
        :param first_name: Persons first name
        :param last_name: Persons last name
        :param pin: Account PIN
        :param amount: Amount to deposit
        :return: New balance after the deposit
        """
        if amount <= 0:
            raise ValueError("Deposit can not be 0.")

        accounts = self._read_accounts()
        index = self._find_account_index(accounts, first_name, last_name, pin)

        balance_text = accounts[index].get("balance", "0")
        try:
            old_balance = float(balance_text)
        except ValueError:
            raise ValueError("Invalid balance")

        new_balance = old_balance + amount
        accounts[index]["balance"] = f"{new_balance:.2f}"
        self._write_accounts(accounts)

        return new_balance

    def withdraw(
        self,
        first_name: str,
        last_name: str,
        pin: str,
        amount: float,
    ) -> float:
        """
        Method to withdraw money and return new balance
        :param first_name: Persons first name
        :param last_name: Persons last name
        :param pin: Account PIN
        :param amount: Amount to withdrawal
        :return: new balance after the withdrawal
        """
        if amount <= 0:
            raise ValueError("Withdrawal must be more than 0")

        accounts = self._read_accounts()
        index = self._find_account_index(accounts, first_name, last_name, pin)

        balance_text = accounts[index].get("balance", "0")
        try:
            old_balance = float(balance_text)
        except ValueError:
            raise ValueError("Invalid balance")

        if amount > old_balance:
            raise ValueError("Insufficient funds")

        new_balance = old_balance - amount
        accounts[index]["balance"] = f"{new_balance:.2f}"
        self._write_accounts(accounts)

        return new_balance
