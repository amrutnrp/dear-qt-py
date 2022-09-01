# dear-qt-py
 
 
 This tool/script converts the GUI Layout of a auto-generated pyqt file.
 
 Step 1-  Open "qt5-tools designer" and define UI.  
 Step 2- save it to .ui file (xml format)   
 Step 3-  Open cmd prompt and run :"pyuic5 -x RUN 1.ui -o RUN1.py" , so that the GUI is saved into a .py file   
 Step 4-  Run the qt2dearpygui.py script and give RUN1.py file as argment  
 Step 5-  Inspect the 'reduced' file to see which lines got missed. Run 'results.py' output to ensure that GUI is as expected.  
 Step 6-  Modify the parameters as you wish. and enjoy it with a cup of coffee :D  
 

	
This script is kinda incomplete (i.e running for few widgets only). Help expand it's feature set by contributing to this project!
