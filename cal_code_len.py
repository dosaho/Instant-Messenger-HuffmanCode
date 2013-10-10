import yaml
from operator import itemgetter

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

temp_num = 0
code_len = 0.0
test = 0.0
print type(code_len)
for key, value in sorted(char_num.iteritems(), key=itemgetter(1), reverse=True):
    ratio = float(value)/float(char_num['all'])
    print key, value, ratio
    if key != 'all':
        temp = {key: '1'*temp_num + '0'}
        #print temp, temp_num + 1
        code_len = code_len + ratio * (temp_num + 1)
        test = test + ratio
        #print code_len
        temp_num = temp_num + 1
print code_len
print test
