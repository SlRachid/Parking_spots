# The DytyCS's Parking Spots project  

## Description :  
Notre projet consiste à la création d'un site Web qui permet, d'une part, aux conducteurs de sélectionner un parking parmis ceux proposés et de voir les places de parking disponibles et, d'autre part, aux détenteurs de parkings de charger leur parking dans le site.

Le **MVP (Minimum Viable Product)** de ce projet consistera à livrer une première version de l'outil de détection des places vides d'un parking de bout à bout , c'est-à-dire de la lecture de l'image du parking à la démonstration des places vacantes dudit parking.

En particulier, le MVP :
* Permettera de charger une image d'un parking afin d'en détecter les places vacantes.
* Détectera les places disponibles d'un parking, vacantes ou non, en les encadrant et en associant à chacune un label.
* Extraira les images de chaque place du parking.
* Entraînera un réseau de neurones sur une base de données constituée d'images de places de parking vacantes et d'autres contenant une voiture.
* Testera le réseau de neurones sur une autre partie de la base de données considérée.
* Affichera le résultat de l'ensemble des places vides du parking.


## Sprints :

**Sprint 0 :** Analyse des besoins et conception du produit

**Sprint 1 :** Détection et identification des places existant dans le parking

* *Fonctionnalité 1* : Charger l'image du parking et sélectionner les places qui s'y trouvent.  

* *Fonctionnalité 2* : Extraire les images des places du parking et les stocker dans un dossier  

**Sprint 2 :** vérification de la présence ou non d'une voiture sur une place du parking

* *Fonctionnalité 1 *: Construire une base de données constituée d'images de places de parking vacantes et d'autres occupées à partir de photos aériennes de différents parkings.

* *Fonctionnalité 2* : Créer et entraîner un réseau de neurones sur une partie de la base de données.

* *Fonctionnalité 3* : Tester le réseau de neurones sur d'autres images.

**Sprint 3 :** Mise en place du site Web  
* *Fonctionnalité 1* : fournir une platforme interactive à l'utilisateur.    

* *Fonctionnalité 2* : permettre à l'utilisateur d'uploader une image.   

* *Fonctionnalité 3* : afficher l'image traitée et la liste des places libres.   

## The DytyCS team :
1. **D**EMRI Lina :
* Construction du site Web
* Préparation de la présentation   
2. **Y**EBARI Moghit : 
* Détection et stockage des places de stationnement
* Construction et enrichissement de la base de données
* Rassemblement de la fonction main()
* 
3. **T**BATOU Hamza :
* Construction la base de données 
* Entraînement réseau de neurones
* Codage des fonctions tests
4. **Y**ARTAOUI Farouk : 
* Identification des places de parking
* Rassemblement de la fonction main()
* Construction de la base de données
* Codage des fonctions tests
5. **C**HAFIK Hala : 
* Identification des places du parking 
* Construction de la base de données
* Préparation de la présentation PowerPoint.
6. **S**LIMANI Rachid : 
* Structuration et entraînement du réseau de neurones 
* Création du site Web
## Consignes d'utilisation :
+ Le projet est le dossier codingweeks dans le repertoire git, donc on commence par se placer dans le dossier sur le terminal;
+ Au debut, il n'y a pas de cache (normalement);
+ On lance l'app_original.py (l'app flask);
+ Une fois lancé revient sur le fichier détection_de_voiture.py et comment les deux lignes 111-112;
+ On est sur la page d'acceuil, on se dirige vers la partie services sur la barre de navigation;
+ On commence par le service parking owners pour fixer les positions des rectangles;
+ Après, on télécharge l'image du parking vide avec le boutton "choose file" (vous trouverez un exemple sur le dossier statit/uploads);
+ Une fenêtre permettant la sélection des spots apparait alors(les dimensions des rectangles sont ajustables);
+ On appuie sur "x" pour sortir;
+ Maintenant pour resetter, il faut partir a la fonction app.py et faire ctrl+s;
+ Maintenant tout est pret pour un conducteur;
+ Etant donnée une image du même parking à moitié rempli, on va afficher les spots vacants;
+ Pour ce faire, on se dirige vers la partie service du driver;
+ On clique  sur "show available spots" pour commencer;
+ On upload la photo qu'on veut traiter(vous trouverez un exemple sur le dossier statit/uploads) et on clique sur "submit";
+ On trouve donc à gauche les spots disponibles et à droite l'image avec les labels des spots pour pouvoir se repérer.



## Some errors you could encounter :
+ in the keras library there some things missing that are now in tensorflow like layer_utils and get_file, but in vggface these changes are still not udated so you could have to change in the keras_vggface.vggface : "keras.utils" to "tensorflow.python.keras.utils" 
+ There is also one error concerning the topology. In the keras_vggface/models.py file, you could have to change the import from:
"from keras.engine.topology import get_source_inputs"
to:
"from keras.utils.layer_utils import get_source_inputs"