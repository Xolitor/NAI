# NAI: Votre Assistant Personnel
NAI (Assistant de Nouvelles et de Météo) est un assistant personnel qui offre deux fonctionnalités principales :

1. Récupérer et résumer une liste d'articles en ligne sur un sujet donné.
2. Fournir une prévision météorologique pour une ville spécifiée jusqu'à 5 jours dans le future et générer une image météo basée sur la prévision.
## Fonctionnalités
- **Récupération d'articles :** Obtenez les derniers articles en fonction d'un sujet spécifié.
* **Prévision Météorologique :** Obtenez les prévisions météorologiques pour une ville spécifiée pour jusqu'à 5 jours.
+ **Génération d'Image Météo :** Générez une image basée sur les dernières prévisions météorologiques pour une ville spécifiée.
  
## Installation et Configuration
Pour commencer avec NAI, suivez ces étapes :

## Prérequis
+ La liste des librairies et de leur version est disponible dans le requirements.txt
- Outil de virtualisation d'environnement (par exemple, venv)
## Cloner le Répertoire
```bash
Copier le code
git clone https://github.com/votre-nom-utilisateur/nai-assistant.git
cd nai-assistant
```
## Créer et Activer l'Environnement Virtuel
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

## Configurer les Variables d'Environnement
Créez un fichier .env dans le répertoire racine du projet et ajoutez vos clés API comme suit :
makefile
Copier le code
```
OPENAI_API_KEY=votre_cle_api_openai
NEWS_API_KEY=votre_cle_api_news
WEATHER_API_KEY=votre_cle_api_weather
ASSISTANT_KEY=votre_cle_api_assistant
```

## Lancer le Site Web
Pour démarrer l'application web Streamlit, exécutez la commande suivante :
```bash
streamlit run app.py
```

## Utilisation
**Récupération de Nouvelles**
1. Entrez un sujet dans le champ de saisie intitulé "Ask for news on a topic or the weather of a city:".
Exemple de prompt: "Give me the latest news on bitcoin ?" ou encore "What's the news on Microsoft ?" 
2. Note : Il est préférable de choisir des sujets connus et mondiaux, car l'assistant va chercher dans une base de données de sites principalement américains.
3. Cliquez sur "Run NAI".
4. L'assistant récupérera et résumera les derniers articles sur le sujet spécifié.
   
**Prévision Météorologique**
1. Entrez une ville dans le champ de saisie intitulé "Ask for news on a topic or the weather of a city:".
2. Exemple de prompt: "Give me the weather forecast for Paris ?" ou encore "What is the weather going to be in Dubai ?"
3. Cliquez sur "Run NAI".
4. L'assistant récupérera et résumera les prévisions météos sur la ville pour les 5 jours qui arrivent.
   
**Génération d'image météorologique:**
1. Entrez uniquement le nom d'une ville dans le champ de saisie intitulé "Enter City for an image of the weather:"
Exemple de prompt: "Paris", "Nice", "London", "New York"
2. Cliquez sur "Generate Weather Image" pour générer une image basée sur les dernieres prévisions météorologiques.
3. L'assistant génerera une image de la ville avec la météo de la prévision la plus récente.
