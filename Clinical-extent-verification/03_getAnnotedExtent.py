import time
begin = time.time()

from lxml import etree
import os

CLINENTITY_path = '/xmi_XMI/custom_CLINENTITY'
document_path = '/xmi_XMI/cas_Sofa'
sentence_path = '/xmi_XMI/type4_Sentence'
FOLDER = 'Underscored_datas'
CLINENTITY_extent = {}
dictionnary_index = 0
CLINENTITY_extent_repartition = {}
words_code = {}



for file in os.listdir(FOLDER):
    name_of_infile = FOLDER + "/" + file

    tree = etree.parse(name_of_infile)

    for element in tree.xpath(document_path):
        document = element.attrib['sofaString']

    for element in tree.xpath(CLINENTITY_path):
        dictionnary_index += 1
        try:
            words_code[element.attrib['entityID']] = document[int(element.attrib['begin']):int(element.attrib['end'])]
            CLINENTITY_extent[dictionnary_index] = [int(element.attrib['begin']), int(element.attrib['end']), element.attrib['entityID']]
        except KeyError:
            CLINENTITY_extent[dictionnary_index] = [int(element.attrib['begin']), int(element.attrib['end']), 'NO_entityID']
            print(file, document[int(element.attrib['begin']):int(element.attrib['end'])])


    #for element in tree.xpath(sentence_path):
    #    print(element.attrib['begin'], element.attrib['end'])

    print(file, '------\tdone\t✅')

    #break

for key, value in CLINENTITY_extent.items():
    if value[2] not in CLINENTITY_extent_repartition:
        CLINENTITY_extent_repartition[value[2]] = 1
    else:
        CLINENTITY_extent_repartition[value[2]] += 1

CLINENTITY_extent_repartition = dict(sorted(CLINENTITY_extent_repartition.items(), key=lambda x: x[1], reverse=True))

with open('10_CLINENTITY_extent_repartition.txt', 'w', encoding='utf-8') as repartition_outfile:
    for key, value in CLINENTITY_extent_repartition.items():
        repartition_outfile.write(key + '\t' + str(value) + '\n')

with open('11_words_code.txt', 'w', encoding='utf-8') as code_outfile:
    for key, value in words_code.items():
        code_outfile.write(key + '\t' + value + '\n')

end = time.time()
temps = end-begin
minutes = round((temps / 60),2)
print('Temps d\'execution : '+str(minutes)+' minute.s.')
