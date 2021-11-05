import time
begin = time.time()

import os
from lxml import etree

FOLDER = 'Underscored_datas'

words_to_find = str(input('Mots à chercher ? [si plusieurs, séparer par un underscore "_"]')).lower().split('_')
print('Les mots à chercher sont :', words_to_find)

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
                        print(word_compt, word, key)
                word_compt += 1

                document = document.replace(word + ' ', '#'*len(word) + ' ', 1)

                #print(word, file)


    break

# Il faut une liste de mots à rechercher et
# partir de cette liste pour faire un t in s et
# extraire les coordonnées des mots trouvés (document, sentence, start_char, end_char)

end = time.time()
temps = end-begin
minutes = round((temps / 60),2)
print('Temps d\'execution : '+str(minutes)+' minute.s.')
