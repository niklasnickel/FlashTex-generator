import urllib.request
import wptools
import wikipedia

so = wptools.page('Anilin', lang='de').get_parse()
infobox = so.data['infobox']

page = wikipedia.page('Anilin')
images = page.images

image = infobox['Strukturformel']
image_name = image[image.find(':') + 1: image.find('|')]
image_name = image_name.replace(' ', '_')

for image in images:
    if image_name in image:
        image_url = image
        break
else:
    print(f"{image_name} not found")

urllib.request.urlretrieve(image_url, f"out/images/{image_name}")

print(infobox)

# import requests
#
# response = requests.get('https://de.wikipedia.org/w/api.php',
#                         params={'action': 'query', 'prop': 'revisions', 'format': 'json', 'rvprop': 'content',
#                                 'rvsection': 0, 'titles': 'Phenol'}
#                         ).json()
# page = next(iter(response['query']['pages'].values()))
# print(page)
