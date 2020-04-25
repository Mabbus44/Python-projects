class Category:
    def __init__(self, name):
        self.name = name
        self.id = 0
        self.subCat = []


class Transaction:
    def __init__(self, dateTime, text, amount, balance, accountID, categoryID):
        self.dateTime = dateTime
        self.text = text
        self.amount = amount
        self.balance = balance              # Account balance after transaction
        self.accountID = accountID
        self.categoryID = categoryID


def loadTransactions(fileName):
    f = open(fileName, "r")
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
    transactions = []
    for row in cols:
        if maxID <= len(row)-1:
            transactions.append(Transaction(row[dateID], row[textID], row[amountID], row[balanceID], 0, 0))
    return transactions


def main():
    base = Category("Base")
    transactions = loadTransactions("money.csv")
    for t in transactions:
        print(t.dateTime + " " + t.text + " " + str(t.amount) + " " + str(t.balance) + " " + str(t.accountID) + " " +
              str(t.categoryID))


if __name__ == "__main__":
    main()