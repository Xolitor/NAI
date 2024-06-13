NAI: Votre Assistant Personnel
NAI (Assistant de Nouvelles et de Météo) est un assistant personnel qui offre deux fonctionnalités principales :

Récupérer et résumer une liste d'articles en ligne sur un sujet donné.
Fournir une prévision météorologique pour une ville spécifiée jusqu'à 5 jours dans le future et générer une image météo basée sur la prévision.
Fonctionnalités
Récupération de Nouvelles : Obtenez les derniers articles de nouvelles en fonction d'un sujet spécifié.
Prévision Météorologique : Obtenez les prévisions météorologiques pour une ville spécifiée pour jusqu'à 5 jours.
Génération d'Image Météo : Générez une image basée sur les dernières prévisions météorologiques pour une ville spécifiée.
Installation et Configuration
Pour commencer avec NAI, suivez ces étapes :

Prérequis
La liste des librairies et de leur version est disponible dans le requirements.txt
Outil de virtualisation d'environnement (par exemple, venv)
Cloner le Répertoire
bash
Copier le code
git clone https://github.com/votre-nom-utilisateur/nai-assistant.git
cd nai-assistant
Créer et Activer l'Environnement Virtuel
Pour Windows :
bash
Copier le code
python -m venv venv
.\venv\Scripts\activate
Pour macOS et Linux :
bash
Copier le code
python3 -m venv venv
source venv/bin/activate
Installer les Dépendances
bash
Copier le code
pip install -r requirements.txt
Configurer les Variables d'Environnement
Créez un fichier .env dans le répertoire racine du projet et ajoutez vos clés API comme suit :

makefile
Copier le code
OPENAI_API_KEY=votre_cle_api_openai
NEWS_API_KEY=votre_cle_api_news
WEATHER_API_KEY=votre_cle_api_weather
ASSISTANT_KEY=votre_cle_api_assistant
Lancer le Site Web
Pour démarrer l'application web Streamlit, exécutez la commande suivante :
bash
Copier le code
streamlit run app.py

Utilisation
Récupération de Nouvelles
Entrez un sujet dans le champ de saisie intitulé "Ask for news on a topic or the weather of a city:".
Exemple de prompt: "Give me the latest news on bitcoin ?" ou encore "What's the news on Microsoft ?" 
Note : Il est préférable de choisir des sujets connus et mondiaux, car l'assistant va chercher dans une base de données de sites principalement américains.
Cliquez sur "Run NAI".
L'assistant récupérera et résumera les derniers articles sur le sujet spécifié.
Prévision Météorologique
Entrez une ville dans le champ de saisie intitulé "Ask for news on a topic or the weather of a city:".
Exemple de prompt: "Give me the weather forecast for Paris ?" ou encore "What is the weather going to be in Dubai ?"
Génération d'image météorologique:
Entrez uniquement le nom d'une ville dans le champ de saisie intitulé "Enter City for an image of the weather:"
Exemple de prompt: "Paris", "Nice", "London", "New York"
Cliquez sur "Generate Weather Image" pour générer une image basée sur les dernieres prévisions météorologiques.
