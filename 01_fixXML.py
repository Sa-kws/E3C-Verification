import time
begin = time.time()

import os
print('Module importés')

FOLDER = 'Data'
NEW_FOLDER = 'Underscored_datas'
compteur = 1
try:
    os.mkdir(NEW_FOLDER)
except FileExistsError:
    pass
print('Variables initialisées et dossier créé')

for file in os.listdir(FOLDER):
    name_of_infile = FOLDER + '/' + file
    name_of_outfile = NEW_FOLDER + '/' + file
    new_file = []
    with open(name_of_infile, 'r', encoding='utf-8') as infile:
        for line in infile:
            line = line.replace(':', '_', 1)
            new_file.append(line)
    with open(name_of_outfile, 'w', encoding='utf-8') as outfile:
        for element in new_file:
            outfile.write(element)
    print(compteur, '--- Fichier\t', file, '\ttraité\t✅')
    compteur += 1

end = time.time()
temps = end-begin
minutes = round((temps / 60),2)
print('Temps d\'execution : '+str(minutes)+' minute.s.')
