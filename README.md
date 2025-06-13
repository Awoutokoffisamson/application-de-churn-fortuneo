# Fortuneo Banque - Application de Prédiction de Churn

Cette application Streamlit permet d'analyser et de prédire le risque de désabonnement (churn) des clients de Fortuneo Banque.

## Fonctionnalités

- **Accueil** : Présentation de l'application et de ses fonctionnalités
- **Statistiques** : Analyse descriptive des données clients
- **Visualisation** : Graphiques interactifs pour explorer les facteurs de churn
- **Prédiction** : Évaluation du risque de churn pour un client individuel
- **Prédiction Multiple** : Analyse du risque pour un groupe de clients via import de fichier, un test peut être fait avec un exemple s'y trouvant 

## Installation

1. Assurez-vous d'avoir Python 3.8+ installé
2. Installez les dépendances requises :

```bash
pip install -r requirements.txt
```

## Lancement de l'application

```bash
streamlit run main.py
```

L'application sera accessible dans votre navigateur à l'adresse : http://localhost:8501

## Structure du projet

- `main.py` : Point d'entrée de l'application
- `accueil.py` : Module pour la page d'accueil
- `statistiques.py` : Module pour les statistiques descriptives
- `visualisation.py` : Module pour les visualisations interactives
- `prediction.py` : Module pour la prédiction individuelle
- `multi_prediction.py` : Module pour la prédiction par lot
- `assets/` : Dossier contenant les ressources graphiques

## Sources de données

- Base de données : [GitHub](https://github.com/Awoutokoffisamson/machine_learning2_Documents/blob/main/Churn_Modelling.csv)
- Modèle : [Google Drive](https://drive.google.com/file/d/1JZji6K_r-Msko1xuk3R9ONycgPtliSK2/view)

Si les ressources en ligne ne sont pas accessibles, l'application entraînera automatiquement un nouveau modèle à partir des données disponibles.

## Personnalisation

Vous pouvez personnaliser l'apparence de l'application en modifiant les styles CSS dans chaque module ou en ajoutant vos propres assets graphiques dans le dossier `assets/`.

## Dépendances principales

- streamlit
- pandas
- numpy
- scikit-learn
- plotly
- streamlit-option-menu
- requests

## Contact

Pour toute question ou assistance, veuillez contacter l'équipe Data Science à *awoutokoffisamson@gmail.com*
