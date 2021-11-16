# E3C-Verification

**PYTHON VERSION : Python 3.9.8**

**REQUIREMENT PACKAGES : NONE**

##### EXECUTION ORDER : 

1. _01_fixXML.py_
2. _02_searchInCorpus.py_

:warning: It is important to respect the execution order to make the program work. :warning:

### INPUT : 

###### _01_fixXML.py_
- E3C xml files
	- Type the name of the folder containing the E3C xml files you want to treat at **line 7**.
	- You can modify the name of the folder in _datas_ or modify the name of the folder in the script.
###### _02_searchInCorpus.py_
- Script 1 output
	- Type the name of the folder containing the modified E3C xml files you want to treat at **line 59**.
	- If no modifications has been made in script 1 and if your using Windows, the folder should be the right one.
- Words to search
	- Type the words you want to search separated by an underscore ('_'), if one word only, you can type the word without underscore.
	- The words are requested by the program during its execution, you don't have to put them in a variable.

### FUNCTIONALITIES :

###### _01_fixXML.py_
- Modifying E3C xml files
- Store the modification in a new folder.
###### _02_searchInCorpus.py_
- Searching words choosen by users.
- Searching annotations associated to the founded occurences.
- Writing the results of the search in a csv files.

### OUTPUT

###### _01_fixXML.py_

- New folder named _Underscored_datas_

###### _02_searchInCorpus.py_

csv file containing :
- Word : each founded occurences will appear in this column
- file	 : indicates the file where the occurences has been founded
- Sentence_number : indicates the sentence number where the occurences has been founded
- Word_start_position : indicates the index where founded occurences strats in the file
- Word_end_position	 : indicates the index where founded occurences ends in the file
- contexte_gauche	: indicates what's before the founded occurences
- contexte_droit : indicates what's after the founded occurences
- Sentence : indicates the sentence where the occurences is in. 
- OTHER ANNOTATIONS FROM THE XML FILE : 
	- EVENT_eventType
	- EVENT_polarity
	- EVENT_contextualModality
	- EVENT_docTimeRel
	- TIMEX3_timex3Class
	- TIMEX3_value
	- CLINENTITY_EntityID
	- ACTOR_role
