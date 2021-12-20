import time
begin = time.time()

import os
import re
from lxml import etree

# Initalisation des variables
founded_words = []
number_regex = r'[0-9]*'
temp = []

EVENT_att = ['eventType', 'polarity', 'contextualModality', 'docTimeRel', 'begin', 'end']
TIMEX3_att = ['timex3Class', 'value', 'begin', 'end']
CLINENTITY_att = ['entityID', 'begin', 'end']
ACTOR_att = ['role', 'begin', 'end']

# Récupération des informations souhaitées
for file in os.listdir(FOLDER):
    name_of_infile = FOLDER + '/' + file
    sentences = {}
    sentences_comp = 1

    tree = etree.parse(name_of_infile)

    ## Récupération des frontières des phrases et décompte des phrases
    for element in tree.xpath('/xmi_XMI/type4_Sentence'):
        attributes = list(element.attrib) # [ID, sofa, start_char, end_char]
        sentences['Sentence_' + str(sentences_comp)] = [element.attrib[x] for x in attributes]
        sentences_comp += 1

    ## Récupération des attributs à vérifier
    EVENT = findAttributes('/xmi_XMI/custom_EVENT', EVENT_att)
    TIMEX3 = findAttributes('/xmi_XMI/custom_TIMEX3', TIMEX3_att)
    CLINENTITY = findAttributes('/xmi_XMI/custom_CLINENTITY', CLINENTITY_att)
    ACTOR = findAttributes('/xmi_XMI/custom_ACTOR', ACTOR_att)

    for element in tree.xpath('/xmi_XMI/cas_Sofa'):
        for word in words_to_find:
            document = element.attrib['sofaString'].lower()

            while word in document: # or word[-1] == "'":
                temp = []

                ### Récupération des frontières des mots
                position_start = document.index(word)
                position_end = position_start + len(word)

                ### Comparaison des frontières des mots à celles des phrases,
                #   afin de déterminer la phrase à laquelle appartient le mot
                for key, value in sentences.items():
                    if position_start >= int(value[2]) and position_end <= int(value[3]):

                        ### Récupération des contextes des mots
                        contexte_g = 20
                        try:
                            while document[position_start-contexte_g] != ' ' and document[position_start-contexte_g] != '\n':
                                contexte_g += 1
                        except IndexError:
                            contexte_g = 0
                        contexte_d = 20
                        try:
                            while document[position_end+contexte_d] != ' ' and document[position_end+contexte_d] != '\n':
                                contexte_d += 1
                        except IndexError:
                            contexte_d = 0

                        temp.append(word)
                        temp.append(file)
                        temp.append(key)
                        temp.append(position_start)
                        temp.append(position_end)
                        temp.append(document[position_start-contexte_g:position_end])
                        temp.append(document[position_start:position_end+contexte_d])
                        temp.append(document[int(value[2]):int(value[3])])

                temp = fillWithAttibutesValues(EVENT, temp, len(temp)+len(EVENT_att), len(EVENT_att))
                temp = fillWithAttibutesValues(TIMEX3, temp, len(temp) + len(TIMEX3_att), len(TIMEX3_att))
                temp = fillWithAttibutesValues(CLINENTITY, temp, len(temp) + len(CLINENTITY_att), len(CLINENTITY_att))
                temp = fillWithAttibutesValues(ACTOR, temp, len(temp) + len(ACTOR_att), len(ACTOR_att))

                document = document.replace(word2, '#'*len(word2), 1) # permet de chercher le mot suivant si plusieurs occurences du même mot dans une phrase
                founded_words.append(temp)

# Ecriture dans un fichier CSV ou affichage des résultats
csv_name = 'Searched_words_result_ALL-EXTENT.csv'
with open(csv_name, 'w', encoding='utf-8') as csv_file:
    csv_file.write('Word\tfile\tSentence_number\tWord_start_position\tWord_end_position\tcontexte_gauche\tcontexte_droit\tSentence\tEVENT_eventType\tEVENT_polarity\tEVENT_contextualModality\tEVENT_docTimeRel\tTIMEX3_timex3Class\tTIMEX3_value\tCLINENTITY_EntityID\tACTOR_role\n')
    for line in founded_words:
        csv_file.write(str(line[0]) + '\t' + str(line[1]) + '\t' + str(line[2]) + '\t' + str(line[3]) + '\t' + str(line[4]) +
        '\t' + str(line[5]).replace('\n','') + '\t' + str(line[6]).replace('\n','') + '\t' + str(line[7]).replace('\n','') +
        '\t' +str(line[8]) + '\t' + str(line[9]) + '\t' + str(line[10]) + '\t' + str(line[11]) + '\t' +
        str(line[12]) + '\t' + str(line[13]) + '\t' +
        str(line[14]) + '\t' + line[15] + '\n')
print('CSV file created as "' + csv_name + '".')

end = time.time()
temps = end-begin
minutes = round((temps / 60),2)
print('Temps d\'execution : '+str(minutes)+' minute.s.')
