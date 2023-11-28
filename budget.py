
class Category:
    def __str__(self):
        category_name_len = len(self.cat_name)
        f_p =  '*'*((30-category_name_len)//2)
        first =f_p+self.cat_name+'*'*(30-category_name_len-len(f_p))+"\n"
        foll_lines = ''
        for items in self.ledger:
            items_descrips = items.get('description')
            if len(items_descrips)>23:
                items_descrips = items_descrips[:23]
            foll_lines+=items_descrips
            amount = items.get('amount')
            amount = "%.2f" % amount
            raligned = len(amount)
            space_place = 30-len(items_descrips)-raligned
            foll_lines+=" "*space_place+amount+"\n"
        return first+foll_lines+ f"Total: {self.get_balance()}"


    def __init__(self, cat_name):
        self.cat_name = cat_name
        self.ledger = []
    def deposit(self, amount, description=''):
        my_dict = {
            "amount":amount,
            "description":description}
        return self.ledger.append(my_dict)
    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            with_dict = {
                "amount":-amount,
                "description":description
            }
            self.ledger.append(with_dict)
            return True
        return False
    def get_balance(self):
        sum_expense = 0
        for expense in self.ledger:
            sum_expense+=expense.get('amount')
        return  sum_expense
    def transfer(self,amount, budget_cat):
        if self.check_funds(amount):
            self.withdraw(amount,f"Transfer to {budget_cat.cat_name}")
            budget_cat.deposit(amount, f"Transfer from {self.cat_name}")
            return True
        return False
    def check_funds(self, amount):
        return (self.get_balance()>=amount)
def create_spend_chart(categories:list) -> str:
    chart = "Percentage spent by category\n"
    bar = []

    for category in categories:
        percents = 0
        for transaction in category.ledger:
            if transaction.get('amount')>0:
                continue
            else:
                percents-= transaction.get('amount')
        bar.append(percents)
    denom = sum(bar)
    for per in range(len(bar)):
        bar[per] = (bar[per]/denom)*100
    for i in range(100,-10,-10):
        initial_space = 3
        chart += " "*(initial_space-len(str(i))) + str(i)+'|'+ ' '
        for j in bar:
            if i <= j:
                chart+= 'o'+'  '
            else:
                chart+="   "
        chart+="\n"
    chart+="    ----------\n"
    biggest = ''
    for cat in categories:
        if len(cat.cat_name)>len(biggest):
            biggest = cat.cat_name
    for index in range(len(biggest)):
        chart += "     "
        for i in range(3):
            if len(categories[i].cat_name)<=index:
                chart+='   '
            elif len(biggest)-1 == index:
                chart+= categories[i].cat_name[index] + '  '
                return chart
            else:
                chart += categories[i].cat_name[index] + '  '
        chart+="\n"
    return chart
