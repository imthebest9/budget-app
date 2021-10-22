class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []
        self.__balance = 0.0
    
    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})
        self.__balance += amount
    
    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -1 * amount, "description": description})
            self.__balance -= amount
            return True
        else:
            return False
    
    def get_balance(self):
        return self.__balance

    def transfer(self, amount, category):
        if(self.withdraw(amount, description="Transfer to {}".format(category.name))):
            return True
        else:
            return False

    def check_funds(self, amount):
        if amount > self.__balance:
            return False
        else:
            return True

    def __repr__(self):
        title = self.name.center(30, "*") + "\n"
        ledger = ""
        for item in self.ledger:
            desc = "{:<23}".format(item["description"])
            price = "{:>7.2f}".format(item["amount"])
            # truncate
            ledger += "{}{}\n".format(desc[:23], price[:7])
        total = "Total: {:.2f}".format(self.__balance)
        return title + ledger + total




def create_spend_chart(categories):
    spent = []
    for category in categories:
        s = 0
        for item in category.ledger:
            if(item["amount"] < 0):
                s += abs(item["amount"])
        spent.append(round(s, 2))

    total = round(sum(spent),2)
    spent_percentage = list(map(lambda amount: int((((amount / total) * 10) // 1) * 10), spent))

    title = "Percentage spent by category\n"

    # chart substring
    chart = ""
    for i in reversed(range(0, 101, 10)):
        chart += str(i).rjust(3) + "|"
        for percent in spent_percentage:
            if percent >= i:
                chart += " o "
            else:
                chart += "   "
        chart += " \n"
    
    bottom = "    " + "-" * ((3*len(categories)) +1) + "\n"
    desc = list(map(lambda category: category.name, categories))
    max_length = max(map(lambda description: len(description), desc))
    desc = list(map(lambda description: description.ljust(max_length), desc))

    for x in zip(*desc):
        bottom += "    " + "".join(map(lambda s: s.center(3), x)) + "\n"

    return (title + chart + bottom).rstrip("\n")