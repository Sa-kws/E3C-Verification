import time
begin = time.time()

import os
from lxml import etree
print('Module importés')

FOLDER = 'Underscored_datas-v2'

empty_clinentity = []
no_attribute_clinentity = []
empty_event = []
no_attribute_event = []
empty_timex3Class = []
empty_value = []
no_attribute_timex3Class = []
no_attribute_value = []


def extractEmptyAnnotation(tree, path, attribute, file, empty, no_attribute, sentence):
    for ID in tree.xpath(path):
        if attribute in ID.attrib:
            if ID.attrib[attribute] == '':
                empty.append([file, attribute, path.split('_')[-1], str(sentence[int(ID.attrib['begin']):int(ID.attrib['end'])]), ID.attrib['begin'], ID.attrib['end'], 'PAS D\'ID'])
            elif ID.attrib[attribute] == 'CUILESS':
                empty.append([file, attribute, path.split('_')[-1], str(sentence[int(ID.attrib['begin']):int(ID.attrib['end'])]), ID.attrib['begin'], ID.attrib['end'], 'CUILESS'])
        else:
            no_attribute.append([file, attribute, path.split('_')[-1], str(sentence[int(ID.attrib['begin']):int(ID.attrib['end'])]),  ID.attrib['begin'], ID.attrib['end'], 'PAS D\'ATTRTIBUT'])
    return empty, no_attribute


for file in os.listdir(FOLDER):
    name_of_infile = FOLDER + '/' + file
    tree = etree.parse(name_of_infile)
    for element in tree.xpath('/xmi_XMI/cas_Sofa'):
        sentence = element.attrib['sofaString']

    empty_clinentity, no_attribute_clinentity = extractEmptyAnnotation(tree, '/xmi_XMI/custom_CLINENTITY', 'entityID', file, empty_clinentity, no_attribute_clinentity, sentence)
    empty_event, no_attribute_event = extractEmptyAnnotation(tree, '/xmi_XMI/custom_EVENT', 'contextualModality', file, empty_event, no_attribute_event, sentence)
    empty_timex3Class, no_attribute_timex3Class = extractEmptyAnnotation(tree, '/xmi_XMI/custom_TIMEX3', 'timex3Class', file, empty_timex3Class, no_attribute_timex3Class, sentence)
    empty_value, no_attribute_value = extractEmptyAnnotation(tree, '/xmi_XMI/custom_TIMEX3', 'value', file, empty_value, no_attribute_value, sentence)

'''
print('--- CLINENTITY ---')
print(empty_clinentity)
print(no_attribute_clinentity)
print('--- EVENT ---')
print(empty_event)
print(no_attribute_event)
print('--- TIMEX-class ---')
print(empty_timex3Class)
print(no_attribute_timex3Class)
print('--- TIMEX-value ---')
print(empty_value)
print(no_attribute_value)
'''

with open('OUTPUT/21_Annotations_manquantes.tsv', 'w', encoding='utf-8') as outfile:
    outfile.write('Fichier\tAttribut\tType d\'entité\tEntité\tbegin\tend\tValeur\n')
    for element in empty_clinentity:
        line = ''
        for info in element:
            line += info + '\t'

        outfile.write(line + '\n')
    for element in no_attribute_clinentity:
        line = ''
        for info in element:
            line += info + '\t'
        outfile.write(line + '\n')
    for element in empty_event:
        line = ''
        for info in element:
            line += info + '\t'
        outfile.write(line + '\n')
    for element in no_attribute_event:
        line = ''
        for info in element:
            line += info + '\t'
        outfile.write(line + '\n')
    for element in empty_timex3Class:
        line = ''
        for info in element:
            line += info + '\t'
        outfile.write(line + '\n')
    for element in no_attribute_timex3Class:
        line = ''
        for info in element:
            line += info + '\t'
        outfile.write(line + '\n')
    for element in empty_value:
        line = ''
        for info in element:
            line += info + '\t'
        outfile.write(line + '\n')
    for element in no_attribute_value:
        line = ''
        for info in element:
            line += info + '\t'
        outfile.write(line + '\n')

end = time.time()
temps = end-begin
minutes = round((temps / 60),2)
print('Temps d\'execution : '+str(minutes)+' minute.s.')
