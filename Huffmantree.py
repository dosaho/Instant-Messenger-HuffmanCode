from operator import itemgetter
import code_book_api

#3 2 1 6 5 2 6 4 3
#num_list = {'a': 3, 'b': 2, 'c': 1, 'd': 6, 'e': 5, 'f': 2, 'g': 6, 'h': 4, 'i': 3}
'''
num_list = code_book_api.get_ch_char_num('total.yaml')
temp_list = code_book_api.get_ch_char_num('total.yaml')
del num_list['all']
new_list = sorted(num_list.iteritems(), key=itemgetter(1))
'''

'''
char_num = code_book_api.get_ch_char_num('total.yaml')
temp_list = code_book_api.get_ch_char_num('total.yaml')
print char_num
temp = {'ch_en': char_num['all']}
char_num.update(temp)
temp_list.update(temp)
char_num['all'] = char_num['all'] + char_num['all']
temp_list['all'] = temp_list['all'] + temp_list['all']
code_book_api.save_data(char_num, 'group_ch.yaml')
'''

char_num = code_book_api.get_ch_char_num('cb_ch_to_code.yaml')
temp_list = code_book_api.get_ch_char_num('char_num.yaml')
#print char_num
#temp = {'en_ch': char_num['all']}
#char_num.update(temp)
#temp_list.update(temp)
#char_num['all'] = char_num['all'] + char_num['all']
#temp_list['all'] = temp_list['all'] + temp_list['all']
#code_book_api.save_data(char_num, 'group_en.yaml')

#del char_num['all']
#new_list = sorted(char_num.iteritems(), key=itemgetter(1))
temp = 0
temp_value = ''
temp_ch = ''
for key in char_num:
    if len(char_num[key]) > temp:
        temp_value = char_num[key]
        temp_ch = key
        temp = len(char_num[key]) 
print temp_ch
print temp_value
print temp_value[0:len(temp_value)]
temp = {temp_ch: temp_value}
char_num.update(temp)



class tree_root(object):

    def __init__(self):
        self.left = None
        self.right = None
        self.char = None
        self.value = None


def build_tree(new_list, current_value=None, current_node=None):
    global temp_id
    while len(new_list) > 0:
        #print new_list
        if len(new_list) == 1:
            return new_list[0][0]
        if type(new_list[0][0]) == tree_root and type(new_list[1][0]) == tree_root:
            node = tree_root()
            node.left = new_list[1][0]
            node.right = new_list[0][0]
        elif type(new_list[0][0]) == tree_root and type(new_list[1][0]) != tree_root:
            node = tree_root()
            node.left = tree_root()
            node.left.char = new_list[1][0]
            node.right = new_list[0][0]
        elif type(new_list[0][0]) != tree_root and type(new_list[1][0]) == tree_root:
            node = tree_root()
            node.left = new_list[1][0]
            node.right = tree_root()
            node.right.char = new_list[0][0]
        else:
            node = tree_root()
            node.left = tree_root()
            node.left.char = new_list[1][0]
            node.right = tree_root()
            node.right.char = new_list[0][0]

        node.value = new_list[0][1] + new_list[1][1]
        new_list = sorted(new_list[2:], key=lambda x: x[1])
        for index in range(len(new_list)):
            if new_list[index][1] == node.value:
                temp_num = index
                break
        new_list.insert(temp_num, (node, node.value))        
        #print new_list


def printHuffTree(huffTree, prefix=''):
    '''
    global cb_ch_to_code
    global cb_code_to_ch
    '''
    global cb_en_to_code
    global cb_code_to_en
    if huffTree.char is not None:
        temp1 = {huffTree.char: prefix}
        temp2 = {prefix: huffTree.char}
        '''
        cb_ch_to_code.update(temp1)
        cb_code_to_ch.update(temp2)
        '''
        cb_en_to_code.update(temp1)
        cb_code_to_en.update(temp2)
    else:
        printHuffTree(huffTree.left, prefix + '0')
        printHuffTree(huffTree.right, prefix + '1')
'''
global cb_ch_to_code
global cb_code_to_ch
cb_ch_to_code = {}
cb_code_to_ch = {}
'''
global cb_en_to_code
global cb_code_to_en
cb_en_to_code = {}
cb_code_to_en = {}


tree = build_tree(new_list)
printHuffTree(tree)

'''
code_book_api.save_data(cb_ch_to_code, 'cb_ch_to_code.yaml')
code_book_api.save_data(cb_code_to_ch, 'cb_code_to_ch.yaml')
code_book_api.cal_code_len(temp_list, cb_ch_to_code)
'''     
code_book_api.save_data(cb_en_to_code, 'cb_en_to_code.yaml')
code_book_api.save_data(cb_code_to_en, 'cb_code_to_en.yaml')
code_book_api.cal_code_len(temp_list, cb_en_to_code)

