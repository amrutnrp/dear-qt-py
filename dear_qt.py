# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 19:58:01 2022

@author: Amrut

This script converts a GUI script from PyQt to dearpygui

"""
import sys
from base import *



if len(sys.argv) == 1:
    h= input ('No argument found, using the example file.. press enter')
    f= open('example_Qt-files/UI_6.py','r')
else:
    input_py = sys.argv[1]
    f= open(input_py,'r')
    
fw = open ('result.py', 'w')
fw.write(first_str)


f_reduce = open('reduced','w')
fsm = 0
continue_flag =  False

obj_dict = {}
layout_dict = {}
layout_widget_dict = {}

for line in f:
    line = line.strip()
    if 'if' in line:
        break
    if 'class' in line:
        fsm = 1
    if fsm == 0:
        continue
    continue_flag =  False
    for i in ignoreList:
        if i in line:
            continue_flag =  True
            break
    if continue_flag == True: continue
    if len(line) < 2:   continue
    if line[0][0] == '#' or line[0][0] == '\'' or  line[0][0] == '\"' :  continue

    has_argument, arg, is_assignmnt, a = get_all(line)



    if a[0] == 'MainWindow':
        if 'resize' in line:
            main_window_property [1:3] = list(map(int, arg.split(',')))
        if 'setWindowTitle' in line:
            tmp_str = arg.split(',')[-1]
            tmp_str = (tmp_str.strip()).replace('"','')
            main_window_property [0] = tmp_str
        continue
    a_valid_type = True
    #=========================================================
    if is_assignmnt [0] == True and is_assignmnt[1][0] == 'QtWidgets':
        if is_assignmnt[1][1] == 'QPushButton':
            obj_dict [ a[1] ] = [obj_types[0]]
        elif is_assignmnt[1][1] == 'QTextEdit':
            obj_dict [ a[1] ] = [obj_types[2]]
        elif is_assignmnt[1][1] == 'QLabel':
            obj_dict [ a[1] ] = [obj_types[1]]
        elif is_assignmnt[1][1] == 'QRadioButton':
            obj_dict [ a[1] ] = [obj_types[3]]
        elif is_assignmnt[1][1] == 'QLineEdit':
            obj_dict [ a[1] ] = [obj_types[4]]
        elif is_assignmnt[1][1] == 'QWidget':
            layout_dict [ a[1] ] = [obj_types[5]]
            layout_widget_dict [a[1] ]=[]
        elif is_assignmnt[1][1] =='QVBoxLayout':
            layout_dict [a[1]] = ['V']
        elif is_assignmnt[1][1] =='QHBoxLayout':
            layout_dict [a[1]] = ['H']
        elif is_assignmnt[1][1] =='QSplitter':
            # obj_dict [ a[1] ] = [obj_types[6]]
            layout_dict [a[1]] = ['H']
            layout_widget_dict [a[1]] = [a[1]+ '_group']
            layout_dict [a[1]  + '_group'] = ['H']
        else:
            pass  # print (is_assignmnt[1] )
            a_valid_type = False
        if arg == '' or arg == 'self.centralwidget':
            pass
        elif a_valid_type:
            layout_widget_dict [ arg.split('.')[-1] ] .append(a[1])

            if 'ayout' not in line:
                print (line, '?')
                layout_dict [arg.split('.')[-1] + '_group'] .append( a[1] )
        else:
            f_reduce.write(line+ '\n')
            continue


    elif  '_translate' in line:
        obj_dict [a[1]] .append(arg.split(',')[-1])
    elif 'setGeometry' in line:
        if (a[1] in obj_dict):
            obj_dict [a[1]] .append(arg)
        elif (a[1] in layout_dict):
            layout_dict [a[1]] .append(arg)
    elif 'addWidget' in line:
        item = arg.split('.')[-1]       ;     layout_dict [a[1]]  .append(item )     ;        obj_dict[item] .append([ 1, a[1] ] )
    elif 'addLayout' in line:
        item = arg.split('.')[-1]       ;    layout_dict [a[1]]  .append(item )      ;        layout_dict[item] .append([ 1, a[1] ] )
    else:
        continue_flag =  False
        for i in ignore_at_end_list:
            if i in line:
                continue_flag =  True
                break
        if continue_flag == True: continue
        f_reduce.write(line+ '\n')


#=====================      compile done
#                           now dump the data



var_str = {}

varS =  ''
var_i = ''
label_flag = False


for i in obj_dict:# i being the keys
    var_i = ''
    geo_param = ''
    after_line_add = ''
    object_type_i = -1
    label_flag = False
    if obj_dict [i][0] == obj_types [0]: # btn
        var_i  =  '{} = dpg.add_button(tag= \'{}\'' .format(i,i)
        object_type_i = 0
    elif obj_dict [i][0] == obj_types [1]: # label
        var_i  =  '{} = dpg.add_text(tag= \'{}\'' .format(i,i)
        label_flag = True
        object_type_i = 1
    elif obj_dict [i][0] == obj_types [2]: # textEdit
        var_i  =  '{} = dpg.add_input_text(tag= \'{}\',multiline= True' .format(i, i)
        # after_line_add = ': {} = dpg.add_text( default_value="Default string", tag="{}"  )' .format(i, i)
        object_type_i = 2
    elif obj_dict [i][0] == obj_types [3]: # radio button
        var_i  =  '{} = dpg.add_checkbox(tag= \'{}\'' .format(i,i)
        object_type_i = 3
    elif obj_dict [i][0] == obj_types [4]: # lineEdit
        var_i  =  '{} = dpg.add_input_text(tag= \'{}\'' .format(i,i)
        object_type_i = 4
    # elif obj_dict [i][0] == obj_types [5]: #  layoutwdiget
    #     # var_i  =  '{} = dpg.add_text(tag= \'{}\'' .format(i,i)
    #     object_type_i = 5




    label_found_flag = False
    for j in obj_dict [i][1:]:
        if type(j) == list:
            continue
        if type(j) == str:
            if not (any(k.isalpha() for k in j) ):  # all are numbers -> coordinates
                x,y,w,h = j.split(',')
                x,y,w,h = int (x), int (y), int (w), int (h)
                x,y,w,h = int (x*resize_factor), int(y*resize_factor), int(w*resize_factor), int (h * resize_factor)
                if label_flag:
                    geo_param= ',pos=({}, {}) '.format(x,y)
                else:
                    geo_param = ',pos=({}, {}), width={}, height={} '.format(x,y,w,h)
            else: # label
                if label_flag:
                    var_i = var_i + ', default_value = {}' .format( j )
                else:
                    var_i = var_i + ',label={}' .format( j )
                label_found_flag = True

    if object_type_i == -1 or  (object_type_i == 1 and label_found_flag == False):
        print ('skipped - '+i)
        var_str [i]  = '\n'
        continue

    var_i = var_i +geo_param
    # print (var_i)
    #varS =  varS + '\t'+var_i + ')\n'
    # print (var_i, "========", i)
    var_str [i] =var_i + ')'+ after_line_add+'\n'

# print (varS)

num_of_tabs = 1
flags_obj = dict(obj_dict)
flags_obj = flags_obj.fromkeys(flags_obj, False)





def check_down_the_line (item):
    global stack_of_widgets, stack_of_parents
    # print (layout_dict [item] )
    children = layout_dict [item][1:]
    # print (item, children)
    for child in children:
        if type(child) == list:
            continue
        elif child in obj_dict:
            if child in stack_of_widgets:
                stack_of_widgets.remove(child)
            else:
                print (child+' doesn\'t exist in '+item)
                stack_of_parents.remove(child)
        elif child in layout_dict :
            check_down_the_line(child)
        else:
            print ('Couldn\'t check ' , child)



for i in layout_widget_dict:
    stack_of_widgets =[]
    stack_of_parents = []
    for j in layout_widget_dict[i]:
        if j not in layout_dict: # that means it's a widget
            stack_of_widgets.append(j)
        else:
            stack_of_parents.append(j)

    for j in stack_of_parents:
        # print ('passsing', j)
        pass
        check_down_the_line (j)



    # print (stack_of_widgets, stack_of_parents)
    # layout_dict [ide  =     layout_dict [i]  +  stack_of_widgets + stack_of_parents
    if len(stack_of_widgets) != 0 or len(stack_of_parents) != 1:
        print ('Something wrong')
        print (stack_of_widgets, stack_of_parents)

    layout_dict[stack_of_parents [0] ].append( layout_dict [i] [1] )

    del layout_dict [i]








def add_if_indent(item):
    global varS, num_of_tabs  , flags_obj
    # print (item)
    temp_var_s = ''
    varS = varS + tab*num_of_tabs+"with dpg.group(horizontal={}".format(layout_dict[item][0] == "H")

    for j in  layout_dict [item][1:]:
        if type(j) == list:
            continue
        if not (any(k.isalpha() for k in j) ): # number+comma
            x,y,w,h = j.split(',')
            x,y,w,h = int (x), int (y), int (w), int (h)
            x,y,w,h = int (x*resize_factor), int(y*resize_factor), int(w*resize_factor), int (h * resize_factor)
            varS = varS + ',pos=({}, {})'.format(x,y)
            if ('group' in item) :
                varS = varS + ',width = {}'.format(w)

    varS = varS + '):\n'

    num_of_tabs = num_of_tabs +1
    for j in  layout_dict [item][1:]:
        if type(j) == list:
            continue
        elif j in layout_dict:
            add_if_indent (j)
        elif j in obj_dict:
            varS = varS + tab*num_of_tabs + var_str[j]
            flags_obj [j] = True




    num_of_tabs = num_of_tabs -1




for i in layout_dict:
    if any( type(k) == list for k in layout_dict[i]):
        continue
    add_if_indent(i)
for i in flags_obj:
    if flags_obj[i] == False:
        varS = varS + tab*num_of_tabs + var_str[i]

















print ('Done')





# fw.write(needs)
fw.write(varS)

for i in main_window_property[0:3]:
    if i == 0:
        print ('Error - parameters not found for main window ')
        sys.exit()



fw.write ('\n')
fw.write("dpg.create_viewport(title='{}', width={}, height={})\n".format(main_window_property[0],int (main_window_property[1]* resize_factor), int(main_window_property[2]*resize_factor)))
f_reduce.close()
fw.write(last_str)
f.close()

fw.close()


# retention_list = ['retention_list', 'this', 'obj_dict','layout_dict','','']
# this = sys.modules[__name__]
# for n in dir():
#     if n not in retention_list:  delattr(this, n)
# del this, retention_list, n
