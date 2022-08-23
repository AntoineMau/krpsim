# krpsim
## Table des Matières
* [Introduction](#introduction)
* [Python Requirements](#python-requirements)
* [Utilisation](#utilisation)
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
**install requirements:** <code>$ python3 -m pip install -r requirements.txt</code>  
  
## Utilisation
<pre><code>usage: krpsim.py [-h] [-c CYCLE] file delay

positional arguments:
  file                  file to process
  delay                 max time to process

optional arguments:
  -h, --help            show this help message and exit
  -c CYCLE, --cycle CYCLE
                        max number of cycle. default:10000</code></pre>  
  
## Plus info
**Autor:** [Antoine Mauffret](https://github.com/AntoineMau) [Martin de Lagarde](https://github.com/Martydl)  
  
**Subject:** [krpsim](https://cdn.intra.42.fr/pdf/pdf/57255/fr.subject.pdf)
