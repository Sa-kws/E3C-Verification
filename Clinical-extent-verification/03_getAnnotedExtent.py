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

    for element in tree.xpath(CLINENTITY_path):
        dictionnary_index += 1
        CLINENTITY_extent[dictionnary_index] = [int(element.attrib['begin']), int(element.attrib['end']), element.attrib['entityID']]

    for element in tree.xpath(document_path):
        document = element.attrib['sofaString']

    #for element in tree.xpath(sentence_path):
    #    print(element.attrib['begin'], element.attrib['end'])

    break

for key, value in CLINENTITY_extent.items():
    words_code[value[2]] = document[value[0]:value[1]]
    if value[2] not in CLINENTITY_extent_repartition:
        CLINENTITY_extent_repartition[value[2]] = 1
    else:
        CLINENTITY_extent_repartition[value[2]] += 1
CLINENTITY_extent_repartition = dict(sorted(CLINENTITY_extent_repartition.items(), key=lambda x: x[1], reverse=True))

print(CLINENTITY_extent_repartition)
print(words_code)
