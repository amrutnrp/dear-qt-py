# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 20:54:18 2022

@author: Amrut
"""

from base import *

f = open('reduced', 'r')
fw = open('unprocessed','w')


obj_dict = {}
layout = {}

for line in f:
    has_argument, arg, is_assignmnt, a = get_all(line)
    process = False
    
    if has_argument== True and arg== "MainWindow":
        process = True 
        # print (line)
        continue
    if is_assignmnt [0] == True and is_assignmnt[1][0] == 'QtWidgets':
        # print (is_assignmnt[1],)
        process = True
        if is_assignmnt[1][1] == 'QPushButton':
            obj_dict [ a[1] ] = ['btn']
        elif is_assignmnt[1][1] == 'QTextEdit':
            obj_dict [ a[1] ] = ['txedit']
        elif is_assignmnt[1][1] == 'QLabel':
            obj_dict [ a[1] ] = ['label']
        elif is_assignmnt[1][1] == 'QRadioButton':
            obj_dict [ a[1] ] = ['radiobtn']
        elif is_assignmnt[1][1] == 'QLineEdit':
            obj_dict [ a[1] ] = ['lineEdit']
        elif is_assignmnt[1][1] == 'QWidget':
            obj_dict [ a[1] ] = ['layoutwdiget']
        elif is_assignmnt[1][1] =='QVBoxLayout':
            layout [a[1]] = ['V']
        elif is_assignmnt[1][1] =='QHBoxLayout':
            layout [a[1]] = ['H']
        else:
            # print (is_assignmnt[1] )
            process = False
            
    if  '_translate' in line:
        obj_dict [a[1]] .append(arg.split(',')[-1])
        # print (a)
        process = True
    if 'setGeometry' in line:
        # print (line)
        obj_dict [a[1]] .append(arg)
        process = True


    if 'addWidget' in line:
        item = arg.split('.')[-1]
        # print (arg.split('.')[-1])
        layout [a[1]]  .append(item )
        obj_dict[item] .append([ 1, a[1] ] )
        process = True
    if 'addLayout' in line:
        item = arg.split('.')[-1]
        layout [a[1]]  .append(item )
        layout[item] .append([ 1, a[1] ] )
        process = True
        
        
    
        

        
    if not process :
        fw.write(line)
        
        
     
 
    



f.close()
fw.close()  