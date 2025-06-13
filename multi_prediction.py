import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import requests
import io
import pickle
import tempfile

def afficher_multi_prediction(data):
    # Configuration du style de la page
    st.markdown(
        """
        <style>
        .multi-pred-title {
            font-size: 2.5rem;
            font-weight: bold;
            text-align: center;
            color: #0052CC;
            margin-bottom: 1.5rem;
        }
        .section-title {
            font-size: 1.8rem;
            font-weight: bold;
            color: #00468B;
            margin-top: 2rem;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid #0052CC;
        }
        .upload-container {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        .results-container {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-top: 20px;
        }
        .info-box {
            background-color: #e6f0ff;
            border-left: 5px solid #0052CC;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .download-button {
            background-color: #0052CC;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 5px;
            border: none;
        }
        .risk-high {
            color: #FF5252;
            font-weight: bold;
        }
        .risk-medium {
            color: #FFC107;
            font-weight: bold;
        }
        .risk-low {
            color: #4CAF50;
            font-weight: bold;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Titre principal
    st.markdown('<h1 class="multi-pred-title">Prédiction de churn par lot</h1>', unsafe_allow_html=True)
    
    # Information sur la prédiction par lot
    st.markdown(
        """
        <div class="info-box">
            <h4>Prédiction pour plusieurs clients</h4>
            <p>Téléchargez un fichier CSV ou Excel contenant les informations de plusieurs clients pour obtenir des prédictions de churn en masse.
            Le fichier doit contenir les colonnes suivantes : CreditScore, Geography, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Section de téléchargement de fichier
    st.markdown('<h3 class="section-title">Téléchargement du fichier</h3>', unsafe_allow_html=True)
    
    st.markdown('<div class="upload-container">', unsafe_allow_html=True)
    
    # Téléchargement du fichier
    uploaded_file = st.file_uploader(
        "Téléchargez un fichier CSV ou Excel",
        type=["csv", "xlsx", "xls"],
        help="Le fichier doit contenir les colonnes suivantes : CreditScore, Geography, Gender, Age, Tenure, Balance, NumOfProducts, HasCrCard, IsActiveMember, EstimatedSalary"
    )

    # Exemple de fichier avec des clients dans les trois catégories de risque
    with st.expander("Voir un exemple de format de fichier"):
        # Exemple avec des clients ayant des probabilités de churn variées
        # Assurons-nous d'avoir des clients dans chaque catégorie, notamment dans la catégorie moyenne (40-60%)
        example_data = pd.DataFrame({
            'CreditScore': [619, 608, 502, 699, 850, 645, 732],
            'Geography': ['France', 'Spain', 'France', 'France', 'Spain', 'Germany', 'France'],
            'Gender': ['Female', 'Female', 'Female', 'Female', 'Female', 'Male', 'Male'],
            'Age': [42, 41, 42, 39, 43, 50, 58],  # Âge plus élevé pour augmenter la probabilité de churn
            'Tenure': [2, 1, 8, 1, 2, 5, 7],
            'Balance': [0.00, 83807.86, 159660.80, 0.00, 125510.82, 75000.25, 130000.50],
            'NumOfProducts': [1, 1, 3, 2, 1, 2, 1],
            'HasCrCard': [1, 0, 1, 0, 1, 1, 0],
            'IsActiveMember': [1, 1, 0, 0, 1, 0, 1],  # Membre non actif pour augmenter la probabilité de churn
            'EstimatedSalary': [101348.88, 112542.58, 113931.57, 93826.63, 79084.10, 85000.00, 120000.00]
        })
        
        st.dataframe(example_data, use_container_width=True)
        
        # Bouton pour télécharger l'exemple
        csv = example_data.to_csv(index=False)
        st.download_button(
            label="Télécharger l'exemple en CSV",
            data=csv,
            file_name="exemple_clients.csv",
            mime="text/csv",
            key="download-example-csv"
        )
        
        # Bouton pour tester avec l'exemple
        if st.button("Tester avec l'exemple", key="test-example-button"):
            batch_data = example_data
            st.session_state['batch_data'] = batch_data

    st.markdown('</div>', unsafe_allow_html=True)
    
    # Traitement du fichier téléchargé ou de l'exemple
    if uploaded_file is not None or 'batch_data' in st.session_state:
        try:
            # Charger les données
            if uploaded_file is not None:
                if uploaded_file.name.endswith('.csv'):
                    batch_data = pd.read_csv(uploaded_file)
                else:
                    batch_data = pd.read_excel(uploaded_file)
            else:
                batch_data = st.session_state['batch_data']
            
            # Vérifier les colonnes requises
            required_columns = ['CreditScore', 'Geography', 'Gender', 'Age', 'Tenure', 
                               'Balance', 'NumOfProducts', 'HasCrCard', 'IsActiveMember', 'EstimatedSalary']
            
            missing_columns = [col for col in required_columns if col not in batch_data.columns]
            
            if missing_columns:
                st.error(f"Colonnes manquantes dans le fichier : {', '.join(missing_columns)}")
                return
            
            # Vérifier les valeurs manquantes
            if batch_data[required_columns].isnull().any().any():
                st.error("Le fichier contient des valeurs manquantes dans les colonnes requises. Veuillez vérifier les données.")
                return
            
            # Vérifier les types de données
            expected_dtypes = {
                'CreditScore': np.number,
                'Geography': object,
                'Gender': object,
                'Age': np.number,
                'Tenure': np.number,
                'Balance': np.number,
                'NumOfProducts': np.number,
                'HasCrCard': np.number,
                'IsActiveMember': np.number,
                'EstimatedSalary': np.number
            }
            
            for col, dtype in expected_dtypes.items():
                if not np.issubdtype(batch_data[col].dtype, dtype):
                    st.error(f"La colonne {col} doit être de type {dtype.__name__}. Type trouvé : {batch_data[col].dtype}")
                    return
            
            # Afficher un aperçu des données
            st.markdown('<h3 class="section-title">Aperçu des données</h3>', unsafe_allow_html=True)
            st.dataframe(batch_data.head(5), use_container_width=True)
            
            # Bouton pour lancer la prédiction
            if st.button("Lancer la prédiction par lot", key="batch-predict-button"):
                with st.spinner("Prédiction en cours..."):
                    # Tentative d'appel à l'API pour la prédiction par lot
                    try:
                        # Convertir le DataFrame en liste de dictionnaires pour l'API
                        clients_data = batch_data.to_dict(orient='records')
                        
                        # Appel à l'API
                        response = requests.post(
                            "https://machinelearning2api.onrender.com/predict/batch",
                            json={"clients": clients_data},
                            timeout=15  # Timeout plus long pour les lots importants
                        )
                        
                        if response.status_code == 200:
                            # Traitement de la réponse de l'API
                            api_results = response.json()
                            predictions = api_results["predictions"]
                            summary = api_results["summary"]
                            
                            # Ajouter les résultats au dataframe
                            results_data = batch_data.copy()
                            results_data['Prediction_Churn'] = [pred["churn_prediction"] for pred in predictions]
                            results_data['Probabilite_Churn'] = [pred["churn_probability"] for pred in predictions]
                            
                            # Classification des risques avec les seuils standard
                            results_data['Niveau_Risque'] = pd.cut(
                                [pred["churn_probability"] for pred in predictions],
                                bins=[0, 0.4, 0.6, 1],
                                labels=['Faible', 'Moyen', 'Élevé']
                            )
                            
                            # Compter les effectifs par niveau de risque
                            risk_counts = results_data['Niveau_Risque'].value_counts().to_dict()
                            
                            # S'assurer que tous les niveaux sont représentés dans le dictionnaire
                            for level in ['Faible', 'Moyen', 'Élevé']:
                                if level not in risk_counts:
                                    risk_counts[level] = 0
                            
                            # Calculer les pourcentages
                            total_clients = len(results_data)
                            high_risk = risk_counts['Élevé']
                            high_risk_percent = (high_risk / total_clients) * 100 if total_clients > 0 else 0
                            
                            medium_risk = risk_counts['Moyen']
                            medium_risk_percent = (medium_risk / total_clients) * 100 if total_clients > 0 else 0
                            
                            low_risk = risk_counts['Faible']
                            low_risk_percent = (low_risk / total_clients) * 100 if total_clients > 0 else 0
                        else:
                            st.error(f"Erreur lors de l'appel à l'API : Code {response.status_code}. Veuillez vérifier que l'API est en cours d'exécution.")
                            return
                    except Exception as e:
                        st.error(f"Impossible de se connecter à l'API : {e}. Assurez-vous que le serveur est accessible à https://machinelearning2api.onrender.com/predict/batch.")
                        return
                    
                    # Afficher les résultats
                    st.markdown('<h3 class="section-title">Résultats de la prédiction</h3>', unsafe_allow_html=True)
                    st.markdown('<div class="results-container">', unsafe_allow_html=True)
                    
                    # Source de la prédiction
                    st.info("Prédictions fournies par l'API")
                    
                    # Statistiques des résultats
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.metric(
                            label="Clients à risque élevé",
                            value=f"{high_risk} ({high_risk_percent:.1f}%)",
                            delta=None,
                            delta_color="off"
                        )
                    
                    with col2:
                        st.metric(
                            label="Clients à risque moyen",
                            value=f"{medium_risk} ({medium_risk_percent:.1f}%)",
                            delta=None,
                            delta_color="off"
                        )
                    
                    with col3:
                        st.metric(
                            label="Clients à risque faible",
                            value=f"{low_risk} ({low_risk_percent:.1f}%)",
                            delta=None,
                            delta_color="off"
                        )
                    
                    # Graphique de distribution des risques avec légende fixe
                    # Utiliser toujours les trois catégories, même si certaines ont une valeur de 0
                    fig = px.pie(
    names=['Risque élevé', 'Risque moyen', 'Risque faible'],
    values=[high_risk, medium_risk, low_risk],
    color=['Risque élevé', 'Risque moyen', 'Risque faible'],  # pour associer correctement couleurs et noms
    color_discrete_map={
        'Risque élevé': '#FF0000',   # Rouge
        'Risque moyen': '#FFC107',   # Jaune
        'Risque faible': '#4CAF50'   # Vert
    },
    hole=0.4
)
                    
                    fig.update_layout(
                        title="Distribution des niveaux de risque",
                        legend_title="Niveau de risque",
                        template="plotly_white",
                        showlegend=False
                    )
                    
                    fig.update_traces(
                        textposition='inside', 
                        textinfo='percent+label',
                        hovertemplate='%{label}<br>Nombre: %{value}<br>Pourcentage: %{percent}'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Tableau des résultats avec mise en forme des niveaux de risque
                    styled_results = results_data.style.apply(
                        lambda x: [
                            f'color: #FF5252' if v == 'Élevé' else
                            f'color: #FFC107' if v == 'Moyen' else
                            f'color: #4CAF50' for v in x
                        ],
                        subset=['Niveau_Risque']
                    )
                    
                    st.markdown("<h4>Tableau des résultats détaillés</h4>", unsafe_allow_html=True)
                    st.dataframe(styled_results, use_container_width=True)
                    
                    # Bouton pour télécharger les résultats
                    csv = results_data.to_csv(index=False)
                    st.download_button(
                        label="Télécharger les résultats en CSV",
                        data=csv,
                        file_name="resultats_prediction_churn.csv",
                        mime="text/csv",
                        key="download-results-csv"
                    )
                    
                    # Recommandations
                    st.markdown("<h4>Recommandations</h4>", unsafe_allow_html=True)
                    st.markdown(
                        """
                        <ul>
                            <li><strong>Clients à risque élevé (<span class="risk-high">Élevé</span>)</strong> : Intervention urgente recommandée. Contactez ces clients directement pour identifier les problèmes et proposez des offres de fidélisation spécifiques.</li>
                            <li><strong>Clients à risque moyen (<span class="risk-medium">Moyen</span>)</strong> : Envisagez un contact proactif pour évaluer la satisfaction et proposez des avantages personnalisés.</li>
                            <li><strong>Clients à risque faible (<span class="risk-low">Faible</span>)</strong> : Continuez à maintenir la relation client actuelle et proposez des produits complémentaires adaptés au profil.</li>
                        </ul>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    st.markdown('</div>', unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"Erreur lors du traitement du fichier : {e}. Assurez-vous que le fichier est au bon format (CSV ou Excel) et contient des données valides.")

if __name__ == "__main__":
    # Pour test local
    data = pd.read_csv("data/data.csv")
    afficher_multi_prediction(data)
