from datetime import datetime
import codecs


# Constants
FIELD = {"DATETIME": 1, "TEXT": 2, "AMOUNT": 3}
COND = {"L": 1, "LE": 2, "E": 3, "GE": 4, "G": 5, "NE": 6, "C": 7}
THISVERSION = 1.0

# Settings
decimalSeparator = ","


# Main backend class
class MoneyTracker:
    def __init__(self):
        self.categories = []
        self.accounts = []
        self.transactions = []
        self.rules = []

    def appendCategory(self, name, parent=None):
        self.categories.append(Category(name, parent))

    def deleteCategory(self, category, catCopy):
        for c in catCopy:
            if c.parent == category:
                self.deleteCategory(c, catCopy)
        for t in self.transactions:
            if t.category == category:
                t.category = None
        self.categories.remove(category)

    def appendRule(self, field=FIELD["TEXT"], cond=COND["C"], text="Type text here"):
        category = None
        if len(self.categories) > 0:
            category = self.categories[0]
        r = Rule(category)
        c = Condition(field, cond, text)
        r.conditions.append(c)
        self.rules.append(r)

    def newProject(self):
        self.transactions.clear()
        for r in self.rules:
            r.conditions.clear()
        self.rules.clear()
        self.categories.clear()
        self.accounts.clear()

    def openProject(self, fileName):
        self.transactions.clear()
        for r in self.rules:
            r.conditions.clear()
        self.rules.clear()
        self.categories.clear()
        self.accounts.clear()
        f = codecs.open(fileName, 'r', encoding='utf8')
        fileVersion = str2float(f.readline().replace(".", decimalSeparator).replace(",", decimalSeparator))
        if fileVersion > THISVERSION:
            return -1
        accountCount = str2int(f.readline())
        for i in range(accountCount):
            self.accounts.append(Account(f.readline()[:-1]))
        categoriesCount = str2int(f.readline())
        for i in range(categoriesCount):
            categoryName = f.readline()[:-1]
            parentID = str2int(f.readline())
            self.categories.append(Category(categoryName, parentID))
        for c in self.categories:
            if c.parent > 0:
                c.parent = self.categories[c.parent-1]
            else:
                c.parent = None
        transactionsCount = str2int(f.readline())
        for i in range(transactionsCount):
            transDate = datetime.strptime(f.readline()[:-1], "%Y-%m-%d").date()
            transText = f.readline()[:-1]
            transAmount = str2float(f.readline().replace(".", decimalSeparator).replace(",", decimalSeparator))
            transBalance = str2float(f.readline().replace(".", decimalSeparator).replace(",", decimalSeparator))
            aID = str2int(f.readline())
            transAccount = self.accounts[aID-1] if aID > 0 else None
            cID = str2int(f.readline())
            transCategory = self.categories[cID-1] if cID > 0 else None
            self.transactions.append(Transaction(transDate, transText, transAmount, transBalance, transAccount,
                                     transCategory))
        rulesCount = str2int(f.readline())
        for i in range(rulesCount):
            self.rules.append(Rule(self.categories[str2int(f.readline())-1]))
            conditionsCount = str2int(f.readline())
            for i2 in range(conditionsCount):
                field = str2int(f.readline())
                conditionType = str2int(f.readline())
                value = 0
                if field == FIELD["DATETIME"]:
                    value = datetime.strptime(f.readline()[:-1], "%Y-%m-%d").date()
                if field == FIELD["TEXT"]:
                    value = f.readline()[:-1]
                if field == FIELD["AMOUNT"]:
                    value = str2int(f.readline())
                self.rules[i].conditions.append(Condition(field, conditionType, value))
        f.close()
        return 0

    def saveProject(self, fileName):
        f = codecs.open(fileName, 'w', encoding='utf8')
        f.write("File structure version: " + str(1.0) + "\n")
        for i in range(len(self.accounts)):
            self.accounts[i].id = i+1
        for i in range(len(self.categories)):
            self.categories[i].id = i+1
        f.write("Accounts: " + str(len(self.accounts)) + "\n")
        for a in self.accounts:
            f.write(a.name + "\n")
        f.write("Categories: " + str(len(self.categories)) + "\n")
        for c in self.categories:
            f.write(c.name + "\n")
            if c.parent:
                f.write(str(c.parent.id) + "\n")
            else:
                f.write("0" + "\n")
        f.write("Transactions: " + str(len(self.transactions)) + "\n")
        for t in self.transactions:
            f.write(str(t.dateTime) + "\n")
            f.write(t.text + "\n")
            f.write(str(t.amount) + "\n")
            f.write(str(t.balance) + "\n")
            if t.account:
                f.write(str(t.account.id) + "\n")
            else:
                f.write("0" + "\n")
            if t.category:
                f.write(str(t.category.id) + "\n")
            else:
                f.write("0" + "\n")
        f.write("Rules: " + str(len(self.rules)) + "\n")
        for r in self.rules:
            f.write(str(r.category.id) + "\n")
            f.write("Conditions: " + str(len(r.conditions)) + "\n")
            for c in r.conditions:
                f.write(str(c.field) + "\n")
                f.write(str(c.conditionType) + "\n")
                f.write(str(c.value) + "\n")
        f.close()
        return 0

    def loadTransactions(self, fileName, account):
        f = codecs.open(fileName, 'r', encoding='utf8')
        rows = f.read().split("\n")
        f.close()
        cols = []
        rows = rows[1:]
        for row in rows:
            cols.append(row.split(";;"))
        dateID = 1
        textID = 2
        amountID = 3
        balanceID = 4
        maxID = max(dateID, textID, amountID, balanceID)
        originalLen = len(self.transactions)
        for row in cols:
            if maxID <= len(row)-1:
                newTransaction = Transaction(datetime.strptime(row[dateID], "%Y-%m-%d").date(), row[textID],
                                             str2float(row[amountID]), str2float(row[balanceID]), account, None)
                duplication = False
                for i in range(originalLen):
                    if self.transactions[i].equals(newTransaction):
                        duplication = True
                if not duplication:
                    self.transactions.append(newTransaction)


# Other classes
class Transaction:
    def __init__(self, dateTime, text, amount, balance, account, category):
        self.dateTime = dateTime
        self.text = text
        self.amount = amount
        self.balance = balance
        self.account = account
        self.category = category

    def equals(self, other):
        if (self.dateTime == other.dateTime and self.text == other.text and self.amount == other.amount and
                self.balance == other.balance):
            return True
        return False


class Rule:
    def __init__(self, category):
        self.conditions = []
        self.category = category

    def appendCondition(self, field=FIELD["TEXT"], cond=COND["C"], text="Type text here"):
        self.conditions.append(Condition(field, cond, text))


class Condition:
    def __init__(self, field, conditionType, value):
        self.field = field
        self.conditionType = conditionType
        self.value = value


class Category:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.id = 0
        self.posSum = 0
        self.negSum = 0


class Account:
    def __init__(self, name):
        self.name = name
        self.id = 0
        self.balance = 0


# Functions
def str2float(string):
    newString = ""
    signFound = False
    firstNumberFound = False
    commaFound = False
    for c in string:
        if not signFound and not firstNumberFound:
            if c in "+-":
                newString = newString + c
                signFound = True
        if c in "0123456789":
            newString = newString + c
            firstNumberFound = True
        if not commaFound and firstNumberFound:
            if c in decimalSeparator:
                newString = newString + "."
                commaFound = True
    if firstNumberFound:
        return float(newString)
    else:
        return 0.0


def str2int(string):
    newString = ""
    signFound = False
    firstNumberFound = False
    for c in string:
        if not signFound and not firstNumberFound:
            if c in "+-":
                newString = newString + c
                signFound = True
        if c in "0123456789":
            newString = newString + c
            firstNumberFound = True
    if firstNumberFound:
        return int(newString)
    else:
        return 0


def fieldString(fID):
    if fID == FIELD["DATETIME"]:
        return "Date/time"
    if fID == FIELD["AMOUNT"]:
        return "Amount"
    if fID == FIELD["TEXT"]:
        return "Text"
    return ""


def condString(condID):
    if condID == COND["L"]:
        return "<"
    if condID == COND["LE"]:
        return "<="
    if condID == COND["E"]:
        return "=="
    if condID == COND["GE"]:
        return ">="
    if condID == COND["G"]:
        return ">"
    if condID == COND["C"]:
        return "Contains"
    if condID == COND["NE"]:
        return "!="
    return ""
