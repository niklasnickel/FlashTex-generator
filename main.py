import os
import urllib

import wptools
import cairosvg
import pubchempy as pcp
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM

from wikidata.client import Client

def generateFlashCardSet(name):
    try:
        os.makedirs(f'out/{name}/images')
    except:
        print("Overwriting existing card set!")
    markdown = f"# {name}\n"

    with open('entities', "r") as file:
        for substance in file:
            substance = substance.strip()
            if substance[0] == "#":
                continue
            if substance[0] == "!":
                break

            print(f"Fetching {substance}...")

            pcp.download('PNG', f"out/{name}/images/{substance}.jpg", substance, 'name')

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

            # try:
            #     image = query.data['image'][0]
            #     image_name = os.path.splitext(image['orig'])
            #     image_path = f"out/{name}/images/{image_name[0]}"
            #     if image_name[1] == '.svg':
            #         urllib.request.urlretrieve(image['url'], f"{image_path}.svg")
            #         cairosvg.svg2png(url=f"{image_path}.svg", write_to=f"{image_path}.png")
            #     else:
            #         urllib.request.urlretrieve(image['url'], f"{image_path}.{image_name[1]}")
            # except:
            #     print("Need to do except")
            #     page = wikipedia.page(substance)
            #     image = infobox['Strukturformel']
            #     image_name = image[image.find(':') + 1: image.find('|')]
            #     image_name = os.path.splitext(image_name.replace(' ', '_'))
            #     image_path = f"out/{name}/images/{image_name[0]}"
            #
            #     for image in page.images:
            #         if image_name[0] in image:
            #             image_url = image
            #             if image_name[1] == '.svg':
            #                 urllib.request.urlretrieve(image_url, f"out/{name}/images/{image_name[0]}.svg")
            #                 try:
            #                     cairosvg.svg2png(url=f"{image_path}.svg", write_to=f"{image_path}.png")
            #                 except:
            #                     print("Couldn't do stuff")
            #             else:
            #                 urllib.request.urlretrieve(image_url, f"out/{name}/images/{image_name[0]}.{image_name[1]}")
            #             break
            #     else:
            #         print(f"Image: {image_name[0]} was not found")

            # MARKDOWN GENERATION
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
