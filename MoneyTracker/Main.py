from tkinter import simpledialog
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from tkinter import *
from datetime import datetime
import codecs

# Constants
FIELD = {"DATETIME": 1, "TEXT": 2, "AMOUNT": 3}
COND = {"L": 1, "LE": 2, "E": 3, "GE": 4, "G": 5, "NE": 6, "C": 7}


# Global variables
categories = []
accounts = []
transactions = []
rules = []
window = Tk()
menuBar = Menu(window)
fileMenu = Menu(menuBar, tearoff=0)
helpMenu = Menu(menuBar, tearoff=0)

tabControl = ttk.Notebook(window)
outerFrame1 = ttk.Frame(tabControl)
canvas1 = Canvas(outerFrame1)
scrollbar1 = ttk.Scrollbar(outerFrame1, orient="vertical", command=canvas1.yview)
tab1 = ttk.Frame(canvas1)
canvas1.create_window((0, 0), window=tab1, anchor="nw")
canvas1.configure(yscrollcommand=scrollbar1.set)
tab1.bind("<Configure>", lambda e: canvas1.configure(scrollregion=canvas1.bbox("all")))

outerFrame2 = ttk.Frame(tabControl)
canvas2 = Canvas(outerFrame2)
scrollbar2 = ttk.Scrollbar(outerFrame2, orient="vertical", command=canvas2.yview)
tab2 = ttk.Frame(canvas2)
canvas2.create_window((0, 0), window=tab2, anchor="nw")
canvas2.configure(yscrollcommand=scrollbar2.set)
tab2.bind("<Configure>", lambda e: canvas2.configure(scrollregion=canvas2.bbox("all")))

outerFrame3 = ttk.Frame(tabControl)
canvas3 = Canvas(outerFrame3)
scrollbar3 = ttk.Scrollbar(outerFrame3, orient="vertical", command=canvas3.yview)
tab3 = ttk.Frame(canvas3)
canvas3.create_window((0, 0), window=tab3, anchor="nw")
canvas3.configure(yscrollcommand=scrollbar3.set)
tab3.bind("<Configure>", lambda e: canvas3.configure(scrollregion=canvas3.bbox("all")))

outerFrame4 = ttk.Frame(tabControl)
canvas4 = Canvas(outerFrame4)
scrollbar4 = ttk.Scrollbar(outerFrame4, orient="vertical", command=canvas4.yview)
tab4 = ttk.Frame(canvas4)
canvas4.create_window((0, 0), window=tab4, anchor="nw")
canvas4.configure(yscrollcommand=scrollbar4.set)
tab4.bind("<Configure>", lambda e: canvas4.configure(scrollregion=canvas4.bbox("all")))

selectedItem = None
decimalSeparator = ","


# Classes
class Transaction:
    def __init__(self, dateTime, text, amount, balance, account, category):
        self.dateTime = dateTime
        self.text = text
        self.amount = amount
        self.balance = balance              # Account balance after transaction
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
        self.id = 0


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


def newProject():
    transactions.clear()
    for r in rules:
        r.conditions.clear()
    rules.clear()
    categories.clear()
    accounts.clear()
    drawTransactions()
    drawRules()
    drawCategories()
    drawAccounts(tab4)


def openProject():
    fileName = filedialog.askopenfilename(initialdir="/", title="Save file",
                                          filetypes=(("Money tracker project files", "*.mtp"), ("all files", "*.*")))
    if fileName:
        transactions.clear()
        for r in rules:
            r.conditions.clear()
        rules.clear()
        categories.clear()
        accounts.clear()
        f = codecs.open(fileName, 'r', encoding='utf8')
        thisVersion = 1.0
        fileVersion = str2float(f.readline().replace(".", decimalSeparator).replace(",", decimalSeparator))
        if fileVersion > thisVersion:
            messagebox.showerror("Error", "Could not load file, program version to old")
            return
        accountCount = str2int(f.readline())
        for i in range(accountCount):
            accounts.append(Account(f.readline()[:-1]))
        categoriesCount = str2int(f.readline())
        for i in range(categoriesCount):
            categoryName = f.readline()[:-1]
            parentID = str2int(f.readline())
            categories.append(Category(categoryName, parentID))
        for c in categories:
            if c.parent > 0:
                c.parent = categories[c.parent-1]
            else:
                c.parent = None
        transactionsCount = str2int(f.readline())
        for i in range(transactionsCount):
            transDate = datetime.strptime(f.readline()[:-1], "%Y-%m-%d").date()
            transText = f.readline()[:-1]
            transAmount = str2float(f.readline().replace(".", decimalSeparator).replace(",", decimalSeparator))
            transBalance = str2float(f.readline().replace(".", decimalSeparator).replace(",", decimalSeparator))
            aID = str2int(f.readline())
            transAccount = accounts[aID-1] if aID > 0 else None
            cID = str2int(f.readline())
            transCategory = categories[cID-1] if cID > 0 else None
            transactions.append(Transaction(transDate, transText, transAmount, transBalance, transAccount,
                                            transCategory))
        rulesCount = str2int(f.readline())
        for i in range(rulesCount):
            rules.append(Rule(categories[str2int(f.readline())-1]))
            conditionsCount = str2int(f.readline())
            for i2 in range(conditionsCount):
                field = str2int(f.readline())
                conditionType = str2int(f.readline())
                if field == FIELD["DATETIME"]:
                    value = datetime.strptime(f.readline()[:-1], "%Y-%m-%d").date()
                if field == FIELD["TEXT"]:
                    value = f.readline()[:-1]
                if field == FIELD["AMOUNT"]:
                    value = str2int(f.readline())
                rules[i].conditions.append(Condition(field, conditionType, value))
        f.close()
        messagebox.showinfo("Info", "File loaded successfully")
        drawTransactions()
        drawRules()
        drawCategories()
        drawAccounts(tab4)


def saveProject():
    fileName = filedialog.asksaveasfilename(initialdir="/", title="Save file",
                                            filetypes=(("Money tracker project files", "*.mtp"), ("all files", "*.*")),
                                            defaultextension=".mtp")
    if fileName:
        f = codecs.open(fileName, 'w', encoding='utf8')
        f.write("File structure version: " + str(1.0) + "\n")
        for i in range(len(accounts)):
            accounts[i].id = i+1
        for i in range(len(categories)):
            categories[i].id = i+1
        f.write("Accounts: " + str(len(accounts)) + "\n")
        for a in accounts:
            f.write(a.name + "\n")
        f.write("Categories: " + str(len(categories)) + "\n")
        for c in categories:
            f.write(c.name + "\n")
            if c.parent:
                f.write(str(c.parent.id) + "\n")
            else:
                f.write("0" + "\n")
        f.write("Transactions: " + str(len(transactions)) + "\n")
        for t in transactions:
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
        f.write("Rules: " + str(len(rules)) + "\n")
        for r in rules:
            f.write(str(r.category.id) + "\n")
            f.write("Conditions: " + str(len(r.conditions)) + "\n")
            for c in r.conditions:
                f.write(str(c.field) + "\n")
                f.write(str(c.conditionType) + "\n")
                f.write(str(c.value) + "\n")
        f.close()
        messagebox.showinfo("Info", "File saved successfully")


# Transactions tab
def drawTransactions():
    deleteAllChildren(tab1)
    btn = Button(tab1, text="Apply rules", command=applyRulesButton)
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
        popup.grab_set()
        popup.title("Accounts")
        popup.geometry("500x400")
        popupFrame = ttk.Frame(popup)
        popupFrame.pack()
        drawAccountsPopup(popupFrame, popup, loadTransactions, filename)


def applyRulesButton():
    for t in transactions:
        if not t.category:
            for r in rules:
                ruleApplies = True
                for c in r.conditions:
                    field = 0
                    if c.field == FIELD["DATETIME"]:
                        field = t.dateTime
                    if c.field == FIELD["TEXT"]:
                        field = t.text
                    if c.field == FIELD["AMOUNT"]:
                        field = t.amount
                    if c.conditionType == COND["L"]:
                        if not(field < c.value):
                            ruleApplies = False
                    if c.conditionType == COND["LE"]:
                        if not(field <= c.value):
                            ruleApplies = False
                    if c.conditionType == COND["E"]:
                        if not(field == c.value):
                            ruleApplies = False
                    if c.conditionType == COND["GE"]:
                        if not(field >= c.value):
                            ruleApplies = False
                    if c.conditionType == COND["G"]:
                        if not(field > c.value):
                            ruleApplies = False
                    if c.conditionType == COND["NE"]:
                        if not(field != c.value):
                            ruleApplies = False
                    if c.conditionType == COND["C"]:
                        if not(c.value.lower() in field.lower()):
                            ruleApplies = False
                if ruleApplies:
                    t.category = r.category
    drawTransactions()


def loadTransactions(fileName, account):
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
    originalLen = len(transactions)
    for row in cols:
        if maxID <= len(row)-1:
            newTransaction = Transaction(datetime.strptime(row[dateID], "%Y-%m-%d").date(), row[textID],
                                         str2float(row[amountID]), str2float(row[balanceID]), account, None)
            duplication = False
            for i in range(originalLen):
                if transactions[i].equals(newTransaction):
                    duplication = True
            if not duplication:
                transactions.append(newTransaction)


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
            popup.add_command(label="Remove account", command=lambda f=frame, aArg=a:
                              removeAccount(f, aArg))
            e.popup = popup
            row += 1
        else:
            lbl = Label(frame, text=a.name)
            lbl.grid(sticky=W, row=row, column=0)
            lbl.account = a
            lbl.bind("<Button-1>", lambda event, f=frame: selectAccount(f, event))
            lbl.bind("<Button-3>", rightClickAccount)
            popup = Menu(lbl, tearoff=0)
            popup.add_command(label="Remove account", command=lambda f=frame, aArg=a:
                              removeAccount(f, aArg))
            lbl.popup = popup
            row += 1
    btn = Button(frame, text="+", command=lambda f=frame: addAccountButton(f))
    btn.grid(row=row, column=0)


def addAccountButton(frame):
    accounts.append(Account("new"))
    drawAccounts(frame)


def rightClickAccount(event):
    popup = event.widget.popup
    try:
        popup.tk_popup(event.x_root+60, event.y_root+13, 0)
    finally:
        popup.grab_release()


def removeAccount(frame, a):
    accounts.remove(a)
    drawAccounts(frame)


def selectAccount(frame, event):
    global selectedItem
    if selectedItem != event.widget.account:
        selectedItem = event.widget.account
        drawAccounts(frame)


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
            sv.trace("w", lambda name, index, mode, svArg=sv: accountNameChanged2(svArg))
            e = Entry(frame, textvariable=sv)
            e.insert(0, a.name)
            e.grid(sticky=W, row=row, column=0)
            e.bind("<Button-3>", rightClickAccount2)
            popupR = Menu(e, tearoff=0)
            popupR.add_command(label="Remove account", command=lambda f=frame, aArg=a, p=popup, fu=func,
                              fi=filename: removeAccount2(f, aArg, p, fu, fi))
            e.popup = popupR
            row += 1
        else:
            lbl = Label(frame, text=a.name)
            lbl.grid(sticky=W, row=row, column=0)
            lbl.account = a
            lbl.bind("<Button-1>", lambda event, f=frame, p=popup, fu=func, fi=filename:
                    selectAccount2(f, event, p, fu, fi))
            lbl.bind("<Button-3>", rightClickAccount2)
            popupR = Menu(lbl, tearoff=0)
            popupR.add_command(label="Remove account", command=lambda f=frame, aArg=a, p=popup, fu=func, fi=filename:
                               removeAccount2(f, aArg, p, fu, fi))
            lbl.popup = popupR
            row += 1
    btn = Button(frame, text="+", command=lambda f=frame, p=popup, fu=func, fi=filename:
                 addAccountButton2(f, p, fu, fi))
    btn.grid(row=row, column=0)
    btn = Button(frame, text="Select", command=lambda argPopup=popup, argFunc=func, argFilename=filename:
                 selectAccountInPopup(argPopup, argFunc, argFilename))
    btn.grid(row=row+1, column=0)
    btn = Button(frame, text="Cancel", command=popup.destroy)
    btn.grid(row=row+1, column=1)


def addAccountButton2(frame, popup, func, filename):
    accounts.append(Account("new"))
    drawAccountsPopup(frame, popup, func, filename)


def rightClickAccount2(event):
    popup = event.widget.popup
    try:
        popup.tk_popup(event.x_root+60, event.y_root+13, 0)
    finally:
        popup.grab_release()


def removeAccount2(frame, a, popup, func, filename):
    accounts.remove(a)
    drawAccountsPopup(frame, popup, func, filename)


def selectAccount2(frame, event, popup, func, filename):
    global selectedItem
    if selectedItem != event.widget.account:
        selectedItem = event.widget.account
        drawAccountsPopup(frame, popup, func, filename)


def accountNameChanged2(sv):
    sv.account.name = sv.get()


def selectAccountInPopup(popup, func, filename):
    if selectedItem in accounts:
        func(filename, selectedItem)
        popup.destroy()
        drawTransactions()


# Main
def main():
    window.title("Money tracker")
    window.geometry("920x800")
    fileMenu.add_command(label="import transactions", command=loadFileButton)
    fileMenu.add_command(label="new", command=newProject)
    fileMenu.add_command(label="open", command=openProject)
    fileMenu.add_command(label="save", command=saveProject)
    helpMenu.add_command(label="about", command=lambda: messagebox.showinfo("About", "Money tracker v0.1"))
    menuBar.add_cascade(label="File", menu=fileMenu)
    menuBar.add_cascade(label="Help", menu=helpMenu)
    window.config(menu=menuBar)

    tabControl.add(outerFrame1, text="Transactions")
    tabControl.add(outerFrame2, text="Rules")
    tabControl.add(outerFrame3, text="Categories")
    tabControl.add(outerFrame4, text="Accounts")
    tabControl.pack(expand=1, fill="both")
    tabControl.bind("<<NotebookTabChanged>>", lambda event: tabChanged(event))

    canvas1.pack(side="left", fill="both", expand=True)
    scrollbar1.pack(side="right", fill="y")
    canvas2.pack(side="left", fill="both", expand=True)
    scrollbar2.pack(side="right", fill="y")
    canvas3.pack(side="left", fill="both", expand=True)
    scrollbar3.pack(side="right", fill="y")
    canvas4.pack(side="left", fill="both", expand=True)
    scrollbar4.pack(side="right", fill="y")

    categories.append(Category("Bil", None))
    categories.append(Category("Mat", None))
    categories.append(Category("Service", categories[0]))
    categories.append(Category("Hyra", None))

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

    r = Rule(categories[3])
    c = Condition(FIELD["TEXT"], COND["C"], "Fastum")
    r.conditions.append(c)
    rules.append(r)

    accounts.append(Account("Rasmus lönekonto"))
    accounts.append(Account("Räkningskonto"))

    window.mainloop()


if __name__ == "__main__":
    main()
