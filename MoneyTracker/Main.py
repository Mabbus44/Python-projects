from tkinter import filedialog
from tkinter import ttk
from tkinter import *


# Constants
FIELD = {"DATETIME": 1, "TEXT": 2, "AMOUNT": 3}
COND = {"L": 1, "LE": 2, "E": 3, "GE": 4, "G": 5, "NE": 6, "C": 7}


# Global variables
categories = []
transactions = []
rules = []
window = Tk()
tab_control = ttk.Notebook(window)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab3 = ttk.Frame(tab_control)
selectedRule = None


class Rule:
    def __init__(self, catID):
        self.conditions = []
        self.categoryID = catID


class Condition:
    def __init__(self, field, conditionType, value):
        self.field = field
        self.conditionType = conditionType
        self.value = value


class Category:
    def __init__(self, name, catID, parentID):
        self.name = name
        self.id = catID
        self.parentID = parentID


class Transaction:
    def __init__(self, dateTime, text, amount, balance, accountID, categoryID):
        self.dateTime = dateTime
        self.text = text
        self.amount = amount
        self.balance = balance              # Account balance after transaction
        self.accountID = accountID
        self.categoryID = categoryID


def selectRule(event):
    print("selectRule")
    global selectedRule
    if selectedRule != event.widget.rule:
        selectedRule = event.widget.rule
        drawRules()


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
    transactions.clear()
    for row in cols:
        if maxID <= len(row)-1:
            transactions.append(Transaction(row[dateID], row[textID], row[amountID], row[balanceID], 0, 0))


def loadFileButton():
    filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    loadTransactions(filename)
    for t in transactions:
        print(t.dateTime + " " + t.text + " " + str(t.amount) + " " + str(t.balance) + " " + str(t.accountID) + " " +
              str(t.categoryID))
    drawTransactions()


def drawRules():
    print("drawRules")
    deleteAllChildren(tab1)
    row = 0
    for r in rules:
        if r == selectedRule:
            categoriesTextList = []
            for c in categories:
                categoriesTextList.append(c.name)
                if c.id == r.categoryID:
                    selectedIndex = len(categoriesTextList)-1
            combo = ttk.Combobox(tab1, values=categoriesTextList, state="readonly")
            combo.grid(row=row, column=0)
            combo.current(selectedIndex)
            row += 1
            for c in r.conditions:
                combo = ttk.Combobox(tab1, values=["Date/time", "Text", "Amount"], state="readonly")
                combo.grid(row=row, column=0)
                combo.current(c.field-1)
                combo = ttk.Combobox(tab1, values=["<", "<=", "==", ">=", ">", "!=", "Contains"], state="readonly")
                combo.grid(row=row, column=1)
                combo.current(c.conditionType-1)
                e = Entry(tab1)
                e.insert(0, c.value)
                e.grid(sticky=W, row=row, column=2)
                row += 1
        else:
            lbl = Label(tab1, text=catFromID(r.categoryID))
            lbl.grid(sticky=W, row=row, column=0)
            lbl.rule = r
            lbl.bind("<Button-1>", selectRule)
            row += 1
            for c in r.conditions:
                lbl = Label(tab1, text=fieldString(c.field), padx=10)
                lbl.grid(sticky=W, row=row, column=0)
                lbl.rule = r
                lbl.bind("<Button-1>", selectRule)
                lbl = Label(tab1, text=condString(c.conditionType))
                lbl.grid(sticky=W, row=row, column=1)
                lbl.rule = r
                lbl.bind("<Button-1>", selectRule)
                lbl = Label(tab1, text=c.value)
                lbl.grid(sticky=W, row=row, column=2)
                lbl.rule = r
                lbl.bind("<Button-1>", selectRule)
                row += 1


def drawTransactions():
    deleteAllChildren(tab2)
    btn = Button(tab2, text="Load file", command=loadFileButton)
    btn.grid(column=0, row=0)
    lbl = Label(tab2, text="Date")
    lbl.grid(sticky=W, row=1, column=0)
    lbl = Label(tab2, text="Text")
    lbl.grid(sticky=W, row=1, column=1)
    lbl = Label(tab2, text="Amount")
    lbl.grid(sticky=W, row=1, column=2)
    lbl = Label(tab2, text="Balance")
    lbl.grid(sticky=W, row=1, column=3)
    row = 2
    for t in transactions:
        lbl = Label(tab2, text=t.dateTime)
        lbl.grid(sticky=W, row=row, column=0)
        lbl = Label(tab2, text=t.text)
        lbl.grid(sticky=W, row=row, column=1)
        lbl = Label(tab2, text=t.amount)
        lbl.grid(sticky=W, row=row, column=2)
        lbl = Label(tab2, text=t.balance)
        lbl.grid(sticky=W, row=row, column=3)
        row += 1


def drawCategories():
    deleteAllChildren(tab3)
    lbl = Label(tab3, text="Category")
    lbl.grid(sticky=W, row=0, column=0)
    lbl = Label(tab3, text="Parent")
    lbl.grid(sticky=W, row=0, column=1)
    row = 1
    for c in categories:
        lbl = Label(tab3, text=c.name)
        lbl.grid(sticky=W, row=row, column=0)
        lbl = Label(tab3, text=catFromID(c.parentID))
        lbl.grid(sticky=W, row=row, column=1)
        row += 1


def catFromID(catID):
    for c in categories:
        if c.id == catID:
            return c.name
    return ""


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
        return "="
    if condID == COND["GE"]:
        return ">="
    if condID == COND["G"]:
        return ">"
    if condID == COND["C"]:
        return "Contains"
    if condID == COND["NE"]:
        return "!="
    return ""


def deleteAllChildren(item):
    _list = item.winfo_children()
    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())
    for i in _list:
        i.destroy()


def main():
    window.title("Money tracker")
    window.geometry("320x200")
    tab_control.add(tab1, text="Rules")
    tab_control.add(tab2, text="Transactions")
    tab_control.add(tab3, text="Categories")
    tab_control.pack(expand=1, fill="both")

    categories.append(Category("Bil", 1, 0))
    categories.append(Category("Mat", 2, 0))
    categories.append(Category("Service", 3, 1))

    r = Rule(1)
    c = Condition(FIELD["TEXT"], COND["C"], "CIRCLE")
    r.conditions.append(c)
    c = Condition(FIELD["AMOUNT"], COND["G"], 100)
    r.conditions.append(c)
    global selectedRule
    selectedRule = r
    rules.append(r)

    r = Rule(2)
    c = Condition(FIELD["TEXT"], COND["C"], "ICA")
    r.conditions.append(c)
    rules.append(r)

    r = Rule(3)
    c = Condition(FIELD["TEXT"], COND["C"], "KISTA")
    r.conditions.append(c)
    rules.append(r)

    drawRules()
    drawTransactions()
    drawCategories()
    window.mainloop()


if __name__ == "__main__":
    main()
