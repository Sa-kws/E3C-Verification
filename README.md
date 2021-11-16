# E3C-Verification

**PYTHON VERSION : Python 3.9.8**

**REQUIREMENT PACKAGES : NONE**

##### EXECUTION ORDER : 

1. _01_fixXML.py_
2. _02_searchInCorpus.py_

:warning: It is important to respect the execution order to make the program work. :warning:

### INPUT : 

- Script 01 : 
	- E3C xml files
		- Type the name of the folder containing the E3C xml files you want to treat at **line 7**. \\
- Script 02 : 
	- Script 1 output
		- Type the name of the folder containing the modified E3C xml files you want to treat at **line 59**.
		- If no modifications has been made in sript 1 and if your using Windows, the folder should be the right one.
	- Words to search
		- Type the words you want to search separated by an underscore ('_'), if one word only, you can type the word without underscore.
		- The words are requested by the program during its execution, you don't have to put them in a variable.

### FUNCTIONALITIES :

- Script 01
	- Modifying E3C xml files
	- Store the modification in a new folder. \\
- Script 02 : 
	- Searching words choosen by users.
	- Searching annotations associated to the founded occurences.
	- Writing the results of the search in a csv files.

### OUTPUT
