from tkinter import simpledialog
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from tkinter import *


# Constants
FIELD = {"DATETIME": 1, "TEXT": 2, "AMOUNT": 3}
COND = {"L": 1, "LE": 2, "E": 3, "GE": 4, "G": 5, "NE": 6, "C": 7}


# Global variables
categories = []
accounts = []
transactions = []
rules = []
window = Tk()
tabControl = ttk.Notebook(window)
tab1 = ttk.Frame(tabControl)
tab2 = ttk.Frame(tabControl)
tab3 = ttk.Frame(tabControl)
tab4 = ttk.Frame(tabControl)
selectedItem = None


# Classes
class Transaction:
    def __init__(self, dateTime, text, amount, balance, account, category):
        self.dateTime = dateTime
        self.text = text
        self.amount = amount
        self.balance = balance              # Account balance after transaction
        self.account = account
        self.category = category


class Rule:
    def __init__(self, category):
        self.conditions = []
        self.category = category


class Condition:
    def __init__(self, field, conditionType, value):
        self.field = field
        self.conditionType = conditionType
        self.value = value


class Category:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent
        self.id = 0


class Account:
    def __init__(self, name):
        self.name = name


# Common functions
def tabChanged(event):
    if tabControl.tab(tabControl.select(), "text") == "Transactions":
        drawTransactions()
    if tabControl.tab(tabControl.select(), "text") == "Rules":
        drawRules()
    if tabControl.tab(tabControl.select(), "text") == "Categories":
        drawCategories()
    if tabControl.tab(tabControl.select(), "text") == "Accounts":
        drawAccounts(tab4)


def appendCategory(name, parent=None):
    categories.append(Category(name, parent))


def deleteCategory(category, catCopy):
    if category.parent:
        deleteCategory(category.parent, catCopy)
    categories.remove(category)


def appendRule(field=FIELD["TEXT"], cond=COND["C"], text="Type text here"):
    category = None
    if len(categories) > 0:
        category = categories[0]
    r = Rule(category)
    c = Condition(field, cond, text)
    r.conditions.append(c)
    global selectedItem
    selectedItem = r
    rules.append(r)


def appendCondition(r, field=FIELD["TEXT"], cond=COND["C"], text="Type text here"):
    c = Condition(field, cond, text)
    r.conditions.append(c)


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


# Transactions tab
def drawTransactions():
    deleteAllChildren(tab1)
    btn = Button(tab1, text="Load file", command=loadFileButton)
    btn.grid(column=0, row=0)
    lbl = Label(tab1, text="Date")
    lbl.grid(sticky=W, row=1, column=0)
    lbl = Label(tab1, text="Text")
    lbl.grid(sticky=W, row=1, column=1)
    lbl = Label(tab1, text="Amount")
    lbl.grid(sticky=W, row=1, column=2)
    lbl = Label(tab1, text="Balance")
    lbl.grid(sticky=W, row=1, column=3)
    lbl = Label(tab1, text="Account")
    lbl.grid(sticky=W, row=1, column=4)
    lbl = Label(tab1, text="Category")
    lbl.grid(sticky=W, row=1, column=5)
    row = 2
    for t in transactions:
        lbl = Label(tab1, text=t.dateTime)
        lbl.grid(sticky=W, row=row, column=0)
        lbl = Label(tab1, text=t.text)
        lbl.grid(sticky=W, row=row, column=1)
        lbl = Label(tab1, text=t.amount)
        lbl.grid(sticky=W, row=row, column=2)
        lbl = Label(tab1, text=t.balance)
        lbl.grid(sticky=W, row=row, column=3)
        lbl = Label(tab1, text=t.account.name if t.account else "None")
        lbl.grid(sticky=W, row=row, column=4)
        lbl = Label(tab1, text=t.category.name if t.category else "None")
        lbl.grid(sticky=W, row=row, column=5)
        row += 1


def loadFileButton():
    filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                          filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
    if filename:
        popup = Toplevel()
        print("Grab set")
        popup.grab_set()
        popup.title("Accounts")
        popup.geometry("500x400")
        popupFrame = ttk.Frame(popup)
        popupFrame.pack()
        drawAccountsPopup(popup, popupFrame, loadTransactions, filename)
        drawTransactions()


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
            transactions.append(Transaction(row[dateID], row[textID], row[amountID], row[balanceID], None, None))


# Rules tab
def drawRules():
    deleteAllChildren(tab2)
    row = 0
    for r in rules:
        if r == selectedItem:
            categoriesTextList = []
            selectedIndex = 0
            for c in categories:
                categoriesTextList.append(c.name)
                if c == r.category:
                    selectedIndex = len(categoriesTextList)-1
            combo = ttk.Combobox(tab2, values=categoriesTextList, state="readonly")
            combo.grid(row=row, column=0)
            combo.current(selectedIndex)
            combo.bind("<<ComboboxSelected>>", ruleCategorySelected)
            combo.bind("<Button-3>", rightClickRule)
            popup = Menu(combo, tearoff=0)
            popup.add_command(label="Remove rule", command=lambda rArg=r: removeRule(rArg))
            combo.popup = popup
            combo.rule = r
            row += 1
            for c in r.conditions:
                combo = ttk.Combobox(tab2, values=["Date/time", "Text", "Amount"], state="readonly")
                combo.grid(row=row, column=0)
                combo.current(c.field-1)
                combo.bind("<<ComboboxSelected>>", conditionFieldSelected)
                combo.bind("<Button-3>", rightClickRule)
                popup = Menu(combo, tearoff=0)
                popup.add_command(label="Remove condition", command=lambda rArg=r, cArg=c: removeCondition(rArg, cArg))
                combo.popup = popup
                combo.condition = c
                combo = ttk.Combobox(tab2, values=["<", "<=", "==", ">=", ">", "!=", "Contains"], state="readonly")
                combo.grid(row=row, column=1)
                combo.current(c.conditionType-1)
                combo.bind("<<ComboboxSelected>>", conditionTypeSelected)
                combo.bind("<Button-3>", rightClickRule)
                popup = Menu(combo, tearoff=0)
                popup.add_command(label="Remove condition", command=lambda rArg=r, cArg=c: removeCondition(rArg, cArg))
                combo.popup = popup
                combo.condition = c
                sv = StringVar()
                sv.condition = c
                sv.trace("w", lambda name, index, mode, svArg=sv: conditionValueChanged(svArg))
                e = Entry(tab2, textvariable=sv)
                e.insert(0, c.value)
                e.grid(sticky=W, row=row, column=2)
                e.bind("<Button-3>", rightClickRule)
                popup = Menu(e, tearoff=0)
                popup.add_command(label="Remove condition", command=lambda rArg=r, cArg=c: removeCondition(rArg, cArg))
                e.popup = popup
                row += 1
            btn = Button(tab2, text="+", command=lambda argR=r: addConditionButton(argR))
            btn.grid(row=row, column=1)
            row += 1
        else:
            lbl = Label(tab2, text=r.category.name)
            lbl.grid(sticky=W, row=row, column=0)
            lbl.rule = r
            lbl.bind("<Button-1>", selectRule)
            lbl.bind("<Button-3>", rightClickRule)
            popup = Menu(lbl, tearoff=0)
            popup.add_command(label="Remove rule", command=lambda rArg=r: removeRule(rArg))
            lbl.popup = popup
            row += 1
            for c in r.conditions:
                lbl = Label(tab2, text=fieldString(c.field), padx=10)
                lbl.grid(sticky=W, row=row, column=0)
                lbl.rule = r
                lbl.bind("<Button-1>", selectRule)
                lbl.bind("<Button-3>", rightClickRule)
                popup = Menu(lbl, tearoff=0)
                popup.add_command(label="Remove condition", command=lambda rArg=r, cArg=c: removeCondition(rArg, cArg))
                lbl.popup = popup
                lbl = Label(tab2, text=condString(c.conditionType))
                lbl.grid(sticky=W, row=row, column=1)
                lbl.rule = r
                lbl.bind("<Button-1>", selectRule)
                lbl.bind("<Button-3>", rightClickRule)
                popup = Menu(lbl, tearoff=0)
                popup.add_command(label="Remove condition", command=lambda rArg=r, cArg=c: removeCondition(rArg, cArg))
                lbl.popup = popup
                lbl = Label(tab2, text=c.value)
                lbl.grid(sticky=W, row=row, column=2)
                lbl.rule = r
                lbl.bind("<Button-1>", selectRule)
                lbl.bind("<Button-3>", rightClickRule)
                popup = Menu(lbl, tearoff=0)
                popup.add_command(label="Remove condition", command=lambda rArg=r, cArg=c: removeCondition(rArg, cArg))
                lbl.popup = popup
                row += 1
    btn = Button(tab2, text="+", command=addRuleButton)
    btn.grid(row=row, column=0)


def addRuleButton():
    appendRule()
    drawRules()


def addConditionButton(r):
    appendCondition(r)
    drawRules()


def rightClickRule(event):
    popup = event.widget.popup
    try:
        popup.tk_popup(event.x_root+60, event.y_root+13, 0)
    finally:
        popup.grab_release()


def removeRule(r):
    rules.remove(r)
    drawRules()


def removeCondition(r, c):
    r.conditions.remove(c)
    if len(r.conditions) == 0:
        rules.remove(r)
    drawRules()


def selectRule(event):
    global selectedItem
    if selectedItem != event.widget.rule:
        selectedItem = event.widget.rule
        drawRules()


def ruleCategorySelected(event):
    event.widget.rule.category = categories[event.widget.current()]


def conditionFieldSelected(event):
    event.widget.condition.field = event.widget.current()+1


def conditionTypeSelected(event):
    event.widget.condition.conditionType = event.widget.current()+1


def conditionValueChanged(sv):
    if sv.condition.field == FIELD["AMOUNT"]:
        try:
            sv.condition.value = int(sv.get())
        except ValueError:
            pass
    else:
        sv.condition.value = sv.get()


# Categories tab
def drawCategories():
    deleteAllChildren(tab3)
    tree = ttk.Treeview(tab3)
    tree.bind("<Button-3>", rightClickCategory)
    tree.bind("<Double-1>", doubleClickCategory)
    popup = Menu(tree, tearoff=0)
    popup.add_command(label="Add new category", command=lambda treeArg=tree: addCategory(treeArg))
    popup.add_command(label="Remove category", command=lambda treeArg=tree: removeCategory(treeArg))
    popup.add_command(label="Rename category", command=lambda treeArg=tree: renameCategory(treeArg))

    tree.popup = popup
    tree.column("#0", width=270, minwidth=270)
    tree.heading("#0", text="Categories", anchor=W)
    tree.insert("", "end", 0, text="root")
    for i in range(len(categories)):
        categories[i].id = i+1
    catCopy = categories.copy()
    while len(catCopy) > 0:
        addTreeItem(tree, catCopy, catCopy[0])
    tree.pack(side=TOP, fill=BOTH, expand=True)


def addTreeItem(tree, catCopy, category):
    if not category.parent:
        tree.insert("0", "end", category.id, text=category.name)
        catCopy.remove(category)
        return
    else:
        for c in catCopy:
            if c == category.parent:
                addTreeItem(tree, catCopy, c)
                break
        tree.insert(category.parent.id if category.parent else "0", "end", category.id, text=category.name)
        catCopy.remove(category)
        return


def rightClickCategory(event):
    iid = event.widget.identify_row(event.y)
    if iid:
        event.widget.selection_set(iid)
        popup = event.widget.popup
        try:
            popup.tk_popup(event.x_root+60, event.y_root+13, 0)
        finally:
            popup.grab_release()


def doubleClickCategory(event):
    iid = event.widget.identify_row(event.y)
    if iid and int(iid) > 0:
        event.widget.selection_set(iid)
        renameCategory(event.widget)


def addCategory(tree):
    name = simpledialog.askstring("Category", "Name category", parent=window)
    if name is None:
        return
    if int(tree.selection()[0]) == 0:
        appendCategory(name, None)
        drawCategories()
        return
    for c in categories:
        if c.id == int(tree.selection()[0]):
            appendCategory(name, c)
            drawCategories()
            return


def renameCategory(tree):
    if int(tree.selection()[0]) == 0:
        return
    name = simpledialog.askstring("Category", "Rename category", parent=window)
    if name is not None:
        for c in categories:
            if c.id == int(tree.selection()[0]):
                c.name = name
                drawCategories()
                return


def removeCategory(tree):
    for c in categories:
        if c.id == int(tree.selection()[0]):
            answer = messagebox.askyesno("Warning!", "Do you really want to remove category '" + c.name + "'?")
            if not answer:
                return
            catCopy = categories.copy()
            deleteCategory(c, catCopy)
            drawCategories()
            return


# Accounts tab
def drawAccounts(frame):
    deleteAllChildren(frame)
    row = 0
    for a in accounts:
        if a == selectedItem:
            sv = StringVar()
            sv.account = a
            sv.trace("w", lambda name, index, mode, svArg=sv: accountNameChanged(svArg))
            e = Entry(frame, textvariable=sv)
            e.insert(0, a.name)
            e.grid(sticky=W, row=row, column=0)
            e.bind("<Button-3>", rightClickAccount)
            popup = Menu(e, tearoff=0)
            popup.add_command(label="Remove account", command=lambda d=drawAccounts, f=frame, aArg=a:
                              removeAccount(d, f, aArg))
            e.popup = popup
            row += 1
        else:
            lbl = Label(frame, text=a.name)
            lbl.grid(sticky=W, row=row, column=0)
            lbl.account = a
            lbl.bind("<Button-1>", lambda event, d=drawAccounts, f=frame: selectAccount(d, f, event))
            lbl.bind("<Button-3>", rightClickAccount)
            popup = Menu(lbl, tearoff=0)
            popup.add_command(label="Remove account", command=lambda d=drawAccounts, f=frame, aArg=a:
                              removeAccount(d, f, aArg))
            lbl.popup = popup
            row += 1
    btn = Button(frame, text="+", command=lambda d=drawAccounts, f=frame: addAccountButton(d, f))
    btn.grid(row=row, column=0)


def addAccountButton(drawFunc, frame):
    accounts.append(Account("new"))
    drawFunc(frame)


def rightClickAccount(event):
    popup = event.widget.popup
    try:
        popup.tk_popup(event.x_root+60, event.y_root+13, 0)
    finally:
        popup.grab_release()


def removeAccount(drawFunc, frame, a):
    accounts.remove(a)
    drawFunc(frame)


def selectAccount(drawFunc, frame, event):
    global selectedItem
    if selectedItem != event.widget.account:
        selectedItem = event.widget.account
        drawFunc(frame)


def accountNameChanged(sv):
    sv.account.name = sv.get()


# Popups
def drawAccountsPopup(frame, popup, func, filename):
    deleteAllChildren(frame)
    row = 0
    for a in accounts:
        if a == selectedItem:
            sv = StringVar()
            sv.account = a
            sv.trace("w", lambda name, index, mode, svArg=sv: accountNameChanged(svArg))
            e = Entry(frame, textvariable=sv)
            e.insert(0, a.name)
            e.grid(sticky=W, row=row, column=0)
            e.bind("<Button-3>", rightClickAccount)
            popup = Menu(e, tearoff=0)
            popup.add_command(label="Remove account", command=lambda d=drawAccountsPopup, f=frame, aArg=a:
                              removeAccount(d, f, aArg))
            e.popup = popup
            row += 1
        else:
            lbl = Label(frame, text=a.name)
            lbl.grid(sticky=W, row=row, column=0)
            lbl.account = a
            lbl.bind("<Button-1>", lambda event, d=drawAccountsPopup, f=frame: selectAccount(d, f, event))
            lbl.bind("<Button-3>", rightClickAccount)
            popup = Menu(lbl, tearoff=0)
            popup.add_command(label="Remove account", command=lambda d=drawAccountsPopup, f=frame, aArg=a:
                              removeAccount(d, f, aArg))
            lbl.popup = popup
            row += 1
    btn = Button(frame, text="+", command=lambda d=drawAccountsPopup, f=frame: addAccountButton(d, f))
    btn.grid(row=row, column=0)
    btn = Button(frame, text="Select", command=lambda argPopup=popup, argFunc=func, argFilename=filename:
                 selectAccountInPopup(argPopup, argFunc, argFilename))
    btn.grid(row=row+1, column=0)
    btn = Button(frame, text="Cancel", command=lambda: popup.destroy())
    btn.grid(row=row+1, column=1)


def selectAccountInPopup(popup, func, filename):
    func(filename)
    popup.destroy()


# Main
def main():
    window.title("Money tracker")
    window.geometry("920x800")
    tabControl.add(tab1, text="Transactions")
    tabControl.add(tab2, text="Rules")
    tabControl.add(tab3, text="Categories")
    tabControl.add(tab4, text="Accounts")
    tabControl.pack(expand=1, fill="both")
    tabControl.bind("<<NotebookTabChanged>>", lambda event: tabChanged(event))

    categories.append(Category("Bil", None))
    categories.append(Category("Mat", None))
    categories.append(Category("Service", categories[0]))
    categories.append(Category("Cat4", None))
    categories.append(Category("Cat5", categories[3]))
    categories.append(Category("Cat6", categories[3]))
    categories.append(Category("Cat7", categories[3]))
    categories.append(Category("Cat8", categories[4]))
    categories.append(Category("Cat9", categories[4]))
    categories.append(Category("Cat10", categories[7]))
    categories.append(Category("Cat11", categories[7]))
    categories.append(Category("Cat12", categories[8]))
    categories.append(Category("Cat13", categories[5]))
    categories.append(Category("Cat14", categories[6]))
    categories.append(Category("Cat15", categories[8]))

    r = Rule(categories[0])
    c = Condition(FIELD["TEXT"], COND["C"], "CIRCLE")
    r.conditions.append(c)
    c = Condition(FIELD["AMOUNT"], COND["G"], 100)
    r.conditions.append(c)
    rules.append(r)

    r = Rule(categories[1])
    c = Condition(FIELD["TEXT"], COND["C"], "ICA")
    r.conditions.append(c)
    rules.append(r)

    r = Rule(categories[2])
    c = Condition(FIELD["TEXT"], COND["C"], "KISTA")
    r.conditions.append(c)
    rules.append(r)

    window.mainloop()


if __name__ == "__main__":
    main()
