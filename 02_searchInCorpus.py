import time
begin = time.time()

import os
import re
from lxml import etree

def extendResearch(input_list, element_to_search, replacement_element):
    for x in range(0, len(input_list)):
        if element_to_search in input_list[x]:
            to_append = input_list[x].replace(element_to_search, replacement_element)
            if to_append not in input_list:
                input_list.append(to_append)
    return input_list

def findAttributes(path, attributes_to_find):
    """
    :param path: str - chemin du xml qui donne l'accès aux attributs recherchés
    :param attributes_to_find: list - Nom des attributs à récupérer
    :return: dict key = xmi_id ; value = [attributes_values]
    """
    result = {}
    for element in tree.xpath(path):
        attributes = []
        key = list(element.attrib)[0]
        key = element.attrib[key]
        result[key] = attributes

        for attribute in attributes_to_find:
            try:
                attributes.append(element.attrib[attribute])
            except KeyError:
                attributes.append('NO_'+ attribute + '_ATTRIBUTE')

    return result

def fillWithAttibutesValues(attributes_list, storage_variable, storage_variable_new_len, annotation_quantity):
    """
    :param attributes_values: dict - key : xmid | value : [attributes_values] (generated by findAttributes function)
    :param storage_variable: list - Temp variable (already containing resaerched word informations)
    :param storage_variable_new_len: int - (len(storage_variable) + len(attributes_list[0]))
    :param annotation_quantity: int - length of _att list
    :return: list - Temp with attributes values when possible or "No_annotation" Value
    """
    for key, value in attributes_list.items():
        if position_start == int(value[-2]) and position_end == int(value[-1]):
            for x in value:
                temp.append(x)
    if len(temp) != storage_variable_new_len:
        for x in range(0, annotation_quantity-2):
            temp.append('No_annotation')
    else:
        # suppression des éléments ajoutés à la liste des attributs à chercher pour le repérage
        del temp[-1] # end
        del temp[-1] # begin

    return storage_variable

FOLDER = 'Underscored_datas'

# Récupération des requêtes de l'user
words_to_find = str(input('Mots à chercher ? [si plusieurs, séparer par un underscore "_"]')).lower().split('_')

    ## gestion des différentes orthographes à rechercher
replacement = {
                '-': ' ',
                ' ': '-',
                "'": ('e', 'u')
                }

for element_to_replace, replacement_element in replacement.items():
    if element_to_replace != "'":
        words_to_find = extendResearch(words_to_find, element_to_replace, replacement_element + ' ')
    else:
        for x in replacement_element:
            words_to_find = extendResearch(words_to_find, element_to_replace, x)

print('Les mots à chercher sont :', words_to_find)

    ## sortie d'un csv ou non
csv = input('Sortie csv ? [y] ou [n]').lower()
csv = True if csv == 'y' or csv == '[y]' else False


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

            if re.search("[0-9]+", word):
                word = re.sub("([0-9]+)","[0-9]+",word)

            while re.search(r""+word, document):
            #while word in document: # or word[-1] == "'":
                temp = []

                word2 = re.findall(r""+word, document)[0]

                ### Récupération des frontières des mots
                position_start = document.index(word2)
                position_end = position_start + len(word2)

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

                        temp.append(word2)
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
if csv == True:
    csv_name = 'Searched_words_result_' + str(words_to_find).replace('\'','').replace('\\','').replace(' ','-').replace('"', '') + '.csv'
    with open(csv_name, 'w', encoding='utf-8') as csv_file:
        csv_file.write('Word\tfile\tSentence_number\tWord_start_position\tWord_end_position\tcontexte_gauche\tcontexte_droit\tSentence\tEVENT_eventType\tEVENT_polarity\tEVENT_contextualModality\tEVENT_docTimeRel\tTIMEX3_timex3Class\tTIMEX3_value\tCLINENTITY_EntityID\tACTOR_role\n')
        for line in founded_words:
            csv_file.write(str(line[0]) + '\t' + str(line[1]) + '\t' + str(line[2]) + '\t' + str(line[3]) + '\t' + str(line[4]) +
            '\t' + str(line[5]).replace('\n','') + '\t' + str(line[6]).replace('\n','') + '\t' + str(line[7]).replace('\n','') +
            '\t' +str(line[8]) + '\t' + str(line[9]) + '\t' + str(line[10]) + '\t' + str(line[11]) + '\t' +
            str(line[12]) + '\t' + str(line[13]) + '\t' +
            str(line[14]) + '\t' + line[15] + '\n')
    print('CSV file created as "' + csv_name + '".')
else:
    for line in founded_words:
        print(line)

end = time.time()
temps = end-begin
minutes = round((temps / 60),2)
print('Temps d\'execution : '+str(minutes)+' minute.s.')
