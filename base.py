# -*- coding: utf-8 -*-
"""
Created on Tue Aug  2 20:13:55 2022

@author: Amrut
"""

import re











obj_types = [
    'btn',
    'label',
    'txedit',
    'radio',
    'lineEdit',
    'layoutwdiget',
    'splitter',
    'checkbox'

    ]










resize_factor = 7/8

ignoreList = [
    'setTabOrder',
    'sizePolicy',
    'setObjectName',
    'setTabShape',
    'setCentralWidget',
    'setWindowOpacity',
    'def',
    'retranslateUi',
    'def',
    'class',
    'setEnabled',
    'QFont',
    'QCoreApplication',
    'connect',
    'setBuddy',
    'setContentsMargins',
    'font',
    # 'setText',  -- cuz it ignores setText_translate
    'QWidget(MainWindow)',
    'HTML'

    ]

ignore_at_end_list = [
    'setText'



    ]


main_window_property = [0,0,0,0]
tab = '    '




def get_all (string):
    if '=' not in string:
        is_assignmnt = False
        # str2 = string
        str2_1 = ''
    else:
        is_assignmnt = True
        str2 , str2_1 = string.split('=')
        str2_1= re.split(' |\.|\(',str2_1.strip())

    if '(' not in string:
        has_argument = False
        arg = ''
    else:
        has_argument = True
        arg = string[string.rfind("(")+1:string.find(")")]
    a = re.split(' |\.',string)
    return has_argument, arg, [is_assignmnt, str2_1 ], a



tab= "    "

first_str = """
import dearpygui.dearpygui as dpg
import sys
dpg.create_context()


with dpg.window(tag="mainWindow", pos=(0, 0), no_resize = False) as win1:
"""

last_str =  """
with dpg.theme() as global_theme:
    with dpg.theme_component(dpg.mvAll):
        dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (255, 230, 196), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (255, 255, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Text, (0, 0, 0), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_PopupBg, (255, 255, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Border, (141,139,139), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (255, 255, 255), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarBg, (192, 179, 197), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ScrollbarGrab, (137, 129, 129), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Button, (208, 208, 220), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_ButtonHovered, (179, 208, 138), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_Tab, (196, 196, 196), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_BorderShadow, (168, 161, 161), category=dpg.mvThemeCat_Core)
        dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (0,0,0), category=dpg.mvThemeCat_Core)
        
        dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 7, category=dpg.mvThemeCat_Core)
        dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1, category=dpg.mvThemeCat_Core)
dpg.bind_item_theme(win1, global_theme)

def clean_up():
    retention_list = ['retention_list', 'this', 'obj_dict','layout','','']
    this = sys.modules[__name__]
    for n in dir():
        if n not in retention_list:  delattr(this, n)
    del this, retention_list, n
def gui_kick_off():
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("mainWindow", True)
    dpg.start_dearpygui()
    dpg.stop_dearpygui()
    dpg.destroy_context()

if __name__ == '__main__':
    gui_kick_off()
    # clean_up()
"""


needs = """


    dpg.add_text("Hello, world")
    dpg.add_button(label="Save")
    dpg.add_input_text(label="string", default_value="Quick brown fox")
    dpg.add_slider_float(label="float", default_value=0.273, max_value=1)
"""
"""

dpg.create_viewport(title='MainWindow', width=694, height=633)


"""

   # if a[0] == 'MainWindow':
   #     if 'resize' in line:
   #         main_window_property [1:3] = list(map(int, arg.split(',')))
   #     if 'setWindowTitle' in line:
   #         tmp_str = arg.split(',')[-1]
   #         tmp_str = (tmp_str.strip()).replace('"','')
   #         main_window_property [0] = tmp_str
   #=========================================================


