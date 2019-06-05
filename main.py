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

Window.size = (1280, 768) # uncomment on windows

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = '192.168.0.17'  # get local machine name
port = 1234

try:
    print('starting host.')
   # sock.connect((host, port))  # uncomment on raspberry pi
except Exception as e:
    print(e)

#conn = sqlite3.connect('/home/sysop/pos/order.db')  # uncomment on raspberry pi

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


def donut_que(data):
    try:
        sock.send(data.encode('utf-8'))
    except Exception as ex:
        print(ex)
    time.sleep(1)


def pos_print(order=None):
    if order is None:
        order = []
    try:
        epson = Network("192.168.1.100")
        epson.image("rosie.png")
        epson.set(font='a', height=3, width=3, align='center')
        for m in order:
            epson.text(str(m[3]) + '\n')
            epson.set(font='a', height=1, width=1, align='left', text_type='u2')
            epson.text('Order 1 \n')
            epson.set(text_type='normal')
            epson.text(str(m[0]))
            epson.text(' Cups \n')
        epson.qr('hiddenempire.ca', size=8)
        epson.cut()
    except Exception as ex:
        print(ex)


'''
def for_printer(big_list=None):
    if big_list is None:
        big_list = []
    try:
        epson = Network("192.168.1.100")
        epson.image("mrsbot.png")
        price = 0.0
        bar = '1234'
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
        #donut quantity
        self.donut_quantity = 0
        self.donut_price = 4.76
        #hide the total display
        self.hide_widgets([self.ids.order_title,self.ids.order1S,self.ids.order1SZP,self.ids.pops1,self.ids.pop_price1,self.ids.pops2,self.ids.pop_price2,self.ids.pops3,self.ids.pop_price3,self.ids.pops4,self.ids.pop_price4,self.ids.total_title,self.ids.gst_title,self.ids.Gst1,self.ids.Cash1])
        #self.display_widget(self.ids.star,1280,600)
        #self.display_widget(self.ids.start_label, 200, 200)

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
        #self.ids.soup4.pos = 5500, 470
        #self.ids.soup1.pos = 5500, 320
        #self.ids.soup2.pos = 5500, 170
        #self.ids.soup3.pos = 5500, 20
        #self.ids.drink.pos = 1100, 3000
        #self.ids.pop1.pos = 500, 3000
        #self.ids.pop2.pos = 700, 3000
        #self.ids.pop3.pos = 900, 3000
        #self.ids.pop4.pos = 1100, 3000
        #self.ids.done.pos = 550, 3000

        #single method to hide any number of widgets
        #self.hide_widgets([self.ids.soup4,self.ids.soup1,self.ids.soup2,self.ids.soup3,self.ids.drink,self.ids.pop1,self.ids.pop2,self.ids.pop3,self.ids.pop4,self.ids.done])
        self.donut_quantity = 0
        self.ids.donut_price.text = "$0"
        self.ids.quantity_label.text = "0"
        self.hide_widgets([self.ids.donut_price_title, self.ids.donut_price, self.ids.quantity_label, self.ids.donut_minus,self.ids.donut_plus,self.ids.donut_image,self.ids.donut_bag, self.ids.drink, self.ids.pop1,self.ids.pop2, self.ids.pop3, self.ids.pop4, self.ids.done,self.ids.next_button])

    def set_num(self):
        self.key_num = data_test()

    def starts(self):
        #self.ids.star.pos = 5500, 150
        #self.ids.soup1.pos = 500, 360
        #self.ids.soup2.pos = 900, 360
        #self.ids.soup3.pos = 500, 20
        #self.ids.soup4.pos = 900, 20
        #contain all donut positioning within this function
        #self.display_donuts()
        self.display_donuts_new()
        self.ids.new.pos = -50, -60
        self.ids.drink.pos = 1077, -60
        self.num[3] = self.key_num
        #Method to hide start Button
        self.hide_widgets([self.ids.star,self.ids.start_label])

    def soup(self, x):

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

        self.num[0] = int(x)
        #self.ids.soup4.pos = 5500, 470
        #self.ids.soup1.pos = 5500, 320
        #self.ids.soup2.pos = 5500, 170
        #self.ids.soup3.pos = 5500, 20
        #self.ids.drink.pos = 1100, 3000

        #single function to hide all widgets
        self.hide_widgets([self.ids.soup4,self.ids.soup1,self.ids.soup2,self.ids.soup3,self.ids.drink])
        # move in the pop.
        #self.ids.pop1.pos = 500, 300
        #self.ids.pop2.pos = 700, 300
        #self.ids.pop3.pos = 900, 300
        #self.ids.pop4.pos = 1100, 300

        #single function to display pop widgets
        self.display_pop()
        self.ids.done.pos = 550, 50
        # cash math
        self.gst = self.cash * .05
        #get 2 decimal points
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
            #self.ids.pop1.pos = 500, 3000
            #self.ids.pop2.pos = 700, 3000
            #self.ids.pop3.pos = 900, 3000
            #self.ids.pop4.pos = 1100, 3000
            #self.ids.done.pos = 550, 3000
            self.ids.pay.pos = 550, 400
            #single method widget hide
            self.hide_widgets([self.ids.pop1,self.ids.pop2,self.ids.pop3,self.ids.pop4,self.ids.done])

    def pops(self):
        self.ids.pop1.pos = 500, 3000
        self.ids.pop2.pos = 700, 3000
        self.ids.pop3.pos = 900, 3000
        self.ids.pop4.pos = 1100, 3000
        self.ids.done.pos = 550, 3000
        self.ids.pay.pos = 550, 400

    def pay(self):
        self.m = 3
        if self.start_time:
            Clock.schedule_interval(self.update, 1)
            self.start_time = False

    def update(self, _):
        if self.m == 3:
            self.payed()
            self.m = 6

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
        m = '$m'
        n = 1
        for x in self.order:
            data_entry(x[0], x[1], x[2], x[3], x[4])
            n = x[3]
            y = str(x)
            y = y.strip('[]')
            print(y)
            m += y[0]
            print(n)
        m += '\n'
        donut_que(str(m))
        #pos_print(self.order)
        self.pop_name = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.num = [0, 0, 0, 0, 0]
        self.pop_index = 0
        del self.order[:]
        self.clear_it()
        self.ids.star.pos = 550, 150

    def next(self):
        #self.ids.pay.pos = 900, 3000
        #self.ids.new.pos = 900, 3000
        del self.order[:]
        self.num = [0, 0, 0, 0, 0]
        self.pop_name = [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ']
        self.pop_index = 0
        self.drink_num = 1000
        self.clear_it()
        #commented out for testing
        #App.get_running_app().stop()
        #self.ids.star.pos = 550, 150
        self.ids.star.pos = 0,0
        self.ids.start_label.pos = 600,300
        #single method display
        self.hide_widgets([self.ids.pay,self.ids.new])

    #### test stuff positioning widgets within functions
    #help with readability and hopefully make changes in the future easier
    #display new donut ui
    def display_donuts_new(self):
        self.ids.donut_minus.pos = 50,200
        self.ids.donut_plus.pos = 900,200
        self.ids.quantity_label.pos = 585,315
        self.ids.donut_price_title.pos = 530,120
        self.ids.donut_price.pos = 640,120
        self.ids.donut_image.pos = 420,135
        self.ids.donut_bag.pos = 420,350
        self.ids.next_button.pos = 505,-60

    #use this to display original donuts ui
    def display_donuts(self):
        self.ids.soup1.pos = 500, 360
        self.ids.soup2.pos = 900, 360
        self.ids.soup3.pos = 500, 20
        self.ids.soup4.pos = 900, 20

    # use this to display pop
    def display_pop(self):
        self.ids.pop1.pos = 500, 300
        self.ids.pop2.pos = 700, 300
        self.ids.pop3.pos = 900, 300
        self.ids.pop4.pos = 1100, 300
        self.ids.done.pos = 550, 50

    def display_pop_new(self):
        print("next")

    #pass widgets you want to hide, will set them out of the window, accepts array of widgets
    def hide_widgets(self,widgets):
        for widget in widgets:
            #print(widget)
            widget.pos = (3000, 3000)
        #widget.pos = 900, 3000
        #widget.disabled = True

    #functions for plus and minus donuts
    def minus_donuts(self):
        #print("minus donut",self.ids.donut_price.color)
        if self.donut_quantity > 0:
            self.donut_quantity -= 1
            string_quantity = str(self.donut_quantity)
            rounded_price = math.ceil(self.donut_price * self.donut_quantity * 100) /100
            string_price = "$" + str(rounded_price)
            #self.ids.quantity_label.color = [0,0,0,1]
            #self.ids.donut_price.color = [0,0,0,1]
            self.ids.donut_price.text = string_price
            self.ids.quantity_label.text = string_quantity

    def plus_donuts(self):
        #print("plus donut",self.ids.donut_price.color)
        if self.donut_quantity < 4:
            self.donut_quantity += 1
            string_quantity = str(self.donut_quantity)
            rounded_price = math.ceil(self.donut_price * self.donut_quantity * 100) / 100
            string_price = "$" + str(rounded_price)
            #self.ids.quantity_label.color = [0,0,0,1]
            #self.ids.donut_price.color = [0,0,0,1]
            self.ids.donut_price.text = string_price
            self.ids.quantity_label.text = string_quantity

create_table()


class PosApp(App):

    def build(self):
        return Pos()


if __name__ == '__main__':
    PosApp().run()
