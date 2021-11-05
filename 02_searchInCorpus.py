import time
begin = time.time()

import os
from lxml import etree

FOLDER = 'Underscored_datas'

words_to_find = str(input('Mots à chercher ? [si plusieurs, séparer par un underscore "_"]')).lower().split('_')
for x in range(0, len(words_to_find)):
    if "'" in words_to_find[x]:
        words_to_find.append(words_to_find[x].replace("'", ' '))
    if "-" in words_to_find[x]:
        words_to_find.append(words_to_find[x].replace("-", ' '))
    if " " in words_to_find[x]:
        words_to_find.append(words_to_find[x].replace(" ", '-'))
print('Les mots à chercher sont :', words_to_find)

csv = input('Sortie csv ? [y] ou [n]').lower()
csv = True if csv == 'y' else False


founded_words = []

for file in os.listdir(FOLDER):
    name_of_infile = FOLDER + '/' + file
    sentences = {}
    sentences_comp = 1

    tree = etree.parse(name_of_infile)

    for element in tree.xpath('/xmi_XMI/type4_Sentence'):
        attributes = list(element.attrib)
        # [ID, sofa, start_char, end_char]
        sentences['Sentence_' + str(sentences_comp)] = [element.attrib[x] for x in attributes]
        sentences_comp += 1


    for element in tree.xpath('/xmi_XMI/cas_Sofa'):
        for word in words_to_find:
            document = element.attrib['sofaString'].lower()

            word_compt = 1

            while word + ' ' in document:

                position_start = document.index(word + ' ')
                position_end = position_start + len(word)

                for key, value in sentences.items():
                    if position_start >= int(value[2]) and position_end <= int(value[3]):
                        contexte_g = 20
                        try:
                            while document[position_start-contexte_g] != ' ' and document[position_start-contexte_g] != '\n':
                                 contexte_g += 1
                        except IndexError:
                            contexte_g = 0
                        contexte_d = 20
                        try:
                            while document[position_start+contexte_d] != ' ' and document[position_start-contexte_d] != '\n':
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

                document = document.replace(word + ' ', '#'*len(word) + ' ', 1)



if csv == True:
    csv_name = 'Searched_words_result_' + str(words_to_find).replace('\'','').replace('\\','').replace(' ','').replace('"', '') + '.csv'
    with open(csv_name, 'w', encoding='utf-8') as csv_file:
        csv_file.write('Word\tfile\tSentence_number\tWord_start_position\tWord_end_position\tcontexte_gauche\tcontexte_droit\tSentence\n')
        for line in founded_words:
            csv_file.write(str(line[0]) + '\t' + str(line[1]) + '\t' + str(line[2]) +
            '\t' + str(line[3]) + '\t' + str(line[4]) + '\t' + str(line[5]) +  '\t' + str(line[6]) + '\t' + str(line[7]) +  '\n')
    print('CSV file created as "' + csv_name + '".')
else:
    for line in founded_words:
        print(line)


end = time.time()
temps = end-begin
minutes = round((temps / 60),2)
print('Temps d\'execution : '+str(minutes)+' minute.s.')
