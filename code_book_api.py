# -*- coding: UTF-8 -*-

import yaml
import codecs
from operator import itemgetter


def get_en_char_num():
    try:
        get_num_data = file('char_num.yaml')

    except:
        get_num_data = None

    if get_num_data is None:
        #create new number table
        print 'create number table'
        temp_num = 32
        char_num = {}
        for j in range(0, 95):
            temp = {chr(temp_num): 0}
            char_num.update(temp)
            temp_num = temp_num + 1
        temp = {'all': 0}
        char_num.update(temp)
    else:
        char_num = yaml.load(get_num_data)
        get_num_data.close()
    return char_num


def get_ch_char_num(text):
    try:
        get_num_data = file(text)

    except:
        get_num_data = None

    if get_num_data is None:
        char_num = {}
        temp = {'all': 0}
        char_num.update(temp)
    else:
        char_num = yaml.load(get_num_data)
        get_num_data.close()
    return char_num


def updata_char_num(char_num, string):
    for i in range(0, len(string)):
        if string[i] != '\n' and string[i] != '\r':
            char_num[string[i]] = char_num[string[i]] + 1
            char_num['all'] = char_num['all'] + 1


def save_data(char_num, text):
    put_data = file(text, 'w')
    yaml.dump(char_num, put_data, default_flow_style=True)
    put_data.close()


def get_code_book(char_num):
    code_book = {}
    temp_num = 0
    for key, value in sorted(char_num.iteritems(), key=itemgetter(1), reverse=True):
        #print key, value
        if key != 'all':
            temp = {key: '1'*temp_num + '0'}
            print key, value, temp
            code_book.update(temp)
            temp_num = temp_num + 1
    return code_book


def cal_code_len(char_num, code_book):
    temp_num = 0
    code_len = 0.0
    print type(code_len)
    for key, value in sorted(char_num.iteritems(), key=itemgetter(1), reverse=True):
        ratio = float(value)/float(char_num['all'])
        #print key, value, ratio
        if key != 'all':
            code_len = code_len + ratio * len(code_book[key])
            #print code_len
            temp_num = temp_num + 1
    print code_len


def import_novel(char_num, text='novel'):
    f = file(text)
    while True:
        string = f.readline()
        #print len(i)
        print string, len(string)
        if len(string) == 0:
            break
        updata_char_num(char_num, string)
    f.close()


def import_ch_novel(temp_char_num, text):
    f = codecs.open(text, 'r', 'utf-8')
    while True:
        i = f.readline()
        #print i.encode('utf-8')
        if len(i) == 0:
            break
        for k in i:
            if ord(k) > 255:
                temp_exist = k.encode('utf-8') in temp_char_num
                if temp_exist is False:
                    temp = {k.encode('utf-8'): 1}
                    temp_char_num['all'] += 1
                    temp_char_num.update(temp)
                else:
                    temp_char_num[k.encode('utf-8')] = temp_char_num[k.encode('utf-8')] + 1
                    temp_char_num['all'] += 1
                #print k.encode('utf-8')
    f.close()
    print temp_char_num['西']
    print temp_char_num['all']
    return temp_char_num
