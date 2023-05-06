Requirements: -
	1. Python3(I Have used Python 3.10.8)
	2. Java 9(I have used java version "17" 2021-09-14 LTS)
	3. Visual Studio Code or any IDE 

Libraries/Software Required in Python Code: -
	1. PyQt5
		Syntax to install this library:-
			pip install pyQt5
	2. tkinter
		Syntax to install this library:-
			pip install tkinter
	3. graphviz
		Syntax to install this library:-
			pip install graphviz
	4. re(just needed to be imported in the code)
	5. os(just needed to be imported in the code)
	6. sys(just needed to be imported in the code)

Files made to conduct the actions:-
Note :  This file are created in python language and saved in a folder src. This folder indicates it a user definder libraries saved in 		  differnt classes nd can be called by other python programs by imporing them from the src folder.
	  Syntax to import libraies:-
			from src.Java_CFG_IO_Count import *
			from src.Condition_Coverage import *
			from src.Function_Coverage import *

	1. Java_CFG_IO_Count.py: A python file that will count number of lines in the java code then draw a control flow graph for it and save 					 it in a pdf form and open it.
	2. Condition_Coverage.py: A python file that will read the java file then find the conditional statements in it and display its condition and the body in the result part.
	3. Function_Coverage.py: A python file that will read the java file then count number of funtions in it what type of function, called by method and how many times called

Note: This files are imported in main.py file from the src folder.

To run the main file place the files in correct folder while importing mark the folder name and file name you are importing the functions.
Open terminal then run the main.py file writing syntax: python main.py . A GUI Window will apear then browse a java file and run the coverages or actions you want to perform from the option available. 
