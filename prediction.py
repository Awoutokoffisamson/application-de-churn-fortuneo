import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import requests
import json

def afficher_prediction(data):
    # Configuration du style de la page
    st.markdown(
        """
        <style>
        .pred-title {
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
        .info-box {
            background-color: #e6f0ff;
            border-left: 5px solid #0052CC;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .form-container {
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
    st.markdown('<h1 class="pred-title">Prédiction de churn individuelle</h1>', unsafe_allow_html=True)
    
    # Information sur la prédiction
    st.markdown(
        """
        <div class="info-box">
            <h4>Évaluation du risque de désabonnement</h4>
            <p>Cette section vous permet d'évaluer la probabilité qu'un client spécifique quitte la banque, 
            en fonction de ses caractéristiques personnelles et de son comportement bancaire.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Formulaire de prédiction
    st.markdown('<h3 class="section-title">Informations du client</h3>', unsafe_allow_html=True)
    
    st.markdown('<div class="form-container">', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        credit_score = st.slider("Score de crédit", min_value=300, max_value=900, value=650, step=1)
        geography = st.selectbox("Pays", options=["France", "Spain", "Germany"])
        gender = st.selectbox("Genre", options=["Female", "Male"])
        age = st.slider("Âge", min_value=18, max_value=100, value=40, step=1)
        tenure = st.slider("Ancienneté (années)", min_value=0, max_value=10, value=5, step=1)
    
    with col2:
        balance = st.number_input("Solde du compte", min_value=0.0, max_value=250000.0, value=50000.0, step=1000.0)
        num_products = st.slider("Nombre de produits", min_value=1, max_value=4, value=1, step=1)
        has_credit_card = st.selectbox("Possède une carte de crédit", options=["Oui", "Non"])
        is_active_member = st.selectbox("Est un membre actif", options=["Oui", "Non"])
        estimated_salary = st.number_input("Salaire estimé", min_value=0.0, max_value=300000.0, value=100000.0, step=5000.0)
    
    # Conversion des valeurs pour la prédiction
    has_credit_card_value = 1 if has_credit_card == "Oui" else 0
    is_active_member_value = 1 if is_active_member == "Oui" else 0
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Bouton de prédiction
    if st.button("Prédire le risque de churn", key="predict_button"):
        with st.spinner("Prédiction en cours..."):
            # Préparation des données client pour l'API
            client_data = {
                "CreditScore": credit_score,
                "Geography": geography,
                "Gender": gender,
                "Age": age,
                "Tenure": tenure,
                "Balance": balance,
                "NumOfProducts": num_products,
                "HasCrCard": has_credit_card_value,
                "IsActiveMember": is_active_member_value,
                "EstimatedSalary": estimated_salary
            }
            
            # Tentative d'appel à l'API
            try:
                response = requests.post("https://machinelearning2api.onrender.com/predict", json=client_data, timeout=15)
                if response.status_code == 200:
                    prediction_result = response.json()
                    churn_probability = prediction_result["churn_probability"]
                    churn_prediction = prediction_result["churn_prediction"]
                    risk_level = prediction_result["risk_level"]
                    api_used = True
                else:
                    st.error(f"Erreur lors de l'appel à l'API : Code {response.status_code}")
                    return
            except Exception as e:
                st.error(f"Impossible de se connecter à l'API : {e}")
                return
            
            # Afficher les résultats
            st.markdown('<h3 class="section-title">Résultats de la prédiction</h3>', unsafe_allow_html=True)
            st.markdown('<div class="results-container">', unsafe_allow_html=True)
            
            # Afficher la probabilité de churn
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    label="Probabilité de churn",
                    value=f"{churn_probability*100:.1f}%"
                )
                
                # Afficher la prédiction
                if churn_prediction:
                    st.error("Prédiction: Client à risque de désabonnement")
                else:
                    st.success("Prédiction: Client fidèle")
            
            with col2:
                # Afficher le niveau de risque
                if risk_level == "Élevé":
                    st.markdown('<p>Niveau de risque: <span class="risk-high">Élevé</span></p>', unsafe_allow_html=True)
                elif risk_level == "Moyen":
                    st.markdown('<p>Niveau de risque: <span class="risk-medium">Moyen</span></p>', unsafe_allow_html=True)
                else:
                    st.markdown('<p>Niveau de risque: <span class="risk-low">Faible</span></p>', unsafe_allow_html=True)
                
                # Afficher la source de la prédiction
                st.info("Prédiction fournie par l'API")
            
            # Jauge de probabilité
            fig = go.Figure(go.Indicator(
                mode = "gauge+number",
                value = churn_probability * 100,
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Probabilité de churn (%)"},
                gauge = {
                    'axis': {'range': [0, 100]},
                    'bar': {'color': "#0052CC"},
                    'steps': [
                        {'range': [0, 40], 'color': "#4CAF50"},
                        {'range': [40, 60], 'color': "#FFC107"},
                        {'range': [60, 100], 'color': "#FF5252"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': churn_probability * 100
                    }
                }
            ))
            
            fig.update_layout(
                height=300,
                margin=dict(l=20, r=20, t=50, b=20),
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Recommandations
            st.markdown("<h4>Recommandations</h4>", unsafe_allow_html=True)
            
            if risk_level == "Élevé":
                st.markdown(
                    """
                    <ul>
                        <li><strong>Action urgente recommandée</strong> : Contactez ce client directement pour identifier les problèmes et proposez des offres de fidélisation spécifiques.</li>
                        <li>Envisagez une réduction temporaire des frais ou une offre promotionnelle personnalisée.</li>
                        <li>Proposez un rendez-vous avec un conseiller pour discuter de ses besoins financiers.</li>
                    </ul>
                    """,
                    unsafe_allow_html=True
                )
            elif risk_level == "Moyen":
                st.markdown(
                    """
                    <ul>
                        <li><strong>Action proactive recommandée</strong> : Envisagez un contact proactif pour évaluer la satisfaction et proposez des avantages personnalisés.</li>
                        <li>Envoyez des communications ciblées sur les produits qui pourraient l'intéresser.</li>
                        <li>Proposez un programme de fidélité ou des avantages exclusifs.</li>
                    </ul>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    """
                    <ul>
                        <li><strong>Surveillance standard</strong> : Continuez à maintenir la relation client actuelle.</li>
                        <li>Proposez des produits complémentaires adaptés au profil.</li>
                        <li>Assurez-vous que le client est informé des nouveaux services et fonctionnalités.</li>
                    </ul>
                    """,
                    unsafe_allow_html=True
                )
            
            st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    # Pour test local
    data = pd.read_csv("data/data.csv")
    afficher_prediction(data)
