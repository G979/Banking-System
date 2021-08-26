import random
import sqlite3


def new_cart_number():
    x = "400000" + str(random.randint(0, 999999999)).zfill(9) # 15 digits in a string
    check_luhn_sum = 0 # Luhn of 15 digits to find digit_16
    for i in range(15): # 0,1,...,14
        n = int(x[i])
        if i % 2 == 0:
            n *= 2
            if n > 9: n -= 9
        check_luhn_sum += n
    digit_16 = (10 - (check_luhn_sum % 10)) % 10 # no comments
    return x + str(digit_16)


def luhn_check(number):
    luhn_sum = 0
    for i in range(15):
        n = int(number[i])
        if i % 2 == 0:
            n *= 2
            if n > 9: n -= 9
        luhn_sum += n
    if int(number[15]) == ((10 - (luhn_sum % 10)) % 10):
        return 1
    else:
        return -1


def creat_an_account():
    card_number = new_cart_number()
    pin = str(random.randint(0, 9999)).zfill(4)
    row = (int(card_number), card_number, pin, 0)
    cur.execute('INSERT INTO card VALUES (?, ?, ?, ?);', row)
    con.commit()
    print("Your card has been created")
    print("Your card number:")
    print(card_number)
    print("Your card PIN:")
    print(pin)

def log_into_accout():
    card_number = input("Enter your card number:")
    pin = input("Enter your PIN:")
    cur.execute(f'SELECT number, pin FROM card WHERE number={card_number};')
    card_and_pin = cur.fetchone()
    con.commit()
    if (card_number, pin) == card_and_pin:
        logged = True
        print("You have successfully logged in!")
        print("")
        while logged:
            print("1. Balance")
            print("2. Add income")
            print("3. Do transfer")
            print("4. Close account")
            print("5. Log out")
            print("0. Exit")
            user_input = int(input())
            if user_input == 1:
                cur.execute(f'SELECT balance FROM card WHERE number={card_number};')
                print(f'Balance: {cur.fetchone()}')
                con.commit()
            elif user_input == 2:
                income = int(input("Enter income:"))
                # new_balance = balance + income
                cur.execute(f'UPDATE card SET balance = balance + {income} WHERE number ={card_number};')
                print("Income was added!")
                con.commit()
            elif user_input == 3:
                card_no = input("Enter card number:")
                if luhn_check(card_no) == -1:
                    print("Probably you made a mistake in the card number. Please try again!")
                    continue
                else:
                    cur.execute(f'SELECT number FROM card WHERE number={card_no};')
                    if cur.fetchone() == None:
                        print("Such a card does not exist.")
                        con.commit()
                        continue
                    else:
                        transfer_money = int(input("Enter how much money you want to transfer:"))
                        cur.execute(f'SELECT balance FROM card WHERE number={card_number};')
                        comparator = int(''.join(map(str, cur.fetchone())))
                        con.commit()
                        if transfer_money > comparator:
                            print("Not enough money!")
                            continue
                        else:
                            cur.execute(f'UPDATE card SET balance = balance + {transfer_money} WHERE number ={card_no};')
                            con.commit()
                            cur.execute(f'UPDATE card SET balance = balance - {transfer_money} WHERE number ={card_number};')
                            print("Success!")
                            con.commit()
            elif user_input == 4:
                cur.execute(f'DELETE FROM card WHERE number={card_number};')
                print("The account has been closed!")
                con.commit()
            elif user_input == 5:
                logged = False
                print("You have successfully logged out!")
            else:
                print("Bye!")
                cur.close()
                con.close()
                exit()
    else:
        print("Wrong card number or PIN!")

random.seed()
con = sqlite3.connect('card.s3db')
cur = con.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);")
con.commit()
balance = 0
while True:
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    user_input = int(input())
    if user_input == 1:
        creat_an_account()
    elif user_input == 2:
        log_into_accout()
    else:
        print("Bye!")
        cur.close()
        con.close()
        exit()