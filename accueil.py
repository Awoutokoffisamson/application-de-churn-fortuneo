import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import base64
from PIL import Image
import io
import os

def afficher_accueil():
    # Configuration du style de la page d'accueil
    st.markdown(
        """
        <style>
        .main-title {
            font-size: 3.2rem;
            font-weight: bold;
            text-align: center;
            color: #0052CC;
            margin-bottom: 1.5rem;
        }
        .subtitle {
            font-size: 1.8rem;
            text-align: center;
            color: #00468B;
            margin-bottom: 2rem;
        }
        .feature-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            text-align: center;
        }
        .feature-icon {
            font-size: 3rem;
            color: #0052CC;
            margin-bottom: 15px;
        }
        .feature-title {
            font-size: 1.5rem;
            font-weight: bold;
            color: #00468B;
            margin-bottom: 10px;
        }
        .feature-text {
            font-size: 1rem;
            color: #333;
        }
        .info-section {
            background-color: #e6f0ff;
            border-left: 5px solid #0052CC;
            padding: 15px;
            border-radius: 5px;
            margin-top: 30px;
        }
        .banner {
            width: 100%;
            border-radius: 10px;
            margin-bottom: 20px;
            background-color: #0052CC;
            padding: 20px;
            text-align: center;
        }
        .bank-image {
            width: 100%;
            max-height: 300px;
            object-fit: cover;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .iframe-container {
            position: relative;
            width: 100%;
            overflow: hidden;
            padding-top: 56.25%; /* 16:9 Aspect Ratio */
        }
        .responsive-iframe {
            position: absolute;
            top: 0;
            left: 0;
            bottom: 0;
            right: 0;
            width: 100%;
            height: 100%;
            border: none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Bannière principale avec image de la banque
    BANK_IMAGE_URL = "https://raw.githubusercontent.com/Awoutokoffisamson/machine_learning2_Documents/main/image%20banque.png"
    
    st.markdown(
        """
        <div class="banner">
        """,
        unsafe_allow_html=True
    )
    
    # Afficher l'image de la banque
    st.image(BANK_IMAGE_URL, use_container_width=True)
    
  
    # Titres
    st.markdown('<h1 class="main-title">Bienvenue sur l\'outil de prédiction de churn</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Analysez et prédisez le risque de désabonnement des clients de Fortuneo Banque</p>', unsafe_allow_html=True)

    # Présentation des fonctionnalités en 3 colonnes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <div class="feature-title">Statistiques détaillées</div>
                <p class="feature-text">Explorez les données clients et découvrez les facteurs qui influencent le plus le désabonnement.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <div class="feature-title">Visualisation interactive</div>
                <p class="feature-text">Visualisez les tendances et patterns dans les données clients à travers des graphiques interactifs.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )
    
    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🎯</div>
                <div class="feature-title">Prédiction précise</div>
                <p class="feature-text">Prédisez la probabilité de désabonnement pour un client individuel ou pour un groupe de clients.</p>
            </div>
            """, 
            unsafe_allow_html=True
        )

    # Section d'information sur le churn
    st.markdown(
        """
        <div class="info-section">
            <h3>Qu'est-ce que le "churn" bancaire ?</h3>
            <p>Le <b>churn</b> (ou attrition) désigne le phénomène par lequel des clients quittent une banque pour une autre. 
            Dans le secteur bancaire en ligne, où la concurrence est intense et les coûts d'acquisition de nouveaux clients sont élevés, 
            la rétention des clients est essentielle à la rentabilité.</p>
            
            <p>Notre outil de prédiction utilise un modèle de <b>Random Forest</b> entraîné sur des données historiques pour identifier 
            les clients à risque de désabonnement, permettant ainsi à Fortuneo Banque de mettre en place des actions préventives ciblées.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Section "Comment utiliser cet outil"
    st.markdown("<h2 style='margin-top: 40px;'>Comment utiliser cet outil</h2>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <ol>
            <li><b>Statistiques</b> : Explorez les statistiques descriptives des données clients</li>
            <li><b>Visualisation</b> : Analysez les relations entre différentes variables et le taux de churn</li>
            <li><b>Prédiction</b> : Évaluez le risque de désabonnement d'un client spécifique</li>
            <li><b>Prédiction Multiple</b> : Analysez le risque pour un groupe de clients en important un fichier</li>
        </ol>
        """,
        unsafe_allow_html=True
    )

    # Note sur les données et l'API
    st.markdown(
        """
        <div class="info-section" style="margin-top: 30px;">
            <h3>À propos des données et de l'API</h3>
            <p>Cette application utilise une API dédiée pour les prédictions et l'analyse des données :</p>
            <ul>
                <li>La base de données est chargée depuis <a href="https://github.com/Awoutokoffisamson/machine_learning2_Documents/blob/main/Churn_Modelling.csv" target="_blank">GitHub</a></li>
                <li>Le modèle Random Forest est géré par l'API</li>
                <li>L'API fournit des endpoints pour les prédictions individuelles, par lot et les statistiques</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    afficher_accueil()