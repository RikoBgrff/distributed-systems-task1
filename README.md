# distributed-systems-task1
This repository contains code files and report of Task 1 of Distributed Systems by Ali Sebetci

CENG 427 Distributed Systems
Assignment 1: Distributed Object Server with ICE

Name Surname: Arifali Baghirli
Student Number: 210201848
Github Repository: 
1. Algorithm Design
The system is designed using ZeroC ICE framework to simulate two remote objects: Calculator and BankAccount.
• The Calculator object provides four basic operations: addition, subtraction, multiplication, and division.
• The BankAccount object allows topping up the balance, withdrawing funds, and displaying the current balance.

Flow of execution:
1. Define interfaces using Slice language (banking.ice).
2. Implement the interfaces in server.py using ICE’s server capabilities.
3. The server adds the objects to the adapter and listens on port 10000.
4. The client (client.py) connects to the server, obtains proxies to the objects, and invokes methods remotely.
5. The Calculator methods perform basic arithmetic. BankAccount manages the balance.
6. Errors such as dividing by zero or insufficient funds raise appropriate exceptions.
2. Application Output
Sample run output:
Calculator Operations:
11 + 2 = 13.0
9 - 7 = 2.0
33 * 33 = 1089.0
788 / 2 = 394.0
Topup:
Balance after topUp $1372: 1372.0
Balance after withdraw $111: 1261.0
3. Conclusion
Through this assignment, I improved my skills in building distributed systems using ZeroC ICE.
I learned how to define remote interfaces with Slice, implement them in Python, and handle remote method invocations.
Challenges included handling exception cases like division by zero and managing balance errors properly.
In the future, the solution can be improved by adding authentication mechanisms and persistent storage for bank accounts.
4. Appends (Source Codes)
banking.ice
module Banking {
    interface Calculator {
        double add(double x, double y);
        double subtract(double x, double y);
        double multiply(double x, double y);
        double divide(double x, double y);
    };

    interface BankAccount {
        void topUp(double amount);
        void withdraw(double amount);
        double displayBalance();
    };
};
server.py
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

client.py
import sys
import Ice
import banking

def main():
    with Ice.initialize(sys.argv) as communicator:
        base_calculator = communicator.stringToProxy("Calculator:default -p 10000")
        calculator = banking.CalculatorPrx.checkedCast(base_calculator)

        base_account = communicator.stringToProxy("BankAccount:default -p 10000")
        bank_account = banking.BankAccountPrx.checkedCast(base_account)

        if not calculator or not bank_account:
            print("Invalid proxy")
            return

        print("Calculator Operations:")
        print(f"11 + 2 = {calculator.add(11, 2)}")
        print(f"9 - 7 = {calculator.subtract(9, 7)}")
        print(f"33 * 33 = {calculator.multiply(33, 33)}")
        print(f"788 / 2 = {calculator.divide(788, 2)}")

        print("\nTopup:")
        bank_account.topUp(1372)
        print(f"Balance after topUp $1372: {bank_account.displayBalance()}")
        bank_account.withdraw(111)
        print(f"Balance after withdraw $111: {bank_account.displayBalance()}")

if __name__ == "__main__":
    sys.exit(main())

