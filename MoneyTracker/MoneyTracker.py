import tkinter
import tkinter.ttk as ttk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messagebox
import tkinter.simpledialog as simpledialog
from datetime import datetime
import numpy
import matplotlib.backends.backend_tkagg as matTkagg
import matplotlib.figure as matFig
import matplotlib.pyplot as plt
import MTBackend as mt


# Main frontend class
class MoneyWindow:
    def __init__(self):
        self.mt = mt.MoneyTracker()
        self.selectedItem = None
        self.window = tkinter.Tk()
        self.menuBar = tkinter.Menu(self.window)
        self.fileMenu = tkinter.Menu(self.menuBar, tearoff=0)
        self.helpMenu = tkinter.Menu(self.menuBar, tearoff=0)
        self.popup = None
        self.popupFrame = None
        self.fileName = None

        self.tabControl = ttk.Notebook(self.window)
        self.outerFrame1 = tkinter.Frame(self.tabControl)
        self.canvas1 = tkinter.Canvas(self.outerFrame1)
        self.scrollbar1 = tkinter.Scrollbar(self.outerFrame1, orient="vertical", command=self.canvas1.yview)
        self.tab1 = tkinter.Frame(self.canvas1)
        self.canvas1.create_window((0, 0), window=self.tab1, anchor="nw")
        self.canvas1.configure(yscrollcommand=self.scrollbar1.set)
        self.tab1.bind("<Configure>", lambda e: self.canvas1.configure(scrollregion=self.canvas1.bbox("all")))

        self.outerFrame2 = tkinter.Frame(self.tabControl)
        self.canvas2 = tkinter.Canvas(self.outerFrame2)
        self.scrollbar2 = tkinter.Scrollbar(self.outerFrame2, orient="vertical", command=self.canvas2.yview)
        self.tab2 = tkinter.Frame(self.canvas2)
        self.canvas2.create_window((0, 0), window=self.tab2, anchor="nw")
        self.canvas2.configure(yscrollcommand=self.scrollbar2.set)
        self.tab2.bind("<Configure>", lambda e: self.canvas2.configure(scrollregion=self.canvas2.bbox("all")))

        self.outerFrame3 = tkinter.Frame(self.tabControl)
        self.canvas3 = tkinter.Canvas(self.outerFrame3)
        self.scrollbar3 = tkinter.Scrollbar(self.outerFrame3, orient="vertical", command=self.canvas3.yview)
        self.tab3 = tkinter.Frame(self.canvas3)
        self.canvas3.create_window((0, 0), window=self.tab3, anchor="nw")
        self.canvas3.configure(yscrollcommand=self.scrollbar3.set)
        self.tab3.bind("<Configure>", lambda e: self.canvas3.configure(scrollregion=self.canvas3.bbox("all")))

        self.outerFrame4 = tkinter.Frame(self.tabControl)
        self.canvas4 = tkinter.Canvas(self.outerFrame4)
        self.scrollbar4 = tkinter.Scrollbar(self.outerFrame4, orient="vertical", command=self.canvas4.yview)
        self.tab4 = tkinter.Frame(self.canvas4)
        self.canvas4.create_window((0, 0), window=self.tab4, anchor="nw")
        self.canvas4.configure(yscrollcommand=self.scrollbar4.set)
        self.tab4.bind("<Configure>", lambda e: self.canvas4.configure(scrollregion=self.canvas4.bbox("all")))

        self.outerFrame5 = tkinter.Frame(self.tabControl)
        self.canvas5 = tkinter.Canvas(self.outerFrame5)
        self.scrollbar5 = tkinter.Scrollbar(self.outerFrame5, orient="vertical", command=self.canvas5.yview)
        self.tab5 = tkinter.Frame(self.canvas5)
        self.canvas5.create_window((0, 0), window=self.tab5, anchor="nw")
        self.canvas5.configure(yscrollcommand=self.scrollbar5.set)
        self.tab5.bind("<Configure>", lambda e: self.canvas5.configure(scrollregion=self.canvas5.bbox("all")))

        self.window.title("Money tracker")
        self.window.geometry("920x800")
        self.fileMenu.add_command(label="import transactions", command=self.loadFileButton)
        self.fileMenu.add_command(label="new", command=self.newProject)
        self.fileMenu.add_command(label="open", command=self.openProject)
        self.fileMenu.add_command(label="save", command=self.saveProject)
        self.helpMenu.add_command(label="about", command=lambda: messagebox.showinfo("About", "Money tracker v0.1"))
        self.menuBar.add_cascade(label="File", menu=self.fileMenu)
        self.menuBar.add_cascade(label="Help", menu=self.helpMenu)
        self.window.config(menu=self.menuBar)

        self.tabControl.add(self.outerFrame1, text="Transactions")
        self.tabControl.add(self.outerFrame2, text="Rules")
        self.tabControl.add(self.outerFrame3, text="Categories")
        self.tabControl.add(self.outerFrame4, text="Accounts")
        self.tabControl.add(self.outerFrame5, text="Graphs")
        self.tabControl.pack(expand=1, fill="both")
        self.tabControl.bind("<<NotebookTabChanged>>", lambda event: self.tabChanged())

        self.canvas1.pack(side="left", fill="both", expand=True)
        self.scrollbar1.pack(side="right", fill="y")
        self.canvas2.pack(side="left", fill="both", expand=True)
        self.scrollbar2.pack(side="right", fill="y")
        self.canvas3.pack(side="left", fill="both", expand=True)
        self.scrollbar3.pack(side="right", fill="y")
        self.canvas4.pack(side="left", fill="both", expand=True)
        self.scrollbar4.pack(side="right", fill="y")
        self.canvas5.pack(side="left", fill="both", expand=True)
        self.scrollbar5.pack(side="right", fill="y")

    # Common functions
    def mainLoop(self):
        self.window.mainloop()

    def tabChanged(self):
        if self.tabControl.tab(self.tabControl.select(), "text") == "Transactions":
            self.drawTransactions()
        if self.tabControl.tab(self.tabControl.select(), "text") == "Rules":
            self.drawRules()
        if self.tabControl.tab(self.tabControl.select(), "text") == "Categories":
            self.drawCategories()
        if self.tabControl.tab(self.tabControl.select(), "text") == "Accounts":
            self.drawAccounts()
        if self.tabControl.tab(self.tabControl.select(), "text") == "Graphs":
            self.drawGraphs()

    def newProject(self):
        self.mt.newProject()
        self.tabChanged()

    def openProject(self):
        fileName = filedialog.askopenfilename(initialdir="/", title="Save file",
                                              filetypes=(("Money tracker project files", "*.mtp"),
                                                         ("all files", "*.*")))
        if fileName:
            if self.mt.openProject(fileName) == -1:
                messagebox.showerror("Error", "Could not load file, program version to old")
                return
            self.drawTransactions()
            self.drawRules()
            self.drawCategories()
            self.drawAccounts()

    def saveProject(self):
        fileName = filedialog.asksaveasfilename(initialdir="/", title="Save file",
                                                filetypes=(("Money tracker project files", "*.mtp"),
                                                           ("all files", "*.*")), defaultextension=".mtp")
        if fileName:
            self.mt.saveProject(fileName)
            messagebox.showinfo("Info", "File saved successfully")

    # Transactions tab
    def drawTransactions(self):
        deleteAllChildren(self.tab1)
        btn = tkinter.Button(self.tab1, text="Apply rules", command=self.applyRulesButton)
        btn.grid(column=0, row=0)
        lbl = tkinter.Label(self.tab1, text="Date")
        lbl.grid(sticky=tkinter.W, row=1, column=0)
        lbl = tkinter.Label(self.tab1, text="Text")
        lbl.grid(sticky=tkinter.W, row=1, column=1)
        lbl = tkinter.Label(self.tab1, text="Amount")
        lbl.grid(sticky=tkinter.W, row=1, column=2)
        lbl = tkinter.Label(self.tab1, text="Balance")
        lbl.grid(sticky=tkinter.W, row=1, column=3)
        lbl = tkinter.Label(self.tab1, text="Account")
        lbl.grid(sticky=tkinter.W, row=1, column=4)
        lbl = tkinter.Label(self.tab1, text="Category")
        lbl.grid(sticky=tkinter.W, row=1, column=5)
        row = 2
        for t in self.mt.transactions:
            lbl = tkinter.Label(self.tab1, text=t.dateTime)
            lbl.grid(sticky=tkinter.W, row=row, column=0)
            lbl = tkinter.Label(self.tab1, text=t.text)
            lbl.grid(sticky=tkinter.W, row=row, column=1)
            lbl = tkinter.Label(self.tab1, text=t.amount)
            lbl.grid(sticky=tkinter.W, row=row, column=2)
            lbl = tkinter.Label(self.tab1, text=t.balance)
            lbl.grid(sticky=tkinter.W, row=row, column=3)
            lbl = tkinter.Label(self.tab1, text=t.account.name if t.account else "None")
            lbl.grid(sticky=tkinter.W, row=row, column=4)
            lbl = tkinter.Label(self.tab1, text=t.category.name if t.category else "None")
            lbl.grid(sticky=tkinter.W, row=row, column=5)
            row += 1

    def loadFileButton(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                              filetypes=(("csv files", "*.csv"), ("all files", "*.*")))
        if filename:
            self.popup = tkinter.Toplevel()
            self.popup.grab_set()
            self.popup.title("Accounts")
            self.popup.geometry("500x400")
            self.popupFrame = tkinter.Frame(self.popup)
            self.popupFrame.pack()
            self.fileName = filename
            self.drawAccountsPopup()

    def applyRulesButton(self):
        for t in self.mt.transactions:
            if not t.category:
                for r in self.mt.rules:
                    ruleApplies = True
                    for c in r.conditions:
                        field = 0
                        if c.field == mt.FIELD["DATETIME"]:
                            field = t.dateTime
                        if c.field == mt.FIELD["TEXT"]:
                            field = t.text
                        if c.field == mt.FIELD["AMOUNT"]:
                            field = t.amount
                        if c.conditionType == mt.COND["L"]:
                            if not(field < c.value):
                                ruleApplies = False
                        if c.conditionType == mt.COND["LE"]:
                            if not(field <= c.value):
                                ruleApplies = False
                        if c.conditionType == mt.COND["E"]:
                            if not(field == c.value):
                                ruleApplies = False
                        if c.conditionType == mt.COND["GE"]:
                            if not(field >= c.value):
                                ruleApplies = False
                        if c.conditionType == mt.COND["G"]:
                            if not(field > c.value):
                                ruleApplies = False
                        if c.conditionType == mt.COND["NE"]:
                            if not(field != c.value):
                                ruleApplies = False
                        if c.conditionType == mt.COND["C"]:
                            if c.field != mt.FIELD["TEXT"] or not(c.value.lower() in field.lower()):
                                ruleApplies = False
                    if ruleApplies:
                        t.category = r.category
        self.drawTransactions()

    # Rules tab
    def drawRules(self):
        deleteAllChildren(self.tab2)
        row = 0
        for r in self.mt.rules:
            if r == self.selectedItem:
                categoriesTextList = []
                selectedIndex = 0
                for c in self.mt.categories:
                    categoriesTextList.append(c.name)
                    if c == r.category:
                        selectedIndex = len(categoriesTextList)-1
                combo = ttk.Combobox(self.tab2, values=categoriesTextList, state="readonly")
                combo.grid(row=row, column=0)
                combo.current(selectedIndex)
                combo.bind("<<ComboboxSelected>>", self.ruleCategorySelected)
                combo.bind("<Button-3>", showPopup)
                popup = tkinter.Menu(combo, tearoff=0)
                popup.add_command(label="Remove rule", command=lambda rArg=r: self.removeRule(rArg))
                combo.popup = popup
                combo.rule = r
                row += 1
                for c in r.conditions:
                    combo2 = ttk.Combobox(self.tab2, values=["<", "<=", "==", ">=", ">", "!=", "Contains"],
                                          state="readonly")
                    combo2.grid(row=row, column=1)
                    combo2.current(c.conditionType-1)
                    combo2.bind("<<ComboboxSelected>>", self.conditionTypeSelected)
                    combo2.bind("<Button-3>", showPopup)
                    popup = tkinter.Menu(combo2, tearoff=0)
                    popup.add_command(label="Remove condition",
                                      command=lambda rArg=r, cArg=c: self.removeCondition(rArg, cArg))
                    combo2.popup = popup
                    combo2.condition = c
                    sv = tkinter.StringVar()
                    sv.condition = c
                    sv.trace("w", lambda name, index, mode, svArg=sv: self.conditionValueChanged(svArg))
                    e = tkinter.Entry(self.tab2, textvariable=sv)
                    e.insert(0, c.value)
                    e.grid(sticky=tkinter.W, row=row, column=2)
                    e.bind("<Button-3>", showPopup)
                    popup = tkinter.Menu(e, tearoff=0)
                    popup.add_command(label="Remove condition",
                                      command=lambda rArg=r, cArg=c: self.removeCondition(rArg, cArg))
                    e.popup = popup
                    combo1 = ttk.Combobox(self.tab2, values=["Date/time", "Text", "Amount"], state="readonly")
                    combo1.grid(row=row, column=0)
                    combo1.current(c.field-1)
                    combo1.bind("<<ComboboxSelected>>", self.conditionFieldSelected)
                    combo1.bind("<Button-3>", showPopup)
                    popup = tkinter.Menu(combo1, tearoff=0)
                    popup.add_command(label="Remove condition",
                                      command=lambda rArg=r, cArg=c: self.removeCondition(rArg, cArg))
                    combo1.popup = popup
                    combo1.condition = c
                    combo1.conditionTypeBox = combo2
                    combo1.valueBox = sv
                    row += 1
                btn = tkinter.Button(self.tab2, text="+", command=lambda argR=r: self.addConditionButton(argR))
                btn.grid(row=row, column=1)
                row += 1
            else:
                lbl = tkinter.Label(self.tab2, text=r.category.name)
                lbl.grid(sticky=tkinter.W, row=row, column=0)
                lbl.rule = r
                lbl.bind("<Button-1>", self.selectRule)
                lbl.bind("<Button-3>", showPopup)
                popup = tkinter.Menu(lbl, tearoff=0)
                popup.add_command(label="Remove rule", command=lambda rArg=r: self.removeRule(rArg))
                lbl.popup = popup
                row += 1
                for c in r.conditions:
                    lbl = tkinter.Label(self.tab2, text=mt.fieldString(c.field), padx=10)
                    lbl.grid(sticky=tkinter.W, row=row, column=0)
                    lbl.rule = r
                    lbl.bind("<Button-1>", self.selectRule)
                    lbl.bind("<Button-3>", showPopup)
                    popup = tkinter.Menu(lbl, tearoff=0)
                    popup.add_command(label="Remove condition",
                                      command=lambda rArg=r, cArg=c: self.removeCondition(rArg, cArg))
                    lbl.popup = popup
                    lbl = tkinter.Label(self.tab2, text=mt.condString(c.conditionType))
                    lbl.grid(sticky=tkinter.W, row=row, column=1)
                    lbl.rule = r
                    lbl.bind("<Button-1>", self.selectRule)
                    lbl.bind("<Button-3>", showPopup)
                    popup = tkinter.Menu(lbl, tearoff=0)
                    popup.add_command(label="Remove condition",
                                      command=lambda rArg=r, cArg=c: self.removeCondition(rArg, cArg))
                    lbl.popup = popup
                    lbl = tkinter.Label(self.tab2, text=c.value)
                    lbl.grid(sticky=tkinter.W, row=row, column=2)
                    lbl.rule = r
                    lbl.bind("<Button-1>", self.selectRule)
                    lbl.bind("<Button-3>", showPopup)
                    popup = tkinter.Menu(lbl, tearoff=0)
                    popup.add_command(label="Remove condition",
                                      command=lambda rArg=r, cArg=c: self.removeCondition(rArg, cArg))
                    lbl.popup = popup
                    row += 1
        btn = tkinter.Button(self.tab2, text="+", command=self.addRuleButton)
        btn.grid(row=row, column=0)

    def addRuleButton(self):
        self.mt.appendRule()
        self.drawRules()

    def addConditionButton(self, r):
        r.appendCondition()
        self.drawRules()

    def removeRule(self, r):
        self.mt.rules.remove(r)
        self.drawRules()

    def removeCondition(self, r, c):
        r.conditions.remove(c)
        if len(r.conditions) == 0:
            self.mt.rules.remove(r)
        self.drawRules()

    def selectRule(self, event):
        if self.selectedItem != event.widget.rule:
            self.selectedItem = event.widget.rule
            self.drawRules()

    def ruleCategorySelected(self, event):
        event.widget.rule.category = self.mt.categories[event.widget.current()]

    @staticmethod
    def conditionFieldSelected(event):
        event.widget.condition.field = event.widget.current()+1
        if event.widget.condition.field == mt.FIELD["DATETIME"]:
            try:
                event.widget.condition.value = datetime.strptime(event.widget.valueBox.get(), "%Y-%m-%d").date()
            except ValueError:
                event.widget.valueBox.set("1986-07-25")
        if event.widget.condition.field == mt.FIELD["AMOUNT"]:
            event.widget.condition.value = mt.str2float(event.widget.valueBox.get())
            event.widget.valueBox.set(str(event.widget.condition.value))

    @staticmethod
    def conditionTypeSelected(event):
        event.widget.condition.conditionType = event.widget.current()+1

    @staticmethod
    def conditionValueChanged(sv):
        if sv.condition.field == mt.FIELD["AMOUNT"]:
            sv.condition.value = mt.str2float(sv.get())
        if sv.condition.field == mt.FIELD["TEXT"]:
            sv.condition.value = sv.get()
        if sv.condition.field == mt.FIELD["DATETIME"]:
            try:
                sv.condition.value = datetime.strptime(sv.get(), "%Y-%m-%d").date()
            except ValueError:
                pass

    # Categories tab
    def drawCategories(self):
        deleteAllChildren(self.tab3)
        tree = ttk.Treeview(self.tab3)
        tree.bind("<Button-3>", self.rightClickCategory)
        tree.bind("<Double-1>", self.doubleClickCategory)
        popup = tkinter.Menu(tree, tearoff=0)
        popup.add_command(label="Add new category", command=lambda treeArg=tree: self.addCategory(treeArg))
        popup.add_command(label="Remove category", command=lambda treeArg=tree: self.removeCategory(treeArg))
        popup.add_command(label="Rename category", command=lambda treeArg=tree: self.renameCategory(treeArg))

        tree.popup = popup
        tree.column("#0", width=270, minwidth=270)
        tree.heading("#0", text="Categories", anchor=tkinter.W)
        tree.insert("", "end", 0, text="root")
        for i in range(len(self.mt.categories)):
            self.mt.categories[i].id = i+1
        catCopy = self.mt.categories.copy()
        while len(catCopy) > 0:
            self.addTreeItem(tree, catCopy, catCopy[0])
        tree.pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=True)

    def addTreeItem(self, tree, catCopy, category):
        if not category.parent:
            tree.insert("0", "end", category.id, text=category.name)
            catCopy.remove(category)
            return
        else:
            for c in catCopy:
                if c == category.parent:
                    self.addTreeItem(tree, catCopy, c)
                    break
            tree.insert(category.parent.id, "end", category.id, text=category.name)
            catCopy.remove(category)
            return

    @staticmethod
    def rightClickCategory(event):
        iid = event.widget.identify_row(event.y)
        if iid:
            event.widget.selection_set(iid)
            popup = event.widget.popup
            try:
                popup.tk_popup(event.x_root+60, event.y_root+13, 0)
            finally:
                popup.grab_release()

    def doubleClickCategory(self, event):
        iid = event.widget.identify_row(event.y)
        if iid and int(iid) > 0:
            event.widget.selection_set(iid)
            self.renameCategory(event.widget)

    def addCategory(self, tree):
        name = simpledialog.askstring("Category", "Name category", parent=self.window)
        if name is None:
            return
        if int(tree.selection()[0]) == 0:
            self.mt.appendCategory(name, None)
            self.drawCategories()
            return
        for c in self.mt.categories:
            if c.id == int(tree.selection()[0]):
                self.mt.appendCategory(name, c)
                self.drawCategories()
                return

    def renameCategory(self, tree):
        if int(tree.selection()[0]) == 0:
            return
        name = simpledialog.askstring("Category", "Rename category", parent=self.window)
        if name is not None:
            for c in self.mt.categories:
                if c.id == int(tree.selection()[0]):
                    c.name = name
                    self.drawCategories()
                    return

    def removeCategory(self, tree):
        for c in self.mt.categories:
            if c.id == int(tree.selection()[0]):
                answer = messagebox.askyesno("Warning!", "Do you really want to remove category '" + c.name + "'?")
                if not answer:
                    return
                catCopy = self.mt.categories.copy()
                self.mt.deleteCategory(c, catCopy)
                self.drawCategories()
                return

    # Accounts tab
    def drawAccounts(self):
        deleteAllChildren(self.tab4)
        row = 0
        for a in self.mt.accounts:
            if a == self.selectedItem:
                sv = tkinter.StringVar()
                sv.account = a
                sv.trace("w", lambda name, index, mode, svArg=sv: self.accountNameChanged(svArg))
                e = tkinter.Entry(self.tab4, textvariable=sv)
                e.insert(0, a.name)
                e.grid(sticky=tkinter.W, row=row, column=0)
                e.bind("<Button-3>", showPopup)
                popup = tkinter.Menu(e, tearoff=0)
                popup.add_command(label="Remove account", command=lambda aArg=a:
                                  self.removeAccount(aArg))
                e.popup = popup
                row += 1
            else:
                lbl = tkinter.Label(self.tab4, text=a.name)
                lbl.grid(sticky=tkinter.W, row=row, column=0)
                lbl.account = a
                lbl.bind("<Button-1>", lambda event: self.selectAccount(event))
                lbl.bind("<Button-3>", showPopup)
                popup = tkinter.Menu(lbl, tearoff=0)
                popup.add_command(label="Remove account", command=lambda aArg=a:
                                  self.removeAccount(aArg))
                lbl.popup = popup
                row += 1
        btn = tkinter.Button(self.tab4, text="+", command=lambda: self.addAccountButton())
        btn.grid(row=row, column=0)

    def addAccountButton(self):
        self.mt.accounts.append(mt.Account("new"))
        self.drawAccounts()

    def removeAccount(self, a):
        self.mt.accounts.remove(a)
        for t in self.mt.transactions:
            if t.account == a:
                t.account = None
        self.drawAccounts()

    def selectAccount(self, event):
        if self.selectedItem != event.widget.account:
            self.selectedItem = event.widget.account
            self.drawAccounts()

    @staticmethod
    def accountNameChanged(sv):
        sv.account.name = sv.get()

    # Graphs tab
    def drawGraphs(self):
        deleteAllChildren(self.tab5)
        for a in self.mt.accounts:
            a.balance = 0
        self.mt.transactions.sort(key=lambda tran: tran.dateTime)
        dates = []
        for c in self.mt.categories:
            c.posSum = 0
            c.negSum = 0
            c.children = [mt.Category(c.name)]
        level1Categories = []
        for c in self.mt.categories:
            if c.parent:
                c.parent.children.append(c)
            else:
                level1Categories.append(c)
        balancePerDay = []
        for i in range(len(self.mt.transactions)):
            if self.mt.transactions[i].category:
                cat = self.mt.transactions[i].category
                if self.mt.transactions[i].amount > 0:
                    cat.children[0].posSum += self.mt.transactions[i].amount
                else:
                    cat.children[0].negSum -= self.mt.transactions[i].amount
                while cat:
                    if self.mt.transactions[i].amount > 0:
                        cat.posSum += self.mt.transactions[i].amount
                    else:
                        cat.negSum -= self.mt.transactions[i].amount
                    cat = cat.parent
            if self.mt.transactions[i].account:
                self.mt.transactions[i].account.balance = self.mt.transactions[i].balance
            totalBalance = 0
            for a in self.mt.accounts:
                totalBalance += a.balance
            if (i == len(self.mt.transactions)-1 or self.mt.transactions[i].dateTime !=
                    self.mt.transactions[i+1].dateTime):
                dates.append(self.mt.transactions[i].dateTime)
                balancePerDay.append(totalBalance)
        fig = matFig.Figure(figsize=(10, 10), dpi=100)
        graph1 = fig.add_subplot(211)
        graph1.plot_date(dates, balancePerDay, xdate=True, ls="-")
        graph1.set_ylabel("Total money")
        graph2 = fig.add_subplot(212)
        cmap = plt.get_cmap("tab20c")
        level1Values = []
        level1Colors = []
        level1Labels = []
        level2Values = []
        level2Colors = []
        level2Labels = []
        color = 0
        for c in level1Categories:
            level1Values.append(c.negSum)
            level1Colors.append(color)
            level1Labels.append(c.name)
            childColor = color
            for c2 in c.children:
                level2Values.append(c2.negSum)
                level2Colors.append(childColor)
                level2Labels.append(c2.name)
                childColor += 1
                if childColor % 4 == 0:
                    childColor -= 4
            color += 4
            if color == 20:
                color = 0
        graph2.pie(level1Values, colors=cmap(level1Colors), radius=1.0,
                   wedgeprops=dict(width=0.5, edgecolor='w'))
        wedges, notUsed = graph2.pie(level2Values, colors=cmap(level2Colors), radius=0.8,
                                     wedgeprops=dict(width=0.3, edgecolor='w'))
        kw = dict(arrowprops=dict(arrowstyle="-"), va="center")
        for i, p in enumerate(wedges):
            ang = (p.theta2 - p.theta1) / 2. + p.theta1
            y = numpy.sin(numpy.deg2rad(ang))
            x = numpy.cos(numpy.deg2rad(ang))
            horizontalAlignment = {-1: "right", 1: "left"}[int(numpy.sign(x))]
            connectionStyle = "angle,angleA=0,angleB={}".format(ang)
            kw["arrowprops"].update({"connectionstyle": connectionStyle})
            graph2.annotate(level2Labels[i], xy=(x*0.65, y*0.65), xytext=(1.35 * numpy.sign(x), 1.4 * y),
                            horizontalalignment=horizontalAlignment, **kw)
        canvas = matTkagg.FigureCanvasTkAgg(fig, master=self.tab5)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tkinter.TOP, fill=tkinter.BOTH, expand=1)

    # Popups
    def drawAccountsPopup(self):
        deleteAllChildren(self.popupFrame)
        row = 0
        for a in self.mt.accounts:
            if a == self.selectedItem:
                sv = tkinter.StringVar()
                sv.account = a
                sv.trace("w", lambda name, index, mode, svArg=sv: self.accountNameChanged2(svArg))
                e = tkinter.Entry(self.popupFrame, textvariable=sv)
                e.insert(0, a.name)
                e.grid(sticky=tkinter.W, row=row, column=0)
                e.bind("<Button-3>", showPopup)
                popupR = tkinter.Menu(e, tearoff=0)
                popupR.add_command(label="Remove account", command=lambda aArg=a: self.removeAccount2(aArg))
                e.popup = popupR
                row += 1
            else:
                lbl = tkinter.Label(self.popupFrame, text=a.name)
                lbl.grid(sticky=tkinter.W, row=row, column=0)
                lbl.account = a
                lbl.bind("<Button-1>", lambda event: self.selectAccount2(event))
                lbl.bind("<Button-3>", showPopup)
                popupR = tkinter.Menu(lbl, tearoff=0)
                popupR.add_command(label="Remove account",
                                   command=lambda aArg=a:
                                   self.removeAccount2(aArg))
                lbl.popup = popupR
                row += 1
        btn = tkinter.Button(self.popupFrame, text="+", command=self.addAccountButton2)
        btn.grid(row=row, column=0)
        btn = tkinter.Button(self.popupFrame, text="Select", command=self.selectAccountInPopup)
        btn.grid(row=row+1, column=0)
        btn = tkinter.Button(self.popupFrame, text="Cancel", command=self.popup.destroy)
        btn.grid(row=row+1, column=1)

    def addAccountButton2(self):
        self.mt.accounts.append(mt.Account("new"))
        self.drawAccountsPopup()

    def removeAccount2(self, a):
        self.mt.accounts.remove(a)
        self.drawAccountsPopup()

    def selectAccount2(self, event):
        if self.selectedItem != event.widget.account:
            self.selectedItem = event.widget.account
            self.drawAccountsPopup()

    @staticmethod
    def accountNameChanged2(sv):
        sv.account.name = sv.get()

    def selectAccountInPopup(self):
        if self.selectedItem in self.mt.accounts:
            self.mt.loadTransactions(self.fileName, self.selectedItem)
            self.popup.destroy()
            self.drawTransactions()


# Functions
def deleteAllChildren(item):
    _list = item.winfo_children()
    for item in _list:
        if item.winfo_children():
            _list.extend(item.winfo_children())
    for i in _list:
        i.destroy()


def showPopup(event):
    popup = event.widget.popup
    try:
        popup.tk_popup(event.x_root+60, event.y_root+13, 0)
    finally:
        popup.grab_release()
