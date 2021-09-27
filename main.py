import os

import wptools
import pubchempy as pcp
from PIL import Image, ImageDraw


def generateFlashCardSet(name):
    try:
        os.makedirs(f'out/{name}/images')
    except:
        print("Overwriting existing card set!")
    markdown = f"# {name}\n"

    with open('entities', "r") as file:
        for substance in file:
            if substance[0] == "#":
                continue
            if substance[0] == "!":
                break
            substance = substance.split('/')
            substance_eng = substance[1].strip()
            substance = substance[0].strip()

            print(f"Fetching {substance}...")

            # IMAGE

            img_path = f"out/{name}/images/{substance}.png"
            pcp.download('PNG', 'tmp.png', substance_eng, 'name', overwrite=True, image_size='large')

            im = Image.open("tmp.png").convert('RGBA')
            newImage = []
            for item in im.getdata():
                if item[:3] == (245, 245, 245):
                    newImage.append((255, 255, 255, 0))
                else:
                    newImage.append(item)
            im.putdata(newImage)

            im.save(img_path)

            # STUFF

            page = wptools.page(substance, lang='de', silent=True)
            infobox = page.get_parse().data['infobox']
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

            summary = query.data['extext']
            try:
                description = infobox['Beschreibung']
            except:
                description = None

            try:
                other_names = infobox['Andere Namen']
            except:
                other_names = None

            text = f"\n--- \n**Que:** {substance}\n\n"

            text += f"**Ans:**\n"
            if description is not None:
                text += f"{description}\n"

            text += f"![](images/{substance}.png)\n"

            if other_names is not None:
                text += f"\n**Andere Namen:**\n"
                text += f"{other_names}\n"

            text += f"\n**Informationen:**\n"
            for key, value in disp_infobox.items():
                text += f"- {key}: {value}\n"

            text += f"\n**Beschreibung:**\n"
            text += f"{summary}\n"

            markdown += text

        markdown += "---"

        replacements = {
            "[[Grad Celsius|°C]]": "°C",
            "[[Hektopascal|hPa]]": "hPa",
            "([[IUPAC-Nomenklatur|IUPAC]])": "<small>(IUPAC)</small>",
            "(<small>system.</small> [[IUPAC]])": "<small>(IUPAC)</small>",
            "(<small>system. Name</small>)": "<small>(IUPAC)</small>",
            "<small>([[IUPAC]])</small>": "<small>(IUPAC)</small>",
            "([[IUPAC]])": "<small>(IUPAC)</small>",
            "([[Aminosäuren#Kanonische Aminosäuren|Dreibuchstabencode]])": "",
            "([[Aminosäuren#Kanonische Aminosäuren|Einbuchstabencode]])": ""
        }

        for key, value in replacements.items():
            markdown = markdown.replace(key, value)

        with open(f'out/{name}/{name}.md', 'w') as f:
            f.write(markdown)


test_substances = [
    'Phenol', 'Anilin', 'Benzaldehyd', 'Glycin', 'Salicylsäure', 'Calciumcarbonat', 'Blausäure'
]
generateFlashCardSet('TestSubstances')

# Aminosäuren
# amino_acids = [
#     'Alanin', 'Arginin', 'Asparagin', 'Asparaginsäure', 'Cystein', 'Glutamin', 'Glutaminsäure', 'Glycin', 'Histidin',
#     'Isoleucin', 'Leucin', 'Lysin', 'Methionin', 'Phenylalanin', 'Prolin', 'Serin', 'Threonin', 'Tryptophan',
#     'Tyrosin', 'Valin'
# ]
# generateFlashCardSet('Aminosäuren', amino_acids)
