class BankAccount:
    def __init__(self, owner, balance=0.0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print("Deposited amount:",amount)
        else:
            print("Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount <= 0:
            print("Withdrawal amount must be positive.")
        elif amount > self.balance:
            print("Insufficient funds.")
        else:
            self.balance -= amount
            print("Withdrew :",amount)

    def get_balance(self):
        return self.balance


account = BankAccount("John Doe", 100.0)
account.deposit(50)
account.withdraw(30)
print("Current balance :", account.get_balance())