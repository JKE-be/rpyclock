# rpyclock

## Le project

Ce projet n'invente pas la roue, il a juste pour but de reproduire un type horloge que j'ai vu, et trouvé très sympathique, mais pas dans mon budget ;)

Ce projet a donc pour but d'implémenter une Word's clock en python avec un RasberryPi fortement inspirée de https://qlocktwo.com/eu/qlocktwo-large-creator-s-edition-rust.


## Matériel

Le POC actuel, sera composé:
- d'un bouton pour switcher de mode
- d'un RPI4 en attendant la réception du nouveau rasberry pi Zero w2 ...
- d'un ruban led WS2812B ([amazon.fr](https://www.amazon.fr/gp/product/B07TJCXYBT/ref=ppx_yo_dt_b_asin_title_o02_s00?ie=UTF8&psc=1))

## Les objectifs

Le premier objectif est de réaliser cette horloge avec un carré de 10/10 leds.  (37cm/37cm)
Ensuite, d'ajouter la notion de minute individuelle avec 4 nouvelles leds.
Et finalement rendre le code plus générique pour supporter une version plus grande de 75/75cm avec 2 fois plus de led, ...
And after...

## Et ensuite...

Ajouter une RTC
Ajouter différent mode (affichage digital, multi couleurs, ...)
Interface pour configuration (connexion wifi, set rtc, ...)
Et adapter le project selon les feedbacks...
