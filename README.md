# NAI: Votre Assistant Personnel
Réalisé par SAMUEL Jonathan et VERKIMPE Axel

## MINI PROJET IA: SUJET OUVERT 

NAI (Assistant de Nouvelles et de Météo) est un assistant personnel qui offre deux fonctionnalités principales :

1. Récupérer et résumer une liste d'articles en ligne sur un sujet donné.
2. Fournir une prévision météorologique pour une ville spécifiée jusqu'à 5 jours dans le future et générer une image météo basée sur la prévision actuelle.

## Fonctionnalités
- **Récupération d'articles :** Obtenez les derniers articles en fonction d'un sujet spécifié.
* **Prévision Météorologique :** Obtenez les prévisions météorologiques pour une ville spécifiée pour jusqu'à 5 jours.
+ **Génération d'Image Météo :** Générez une image basée sur les dernières prévisions météorologiques pour une ville spécifiée.
  
## Installation et Configuration
Pour commencer avec NAI, suivez ces étapes :

## Prérequis
+ La liste des librairies et de leur version est disponible dans le requirements.txt
- Outil de virtualisation d'environnement (par exemple, venv)

## Lancer le projet

Pour lancer le projet il y a 3 étapes:

### 1. Créer et Activer l'Environnement Virtuel
Pour Windows :
```bash
python -m venv venv
.\venv\Scripts\activate
```
Pour macOS et Linux :
```bash
python3 -m venv venv
source venv/bin/activate
```
Installer les Dépendances
```bash
pip install -r requirements.txt
```

### 2. Configurer les Variables d'Environnement
Créez un fichier .env dans le répertoire racine du projet et ajoutez les clés API fournit dans le .txt sur Moodle comme suit :

Copier le code
```
OPENAI_API_KEY=votre_cle_api_openai
NEWS_API_KEY=votre_cle_api_news
WEATHER_API_KEY=votre_cle_api_weather
ASSISTANT_KEY=votre_cle_api_assistant
```

### 3. Lancer le Site Web
Pour démarrer l'application web Streamlit, exécutez la commande suivante depuis un terminal dans la racine du projet :
```bash
streamlit run main.py
```

## Utilisation

**Les API**
Les fonctionnalités de notre Assistant utilisent des API, une pour appeller une liste d'articles (newsapi.org), et une pour les prévisions métérologiques (openweathermap.org).

**Génération d'Image**
La génération d'image passe par Dallee 3.0

**Récupération d'Articles**
1. Entrez un sujet dans le champ de saisie intitulé "Ask for news on a topic or the weather of a city:".
    - Exemple de prompt: "Give me the latest news on bitcoin ?" ou encore "What's the news on Microsoft ?" 
    - **Note** : Il est préférable de choisir des sujets connus et mondiaux, car l'assistant va chercher dans une base de données de sites principalement américains.
2. Cliquez sur "Run NAI".
3. L'assistant récupérera et résumera les derniers articles sur le sujet spécifié.
   
**Prévision Météorologique**
1. Entrez une ville dans le champ de saisie intitulé "Ask for news on a topic or the weather of a city:".
     - Exemple de prompt: "Give me the weather forecast for Paris ?" ou encore "What is the weather going to be in Dubai ?"   
2. Cliquez sur "Run NAI".
3. L'assistant récupérera et résumera les prévisions météos sur la ville pour les 5 jours qui arrivent.
   
**Génération d'image météorologique:**
1. Entrez **UNIQUEMENT** le nom d'une ville dans le champ de saisie intitulé "Enter City for an image of the weather:"   
    - Exemple de prompt: "Paris", "Nice", "London", "New York"
2. Cliquez sur "Generate Weather Image" pour générer une image basée sur les dernieres prévisions météorologiques.
3. L'assistant génerera une image de la ville avec la météo de la prévision la plus récente.
