import pylightxl as xl

#for methode in dir(xl):
#    print(methode)

db = xl.readxl(fn='CLIENTITY-Verification.xlsx')
'''
for sheet in db.ws_names:
    #print(db.ws(ws=sheet).address(address='A1'))
    #for x in range(0,len(db.ws(ws=sheet).range(address='A1:S1'))):
    rows = db.ws(ws=sheet).range(address='A1:S1')[0]
    #print(db.ws(ws=sheet).row())

    if '' not in rows:
        break
'''
#for sheet in db.ws_names:
#    print(db.ws(ws=sheet).row(1))

compteur = 0
for sheet in db.ws_names:
    for col in db.ws(ws=sheet).cols:
        #print(col)
        compteur += len(col)-1
        break
print(compteur)
'''
with open('OUTPUT/00_Extent-to-search.txt', 'w', encoding='UTF-8') as outfile:
    for sheet in db.ws_names:
        sheet = sheet.replace('_','')
        if '.' in sheet:
            sing_plur = sheet.split('.')
            outfile.write(sing_plur[0] + '\n' + sing_plur[0] + 's\n')
        elif 'toux' in sheet:
            outfile.write('toux\n')
            outfile.write('toux sèche\n')
            outfile.write('toux-sèche\n')
        elif '-' in sheet:
            outfile.write(sheet + '\n')
            sheet = sheet.replace('-', ' ')
            outfile.write(sheet + '\n')
        else:
            outfile.write(sheet + '\n')
'''
