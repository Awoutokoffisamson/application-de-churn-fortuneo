import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import requests
import json

def afficher_statistiques(data):
    # Configuration du style de la page
    st.markdown(
        """
        <style>
        .stats-title {
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
        .metric-card {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            text-align: center;
            margin-bottom: 20px;
        }
        .metric-value {
            font-size: 2.5rem;
            font-weight: bold;
            color: #0052CC;
        }
        .metric-label {
            font-size: 1rem;
            color: #555;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Titre principal
    st.markdown('<h1 class="stats-title">Statistiques des clients</h1>', unsafe_allow_html=True)
    
    # Information sur les statistiques
    st.markdown(
        """
        <div class="info-box">
            <h4>Analyse statistique des données clients</h4>
            <p>Cette section présente les statistiques descriptives des données clients de Fortuneo Banque, 
            avec un focus sur les facteurs liés au désabonnement (churn).</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Tentative d'obtention des statistiques via l'API
    api_stats = None
    try:
        response = requests.get("https://machinelearning2api.onrender.com/statistics", timeout=15)
        if response.status_code == 200:
            api_stats = response.json()
        else:
            st.error(f"Erreur lors de l'appel à l'API : Code {response.status_code}")
            return
    except Exception as e:
        st.error(f"Impossible de se connecter à l'API : {e}")
        return
    
    # Métriques principales
    st.markdown('<h3 class="section-title">Métriques principales</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_clients = api_stats["total_clients"]
        
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{total_clients:,}</div>
                <div class="metric-label">Clients au total</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col2:
        churn_rate = api_stats["churn_rate"]
        
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{churn_rate:.1f}%</div>
                <div class="metric-label">Taux de churn global</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    with col3:
        # Trouver le pays avec le taux de churn le plus élevé
        highest_churn_country = max(api_stats["churn_by_country"].items(), key=lambda x: x[1]["churn_rate"])
        highest_churn_country_name = highest_churn_country[0]
        highest_churn_country_rate = highest_churn_country[1]["churn_rate"]
        
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-value">{highest_churn_country_rate:.1f}%</div>
                <div class="metric-label">Taux de churn le plus élevé ({highest_churn_country_name})</div>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Distribution du churn par pays
    st.markdown('<h3 class="section-title">Distribution du churn par pays</h3>', unsafe_allow_html=True)
    
    countries = list(api_stats["churn_by_country"].keys())
    churn_rates = [country_data["churn_rate"] for country_data in api_stats["churn_by_country"].values()]
    client_counts = [country_data["count"] for country_data in api_stats["churn_by_country"].values()]
    
    fig = px.bar(
        x=countries,
        y=churn_rates,
        text=[f"{rate:.1f}%" for rate in churn_rates],
        color=countries,
        labels={"x": "Pays", "y": "Taux de churn (%)"},
        title="Taux de churn par pays"
    )
    
    fig.update_layout(
        xaxis_title="Pays",
        yaxis_title="Taux de churn (%)",
        showlegend=False,
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Ajouter un graphique en camembert pour la répartition des clients par pays
    fig_pie = px.pie(
        names=countries,
        values=client_counts,
        title="Répartition des clients par pays",
        hole=0.4
    )
    
    fig_pie.update_layout(
        legend_title="Pays",
        template="plotly_white"
    )
    
    fig_pie.update_traces(
        textposition='inside', 
        textinfo='percent+label',
        hovertemplate='%{label}<br>Nombre: %{value}<br>Pourcentage: %{percent}'
    )
    
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Distribution du churn par genre
    st.markdown('<h3 class="section-title">Distribution du churn par genre</h3>', unsafe_allow_html=True)
    
    genders = list(api_stats["churn_by_gender"].keys())
    gender_churn_rates = [gender_data["churn_rate"] for gender_data in api_stats["churn_by_gender"].values()]
    gender_client_counts = [gender_data["count"] for gender_data in api_stats["churn_by_gender"].values()]
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            x=genders,
            y=gender_churn_rates,
            text=[f"{rate:.1f}%" for rate in gender_churn_rates],
            color=genders,
            labels={"x": "Genre", "y": "Taux de churn (%)"},
            title="Taux de churn par genre"
        )
        
        fig.update_layout(
            xaxis_title="Genre",
            yaxis_title="Taux de churn (%)",
            showlegend=False,
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        fig_pie = px.pie(
            names=genders,
            values=gender_client_counts,
            title="Répartition des clients par genre",
            hole=0.4
        )
        
        fig_pie.update_layout(
            legend_title="Genre",
            template="plotly_white"
        )
        
        fig_pie.update_traces(
            textposition='inside', 
            textinfo='percent+label',
            hovertemplate='%{label}<br>Nombre: %{value}<br>Pourcentage: %{percent}'
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Distribution du churn par tranche d'âge
    st.markdown('<h3 class="section-title">Distribution du churn par tranche d\'âge</h3>', unsafe_allow_html=True)
    
    age_groups = list(api_stats["churn_by_age_group"].keys())
    age_churn_rates = [age_data["churn_rate"] for age_data in api_stats["churn_by_age_group"].values()]
    age_client_counts = [age_data["count"] for age_data in api_stats["churn_by_age_group"].values()]
    
    fig = px.bar(
        x=age_groups,
        y=age_churn_rates,
        text=[f"{rate:.1f}%" for rate in age_churn_rates],
        color=age_groups,
        labels={"x": "Tranche d'âge", "y": "Taux de churn (%)"},
        title="Taux de churn par tranche d'âge"
    )
    
    fig.update_layout(
        xaxis_title="Tranche d'âge",
        yaxis_title="Taux de churn (%)",
        showlegend=False,
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Ajouter un graphique en barres pour la répartition des clients par tranche d'âge
    fig_bar = px.bar(
        x=age_groups,
        y=age_client_counts,
        text=[f"{count:,}" for count in age_client_counts],
        color=age_groups,
        labels={"x": "Tranche d'âge", "y": "Nombre de clients"},
        title="Répartition des clients par tranche d'âge"
    )
    
    fig_bar.update_layout(
        xaxis_title="Tranche d'âge",
        yaxis_title="Nombre de clients",
        showlegend=False,
        template="plotly_white"
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Distribution du churn par nombre de produits
    st.markdown('<h3 class="section-title">Distribution du churn par nombre de produits</h3>', unsafe_allow_html=True)
    
    products = list(api_stats["churn_by_products"].keys())
    product_churn_rates = [product_data["churn_rate"] for product_data in api_stats["churn_by_products"].values()]
    product_client_counts = [product_data["count"] for product_data in api_stats["churn_by_products"].values()]
    
    fig = px.bar(
        x=products,
        y=product_churn_rates,
        text=[f"{rate:.1f}%" for rate in product_churn_rates],
        color=products,
        labels={"x": "Nombre de produits", "y": "Taux de churn (%)"},
        title="Taux de churn par nombre de produits"
    )
    
    fig.update_layout(
        xaxis_title="Nombre de produits",
        yaxis_title="Taux de churn (%)",
        showlegend=False,
        template="plotly_white"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Ajouter un graphique en barres pour la répartition des clients par nombre de produits
    fig_bar = px.bar(
        x=products,
        y=product_client_counts,
        text=[f"{count:,}" for count in product_client_counts],
        color=products,
        labels={"x": "Nombre de produits", "y": "Nombre de clients"},
        title="Répartition des clients par nombre de produits"
    )
    
    fig_bar.update_layout(
        xaxis_title="Nombre de produits",
        yaxis_title="Nombre de clients",
        showlegend=False,
        template="plotly_white"
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Distribution du churn par statut de membre actif - AVEC VÉRIFICATION DE CLÉ
    st.markdown('<h3 class="section-title">Distribution du churn par statut de membre actif</h3>', unsafe_allow_html=True)
    
    # Vérifier si la clé existe dans la réponse de l'API
    if "churn_by_active_member" in api_stats:
        active_status = list(api_stats["churn_by_active_member"].keys())
        active_churn_rates = [active_data["churn_rate"] for active_data in api_stats["churn_by_active_member"].values()]
        active_client_counts = [active_data["count"] for active_data in api_stats["churn_by_active_member"].values()]
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                x=active_status,
                y=active_churn_rates,
                text=[f"{rate:.1f}%" for rate in active_churn_rates],
                color=active_status,
                labels={"x": "Membre actif", "y": "Taux de churn (%)"},
                title="Taux de churn par statut de membre actif"
            )
            
            fig.update_layout(
                xaxis_title="Membre actif",
                yaxis_title="Taux de churn (%)",
                showlegend=False,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig_pie = px.pie(
                names=active_status,
                values=active_client_counts,
                title="Répartition des clients par statut de membre actif",
                hole=0.4
            )
            
            fig_pie.update_layout(
                legend_title="Membre actif",
                template="plotly_white"
            )
            
            fig_pie.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                hovertemplate='%{label}<br>Nombre: %{value}<br>Pourcentage: %{percent}'
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
    else:
        # Afficher un message si la clé n'est pas disponible dans l'API
        st.info("Les statistiques par statut de membre actif ne sont pas disponibles dans cette version de l'API.")
        
        # Utiliser les données locales pour afficher une visualisation alternative
        active_member_data = data.groupby('IsActiveMember')['Exited'].agg(['count', 'mean']).reset_index()
        active_member_data['IsActiveMember'] = active_member_data['IsActiveMember'].map({0: 'Non actif', 1: 'Actif'})
        active_member_data.columns = ['Statut', 'Nombre de clients', 'Taux de churn']
        active_member_data['Taux de churn'] = active_member_data['Taux de churn'] * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig = px.bar(
                active_member_data,
                x='Statut',
                y='Taux de churn',
                text=[f"{rate:.1f}%" for rate in active_member_data['Taux de churn']],
                color='Statut',
                labels={'Taux de churn': 'Taux de churn (%)'}
            )
            
            fig.update_layout(
                title="Taux de churn par statut de membre actif (données locales)",
                xaxis_title="Statut de membre actif",
                yaxis_title="Taux de churn (%)",
                showlegend=False,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig_pie = px.pie(
                active_member_data,
                names='Statut',
                values='Nombre de clients',
                title="Répartition des clients par statut de membre actif (données locales)",
                hole=0.4
            )
            
            fig_pie.update_layout(
                legend_title="Statut de membre actif",
                template="plotly_white"
            )
            
            fig_pie.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                hovertemplate='%{label}<br>Nombre: %{value}<br>Pourcentage: %{percent}'
            )
            
            st.plotly_chart(fig_pie, use_container_width=True)
    
    # Recherche de client spécifique
    st.markdown('<h3 class="section-title">Recherche de client</h3>', unsafe_allow_html=True)
    
    st.markdown(
        """
        <div class="info-box">
            <h4>Rechercher un client spécifique</h4>
            <p>Utilisez cette section pour rechercher un client spécifique dans la base de données et afficher ses informations.</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Créer une liste déroulante pour sélectionner un client par ID
    customer_ids = data['CustomerId'].astype(str).tolist()
    selected_customer_id = st.selectbox("Sélectionner un client par ID", customer_ids)
    
    if selected_customer_id:
        # Filtrer les données pour le client sélectionné
        customer_data = data[data['CustomerId'].astype(str) == selected_customer_id].iloc[0]
        
        st.markdown('<div style="background-color: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("<h4>Informations personnelles</h4>", unsafe_allow_html=True)
            st.markdown(f"**ID Client:** {customer_data['CustomerId']}")
            st.markdown(f"**Nom:** {customer_data['Surname']}")
            st.markdown(f"**Score de crédit:** {customer_data['CreditScore']}")
            st.markdown(f"**Pays:** {customer_data['Geography']}")
            st.markdown(f"**Genre:** {customer_data['Gender']}")
            st.markdown(f"**Âge:** {customer_data['Age']} ans")
        
        with col2:
            st.markdown("<h4>Informations bancaires</h4>", unsafe_allow_html=True)
            st.markdown(f"**Ancienneté:** {customer_data['Tenure']} ans")
            st.markdown(f"**Solde:** {customer_data['Balance']:.2f} €")
            st.markdown(f"**Nombre de produits:** {customer_data['NumOfProducts']}")
            st.markdown(f"**Carte de crédit:** {'Oui' if customer_data['HasCrCard'] == 1 else 'Non'}")
            st.markdown(f"**Membre actif:** {'Oui' if customer_data['IsActiveMember'] == 1 else 'Non'}")
            st.markdown(f"**Salaire estimé:** {customer_data['EstimatedSalary']:.2f} €")
        
        # Afficher le statut de churn
        if customer_data['Exited'] == 1:
            st.markdown('<div style="background-color: #ffebee; padding: 10px; border-radius: 5px; margin-top: 20px;"><h4 style="color: #c62828; margin: 0;">Statut: Client perdu (Churn)</h4></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="background-color: #e8f5e9; padding: 10px; border-radius: 5px; margin-top: 20px;"><h4 style="color: #2e7d32; margin: 0;">Statut: Client actif</h4></div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    # Pour test local
    data = pd.read_csv("data/data.csv")
    afficher_statistiques(data)

    
   
