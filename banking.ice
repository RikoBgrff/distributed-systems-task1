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
