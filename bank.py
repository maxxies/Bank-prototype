import random
import csv
import sys


#  Class responsible for account(s) creation
class CreateAccount:
    def __init__(self):
        print("""
Select an option:
1: Current Account
2: Savings Account
3: Both """)

    # Generates account numbers for users
    def account_number():
        nums = list()
        for i in range(5):
            if i == 0:
                nums.append(random.randint(1, 9))
            else:
                nums.append(random.randint(0, 9))
        return ('{}{}{}{}{}'.format(nums[0],nums[1],nums[2],nums[3],nums[4]))

    # Current account creation
    @staticmethod
    def current_account(name, age, work):
        type_of_account = 0
        account_number = CreateAccount.account_number()
        amount = 0
        loan_status = False
        loan_amount = 0
        data = [name, age, work, type_of_account, account_number, amount, loan_status, loan_amount]
        BankData.addData(data)
        print("Data Saved.")
        print("Your account number is " + account_number)

    # Savings account creation
    @staticmethod
    def saving_account(name, age, work):
        type_of_account = 1
        account_number = CreateAccount.account_number()
        amount = 0
        loan_status = False
        loan_amount = 0
        data = [name, age, work, type_of_account, account_number, amount, loan_status, loan_amount]
        BankData.addData(data)
        print("Data Saved.")
        print("Your account number is " + account_number)

    # Both account creation
    @staticmethod
    def both_account(name, age, work):
        type_of_account_one = 0
        type_of_account_two = 1
        account_number_one = CreateAccount.account_number()
        account_number_two = CreateAccount.account_number()
        amount = 0
        loan_status = False
        loan_amount = 0
        data_one =[name, age, work, type_of_account_one, account_number_one, amount, loan_status, loan_amount]
        data_two = [name, age, work, type_of_account_two, account_number_two, amount, loan_status, loan_amount]
        BankData.addData(data_one)
        BankData.addData(data_two)
        print("Data Saved.")
        print("Your account number for current account is " + account_number_one)
        print("Your account number for savings account is " + account_number_two)


# Class responsible for logins
class Login:
    def __init__(self, account):
        self.account = account

    # Checks for user in the .csv files
    def findUser(self):
        users = BankData.readData()
        matching = [s for s in users if self.account in s]
        if matching == []:
            sys.exit('No account found. Try again!')
        else:
            for i in matching:
                return users.index(i)


# Class responsible for working in a user's data and transferring it to the .csv file.
class BankData:
    def __init__(self, name, age, occupation, account_type, account_number, amount, has_loan, loan_value):
        self.name = name
        self.age = age
        self.occupation = occupation
        self.account_type = account_type
        self.account_number = account_number
        self.amount = amount
        self.has_loan = has_loan
        self.loan_value = loan_value

    def __str__(self):
        out_string = "'{0}', {1}, {2}, {3}, {4}, {5}, {6}, {7}".format(
            self.name,
            self.age,
            self.occupation,
            self.account_type,
            self.account_number,
            self.amount,
            self.has_loan,
            self.loan_value
        )
        return out_string

    # Adds data
    def addData(DataList=[]):
        with open('Bankfile.csv', 'a', newline='\n') as csvfile:
            data_writer = csv.writer(
                csvfile,
                delimiter=',',
                quotechar=" ",
                quoting=csv.QUOTE_MINIMAL
            )
            data_writer.writerow(DataList)
            csvfile.close()


    # Reads data
    def readData():
        with open('Bankfile.csv', 'r', newline='\n') as csvfile:
            data_reader = csv.reader(
                csvfile,
                delimiter=' ',
                quotechar=" ",
                quoting=csv.QUOTE_MINIMAL
            )
            output = []
            for item in data_reader:
                output.append(item[0])
            csvfile.close()
            return output


# Class responsible for bank services options
class Menu:
    def __init__(self, user_id, option):
        self.user_id = user_id
        self.option = option

    # Gets all data of a user
    def user_option(self):
        all_users = BankData.readData()
        record = all_users[self.user_id]
        record_split = record.split(",")
        new_record = BankData(record_split[0].replace("'", ""),
                              int(record_split[1]),
                              record_split[2].replace("'", ""),
                              int(record_split[3]),
                              int(record_split[4]),
                              int(record_split[5]),
                              bool(record_split[6]),
                              int(record_split[7]))
        # Deposits amount
        if self.option == 1:
            print("Amount to deposit:")
            amount_to_deposit = int(input(prompt))
            new_record.amount = new_record.amount + amount_to_deposit
            new_record.has_loan = False
            message = f'\nHello {new_record.name},\n\nAn amount of GHS {amount_to_deposit:,.2f} has been deposited into your \
account.\nYour new balance is GHS {new_record.amount:,.2f}.'
            all_users.append(new_record.__str__())
            all_users.remove(record)
            file = open('Bankfile.csv', 'r+')
            file.truncate(0)
            file.close()
            for i in all_users:
                user = []
                user.append(i)
                BankData.addData(user)
            print(message)
        # Withdraw amount
        elif self.option == 2:
            print("Amount to withdraw:")
            amount_to_withdraw = int(input(prompt))
            # Checks for account type
            if new_record.account_type == 0:
                # Checks if amount is enough for a withdrawal
                if (amount_to_withdraw + 6) <= new_record.amount:
                    new_record.amount = (new_record.amount - amount_to_withdraw) - 6
                    new_record.has_loan = False
                    message = f'\nHello {new_record.name},\n\nAn amount of GHS {amount_to_withdraw:,.2f} has been withdrawn from \
your account.\nYour new balance is GHS {new_record.amount:,.2f}.'
                    all_users.append(new_record.__str__())
                    all_users.remove(record)
                    file = open('Bankfile.csv', 'r+')
                    file.truncate(0)
                    file.close()
                    for i in all_users:
                        user = []
                        user.append(i)
                        BankData.addData(user)
                    print(message)
                else:
                    print("Not enough funds to perform action.")
            else:
                # Checks if amount is enough for a withdrawal
                if (amount_to_withdraw + 1) <= new_record.amount:
                    new_record.amount = (new_record.amount - amount_to_withdraw) - 1
                    new_record.has_loan = False
                    message = f'\nHello {new_record.name},\n\nAn amount of GHS {amount_to_withdraw:,.2f} \
has been withdrawn from your account.\nYour new balance is GHS {new_record.amount:,.2f}.'
                    all_users.append(new_record.__str__())
                    all_users.remove(record)
                    file = open('Bankfile.csv', 'r+')
                    file.truncate(0)
                    file.close()
                    for i in all_users:
                        user = []
                        user.append(i)
                        BankData.addData(user)
                    print(message)
                else:
                    print("Not enough funds to perform action.")
        # Changes loan status of a user
        elif self.option == 3:
            print("Amount to loan. Note: Loan must not be more than 3 times your balance to be eligible.")
            user_loan = int(input(prompt))
            # Checks if user is eligible for a loan
            if user_loan < (new_record.amount * 3.5):
                new_record.amount = new_record.amount + user_loan
                new_record.has_loan = True
                new_record.loan_value = user_loan
                message = f'\nHello {new_record.name},\n\nAn amount of GHS {user_loan:,.2f} \
has been credited into your account as loan.\nYour new balance is GHS {new_record.amount:,.2f}.'
                all_users.append(new_record.__str__())
                all_users.remove(record)
                file = open('Bankfile.csv', 'r+')
                file.truncate(0)
                file.close()
                for i in all_users:
                    user = []
                    user.append(i)
                    BankData.addData(user)
                print(message)
            else:
                print("You are not eligible for the loan, try again. Thank you")
        # Prints balance of a user
        elif self.option == 4:
            if new_record.has_loan:
                message = f'\nHello {new_record.name},\n\nYour balance is GHS {new_record.amount:,.2f} \
with an outstanding debt of GHS {new_record.loan_value:,.2f}'
                print(message)
            else:
                message = f'\nHello {new_record.name},\n\nYour balance is GHS {new_record.amount:,.2f}'
                print(message)
        # Calculates simple and compound interest for a user
        elif self.option == 5:
            print("Number of months")
            time = int(input(prompt))
            # Checks for account type
            if new_record.account_type == 0:
                simple_interest = new_record.amount * 0.3 * (time/12)
                compound_interest = new_record.amount * pow((1 + 0.3), (time/12))
                message = f'\nHello {new_record.name},\n\nYour simple interest by {time} months would be GHS {simple_interest:,.2f} and \
compound interest would be GHS {compound_interest:,.2f}'
                print(message)
            else:
                simple_interest = new_record.amount * 2 * (time/12)
                compound_interest = new_record.amount * pow((1 + 2), (time/12))
                message = f'\nHello {new_record.name},\n\nYour simple interest by {time} months would be GHS {simple_interest:,.2f} and \
compound interest would be GHS {compound_interest:,.2f}'
                print(message)
        # Prints a statement for the user in a different file
        elif self.option == 6:
            if new_record.account_type == 0:
                type_account = "Current account"
            else:
                type_account = "Savings account"
            with open('Printstatement.txt', 'w') as print_statement:
                message = f'{new_record.name}\n\nAccount type: {type_account}\nCurrent Balance: \
GHS {new_record.amount:,.2f}\nOutstanding loan: GHS {new_record.loan_value:,.2f}'
                print_statement.write(message)
                print_statement.close()
            print("Open text file to read and download statement.")


# Prints start message
introduction = '''
  WELCOME TO SEMNOS MOBILE BANKING SERVICES.
~~~~~~~~~~~~~~~~~**************~~~~~~~~~~~~~~~~

Select an option:
1: Create an account
2: Log into an account '''
print(f"{introduction}")
prompt = ">>> "
userInput = input(prompt)
start = True

# Loop to make sure a correct value is been inputted without existing the program
while start:
    while userInput not in ["1", "2"]:
        print("""\nChoice must be within options given.
Select:
1: Create an account
2: Log into an account """)
        userInput = input(prompt)

    userInput = int(userInput)
    start = False

# Calls for inputs to pass to respective classes
# Checks to ask for an account opening questions
if userInput == 1:
    CreateAccount()
    userInputAccount = input(prompt)
    valid = True
    # Loop to make sure a correct value is been inputted without existing the program
    while valid:
        while userInputAccount not in ["1", "2", "3"]:
            print("""\nChoice must be within options given.
    Select:
    1: Current Account
    2: Savings Account
    3: Both """)
            userInputAccount = input(prompt)

        userInputAccount = int(userInputAccount)
        # calls current account method
        if userInputAccount == 1:
            print("\nGive out the following details.")
            print("Enter your name:")
            userName = input(prompt).upper()
            print("Enter age:")
            userAge = input(prompt)
            print("Enter occupation:")
            userWork = input(prompt)
            CreateAccount.current_account(userName, userAge, userWork)
            valid = False
        # calls savings account method
        elif userInputAccount == 2:
            print("Enter your name:")
            userName = input(prompt).upper()
            print("Enter age:")
            userAge = input(prompt)
            print("Enter occupation:")
            userWork = input(prompt)
            CreateAccount.saving_account(userName, userAge, userWork)
            valid = False
        # calls both account method
        elif userInputAccount == 3:
            print("Enter your name:")
            userName = input(prompt).upper()
            print("Enter age:")
            userAge = input(prompt)
            print("Enter occupation:")
            userWork = input(prompt)
            CreateAccount.both_account(userName, userAge, userWork)
            valid = False
# Checks to ask for login questions
elif userInput == 2:
    print("Account Number:")
    userAccount = input(prompt)
    # uses inputted account number to get the index/location of the user's data in the .csv file
    userId = Login(userAccount.__str__()).findUser()
    print('''\nSelect an option:
1: Deposit 
2: Withdraw
3: Loans
4: Check Balance
5: Compound and Simple interest
6: Print Statement ''')
    userInputMenu = input(prompt)
    looping = True

    # Loop to make sure a correct value is been inputted without existing the program
    while looping:
        while userInputMenu not in ["1", "2", "3", "4", "5", "6"]:
            print("""\nChoice must be within options given.
Select:
1: Deposit 
2: Withdraw
3: Loans
4: Check Balance
5: Compound and Simple interest
6: Print Statement """)
            userInputMenu = input(prompt)

        userInputMenu = int(userInputMenu)
        looping = False
    # Calls menu class
    Menu(userId, userInputMenu).user_option()
