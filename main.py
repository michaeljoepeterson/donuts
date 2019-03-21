import sqlite3
import socket
import time
import random
import math
from escpos.printer import Network
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.clock import Clock

Window.size = (1280, 768)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '192.168.1.21'  # get local machine name
port = 12345

try:
    print('starting host.')
    # sock.connect((host, port))  # uncomment on raspberry pi
except Exception as e:
    print(e)

# conn = sqlite3.connect('/home/sysop/bot/order.db')  # uncomment on raspberry pi

conn = sqlite3.connect('order.db')  # uncomment on windows

c = conn.cursor()

drinks = ['None', 'Pepsi', 'Mountain Dew', 'Root Beer', '7 Up', 'coffee', 'decaff']


def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS donut(donutID int, drink int, topping int, orderNUM int,'
              ' pay int)')


def data_entry(a1, b1, c1, d1, e1):
    c.execute("INSERT INTO donut(donutID, drink, topping, orderNUM, pay) VALUES(?, ?, ?, ?, ?)",
              (a1, b1, c1, d1, e1))
    conn.commit()


def data_test():
    while True:
        a1 = random.randrange(1000, 9999)
        c.execute("SELECT * FROM donut WHERE orderNUM=:a1", {"a1": str(a1)})
        data = c.fetchall()
        if not data:
            return a1
        else:
            print('looking....')


def send_ticket(data):
    try:
        sock.send(data.encode('utf-8'))
    except Exception as ex:
        print(ex)
    time.sleep(1)
#the functions I added for the for loop again check them my assumption was that after index you only did anything different when m[6] == 1 so then all the other ones could be handled by the same function I also noticed you are basically doing the same thing in each if/else statement so just put it outside the if else and did a check there
#I also am passing the epson class to the function hoping that the changes it makes will affect the changes to the instance of the class, that might be my JS showing, if it doesn't work like that let me know or modify it
def big_list_func_1(order_part,printer,num):
    f = None
    d = str(drinks[int(order_part[3])]) + '     $1.90 \n'
    if int(order_part[0]) > 0:
        f = soup_print(order_part[1])
    printer.set(font='a', height=3, width=3, align='center')
    printer.text(str(order_part[5]) + '\n')      
    printer.set(font='a', height=1, width=1, align='left', text_type='u2')
    #Use the num passed for the order number instead
    printer.text('Order ' + str(num) + '\n')
    printer.set(text_type='normal')
    #I think this is how single line if statements work in python
    if f != None: printer.text(f)
    printer.text(d)

def big_list_func_2(order_part,printer,num):
    f = None
    d = 'A ' + str(drinks[int(order_part[3])]) + ' to drink  $1.90 \n'
    if int(order_part[0]) > 0:
        f = soup_print(order_part[1])

    printer.set(font='a', height=1, width=1, align='left', text_type='u2')
    printer.text('Order ' + str(num) + '\n')
    printer.set(text_type='normal')
    if f != None: printer.text(f)
    printer.text(d)

def for_printer(big_list=None):
    if big_list is None:
        big_list = []
    try:
        epson = Network("192.168.1.100")
        epson.image("mrsbot.png")
        price = 0.0
        bar = '1234'
        '''
        I am guessing it is what tells the printer of the POS what to put on the receipt 
        You should definitely check these changes since this for loop is more complicated than the other things I changed and I can't run the program locally
        I am also assuming there are 4 columns? I hope other wise it will run more than 4 times
        '''
        for m in big_list:
            counter = 0
            if int(m[6]) == 1:
                big_list_func_1(m,epson,int(m[6]))
                #placed this here to not mess with later print functions
                if int(m[0]) > 0:
                    if m[1] == 1:
                        price = 4.76
                    if m[1] == 2:
                        price = 7.62
                    bar = m[5]
            elif int(m[6]) > 1:
                big_list_func_2(m,epson,int(m[6]))
        '''
        for m in big_list:
            if int(m[6]) == 1:
                if int(m[0]) > 0:
                    f = soup_print(m[1])
                    d = str(drinks[int(m[3])]) + '     $1.90 \n'
                    if m[1] == 1:
                        price = 4.76
                    if m[1] == 2:
                        price = 7.62
                    epson.set(font='a', height=3, width=3, align='center')
                    epson.text(str(m[5]) + '\n')
                    bar = m[5]
                    epson.set(font='a', height=1, width=1, align='left', text_type='u2')
                    epson.text('Order 1 \n')
                    epson.set(text_type='normal')
                    epson.text(f)
                    epson.text(d)
                else:
                    d = str(drinks[int(m[3])]) + '     $1.90 \n'
                    epson.set(font='a', height=3, width=3, align='center')
                    epson.text(str(m[5]) + '\n')
                    epson.set(font='a', height=1, width=1, align='left', text_type='u2')
                    epson.text('Order 1 \n')
                    epson.set(text_type='normal')
                    epson.text(d)
                print(d)
            if int(m[6]) == 2:
                if int(m[0]) > 0:
                    f = soup_print(m[1])
                    d = 'A ' + str(drinks[int(m[3])]) + ' to drink  $1.90 \n'
                    epson.set(font='a', height=1, width=1, align='left', text_type='u2')
                    epson.text('Order 2 \n')
                    epson.set(text_type='normal')
                    epson.text(f)
                    epson.text(d)
                else:
                    d = 'A ' + str(drinks[int(m[3])]) + ' to drink  $1.90 \n'
                    epson.set(font='a', height=1, width=1, align='left', text_type='u2')
                    epson.text('Order 2 \n')
                    epson.set(text_type='normal')
                    epson.text(d)
                print(d)
            if int(m[6]) == 3:
                if int(m[0]) > 0:
                    f = soup_print(m[1])
                    d = 'A ' + str(drinks[int(m[3])]) + ' to drink  $1.90 \n'
                    epson.set(font='a', height=1, width=1, align='left', text_type='u2')
                    epson.text('Order 3 \n')
                    epson.set(text_type='normal')
                    epson.text(f)
                    epson.text(d)
                else:
                    d = 'A ' + str(drinks[int(m[3])]) + ' to drink  $1.90 \n'
                    epson.set(font='a', height=1, width=1, align='left', text_type='u2')
                    epson.text('Order 3 \n')
                    epson.set(text_type='normal')
                    epson.text(d)
                print(d)
            if int(m[6]) == 4:
                if int(m[0]) > 0:
                    f = soup_print(m[1])
                    d = 'A ' + str(drinks[int(m[3])]) + ' to drink  $1.90 \n'
                    epson.set(font='a', height=1, width=1, align='left', text_type='u2')
                    epson.text('Order 4 \n')
                    epson.set(text_type='normal')
                    epson.text(f)
                    epson.text(d)
                else:
                    d = 'A ' + str(drinks[int(m[3])]) + ' to drink  $1.90 \n'
                    epson.set(font='a', height=1, width=1, align='left', text_type='u2')
                    epson.text('Order 4 \n')
                    epson.set(text_type='normal')
                    epson.text(d)
                print(d)
        '''
        epson.text('Total : ')
        epson.text(str(price) + '\n')
        epson.barcode(bar, 'EAN13', 64, 2, '', '')
        # epson.set(font='a', align='center')
        # epson.qr('hiddenempire.ca', size=8)
        epson.cut()
    except Exception as ex:
        print(ex)


def soup_print(size):
    soup_string = ''
    #Replace if statements with a dictionary to reduce number of if statements slightly increasing speed and increasing readiability
    soup_string_components_begin = {
        1:'Cup of ',
        2:'Bowl of ',
    }
    soup_string_components_end = {
        1:'     $4.76',
        2:'     $7.62',
    }

    soup_string = soup_string_components_begin[size] + soup_string_components_end[size] + '\n'

    return soup_string
    '''
    if size == 1:
        soup_string = 'Cup of '
    if size == 2:
        soup_string = 'Bowl of '
    if size == 1:
        soup_string += '     $4.76'
    if size == 2:
        soup_string += '     $7.62'
    soup_string += '\n'
    return soup_string
    '''


class Pos(Widget):

    def __init__(self, **kwargs):
        super(Pos, self).__init__(**kwargs)
        self.cash = 0.00
        self.gst = 0.00
        self.key_num = 0
        self.drink_num = 1000
        self.pop_index = 0
        self.m = 0
        self.start_time = True
        self.pop_name = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.num = [0, 0, 0, 0, 0]
        self.order = []

    def clear_it(self):
        self.cash = 0.00
        self.gst = 0.00
        self.ids.Gst1.text = '$0.00'
        self.ids.Cash1.text = '$0.00'
        self.ids.order1S.text = ''
        self.ids.order1SZP.text = ''
        self.ids.pops1.text = ''
        self.ids.pop_price1.text = ''
        self.ids.pops2.text = ''
        self.ids.pop_price2.text = ''
        self.ids.pops3.text = ''
        self.ids.pop_price3.text = ''
        self.ids.pops4.text = ''
        self.ids.pop_price4.text = ''
        self.ids.soup4.pos = 5500, 470
        self.ids.soup1.pos = 5500, 320
        self.ids.soup2.pos = 5500, 170
        self.ids.soup3.pos = 5500, 20
        self.ids.drink.pos = 1100, 3000
        self.ids.pop1.pos = 500, 3000
        self.ids.pop2.pos = 700, 3000
        self.ids.pop3.pos = 900, 3000
        self.ids.pop4.pos = 1100, 3000
        self.ids.done.pos = 550, 3000

    def set_num(self):
        self.key_num = data_test()

    def starts(self):
        self.ids.star.pos = 5500, 150
        self.ids.soup1.pos = 500, 360
        self.ids.soup2.pos = 900, 360
        self.ids.soup3.pos = 500, 20
        self.ids.soup4.pos = 900, 20
        self.ids.new.pos = 40, -10
        self.ids.drink.pos = 200, -10
        self.num[3] = self.key_num

    def soup(self, x):
        #rounded the price for one donut not sure if that will affect any math you have to do, can always change the price back. Cut back on the long if else statement
        donutStringDict = {
            "1":{
                donutText:'1 Bag of donuts',
                price:4.76
            },
            "2":{
                donutText:'2 Bags of donuts',
                price:9.52
            },
            "3":{
                donutText:'3 Bags of donuts',
                price:14.28
            },
            "4":{
                donutText:'4 Bags of donuts',
                price:19.04
            }
        }
        self.ids.order1S.text = donutStringDict[x].donutText
        self.ids.order1SZP.text = '$' + str(donutStringDict[x].price)
        self.cash += donutStringDict[x].price
        '''
        if x == '1':
            self.ids.order1S.text = '1 Bag of donuts'
            self.ids.order1SZP.text = '$4.76'
            self.cash += 4.7619
        if x == '2':
            self.ids.order1S.text = '2 Bags of donuts'
            self.ids.order1SZP.text = '$9.52'
            self.cash += 9.52
        if x == '3':
            self.ids.order1S.text = '3 Bags of donuts'
            self.ids.order1SZP.text = '$14.28'
            self.cash += 14.28
        if x == '4':
            self.ids.order1S.text = '4 Bags of donuts'
            self.ids.order1SZP.text = '$19.04'
            self.cash += 19.04
        '''
        self.num[0] = int(x)
        self.ids.soup4.pos = 5500, 470
        self.ids.soup1.pos = 5500, 320
        self.ids.soup2.pos = 5500, 170
        self.ids.soup3.pos = 5500, 20
        self.ids.drink.pos = 1100, 3000
        self.ids.pop1.pos = 500, 300
        self.ids.pop2.pos = 700, 300
        self.ids.pop3.pos = 900, 300
        self.ids.pop4.pos = 1100, 300
        self.ids.done.pos = 550, 50
        # cash math
        self.gst = self.cash * .05
        sg = math.ceil(self.gst * 100) / 100
        sub = '$' + str(sg)
        self.ids.Gst1.text = sub
        tot1 = self.cash + self.gst
        tot2 = math.ceil(tot1 * 100) / 100
        tots = '$' + str(tot2) + '0'
        self.ids.Cash1.text = tots

    def sizes(self, x):
        pass

    def side(self, x):
        pass

    def pop(self, x):
        #not exactly sure what drink num is but captured it here could further optimize by changing price to variable that is = to 1.90. I put the price here just in case you ever need different prices for the pop
        popStringDict = {
            "1":{
                popText:'Pepsi',
                price:1.90,
                drinkNum:1
            },
            "2":{
                popText:'7up',
                price:1.90,
                drinkNum:10
            },
            "3":{
                popText:'Root Beer',
                price:1.90,
                drinkNum:100
            },
            "4":{
                popText:'Mountain Dew',
                price:1.90,
                drinkNum:1000
            }
        }
        self.pop_name[self.pop_index] = popStringDict[x].popText
        self.pop_name[self.pop_index + 4] = '$' + str(popStringDict[x].price)
        self.drink_num += popStringDict[x].drinkNum

        '''
        if x == '1':
            self.pop_name[self.pop_index] = 'Pepsi'
            self.pop_name[self.pop_index + 4] = '$1.90'
            self.drink_num += 1
        if x == '2':
            self.pop_name[self.pop_index] = '7up'
            self.pop_name[self.pop_index + 4] = '$1.90'
            self.drink_num += 10
        if x == '3':
            self.pop_name[self.pop_index] = 'Root Beer'
            self.pop_name[self.pop_index + 4] = '$1.90'
            self.drink_num += 100
        if x == '4':
            self.pop_name[self.pop_index] = 'Mountain Dew'
            self.pop_name[self.pop_index + 4] = '$1.90'
            self.drink_num += 1000
        '''
        self.ids.pops1.text = self.pop_name[0]
        self.ids.pop_price1.text = self.pop_name[4]
        self.ids.pops2.text = self.pop_name[1]
        self.ids.pop_price2.text = self.pop_name[5]
        self.ids.pops3.text = self.pop_name[2]
        self.ids.pop_price3.text = self.pop_name[6]
        self.ids.pops4.text = self.pop_name[3]
        self.ids.pop_price4.text = self.pop_name[7]
        self.pop_index += 1
        # end pop display
        self.num[1] = int(self.drink_num)
        self.num[4] = 0
        self.num[3] = self.key_num
        self.cash += 1.9047
        self.gst = self.cash * .05
        sg = math.ceil(self.gst * 100) / 100
        sub = '$' + str(sg)
        self.ids.Gst1.text = sub
        tot1 = self.cash + self.gst
        tot2 = math.ceil(tot1 * 100) / 100
        tots = '$' + str(tot2) + '0'
        self.ids.Cash1.text = tots
        if self.pop_index > 3:
            self.ids.pop1.pos = 500, 3000
            self.ids.pop2.pos = 700, 3000
            self.ids.pop3.pos = 900, 3000
            self.ids.pop4.pos = 1100, 3000
            self.ids.done.pos = 550, 3000
            self.ids.pay.pos = 550, 400

    def pops(self):
        self.ids.pop1.pos = 500, 3000
        self.ids.pop2.pos = 700, 3000
        self.ids.pop3.pos = 900, 3000
        self.ids.pop4.pos = 1100, 3000
        self.ids.done.pos = 550, 3000
        self.ids.pay.pos = 550, 400

    def pay(self):
        self.m = 0
        if self.start_time:
            Clock.schedule_interval(self.update, 1)
            self.start_time = False

    def update(self, dt):
        print(dt)
        if self.m == 3:
            self.payed()
            # Clock.unschedule(self.update)
            self.m = 6
        elif self.m < 3:
            self.m += 1

    def payed(self):
        self.ids.pay.pos = 900, 3000
        self.ids.new.pos = 900, 3000
        self.num[4] = 1
        self.order.append(self.num)
        self.drink_num = 1000
        self.cash = 0.00
        self.gst = 0.00
        self.ids.Gst1.text = '$0.00'
        self.ids.Cash1.text = '$0.00'
        # for_printer(self.order)
        for x in self.order:
            data_entry(x[0], x[1], x[2], x[3], x[4])
            print(x)
        self.pop_name = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.num = [0, 0, 0, 0, 0]
        self.pop_index = 0
        del self.order[:]
        self.clear_it()
        self.ids.star.pos = 550, 150

    def next(self):
        self.ids.pay.pos = 900, 3000
        self.ids.new.pos = 900, 3000
        del self.order[:]
        self.num = [0, 0, 0, 0, 0]
        self.pop_name = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.pop_index = 0
        self.drink_num = 1000
        self.clear_it()
        self.ids.star.pos = 550, 150


create_table()


class PosApp(App):

    def build(self):
        return Pos()


if __name__ == '__main__':
    PosApp().run()
