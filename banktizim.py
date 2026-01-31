import random
import datetime

# ================= User class =================
class User:
    def __init__(self, fullname, password, balance=0):
        self.fullname = fullname
        self.__password = password
        self.__balance = balance
        self.transactions = []

    @property
    def balance(self):
        return self.__balance

    def check_password(self, password):
        return self.__password == password

    def deposit(self, amount):
        self.__balance += amount
        self._add_transaction("deposit", amount)

    def withdraw(self, amount):
        if amount <= self.__balance:
            self.__balance -= amount
            self._add_transaction("withdraw", amount)
            return True
        return False

    def transfer(self, receiver, amount):
        if amount <= self.__balance:
            self.__balance -= amount
            receiver.__balance += amount
            self._add_transaction("transfer", amount)
            receiver._add_transaction("receive", amount)
            return True
        return False

    def _add_transaction(self, t_type, amount):
        self.transactions.append({
            "type": t_type,
            "amount": amount,
            "date": str(datetime.date.today())
        })

    def __str__(self):
        return f"{self.fullname} | Balance: {self.balance}"


# ================= Bank class =================
class Bank:
    def __init__(self):
        self.users = {}   # card_number : User

    @staticmethod
    def generate_card():
        return "".join(str(random.randint(0, 9)) for _ in range(16))

    def register(self):
        fullname = input("Ism familiya: ")
        password = input("Parol: ")
        card = self.generate_card()
        self.users[card] = User(fullname, password)
        print("Ro‘yxatdan o‘tildi! Karta raqamingiz:", card)

    def login(self):
        card = input("Karta raqami: ")
        password = input("Parol: ")
        user = self.users.get(card)
        if user and user.check_password(password):
            print(f"Xush kelibsiz, {user.fullname}!\n")
            self.user_menu(user)
        else:
            print("Karta yoki parol noto‘g‘ri!")

    def user_menu(self, user):
        while True:
            print("""
1. Balansni ko‘rish
2. Pul kiritish
3. Pul yechish
4. Pul o‘tkazish
5. Tranzaksiyalar
6. Chiqish
""")
            try:
                choice = int(input("Tanlovingiz (1-6): "))
            except ValueError:
                print("Faqat raqam kiriting!")
                continue

            if choice == 1:
                print("Balans:", user.balance)
            elif choice == 2:
                try:
                    amount = int(input("Summa: "))
                    if amount <= 0:
                        print("Musbat summa kiriting!")
                        continue
                except ValueError:
                    print("Faqat raqam kiriting!")
                    continue
                user.deposit(amount)
                print(f"{amount} so‘m kiritildi")
            elif choice == 3:
                try:
                    amount = int(input("Summa: "))
                    if amount <= 0:
                        print("Musbat summa kiriting!")
                        continue
                except ValueError:
                    print("Faqat raqam kiriting!")
                    continue
                if user.withdraw(amount):
                    print(f"{amount} so‘m yechildi")
                else:
                    print("Balansda yetarli mablag‘ yo‘q")
            elif choice == 4:
                to_card = input("Qabul qiluvchi karta: ")
                receiver = self.users.get(to_card)
                if not receiver:
                    print("Foydalanuvchi topilmadi")
                    continue
                try:
                    amount = int(input("Summa: "))
                    if amount <= 0:
                        print("Musbat summa kiriting!")
                        continue
                except ValueError:
                    print("Faqat raqam kiriting!")
                    continue
                if user.transfer(receiver, amount):
                    print(f"{amount} so‘m {receiver.fullname} ga o‘tkazildi")
                else:
                    print("Balansda yetarli mablag‘ yo‘q")
            elif choice == 5:
                if not user.transactions:
                    print("Hozircha tranzaksiya yo‘q")
                else:
                    for t in user.transactions:
                        print(t)
            elif choice == 6:
                print("Chiqildi")
                break
            else:
                print("1-6 oralig‘ida raqam kiriting")


def main():
    bank = Bank()
    while True:
        print("""
1. Ro‘yxatdan o‘tish
2. Tizimga kirish
3. Chiqish
""")
        try:
            choice = int(input("Tanlovingiz (1-3): "))
        except ValueError:
            print("Faqat raqam kiriting!")
            continue

        if choice == 1:
            bank.register()
        elif choice == 2:
            bank.login()
        elif choice == 3:
            print("Dastur tugadi")
            break
        else:
            print("1-3 oralig‘ida raqam kiriting")


main()


"Bank"