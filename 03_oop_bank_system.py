"""OOP bank system — accounts, transfers, statements, error handling."""

from dataclasses import dataclass, field
from datetime import datetime
from abc import ABC, abstractmethod
import uuid


class InsufficientFundsError(Exception):
    """Raised when a withdrawal violates an account's balance rules."""


@dataclass
class Transaction:
    kind: str  # 'credit' | 'debit'
    amount: float
    note: str = ""
    when: datetime = field(default_factory=datetime.now)

    def __str__(self) -> str:
        sign = "+" if self.kind == "credit" else "-"
        ts = self.when.strftime("%Y-%m-%d %H:%M")
        return f"{ts}  {sign}₹{self.amount:10.2f}  {self.note}"


class Account(ABC):
    def __init__(self, owner: str, initial: float = 0):
        if initial < 0:
            raise ValueError("Initial balance cannot be negative")
        self._id = str(uuid.uuid4())[:8].upper()
        self._owner = owner
        self._balance = initial
        self._history: list[Transaction] = []

    @property
    def balance(self) -> float:
        return self._balance

    @property
    def account_id(self) -> str:
        return self._id

    @property
    def owner(self) -> str:
        return self._owner

    def deposit(self, amount: float, note: str = "") -> "Account":
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self._balance += amount
        self._history.append(Transaction("credit", amount, note))
        return self

    @abstractmethod
    def withdraw(self, amount: float, note: str = "") -> "Account":
        """Each account type enforces its own withdrawal rules."""

    def transfer(self, to: "Account", amount: float) -> None:
        if to is self:
            raise ValueError("Cannot transfer to the same account")
        self.withdraw(amount, note=f"Transfer to {to.account_id}")
        to.deposit(amount, note=f"Transfer from {self.account_id}")

    def statement(self, last: int = 5) -> None:
        print(f"\nAccount {self._id} ({self.__class__.__name__}) — {self._owner}")
        print(f"Balance: ₹{self._balance:,.2f}\n")
        if not self._history:
            print("  No transactions yet.")
            return
        for t in self._history[-last:]:
            print(f"  {t}")

    def __str__(self) -> str:
        return f"{self._id} | {self._owner} | {self.__class__.__name__} | ₹{self._balance:,.2f}"


class SavingsAccount(Account):
    MIN_BALANCE = 1000

    def withdraw(self, amount: float, note: str = "") -> "Account":
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self._balance - amount < self.MIN_BALANCE:
            raise InsufficientFundsError(
                f"Must maintain ₹{self.MIN_BALANCE:,.2f} minimum balance"
            )
        self._balance -= amount
        self._history.append(Transaction("debit", amount, note))
        return self


class CurrentAccount(Account):
    """No minimum balance, but allows overdraft up to a limit."""

    OVERDRAFT_LIMIT = 5000

    def withdraw(self, amount: float, note: str = "") -> "Account":
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if self._balance - amount < -self.OVERDRAFT_LIMIT:
            raise InsufficientFundsError(
                f"Exceeds overdraft limit of ₹{self.OVERDRAFT_LIMIT:,.2f}"
            )
        self._balance -= amount
        self._history.append(Transaction("debit", amount, note))
        return self


class Bank:
    """Holds and manages all accounts."""

    def __init__(self, name: str):
        self.name = name
        self._accounts: dict[str, Account] = {}

    def open_account(self, owner: str, kind: str = "savings", initial: float = 0) -> Account:
        kinds = {"savings": SavingsAccount, "current": CurrentAccount}
        if kind not in kinds:
            raise ValueError(f"Unknown account type: {kind!r} (use 'savings' or 'current')")
        account = kinds[kind](owner, initial)
        self._accounts[account.account_id] = account
        return account

    def get_account(self, account_id: str) -> Account:
        try:
            return self._accounts[account_id.strip().upper()]
        except KeyError:
            raise ValueError(f"No account with ID {account_id}")

    def list_accounts(self) -> None:
        if not self._accounts:
            print("No accounts yet.")
            return
        for acc in self._accounts.values():
            print(f"  {acc}")


def main() -> None:
    bank = Bank("PyBank")
    menu = """
1. Open account
2. Deposit
3. Withdraw
4. Transfer
5. Statement
6. List accounts
7. Exit
"""
    while True:
        print(menu)
        choice = input("Choose an option: ").strip()
        try:
            if choice == "1":
                owner = input("Owner name: ").strip()
                kind = input("Type (savings/current): ").strip().lower()
                initial = float(input("Initial deposit: ₹"))
                acc = bank.open_account(owner, kind, initial)
                print(f"Opened account {acc.account_id} for {owner}")

            elif choice == "2":
                acc = bank.get_account(input("Account ID: "))
                acc.deposit(float(input("Amount: ₹")), note="Manual deposit")
                print(f"New balance: ₹{acc.balance:,.2f}")

            elif choice == "3":
                acc = bank.get_account(input("Account ID: "))
                acc.withdraw(float(input("Amount: ₹")), note="Manual withdrawal")
                print(f"New balance: ₹{acc.balance:,.2f}")

            elif choice == "4":
                src = bank.get_account(input("From account ID: "))
                dst = bank.get_account(input("To account ID: "))
                src.transfer(dst, float(input("Amount: ₹")))
                print("Transfer complete.")

            elif choice == "5":
                bank.get_account(input("Account ID: ")).statement()

            elif choice == "6":
                bank.list_accounts()

            elif choice == "7":
                print("Goodbye!")
                break

            else:
                print("Invalid option, try again.")

        except ValueError as e:
            print(f"Error: {e}")
        except InsufficientFundsError as e:
            print(f"Transaction declined: {e}")

    bank = Bank("Test")
    sav = bank.open_account("Veda", "savings", 5000)
    cur = bank.open_account("Friend", "current", 0)

    sav.deposit(1000)
    sav.transfer(cur, 2000)
    sav.statement()
    cur.statement()

    try:
        sav.withdraw(10000)  # should fail — below min balance
    except InsufficientFundsError as e:
        print("Caught:", e)

    try:
        cur.withdraw(6000)  # should fail — beyond overdraft
    except InsufficientFundsError as e:
        print("Caught:", e)


if __name__ == "__main__":
    main()