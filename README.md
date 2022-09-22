# krpsim
## Table des Matières
* [Introduction](#introduction)
* [Python Requirements](#python-requirements)
* [Utilisation](#utilisation)
* [Exemples](#exemples)
  * [Normal](#normal)
  * [Cycles](#cycles)
  * [Instructions](#instructions)
  * [Visual](#visual)
* [Plus info](#plus-info)
  
## Introduction
Vous avez peut-être déjà vu un de ces jolis diagrammes de gestion de projet où figurent 
tous les process qui s’enchainent les uns-les autres, selon leurs dépendances et contraintes 
respectives. Bien souvent, le nombre reste faible et les dépendances simples, et vous ne 
cherchez à faire l’ensemble qu’une seule fois. Mais dès lors que vous avez nettement plus 
de processus disponibles, qu’il y a plusieurs choix, que certains doivent éventuellement 
être répétés, ou encore que l’ensemble a vocation à continuer à l’infini, il n’est plus 
possible de spontanément trouver une solution optimisée pour laquelle vous aurez le meilleur 
rendement.  
Ce projet, au cours duquel vous aurez aussi à faire de la gestion de projet et de groupe, 
consiste à réaliser un programme qui va optimiser le rendement d’une chaine (ou plutôt 
d’un graphe en fait) de processus, en maximisant un résultat, et/ou en réduisant le délai 
le plus possible.  
  
## Python Requirements
**install requirements:** <code>$ pip3 install -r requirements.txt</code>  
  
## Utilisation
<pre><code>usage: krpsim.py [-h] [-cy CYCLE] [-ch CHILDREN] [-in INSTRUCTIONS] [-v] file delay

positional arguments:
  file                  file to optimize
  delay                 max time to process

options:
  -h, --help            show this help message and exit
  -cy CYCLE, --cycle CYCLE
                        max number of cycle. default:10000
  -ch CHILDREN, --children CHILDREN
                        max number of children. default:1000
  -in INSTRUCTIONS, --instructions INSTRUCTIONS
                        max number of instructions allowed during child generation. default:10000
  -v, --visual          Print instructions list after execution</code></pre>
  
## Exemples
### Normal
<pre><code>$ python3 krpsim.py resources/pomme 2
Nice file ! 18 processes, 16 stocks, 1 to optimize

Making children ████████████████████████████████ 100%

Main walk
# No more proces doable at cycle 9859

Stock:
 four => 10
 euro => 298000
 [...]
 flan => 0
 boite => 0

time: 1.0594453811645508</code></pre>
  
### Cycles
<pre><code>$ python3 krpsim.py resources/pomme 3 -cy 1000
Nice file ! 18 processes, 16 stocks, 1 to optimize

Making children ████████████████████████████████ 100%

Main walk
# No more proces doable at cycle 533

Stock:
 four => 10
 euro => 10400
 [...]
 flan => 0
 boite => 0

time: 0.8958723545074463</code></pre>
  
### Instructions
<pre><code>$ python3 krpsim.py resources/pomme 3 -in 100
Nice file ! 18 processes, 16 stocks, 1 to optimize

Making children ████████████████████████████████ 100%

Main walk
# No more proces doable at cycle 9577

Stock:
 four => 10
 euro => 17200
 [...]
 flan => 0
 boite => 0

time: 0.09298419952392578</code></pre>
  
### Visual
<pre><code>$ python3 krpsim.py resources/pomme 3 -v
Nice file ! 18 processes, 16 stocks, 1 to optimize

Making children ████████████████████████████████ 100%

Main walk
0:buy_beurre
0:buy_farine
[...]
9827:do_boite
9828:vente_boite

# No more proces doable at cycle 9859

Stock:
 four => 10
 euro => 298000
 [...]
 flan => 0
 boite => 0

time: 0.9811151027679443</code></pre>
  
## Plus info
**Autor:** [Antoine Mauffret](https://github.com/AntoineMau) [Martin de Lagarde](https://github.com/Martydl)  
  
**Subject:** [krpsim](https://cdn.intra.42.fr/pdf/pdf/57255/fr.subject.pdf)
