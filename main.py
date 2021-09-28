import os
import re

import wptools
import pubchempy as pcp
from PIL import Image, ImageDraw


def generateFlashCardSet(name, caching=False):
    try:
        os.makedirs(f'out/{name}/images')
    except:
        print("Overwriting existing card set!")
    markdown = f"# {name}\n"

    with open('entities.txt', "r") as file:
        for substance in file:
            if substance[0] == "#":
                continue
            if substance[0] == "!":
                break

            substance = substance.split('/')
            substance_ger = substance[0].strip()
            substance_eng = substance_ger
            if len(substance) == 2:
                if substance[1].strip() == 'e':
                    substance_eng = f"{substance_ger}e"
                else:
                    substance_eng = substance[1].strip()
            substance_img = substance_eng.replace(' ', '_')

            # IMAGE

            img_path = f"out/{name}/images/{substance_img}.png"
            if caching and os.path.exists(img_path):
                continue

            print(f"Fetching {substance_ger} ({substance_eng})...")
            try:
                pcp.download('PNG', 'tmp.png', substance_eng, 'name', overwrite=True, image_size='large')
            except:
                print(f"-> Couldn't download image for {substance_eng}")
                continue

            im = Image.open("tmp.png").convert('RGBA')
            color = (245, 245, 245)
            newImage = []
            for item in im.getdata():
                alpha = max(abs(item[0] - color[0]), abs(item[1] - color[1]), abs(item[2] - color[2]))
                newImage.append((item[0], item[1], item[2], alpha))
            im.putdata(newImage)
            im.save(img_path)

            # INFORMATION

            page = wptools.page(substance_ger, lang='de', silent=True)
            infobox = page.get_parse().data['infobox']
            if infobox is None:
                print(f"-> Couldn't fetch infobox for {substance_ger}")
            query = page.get_query()

            items = ['Summenformel',
                     'Aggregat', 'Aggregatszustand',
                     'Dichte',
                     'Schmelzpunkt',
                     'Siedepunkt',
                     'pKs', 'pKS-Wert',
                     'Löslichkeit',
                     'Brechungsindex']
            disp_infobox = dict((k, infobox[k]) for k in items if k in infobox)

            summary = query.data['extext'].replace('\n\n', ' <br> ').replace('\n', ' ')

            # GENERATE MARKDOWN

            text = f"\n--- \n**Que:** {substance_ger}"
            if substance_eng != substance_ger and substance_eng != f"{substance_ger}e":
                text += f"\n{substance_eng}"
            text += "\n\n"

            text += f"**Ans:**\n"
            try:
                text += f"{infobox['Beschreibung']}\n"
            except:
                print(f"-> Couldn't print description for {substance_ger}")

            text += f"![](images/{substance_img}.png)\n"

            try:
                text += f"\n# Andere Namen:\n{infobox['Andere Namen']}\n"
            except:
                print(f"-> Couldn't print alternative names for {substance_ger}")

            text += f"\n# Informationen: \n"
            for key, value in disp_infobox.items():
                text += f"- {key}: {value}\n"

            text += f"\n# Beschreibung:\n{summary}\n"
            text += f"[↗︎ Wikipedia]({query.data['url']})\n"

            markdown += text

        markdown += "\n---"

        markdown = re.sub(r"\* {{.*}}", "", markdown)
        # markdown = re.sub(r"\[\[.*|", "", markdown)

        replacements = {
            "[[Grad Celsius|°C]]": "°C",
            "[[Hektopascal|hPa]]": "hPa",
            "([[IUPAC-Nomenklatur|IUPAC]])": "<small>(IUPAC)</small>",
            "(<small>system.</small> [[IUPAC]])": "<small>(IUPAC)</small>",
            "(<small>system. Name</small>)": "<small>(IUPAC)</small>",
            "<small>([[IUPAC]])</small>": "<small>(IUPAC)</small>",
            "([[IUPAC]])": "<small>(IUPAC)</small>",
            "([[Aminosäuren#Kanonische Aminosäuren|Dreibuchstabencode]])": "",
            "([[Aminosäuren#Kanonische Aminosäuren|Einbuchstabencode]])": "",
            # "** ": "\t * ",
            " * ": "\n\t * ",
            # "[[": "",
            # "]]": "",
            " )": ")",
            "( ": "(",
            " ,": ","
        }

        for key, value in replacements.items():
            markdown = markdown.replace(key, value)

        with open(f'out/{name}/{name}.md', 'w') as f:
            f.write(markdown)


# generateFlashCardSet('TestSubstances', caching=True)
# generateFlashCardSet('TestSubstances', caching=False)
generateFlashCardSet('Organische Substanzen', caching=False)


# Aminosäuren
# amino_acids = [
#     'Alanin', 'Arginin', 'Asparagin', 'Asparaginsäure', 'Cystein', 'Glutamin', 'Glutaminsäure', 'Glycin', 'Histidin',
#     'Isoleucin', 'Leucin', 'Lysin', 'Methionin', 'Phenylalanin', 'Prolin', 'Serin', 'Threonin', 'Tryptophan',
#     'Tyrosin', 'Valin'
# ]
# generateFlashCardSet('Aminosäuren', amino_acids)
