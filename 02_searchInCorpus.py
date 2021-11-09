import time
begin = time.time()

import os
import re
from lxml import etree

FOLDER = 'Underscored_datas'


words_to_find = str(input('Mots à chercher ? [si plusieurs, séparer par un underscore "_"]')).lower().split('_')

# gestion des différentes orthographes à rechercher

def extendResearch(input_list, element_to_search, replacement_element):
    for x in range(0, len(input_list)):
        if element_to_search in input_list[x]:
            to_append = input_list[x].replace(element_to_search, replacement_element)
            if to_append not in input_list:
                input_list.append(to_append)
    return input_list

replacement = {
                '-': ' ',
                ' ': '-',
                "'": ('e', 'u')
                }

for element_to_replace, replacement_element in replacement.items():
    if element_to_replace != "'":
        words_to_find = extendResearch(words_to_find, element_to_replace, replacement_element)
    else:
        for x in replacement_element:
            words_to_find = extendResearch(words_to_find, element_to_replace, x)

print('Les mots à chercher sont :', words_to_find)

csv = input('Sortie csv ? [y] ou [n]').lower()
csv = True if csv == 'y' or csv == '[y]' else False


founded_words = []
number_regex = r'[0-9]*'

for file in os.listdir(FOLDER):
    name_of_infile = FOLDER + '/' + file
    sentences = {}
    sentences_comp = 1

    tree = etree.parse(name_of_infile)

    # Récupération des frontières des phrases et décompte des phrases
    for element in tree.xpath('/xmi_XMI/type4_Sentence'):
        attributes = list(element.attrib) # [ID, sofa, start_char, end_char]
        sentences['Sentence_' + str(sentences_comp)] = [element.attrib[x] for x in attributes]
        sentences_comp += 1


    for element in tree.xpath('/xmi_XMI/cas_Sofa'):
        for word in words_to_find:
            document = element.attrib['sofaString'].lower()

            word_compt = 1



            while word + ' ' in document:

                # Récupération des frontières des mots
                position_start = document.index(word + ' ')
                position_end = position_start + len(word)

                # Comparaison des frontières des mots à celles des phrases, afin de déterminer la phrase à laquelle appartient le mot
                for key, value in sentences.items():
                    if position_start >= int(value[2]) and position_end <= int(value[3]):

                        # Récupération des contextes des mots
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

                        founded_words.append([word,
                        file,
                        key,
                        position_start,
                        position_end,
                        document[position_start-contexte_g:position_end],
                        document[position_start:position_end+contexte_d],
                        document[int(value[2]):int(value[3])]])
                word_compt += 1

                document = document.replace(word + ' ', '#'*len(word) + ' ', 1) # permet de chercher le mot suivant si plusieurs occurences du même mot dans une phrase



# Ecriture dans un fichier CSV ou affichage des résultats
if csv == True:
    csv_name = 'Searched_words_result_' + str(words_to_find).replace('\'','').replace('\\','').replace(' ','-').replace('"', '') + '.txt'
    with open(csv_name, 'w', encoding='utf-8') as csv_file:
        csv_file.write('Word\tfile\tSentence_number\tWord_start_position\tWord_end_position\tcontexte_gauche\tcontexte_droit\tSentence\n')
        for line in founded_words:
            if '\n' in line[5] or '\n' in line[6]:
                csv_file.write(str(line[0]) + '\t' + str(line[1]) + '\t' + str(line[2]) +
                '\t' + str(line[3]) + '\t' + str(line[4]) + '\t' + str('Refer to sentence') +  '\t' +
                str('Refer to sentence') + '\t' + str(line[7]) +  '\n')
            else:
                csv_file.write(str(line[0]) + '\t' + str(line[1]) + '\t' + str(line[2]) +
                '\t' + str(line[3]) + '\t' + str(line[4]) + '\t' + str(line[5]) +  '\t' +
                str(line[6]) + '\t' + str(line[7]) +  '\n')
    print('CSV file created as "' + csv_name + '".')
else:
    for line in founded_words:
        print(line)


end = time.time()
temps = end-begin
minutes = round((temps / 60),2)
print('Temps d\'execution : '+str(minutes)+' minute.s.')
