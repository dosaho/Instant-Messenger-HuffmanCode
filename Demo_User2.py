# -*- coding: UTF-8 -*-
from Tkinter import *
import pika
import yaml
import thread

rabbitmq_host = 'localhost'
User = 'Demo_User2'
To_User = 'Demo_User1'


class mywidgets:
    def __init__(self, root):
        self.get_code_book()
        thread.start_new_thread(self.receive_thread,())
        frame = Frame(root)
        frame.pack()
        self.txtfr(frame)
        self.inputfr(frame)
        return

    def txtfr(self, frame):

        #define a new frame and put a text area in it
        textfr = Frame(frame)

        self.text = Text(textfr, height=25, width=90, background='gray', font=("Purisa", 16))
        # put a scroll bar in the frame
        scroll = Scrollbar(textfr)
        self.text.configure(yscrollcommand=scroll.set, bd=1)

        #pack everything
        self.text.pack(side=LEFT)
        scroll.pack(side=RIGHT,fill=Y)
        textfr.pack(side=TOP)
        self.text.tag_config("wel", foreground="purple")
        self.text.insert(END, 'Welcome !!!!   ' + User+'\n\n', 'wel')
        self.text.config(state=DISABLED)
        

    def comp_s(self, event):
        
        message = self.InputFiled.get()
        self.text.config(state=NORMAL)
        
        if ord(message[0])>255:
            msg_code = self.cb_en_to_code['en_ch']
        else:
            msg_code = ''

        temp_size = 0
        dict_remove_en = {}
        dict_add_en = {}
        dict_remove_de = {}
        dict_add_de = {}
        for i in range(0, len(message)):
            if i != 0:
                if ord(message[i])>255 and ord(message[i-1])<=255:
                    msg_code = msg_code + self.cb_en_to_code['en_ch']
                elif ord(message[i])<=255 and ord(message[i-1])>255:
                    msg_code = msg_code + self.cb_ch_to_code['ch_en']
            if ord(message[i])<=255:
                msg_code = msg_code + self.cb_en_to_code[message[i]]
                temp_size = temp_size + 1
                #self.text.insert(END, '(' + self.cb_en_to_code[message[i]] + ')\n')
            else:
                temp_exist = message[i].encode('UTF-8') in self.cb_ch_to_code
                if temp_exist is True:
                    msg_code = msg_code + self.cb_ch_to_code[message[i].encode('UTF-8')]
                else:
                    self.text.tag_config("new", foreground="yellow")
                    self.text.insert(END, 'New World!!!!!!!!!!'  + '\n', "new")
                    temp = 0
                    temp_value = ''
                    temp_ch = ''
                    for key in self.cb_ch_to_code:
                        if len(self.cb_ch_to_code[key]) > temp:
                            temp_value = self.cb_ch_to_code[key]
                            temp_ch = key
                            temp = len(self.cb_ch_to_code[key])
                    
                    dict_remove_en = {temp_ch: temp_value}
                    dict_add_en = {temp_ch: temp_value+'1', message[i].encode('UTF-8'): temp_value+'0'}
                    dict_remove_de = {temp_value: temp_ch}
                    dict_add_de = {temp_value+'1': temp_ch, temp_value+'0': message[i].encode('UTF-8')}
                    for key in dict_remove_en:
                        print key
                        if key in self.cb_ch_to_code:
                            del self.cb_ch_to_code[key]
                    for key in dict_add_en:
                        print key
                        self.cb_ch_to_code.update({key:dict_add_en[key]})
                    for key in dict_remove_de:
                        print key
                        if key in self.cb_code_to_ch:
                            del self.cb_code_to_ch[key]
                    for key in dict_add_de:
                        print key
                        self.cb_code_to_ch.update({key:dict_add_de[key]})
                    msg_code = msg_code + self.cb_ch_to_code[message[i].encode('UTF-8')]
                temp_size = temp_size + 2
                #self.text.insert(END, '(' + self.cb_ch_to_code[message[i].encode('UTF-8')] + ')\n')

        self.text.tag_config("rate", foreground="red")
        self.text.insert(END, User + ' : ' + message + '\n')
        self.text.insert(END, '(' + msg_code + ')\n\n')
        self.text.insert(END, 'size(byte) :' + str(temp_size) + '(' + str(len(message)) + ')' +'  bits :' + str(len(msg_code)) +'\n')
        ratio = (float(temp_size*8)-float(len(msg_code)))/float(temp_size*8) * 100
        self.text.insert(END, 'Space Saving: '+ str(ratio)+ '\n\n', 'rate')
        #self.text.insert(END, message + '\n', 'success')
        self.text.config(state=DISABLED)
        self.InputFiled.delete(0, END)
        msg = {'from_user': User, 'to_user': To_User, 'msg': msg_code, 'remove_en': dict_remove_en, 'add_en': dict_add_en, 'remove_de': dict_remove_de, 'add_de': dict_add_de}
        self.send_msg_to_server(msg)

    def inputfr(self, frame):
        inputfr = Frame(frame)
        self.InputFiled = Entry(inputfr)
        self.button = Button(inputfr, text='Send', command=self.send_message)
        self.InputFiled.configure(bg='white', fg='blue', bd=2)
        self.button.config(bg='black', fg='black', bd=1)
        self.InputFiled.pack(side=LEFT, ipadx=180, ipady=10)
        self.button.pack(side=RIGHT, fill=BOTH, expand=5, ipady=10)
        inputfr.pack(side=LEFT)
        self.InputFiled.bind('<Return>', self.comp_s)

    def send_message(self):
        message = self.InputFiled.get()
        self.text.config(state=NORMAL)
        self.text.tag_config("success", foreground="red")
        self.text.insert(END, User + ' : ' + message + '\n')
        
        #self.text.insert(END, message + '\n', 'success')
        self.text.config(state=DISABLED)
        self.InputFiled.delete(0, END)
        msg = {'from_user': User, 'to_user': 'Demo_User2', 'msg': message}
        self.send_msg_to_server(msg)

    def send_msg_to_server(self, msg):
        self.conn_param = pika.ConnectionParameters(host=rabbitmq_host)
        self.connection = pika.BlockingConnection(self.conn_param)
        self.channel = self.connection.channel()
        string = msg['msg']
        msg1 = {'from_user': msg['from_user'], 'to_user': msg['to_user'], 'msg': string[0:len(string)/2], 'server': 'A', 'remove_en': msg['remove_en'], 'add_en': msg['add_en'], 'remove_de': msg['remove_de'], 'add_de': msg['add_de']}
        msg2 = {'from_user': msg['from_user'], 'to_user': msg['to_user'], 'msg': string[len(string)/2:], 'server': 'B', 'remove_en': msg['remove_en'], 'add_en': msg['add_en'], 'remove_de': msg['remove_de'], 'add_de': msg['add_de']}
        temp_string = ''
        for i in range(0, len(string[0:len(string)/2])):
            if msg1['msg'][i] == msg2['msg'][i]:
                temp_string = temp_string + '0'
            else:
                temp_string = temp_string + '1'
        if len(msg2['msg']) > len(msg1['msg']):
            print 'Odd length'
            temp_string = temp_string + msg2['msg'][len(msg2['msg'])-1] + '1'
        else:
            temp_string = temp_string + '0'
        msg3 = {'from_user': msg['from_user'], 'to_user': msg['to_user'], 'msg': temp_string, 'server': 'A+B', 'remove_en': msg['remove_en'], 'add_en': msg['add_en'], 'remove_de': msg['remove_de'], 'add_de': msg['add_de']}
        msg1 = yaml.dump(msg1)
        self.channel.basic_publish(exchange='server', routing_key='A', body=msg1)
        msg2 = yaml.dump(msg2)
        self.channel.basic_publish(exchange='server', routing_key='B', body=msg2)
        msg3 = yaml.dump(msg3)
        self.channel.basic_publish(exchange='server', routing_key='A+B', body=msg3)
        print 'Done'        

    def get_code_book(self):
        temp = file('cb_en_to_code.yaml')
        self.cb_en_to_code = yaml.load(temp)
        temp = file('cb_code_to_en.yaml')
        self.cb_code_to_en = yaml.load(temp)
        temp = file('cb_ch_to_code.yaml')
        self.cb_ch_to_code = yaml.load(temp)
        temp = file('cb_code_to_ch.yaml')
        self.cb_code_to_ch = yaml.load(temp)

    def receive_thread(self):
        self.conn_param = pika.ConnectionParameters(host=rabbitmq_host)
        self.connection = pika.BlockingConnection(self.conn_param)
        self.channel = self.connection.channel()
        self.channel.exchange_declare(exchange=User, type='direct')
        print User
        self.channel.queue_declare(queue=User)
        self.channel.queue_bind(exchange=User, queue=User, routing_key=User)
        self.channel.basic_consume(self.print_msg, queue=User, no_ack=True)
        self.channel.start_consuming()

    def print_msg(self, channel, method, header, body):
        all_data = yaml.load(body)
        print all_data
        dict_remove_en = all_data['remove_en']
        dict_add_en = all_data['add_en']
        dict_remove_de = all_data['remove_de']
        dict_add_de = all_data['add_de']
        for key in dict_remove_en:
            print key
            if key in self.cb_ch_to_code:
                del self.cb_ch_to_code[key]
        for key in dict_add_en:
            print key
            self.cb_ch_to_code.update({key:dict_add_en[key]})
        for key in dict_remove_de:
            print key
            if key in self.cb_code_to_ch:
                del self.cb_code_to_ch[key]
        for key in dict_add_de:
            print key
            self.cb_code_to_ch.update({key:dict_add_de[key]})
    
        global message_pool
        global receive_flag
        temp_exist = all_data['server'] in message_pool
        if temp_exist is True:
            receive_flag = 0
            message_pool = {}
            return
        temp = {all_data['server']: all_data['msg']}
        message_pool.update(temp)
        if all_data['server'] == 'A' or all_data['server'] == 'B':
            receive_flag = receive_flag + 1
            
        elif all_data['server'] == 'A+B':
            if receive_flag !=2:
                receive_flag = 3
            else:
                receive_flag = 4

        if receive_flag == 4:
            receive_flag = 0
            self.post_text(message_pool['A'] + message_pool['B'], all_data)
            message_pool = {}

        elif receive_flag == 3:
            receive_flag = 0
            temp_exist = 'A' in message_pool
            temp_string = ''
            if temp_exist is False:
                exist_server = 'B'
            else:
                exist_server = 'A'
            if message_pool['A+B'][len(message_pool['A+B'])-1] == '1':
                temp_length = len(message_pool['A+B'])-2
            else:
                temp_length = len(message_pool['A+B'])-1
            for i in range(0, temp_length):
                if message_pool['A+B'][i] == '0':
                    temp_string = temp_string + message_pool[exist_server][i]
                else:
                    if message_pool[exist_server][i] == '1':
                        temp_string = temp_string + '0'
                    else:
                        temp_string = temp_string + '1'
            if temp_exist is True and message_pool['A+B'][len(message_pool['A+B'])-1] == '1':
                temp_string = temp_string + message_pool['A+B'][len(message_pool['A+B'])-2]

            if temp_exist is False:
                self.post_text(temp_string + message_pool['B'], all_data)
                message_pool = {}

            else:
                self.post_text(message_pool['A'] + temp_string, all_data)
                message_pool = {}



        
        

    def post_text(self, message, all_data):
        from_message = ''
        temp = ''
        lan_flag = 0
        for i in range(0, len(message)):
            temp = temp + message[i]
            if lan_flag == 0:
                temp_exist = temp in self.cb_code_to_en
            else:
                temp_exist = temp in self.cb_code_to_ch
            
            if temp_exist is True:
                if lan_flag == 0:
                    if self.cb_code_to_en[temp] == 'en_ch':
                        lan_flag = 1
                    else:
                        from_message = from_message + self.cb_code_to_en[temp]
                else:
                    if self.cb_code_to_ch[temp] == 'ch_en':
                        lan_flag = 0
                    else:
                        from_message = from_message + self.cb_code_to_ch[temp]
                temp = ''
        self.text.config(state=NORMAL)
        self.text.tag_config("success", foreground="red")
        self.text.tag_config("success1", foreground="blue")
        self.text.insert(END, all_data['from_user'] + ' : ' + message + '\n', "success1")
        self.text.insert(END, all_data['from_user'] + ' : ' + from_message+ '\n\n', "success")
        self.text.config(state=DISABLED)


def main():
    global receive_flag
    receive_flag = 0
    global message_pool
    message_pool = {}
    root = Tk()
    s=mywidgets(root)
    root.title(User)
    root.mainloop()
main()