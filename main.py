import streamlit as st
import pandas as pd
import numpy as np
import requests
import io
import pickle
import tempfile
from streamlit_option_menu import option_menu
from accueil import afficher_accueil
from visualisation import afficher_visualisation
from prediction import afficher_prediction
from multi_prediction import afficher_multi_prediction
from statistiques import afficher_statistiques
import hashlib
import os
from PIL import Image

# Configuration de la page
st.set_page_config(
    page_title="Fortuneo Banque - Prédiction de Churn",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# URLs des ressources
GITHUB_DATA_URL = "https://raw.githubusercontent.com/Awoutokoffisamson/machine_learning2_Documents/main/Churn_Modelling.csv"
DRIVE_MODEL_ID = "1JZji6K_r-Msko1xuk3R9ONycgPtliSK2"
API_BASE_URL = "https://machinelearning2api.onrender.com"  # URL de l'API locale
LOGO_URL = "https://raw.githubusercontent.com/Awoutokoffisamson/machine_learning2_Documents/main/logo.png"
BANK_IMAGE_URL = "https://raw.githubusercontent.com/Awoutokoffisamson/machine_learning2_Documents/main/image%20banque.png"

# Utilisateurs autorisés
AUTHORIZED_USERS = {
    "awoutokoffisamson@gmail.com": {
        "name": "M. AWOUTO K. Samson",
        "role": "Data scientist in Fortuneo Bank"
    },
    "annaatchou21@gmail.com": {
        "name": "Mlle Anna ATCHOU",
        "role": "Data scientist in Fortuneo Bank"
    },
    "bamogo6370@gmail.com": {
        "name": "BAMOGO Rasmané",
        "role": "Data scientist in Fortuneo Bank"
    },
    "Madjyamadoumbaye23@gmail.com": {
        "name": "Adoumbaye MDJIM",
        "role": "Data scientist in Fortuneo Bank"
    },
    "mouslydiaw@gmail.com": {
        "name": "Mme Mously DIAW",
        "role": "Professeur chargé du cours de Machine learning"
    }





    




    
}

# Mot de passe commun (hashé)
COMMON_PASSWORD_HASH = hashlib.sha256("machinelearning".encode()).hexdigest()

# Fonction d'authentification
def authenticate():
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user_info = None
    
    if not st.session_state.authenticated:
        st.markdown(
            """
            <style>
            .stApp {
                background-image: url(""" + BANK_IMAGE_URL + """);
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
                font-family: 'Roboto', sans-serif;
            }
            .auth-container {
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                max-width: 400px;
                width: 100%;
                padding: 40px;
                background-color: rgba(255, 255, 255, 0.9);
                border-radius: 15px;
                box-shadow: 0 10px 20px rgba(0, 0, 0, 0.3);
                text-align: center;
                border: 1px solid #e0e0e0;
            }
            .auth-logo {
                display: block;
                margin: 0 auto 30px auto;
                max-width: 150px;
            }
            .auth-title {
                font-size: 2.5rem;
                font-weight: bold;
                color: white;
                margin-bottom: 1rem;
            }
            .auth-subtitle {
                font-size: 1.2rem;
                color: white;
                font-weight: bold;
                margin-bottom: 2rem;
            }
            .stTextInput > div > div > input {
                border-radius: 5px;
                border: 1px solid #ccc;
                padding: 10px;
                font-size: 1rem;
                width: 80%;  /* Réduit la largeur */
                margin: 0 auto;
            }
            .stTextInput label {
                color: white;
                font-weight: bold;
                font-size: 1.1rem;
            }
            .stButton>button {
                background-color: #0052CC;
                color: white;
                border-radius: 5px;
                padding: 10px 20px;
                font-size: 1rem;
                font-weight: bold;
                transition: background-color 0.3s ease;
            }
            .stButton>button:hover {
                background-color: #003D99;
            }
            @media (max-width: 600px) {
                .auth-container {
                    width: 90%;
                    padding: 20px;
                }
                .auth-title {
                    font-size: 2rem;
                }
                .auth-subtitle {
                    font-size: 1rem;
                }
                .stTextInput > div > div > input {
                    width: 100%;
                }
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        
        # Bannière d'authentification
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        # Logo et titre
        st.image(LOGO_URL, width=150)
        
        st.markdown('<h1 class="auth-title">Fortuneo Banque</h1>', unsafe_allow_html=True)
        st.markdown('<p class="auth-subtitle">Outil de prédiction de churn</p>', unsafe_allow_html=True)
        
        # Formulaire d'authentification
        email = st.text_input("Email", key="email_input")
        password = st.text_input("Mot de passe", type="password", key="password_input")
        
        if st.button("Se connecter", key="login_button"):
            if email in AUTHORIZED_USERS and hashlib.sha256(password.encode()).hexdigest() == COMMON_PASSWORD_HASH:
                st.session_state.authenticated = True
                st.session_state.user_info = AUTHORIZED_USERS[email]
                st.success(f"Bienvenue, {AUTHORIZED_USERS[email]['name']} !")
                st.rerun()
            else:
                st.error("Email ou mot de passe incorrect.")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        return False
    
    return True

@st.cache_data
def load_data():
    """Charge les données depuis GitHub"""
    try:
        # Utiliser l'API pour obtenir les statistiques
        response = requests.get(f"{API_BASE_URL}/statistics")
        if response.status_code == 200:
            # Les statistiques contiennent déjà les informations agrégées
            # Nous avons toujours besoin des données brutes pour certaines visualisations
            data_response = requests.get(GITHUB_DATA_URL)
            data_response.raise_for_status()
            data = pd.read_csv(io.StringIO(data_response.text))
            return data
        else:
            # Fallback si l'API n'est pas disponible
            response = requests.get(GITHUB_DATA_URL)
            response.raise_for_status()
            data = pd.read_csv(io.StringIO(response.text))
            return data
    except Exception as e:
        st.error(f"Erreur lors du chargement des données: {e}")
        # Fallback sur un exemple de données
        return pd.DataFrame({
            'CreditScore': [619, 608, 502, 699, 850],
            'Geography': ['France', 'Spain', 'France', 'France', 'Spain'],
            'Gender': ['Female', 'Female', 'Female', 'Female', 'Female'],
            'Age': [42, 41, 42, 39, 43],
            'Tenure': [2, 1, 8, 1, 2],
            'Balance': [0.00, 83807.86, 159660.80, 0.00, 125510.82],
            'NumOfProducts': [1, 1, 3, 2, 1],
            'HasCrCard': [1, 0, 1, 0, 1],
            'IsActiveMember': [1, 1, 0, 0, 1],
            'EstimatedSalary': [101348.88, 112542.58, 113931.57, 93826.63, 79084.10],
            'Exited': [0, 0, 0, 0, 0]
        })

# Vérification de l'authentification
if authenticate():
    # Chargement des données
    data = load_data()

    # Configuration de la barre latérale avec des icônes
    with st.sidebar:
        # Logo Fortuneo au-dessus du menu principal
        st.image(LOGO_URL, width=150)
        
        # Informations utilisateur
        st.markdown(
            f"""
            <div style="background-color: #0052CC; padding: 10px; border-radius: 10px; text-align: center; margin-bottom: 20px;">
                <h2 style="color: white; margin: 0;">Fortuneo Banque</h2>
            </div>
            <div style="background-color: #f0f2f6; padding: 10px; border-radius: 5px; margin-bottom: 20px;">
                <p><b>{st.session_state.user_info['name']}</b><br>
                <small>{st.session_state.user_info['role']}</small></p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.title("Navigation")
        page = option_menu(
            menu_title="Menu principal",
            options=["Accueil", "Statistiques", "Visualisation", "Prédiction", "Prédiction Multiple"],
            icons=["house", "bar-chart-line", "graph-up", "person-check", "people"],
            menu_icon="bank",
            default_index=0,
            styles={
                "container": {"padding": "5px", "background-color": "#f0f2f6"},
                "icon": {"color": "#0052CC", "font-size": "18px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#e6f0ff",
                },
                "nav-link-selected": {"background-color": "#0052CC", "color": "white"},
            },
        )
        
        # Bouton de déconnexion
        if st.button("Déconnexion"):
            st.session_state.authenticated = False
            st.session_state.user_info = None
            st.rerun()

    # Affichage de la page choisie
    if page == "Accueil":
        afficher_accueil()
    elif page == "Statistiques":
        afficher_statistiques(data)
    elif page == "Visualisation":
        afficher_visualisation(data)
    elif page == "Prédiction":
        afficher_prediction(data)
    elif page == "Prédiction Multiple":
        afficher_multi_prediction(data)

    # Ajouter du style CSS pour améliorer l'esthétique globale
    st.markdown("""
        <style>
        .stApp {
            background-color: #f8f9fa;
        }
        .block-container {
            padding: 2rem;
            border-radius: 10px;
            background: white;
            box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
        }
        h1, h2, h3 {
            color: #0052CC;
        }
        h4, h5, h6 {
            color: #00468B;
        }
        .stButton>button {
            background-color: #0052CC;
            color: white;
            border-radius: 5px;
            border: none;
            padding: 0.5rem 1rem;
            font-weight: bold;
        }
        .stButton>button:hover {
            background-color: #003D99;
        }
        .stProgress .st-bo {
            background-color: #0052CC;
        }
        footer {
            visibility: hidden;
        }
        </style>
    """, unsafe_allow_html=True)

    # Pied de page personnalisé
    st.markdown(
        """
        <div style="position: fixed; bottom: 0; width: 100%; background-color: #f8f9fa; padding: 10px; text-align: center; border-top: 1px solid #ddd;">
            <p style="margin: 0; font-size: 0.8rem; color: #666;">© 2025 Fortuneo Banque - Outil de prédiction de churn</p>
        </div>
        """,
        unsafe_allow_html=True
    )      
        
