import secrets
from PIL import Image, ImageDraw, ImageFont

alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789{%}?!.,_;\'[]#'
head = ['ABC', 'DEF', 'GHI', 'JKL', 'MNO', 'PQR', 'STU', 'VWX', 'YZ', '.!#']

AnzahlZeichenProZelle = 3

def random_string():
    zeichenkette = ""
    for i in range(AnzahlZeichenProZelle):
        zeichenkette += secrets.choice(alphabet)
    return zeichenkette

def generate_password_card(row_count,):
    pc = []
    for row in range (row_count):
        row = []
        for col in range(len(head)):
            row.append(random_string())
        pc.append(row)
    return pc

def save_pc(filename, pc):
    to_save = ''
    for row in range(len(pc)):
        for col in range(len(pc[0])):
            to_save += pc[row][col]
        if row != len(range(len(pc)))-1:
            to_save += '\n'
    with open(filename, 'w+') as out:
        out.write(to_save)

def load_pc(filename):
    pc = []
    with open(filename, 'r') as pc_in:
        for row in pc_in:
            row = row.strip()
            pc.append([row[0+i:AnzahlZeichenProZelle+i] for i in range(0, len(row), AnzahlZeichenProZelle)])
    return pc

def generate_password(pc, keyword):
    password = ''
    rows = len(pc)
    for row in range(len(keyword)):
        for col in range(len(head)):
            if keyword[row].lower() in head[col].lower():
                password += pc[row%rows][col]
                break
    return password

def text_for_each_zell(pc):
    mytext = []
    onerow = []
    onerow.append('0')

    for zell in head:
        onerow.append(zell)
    onerow.append('-')

    for index, element in enumerate(pc):
        mytext.append(onerow)
        onerow = []
        onerow.append(str(index+1))
        for item in element:
            onerow.append(item)
        onerow.append('-')
    mytext.append(onerow)
    return mytext

def techcode_pdf(Bildsize, pc_file, speichernAls):
    pc = load_pc(pc_file)

    rows_tabel = len(pc) + 1
    col = len(head) + 1

    mytext = text_for_each_zell(pc)
    breite_rahmen = int(Bildsize[0]*0.0016)

    # Erstelle ein neues Bild mit den angegebenen Abmessungen
    img = Image.new('RGB', (Bildsize[0], Bildsize[1]), color = (0, 0, 0))

    BreiteZelle = Bildsize[0]/col - (breite_rahmen/col)
    HeigthZelle = Bildsize[1]/rows_tabel  - (breite_rahmen/rows_tabel)

    # Erstelle einen Zeichenkontext
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, Bildsize[0], HeigthZelle + breite_rahmen*1.5], fill=(0, 0, 0))
    d.rectangle([0, 0, BreiteZelle + breite_rahmen*1.5, Bildsize[1]], fill=(0, 0, 0))

    # Erstelle eine Schriftart
    textSize = int(HeigthZelle*0.8)

    fnt = ImageFont.truetype('C:\\Windows\\Fonts\\Segoe UI\\UbuntuMono-Bold.ttf', textSize)

    # Berechne die Größe des Textes
    text_width, text_height = d.textsize(f'{mytext[1][1]}', font=fnt)

    if text_width >= BreiteZelle: 
        faktor = BreiteZelle / text_width
        textSize = int(textSize * (faktor - 0.12))
        fnt = ImageFont.truetype('C:\\Windows\\Fonts\\Segoe UI\\UbuntuMono-Bold.ttf', textSize)

    # Zeichne die Tabelle
    for i in range(rows_tabel):
        if i == 0:
            color = (153, 153, 153)
        elif i%2 == 0:
            color = (255, 255, 255)
        else:
            color = (209, 227, 255)

        for j in range(col):
            if i == 1 and j ==1:
                d.rectangle([(j*BreiteZelle + breite_rahmen*2, i*HeigthZelle + breite_rahmen*2), j*BreiteZelle + BreiteZelle, i*HeigthZelle + HeigthZelle], fill=color)
            elif i == 1 and j != 0:
                d.rectangle([(j*BreiteZelle + breite_rahmen, i*HeigthZelle + breite_rahmen*2), j*BreiteZelle + BreiteZelle, i*HeigthZelle + HeigthZelle], fill=color)
            elif j == 1 and i != 0:
                d.rectangle([(j*BreiteZelle + breite_rahmen*2, i*HeigthZelle + breite_rahmen), j*BreiteZelle + BreiteZelle, i*HeigthZelle + HeigthZelle], fill=color)
            else:                
                d.rectangle([(j*BreiteZelle + breite_rahmen, i*HeigthZelle + breite_rahmen), j*BreiteZelle + BreiteZelle, i*HeigthZelle + HeigthZelle], fill=color)

            aktuellerText = mytext[i][j]

            if i == 0 and j==0:aktuellerText = ''

            # Berechne die Größe des Textes
            text_width, text_height = d.textsize(f'{aktuellerText}', font=fnt)

            # Berechne die Position des Textes
            text_x = j*BreiteZelle + (BreiteZelle - text_width) / 2
            text_y = i*HeigthZelle + (HeigthZelle - text_height) / 2
            
            # Schreibe den Text
            d.text((text_x, text_y), f'{aktuellerText}', fill=(0, 0, 0), font=fnt)

    # Speichere das Bild
    img.show()
    img.save(speichernAls + '.jpg')


# save_pc("pc.txt", generate_password_card(16))

print(generate_password(load_pc('ffw_pc.txt'), 'WEB.de'))

# techcode_pdf((3508, 2480), 'ffw_pc.txt', 'PWCard')