import random
import time

def rand_string(chars=2):
    r_str = ''
    charlist = list("abcdefghijklmnopqrstuvwxyz")
    r_list = [charlist[random.randint(0, 25)] for i in range(chars)]
    for i in range(len(r_list)):
        r_str += r_list[i]
    return r_str

def gen_users():
    rusers = [dict(username = rand_string(9), pin = random.randint(1000, 9999), balance = dict(GHS = random.randint(0, 99999), USD = random.randint(0, 99999))) for i in range(20)]
    return rusers

def print_header():
    print("################################")
    print(" _______     ______  _   _ _  __")
    print("|  __ \ \   / /  _ \| \ | | |/ /")
    print("| |__) \ \_/ /| |_) |  \| | ' / ")
    print("|  ___/ \   / |  _ <| . ` |  <  ")
    print("| |      | |  | |_) | |\  | . \ ")
    print("|_|      |_|  |____/|_| \_|_|\_\\")
    print("################################")

class Ledger:
    def __init__(self):
        self.users = []
        self.transactions = []


class User:
    def __init__(self, username, pin, ledger):
        assert ledger is not None
        assert isinstance(ledger, Ledger)
        assert username is not None
        assert pin is not None
        assert int(pin) <= 9999

        self.username = username
        self.pin = pin
        self.signedin = False
        self.current_user = None
        self.ledger = ledger
    
    def user_exists(self):
        for user in self.ledger.users:
            if user['username'] == self.username and user['pin'] == self.pin:
                return True
        return False

    def login(self):
        if self.user_exists() and not self.signedin:
            self.signedin = True
            for user in self.ledger.users:
                if user['username'] == self.username and user['pin'] == self.pin:
                    self.current_user = user
        return self.current_user

    def register(self):
        if not self.user_exists() and not self.signedin:
            new_user = dict(username=self.username, pin=self.pin, balance=dict(GHS=0, USD=0))
            self.ledger.users.append(new_user)     
        return self.login()

    def check_balance(self):
        return self.current_user['balance']['USD']

    def logout(self):
        self.signedin = False


class Transaction:
    def __init__(self, user, ledger, amount):
        assert isinstance(user, User)
        assert isinstance(ledger, Ledger)
        self.user = user
        self.ledger = ledger
        self.amount = amount
        self.balance = 0
        self.ttime = time.time()
    
    def withdraw(self):
        if self.user.user_exists():
            self.balance = self.user.current_user['balance']['USD']
            if self.balance >= self.amount:
                self.user.current_user['balance']['USD'] -= self.amount
                self.balance = self.user.current_user['balance']['USD']
                self.ledger.transactions.append(dict(ttime=self.ttime, username=self.user.username, pin=self.user.pin, amount=self.amount, balance=self.balance))

    def reciept(self):
        print_header()
        print("\n")
        print("Username: " + self.user.username)
        print("Transactions 📜")
        print("--------------")
        print("Withdrew: %d $" % self.amount)
        print("Balance: %d $" % self.balance)
        print("\n")
        print("------End of Transaction------")

        

    def mini_statement(self):
        print_header()
        print("\n")
        print("Username: " + self.user.username)
        print("Transactions 📜")
        print("--------------")
        for tr in self.ledger.transactions:
            if tr['username'] == self.user.username and tr['pin'] == self.user.pin:
                print("------------" + str(tr['ttime']) + "-------------")
                print("Withdrew: %d $" % tr['amount'])
                print("Balance: %d $" % tr['balance'])
                print("\n")
        print("\n")
        print("------End of Transaction------")


def run():
    print_header()
    ledger = Ledger()
    ledger.users = gen_users()

    print('Hello ! Welcome to PYBANK !')
    print('Please login to proceed.')
    
    username = input('Please enter your username: ')
    while len(username) < 3:
        username = input("Invalid username! Try Again: ")
    pin = input('Please enter your 4 digit pin: ')
    while not (pin.isnumeric() and len(pin) == 4):
        pin = input('Invalid pin! Try again: ')

    print("\nLogging in")
    auth = User(username, pin, ledger)

    if not auth.user_exists():
        print("\n It seems you are yet to open an acount with us.")
        print("If you would like to  register with us type yes.")
        new_account = input("Create an account?")
        if new_account.lower() == "yes":
            auth.register()
        else:
            run()
    else:
        auth.login()
    print("\n Logged in as: %s" % auth.username)
    print("##########################################")
    print("1) Withdraw Cash")
    print("2) Check your Balance")
    print("3) Get your MiniStatement")
    print("4) Logout")
    main_opt = input("Enter your choice: ")
    if main_opt == str(1):
        tamount = int(input("How much do you want?"))
        while tamount > int(auth.check_balance()):
            tamount = int(input("That's too much! Try Again"))
        transactions = Transaction(auth, ledger, tamount)
        transactions.withdraw()
        print("\nTransaction successful")
        rcpts = input("Do you want a Receipt?")
        if rcpts.lower() == "yes":
            transactions.reciept()
        else:
            run()
    elif main_opt == str(2):
        print("/n########################")
        print("Your account balance is: " + str(auth.check_balance()))
    elif main_opt == str(3):
        print("/n########################")
        transactions = Transaction(auth, ledger, 0)
        transactions.mini_statement()


if __name__ == '__main__':
    run()



