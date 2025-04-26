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

        print("\Topup:")
        bank_account.topUp(1372)
        print(f"Balance after topUp $1372: {bank_account.displayBalance()}")
        bank_account.withdraw(111)
        print(f"Balance after withdraw $111: {bank_account.displayBalance()}")

if __name__ == "__main__":
    sys.exit(main())
