`
# Chatbot BI Analyst Roole X Souha BOUGHRARA
Ce chatbot est exclusivement dédié aux questions de restitution et n’est pas autorisé à traiter d’autres types de demandes. J’ai mis à votre disposition deux méthodes pour le lancer, au cas où vous rencontreriez un problème Python sur l’un des environnements.
---

## ⚙️ Configuration

### Instructions système
Modifiez le comportement du chatbot dans `system_instructions.py` :

 ⁠python
SYSTEM_INSTRUCTIONS = """
Votre prompt système ici...
"""
⁠ `

### Paramètres du modèle

Dans `config.py` ou `config/llm/settings.py`, vous pouvez ajuster :

* `llm_model_id` : Identifiant du modèle HuggingFace à utiliser
* `max_new_tokens` : Longueur maximale des réponses
* `temperature` : Créativité du modèle (0.0 = déterministe, 1.0 = très créatif)

---

## 🏃 Lancement
## Méthode 1 

1. Créez et activez votre environnement virtuel :

 ⁠bash
python -m venv venv
venv\Scripts\activate 


⁠ 2. Installez les dépendances :

 ⁠bash
pip install -r requirements.txt


⁠ 3. Configurez votre token HuggingFace :

* Allez sur [HuggingFace Tokens](https://huggingface.co/settings/tokens)
* Créez un nouveau token et copiez-le
* Créez un fichier `.env` à la racine du projet :

 ⁠env
HUGGINGFACEHUB_API_TOKEN='votre_token_ici'


⁠ 4. Lancez l’application :

 ⁠bash
streamlit run chatbot_app.py

⁠ ## 🎯 Utilisation

* Posez vos questions directement dans le chat######
* Les réponses sont générées selon vos instructions système et paramètres de configuration
---

## Méthode 2 
## Assurez vous que l'environnement Anaconda + VS Code est installé sur votre ordinateur

1. Créez et activez votre environnement virtuel :
Une fois décompresser , copier le chemin d'accès de votre dossier et ouvrez le sur la prompt avec la commande cd + chemin du dossier

 ⁠bash
cd C:\Users\ASUS\Downloads\Chatbot


⁠ 2. Activer l’environnement
 ⁠bash
conda create -n monenv python=3.12
conda activate monenv

⁠ 3. Lancer VS Code à partir d’Anaconda
 ⁠bash
pip install -r requirements.txt


⁠ 4. Configurez votre token HuggingFace :

* Allez sur [HuggingFace Tokens](https://huggingface.co/settings/tokens)
* Créez un nouveau token et copiez-le
* Créez un fichier `.env` à la racine du projet :

 ⁠env
HUGGINGFACEHUB_API_TOKEN='votre_token_ici'


⁠ 5. Lancez l’application :

 ⁠bash
streamlit run chatbot_app.py



## Bonne Utilisation !!!! 


## 🔧 Structure du projet


.
├── chatbot_app.py              # Application Streamlit principale
├── system_instructions.py      # Instructions système
├── config.py                   # Configuration LLM (legacy)
├── config/
│   └── llm/
│       └── settings.py         # Configuration Pydantic
└── services/
    └── llm_service.py          # Service LLM avec nettoyage automatique
```

---