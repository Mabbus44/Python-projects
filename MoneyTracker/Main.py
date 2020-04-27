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


def ruleCategorySelected(event):
    event.widget.rule.categoryID = categories[event.widget.current()].id


def conditionFieldSelected(event):
    event.widget.condition.field = event.widget.current()+1


def conditionTypeSelected(event):
    event.widget.condition.conditionType = event.widget.current()+1


def conditionValueChanged(sv):
    if sv.condition.field == FIELD["AMOUNT"]:
        try:
            sv.condition.value = int(sv.get())
        except ValueError:
            None
    else:
        sv.condition.value = sv.get()
    print("Value changed")


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
            selectedIndex = 0
            for c in categories:
                categoriesTextList.append(c.name)
                if c.id == r.categoryID:
                    selectedIndex = len(categoriesTextList)-1
            combo = ttk.Combobox(tab1, values=categoriesTextList, state="readonly")
            combo.grid(row=row, column=0)
            combo.current(selectedIndex)
            combo.bind("<<ComboboxSelected>>", ruleCategorySelected)
            combo.rule = r
            row += 1
            for c in r.conditions:
                combo = ttk.Combobox(tab1, values=["Date/time", "Text", "Amount"], state="readonly")
                combo.grid(row=row, column=0)
                combo.current(c.field-1)
                combo.bind("<<ComboboxSelected>>", conditionFieldSelected)
                combo.condition = c
                combo = ttk.Combobox(tab1, values=["<", "<=", "==", ">=", ">", "!=", "Contains"], state="readonly")
                combo.grid(row=row, column=1)
                combo.current(c.conditionType-1)
                combo.bind("<<ComboboxSelected>>", conditionTypeSelected)
                combo.condition = c
                sv = StringVar()
                sv.condition = c
                sv.trace("w", lambda name, index, mode, svArg=sv: conditionValueChanged(svArg))
                e = Entry(tab1, textvariable=sv)
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


def addTreeItem(tree, catCopy, category):
    if category.parentID == 0:
        tree.insert("", "end", category.id, text=category.name)
        catCopy.remove(category)
        return
    else:
        for c in catCopy:
            if c.id == category.parentID:
                addTreeItem(tree, catCopy, c)
                break
        tree.insert(category.parentID, "end", category.id, text=category.name)
        catCopy.remove(category)
        return


def drawCategories():
    deleteAllChildren(tab3)
    tree = ttk.Treeview(tab3)
    tree.column("#0", width=270, minwidth=270)
    tree.heading("#0", text="Categories", anchor=W)
    catCopy = categories.copy()
    while len(catCopy) > 0:
        addTreeItem(tree, catCopy, catCopy[0])
    tree.pack(side=TOP, fill=X)


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
    categories.append(Category("Cat4", 4, 15))
    categories.append(Category("Cat5", 5, 12))
    categories.append(Category("Cat6", 6, 15))
    categories.append(Category("Cat7", 7, 10))
    categories.append(Category("Cat8", 8, 15))
    categories.append(Category("Cat9", 9, 8))
    categories.append(Category("Cat10", 10, 4))
    categories.append(Category("Cat11", 11, 15))
    categories.append(Category("Cat12", 12, 10))
    categories.append(Category("Cat13", 13, 7))
    categories.append(Category("Cat14", 14, 7))
    categories.append(Category("Cat15", 15, 0))

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
