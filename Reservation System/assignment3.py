from sys import argv

X, Y = 0, 1
abc = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
price = {'student': 10, 'full': 20, 'season': 250}
category_data = {}

def read_file(file):
    with open(file, mode="r", encoding="utf-8") as f:
        return [line.split(' ') for line in f.read().split('\n')]

def make_coor(seat_num):
    limits = list(map(int, seat_num[1:].split("-")))
    seats = [seat_num[0] + str(n) for n in range(limits[0], limits[1] + 1)]
    text_to_coor = lambda text: (abc.index(text[0]), int(text[1:]))
    return list(map(text_to_coor, seats))

class c:
    def __init__(self, size):
        self.dims = tuple(map(int, size.split("x")))
        self.size = self.dims[X] * self.dims[Y]
        self.seats = [[{'name': '', 'plan': ''} for j in range(self.dims[Y])] for i in range(self.dims[X])]

    def taken_seats(self, seat_num, customer_name, customer_type):
        if not (customer_type == 'student' or customer_type == 'full' or customer_type == 'season'):
            pass
        if not '-' in seat_num:
            x,y = (abc.index(seat_num[0]), int(seat_num[1:]) - 1)
            self.seats[x][y] = {'name': customer_name, 'plan': customer_type}
        else:
            seatCoors = make_coor(seat_num)
            for x,y in seatCoors: self.seats[x][y] = {'name': customer_name, 'plan': customer_type}

    def balance(self):
        students, fulls, seasons = 0,0,0
        for seats in self.seats:
            for seat in seats:
                if seat['plan'] == 'student': students += 1
                elif seat['plan'] == 'full': fulls += 1
                elif seat['plan'] == 'season': seasons += 1
        total: int = students * price['student'] + fulls * price['full'] + seasons * price['season']
        balance = f"Sum of students = {students}, Sum of full pay = {fulls}, Sum of season ticket = {seasons}, and Revenues = {total} Dollars\n"
        return balance

    def empty_seats(self, seat_num):
        if not '-' in seat_num:
            x, y = (abc.index(seat_num[0]), int(seat_num[1:]) - 1)
            self.seats[x][y] = {'name': '', 'plan': ''}
        else:
            seat_coors = make_coor(seat_num)
            for x, y in seat_coors: self.seats[x][y] = {'name': '', 'plan': ''}

    def print(self):
        signs = {'': 'X', 'student': 'S', 'full': 'F', 'season': 'T'}
        seats = [[signs[self.seats[i][j]['plan']] for j in range(self.dims[Y])] for i in range(self.dims[X])]
        table = '\n'.join([abc[i] + ' ' + (" " * len(str(self.dims[Y]))).join(list(map(str, line))) for i, line in enumerate(seats)][::-1])
        table += '\n' + ''.join([' ' * (len(str(self.dims[Y])) - len(str(n)) + 1) + str(n) for n in range(self.dims[Y])]) + '\n'
        return table

file = open('output.txt', mode='a')
def createcategory(line):
    name, size = line[1], line[2]
    try:
        condition3 = name[10] in abc #bool
        condition1 = (name[:10] == 'category-1') or (name[:10] == 'category-2') # bool
        condition2 = len(name) == 11 #bool
    except:
        condition1, condition2, condition3 = False, False, False
    if name in category_data.keys():
        file.write(f"Warning: Cannot create the category for the second time. The stadium has already {name}\n")
    elif tuple(map(int, size.split('x')))[0] > 26:
        file.write("Error: Category size exceeds the number of letters in alphabet\n")
    elif not (condition1 and condition2 and condition3):
        file.write(f"Error: Category name needs to be in the format of 'category-(1/2)X', instead given '{name}'\n")
    else:
        category_data.update({name: c(size)})
        file.write(f"The category '{name}' having {category_data[name].size} seats has been created\n")

def category_check(category, category_data, file):
    if category in category_data.keys():
        return True
    file.write(f"Error: The category '{category}' does not exist\n")
    return False

sold_tickets: {str: list} = {} #TODO: str: list olmalı
def selltickets(line):
    name, plan, category = line[1:4]
    seats = line[4:]
    sold_list = []
    for seat in seats:
        if "-" in seat:
            letter = seat[0]
            limits = list(map(int, seat[1:].split("-")))
            seats_in_order = [letter + str(n) for n in range(limits[0], limits[1]+1)]
            if limits[1] > 26:
                file.write(f"Error: The category '{category}' has less column than the specified index {seat}")
            a = 0
            for s in seats_in_order:
                if s in sold_tickets.get(category, " "):
                    a += 1
                else:
                    sold_list.append(s)
            sold_tickets[category] = sold_list
            if a > 0:
                file.write(f"Warning: The seats {seat} cannot be sold to {name} due some of them have already been sold\n")
            else:
                file.write(f"Success: {name} has bought {seat} at {category}\n")
        elif category_check(category, category_data, file):
            sold_list.append(seat)
            category_data[category].taken_seats(seat, name, plan)
            file.write(f"Success: {name} has bought {seat} at {category}\n")
        else:
            file.write(f"Warning: The seats {seat} cannot be sold to {name} due some of them have already been sold")
        sold_tickets[category] = sold_list

def canceltickets(line):
    category = line[1]
    seats = line[2:]
    for seat in seats:
        category_data[category].empty_seats(seat)
        file.write(f"Success: The seat {seat} at {category} has been canceled and now ready to sell again\n")

def balance(line):
    category = line[1]
    title = f"category report of {category}"
    line = "-" * len(title)
    file.write(title + "\n" + line + "\n" + category_data[category].balance())

def showcategory(line):
    category = line[1]
    file.write(f"Printing category layout of {category}\n" + category_data[category].print())

def write():
    file = open('output.txt', mode='w')
    text = read_file(argv[1])
    for line in text:
        try:
            if line[0] == 'CREATECATEGORY':
                createcategory(line)
            elif line[0] == 'SELLTICKET':
                selltickets(line)
            elif line[0] == 'CANCELTICKET':
                canceltickets(line)
            elif line[0] == 'BALANCE':
                balance(line)
            elif line[0] == 'SHOWCATEGORY':
                showcategory(line)
            else:
                pass
        except:
            pass
    file.close()
write()