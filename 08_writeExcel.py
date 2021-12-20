import time
begin = time.time()

import pylightxl as xl

all_extent = [x.rstrip() for x in open('Searched_results/ALL-SEARCHED-EXTENT.csv', 'r', encoding='UTF-8')]
words = [x.split('\t')[0] for x in open('Searched_results/ALL-SEARCHED-EXTENT.csv', 'r', encoding='UTF-8')]
words = set(words)

words = sorted(words)
sorted_list = []

del words[0]
try:
    while words[0] in words[1]:
        temp = []
        len_word = len(words[0])
        for ligne in all_extent:
            if words[0] in ligne[0:len_word]:
                temp.append(ligne)
        sorted_list.append(temp)
        del words[0:2]
        try:
            while words[0] not in words[1]:
                temp = []
                len_word = len(words[0])
                for ligne in all_extent:
                    if words[0] in ligne[0:len_word]:
                        temp.append(ligne)
                sorted_list.append(temp)
                del[words[0]]
        except IndexError:
            pass
except IndexError:
    pass


last_list = []

compteur = 1
for ligne in sorted_list:
    #print(compteur)
    compteur += 1
    if ligne not in last_list:
        last_list.append(ligne)


db = xl.Database()

for ligne in range(0,len(sorted_list)):
# add a blank worksheet to the db
    db.add_ws(ws=sorted_list[ligne][0].split('\t')[0])

# loop to add our data to the worksheet
    for row_id, data in enumerate(sorted_list[ligne], start=1):
        data = data.split('\t')
        for x, y in zip(range(0, len(data)), data):
            db.ws(ws=sorted_list[ligne][0].split('\t')[0]).update_index(row=row_id, col=x+1, val=y)

# write out the db
#xl.writexl(db=db, fn="Corrected_CLINENTITY-VerificationsXXXXXX.xlsx")

end = time.time()
temps = end-begin
minutes = round((temps / 60),2)
print('\n\nTemps d\'execution : '+str(minutes)+' minute.s.')


db = xl.Database()
# write text
db.add_ws(ws='Sheet1')
db.ws(ws='Sheet1').update_index(row=1, col=2, val='twenty')


xl.writexl(db=db, fn='updated.xlsx')
