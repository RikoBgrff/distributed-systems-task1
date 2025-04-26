import sys
import Ice
import banking

class CalculatorI(banking.Calculator):
    def add(self, x, y, current=None):
        return x + y

    def subtract(self, x, y, current=None):
        return x - y

    def multiply(self, x, y, current=None):
        return x * y

    def divide(self, x, y, current=None):
        if y == 0:
            raise ZeroDivisionError("Are you first grade? you can't divide to 0")
        return x / y

class BankAccountI(banking.BankAccount):
    def __init__(self):
        self.balance = 0.0

    def topUp(self, amount, current=None):
        self.balance += amount

    def withdraw(self, amount, current=None):
        if amount > self.balance:
            raise ValueError("Sorry you are broke")
        self.balance -= amount

    def displayBalance(self, current=None):
        return self.balance

class Server(Ice.Application):
    def run(self, args):
        adapter = self.communicator().createObjectAdapterWithEndpoints("BankingAdapter", "default -p 10000")
        calculator = CalculatorI()
        bank_account = BankAccountI()
        
        adapter.add(calculator, Ice.stringToIdentity("Calculator"))
        adapter.add(bank_account, Ice.stringToIdentity("BankAccount"))

        adapter.activate()
        print("Server is up...")
        self.communicator().waitForShutdown()
        return 0

if __name__ == "__main__":
    sys.exit(Server().main(sys.argv))
