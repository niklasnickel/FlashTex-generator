# FlashTex-generator

This script automatically creates flashcards for [FlashTex](https://flashtex.app/) from a .txt-file of chemical substances.

## Usage

Under `substances` you find a list of .txt-files with chemical substances. 
Every substance must have its own line in the format `[german name] / [english name]`. 
If the english name differs from only appending an "e", instead of writing `Diazomethan / Diazomethane` you can simply write `Diazomethan/e`. 
Comments start with `#`.
The generated `.md` files and fetched images are built in the directory `out`. You can import this set into FlashTex using the gui.

## Example card!


### Front side
> Fructose

### Back side
> farb- und geruchlose, sehr süß schmeckende Prismen oder Nadeln
> 
> ![Fructose](https://user-images.githubusercontent.com/24753584/170916679-2e486b9a-43f0-4ae1-9446-6e7ead7a78b4.png)
> 
> #### Andere Namen:
> * <small>D</small>-(−)-Fructose
> * Fruchtzucker
> * Lävulose
> * Laevulose
> * <small>L</small>,<small>D</small>,<small>D</small>-Ketohexose
> * α-Acrose
> * <small>D</small>-arabino-Hex-2-ulose
> 
> #### Informationen: 
> - Summenformel: C<sub>6</sub>H<sub>12</sub>O<sub>6</sub>
> - Aggregat: fest
> - Dichte: 1,59 g·cm<sup>−3</sup> (20&nbsp;°C)
> - Schmelzpunkt:
> 	 * 106 °C (Zersetzung; <small>D</small>-Fructose)
> 	 * 129–130 °C (<small>D,L</small>-Fructose)
> - Löslichkeit:
> 	 * sehr gut in Wasser: 790 g/l (20&nbsp;°C)
> 	 * gut in [[Aceton]], mäßig in [[Ethanol]], schlecht in [[Diethylether]], [[Benzol]] und [[Chloroform]]
> 
> #### Beschreibung:
> **Fructose** (oft auch **Fruktose**, von lateinisch fructus „Frucht“, veraltet **Lävulose**, umgangssprachlich **Fruchtzucker**) ist eine natürlich vorkommende chemische Verbindung. Fructose gehört als Monosaccharid (_Einfachzucker_) zu den Kohlenhydraten. Sie kommt in mehreren isomeren (anomeren) Formen vor. In diesem Artikel betreffen die Angaben zur Physiologie allein die D-Fructose. L-Fructose ist praktisch bedeutungslos.
> [↗︎ Wikipedia](https://de.wikipedia.org/wiki/Fructose)

## Contributios, questions, etc.
If you want to contribute to this project, feel free to do so! If you have any questions, just write me a message! Please excuse the messieness of the project's repo. Have fun! :)
