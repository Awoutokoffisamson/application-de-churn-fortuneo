import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def afficher_visualisation(data):
    # Configuration du style de la page
    st.markdown(
        """
        <style>
        .viz-title {
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
        </style>
        """,
        unsafe_allow_html=True
    )

    # Titre principal
    st.markdown('<h1 class="viz-title">Visualisation des données</h1>', unsafe_allow_html=True)
    
    # Information sur les données
    st.markdown(
        """
        <div class="info-box">
            <h4>Analyse visuelle des facteurs de churn</h4>
            <p>Cette section présente des visualisations interactives pour explorer les relations entre différentes variables 
            et le taux de désabonnement (churn) des clients de Fortuneo Banque.</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Aperçu des données
    with st.expander("Aperçu des données"):
        # Ajout de la recherche client
        client_search = st.text_input("Rechercher un client par ID, nom ou autre critère", "")
        
        if client_search:
            # Recherche dans toutes les colonnes
            filtered_data = data[data.astype(str).apply(lambda x: x.str.contains(client_search, case=False)).any(axis=1)]
            if not filtered_data.empty:
                st.dataframe(filtered_data, use_container_width=True)
                st.write(f"**{len(filtered_data)}** clients trouvés")
            else:
                st.warning("Aucun client trouvé avec ces critères")
        else:
            st.dataframe(data.head(10), use_container_width=True)
        
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Nombre total de clients:** {len(data):,}")
        with col2:
            st.write(f"**Taux de churn global:** {data['Exited'].mean()*100:.1f}%")

    # Onglets pour différentes visualisations
    tab1, tab2, tab3, tab4 = st.tabs(["Distribution du churn", "Analyse démographique", "Analyse financière", "Corrélations"])
    
    # Onglet 1: Distribution du churn
    with tab1:
        st.markdown('<h3 class="section-title">Distribution du churn</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Diagramme circulaire du churn
            churn_counts = data['Exited'].value_counts().reset_index()
            churn_counts.columns = ['Statut', 'Nombre']
            churn_counts['Statut'] = churn_counts['Statut'].map({0: 'Fidèle', 1: 'Churné'})
            churn_counts['Pourcentage'] = churn_counts['Nombre'] / churn_counts['Nombre'].sum() * 100
            
            fig = px.pie(
                churn_counts, 
                values='Nombre', 
                names='Statut',
                color='Statut',
                color_discrete_map={'Fidèle': "#0052CC", 'Churné': "#FF5252"},
                hole=0.4,
                labels={'Statut': 'Statut du client'}
            )
            
            fig.update_layout(
                title="Distribution des clients par statut",
                legend_title="Statut",
                template="plotly_white"
            )
            
            fig.update_traces(
                textposition='inside', 
                textinfo='percent+label',
                hovertemplate='%{label}<br>Nombre: %{value}<br>Pourcentage: %{percent}'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Churn par pays
            country_churn = data.groupby('Geography')['Exited'].agg(['count', 'mean']).reset_index()
            country_churn.columns = ['Pays', 'Nombre de clients', 'Taux de churn']
            country_churn['Taux de churn'] = country_churn['Taux de churn'] * 100
            
            fig = px.bar(
                country_churn,
                x='Pays',
                y='Taux de churn',
                color='Pays',
                text_auto='.1f',
                labels={'Taux de churn': 'Taux de churn (%)'}
            )
            
            fig.update_layout(
                title="Taux de churn par pays",
                xaxis_title="Pays",
                yaxis_title="Taux de churn (%)",
                showlegend=False,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Churn par genre et pays
        gender_country_churn = data.groupby(['Geography', 'Gender'])['Exited'].agg(['count', 'mean']).reset_index()
        gender_country_churn.columns = ['Pays', 'Genre', 'Nombre de clients', 'Taux de churn']
        gender_country_churn['Taux de churn'] = gender_country_churn['Taux de churn'] * 100
        
        fig = px.bar(
            gender_country_churn,
            x='Pays',
            y='Taux de churn',
            color='Genre',
            barmode='group',
            text_auto='.1f',
            labels={'Taux de churn': 'Taux de churn (%)'}
        )
        
        fig.update_layout(
            title="Taux de churn par pays et genre",
            xaxis_title="Pays",
            yaxis_title="Taux de churn (%)",
            legend_title="Genre",
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Onglet 2: Analyse démographique
    with tab2:
        st.markdown('<h3 class="section-title">Analyse démographique</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Distribution de l'âge par statut de churn
            fig = px.histogram(
                data,
                x="Age",
                color="Exited",
                marginal="box",
                opacity=0.7,
                barmode="overlay",
                color_discrete_map={0: "#0052CC", 1: "#FF5252"},
                labels={"Exited": "A quitté la banque", "Age": "Âge"}
            )
            
            fig.update_layout(
                title="Distribution de l'âge par statut",
                xaxis_title="Âge",
                yaxis_title="Nombre de clients",
                legend_title="Statut",
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Taux de churn par tranche d'âge
            data['Age_Group'] = pd.cut(
                data['Age'],
                bins=[0, 30, 40, 50, 60, 100],
                labels=['<30', '30-40', '40-50', '50-60', '>60']
            )
            
            age_churn = data.groupby('Age_Group')['Exited'].agg(['count', 'mean']).reset_index()
            age_churn.columns = ['Tranche d\'âge', 'Nombre de clients', 'Taux de churn']
            age_churn['Taux de churn'] = age_churn['Taux de churn'] * 100
            
            fig = px.bar(
                age_churn,
                x='Tranche d\'âge',
                y='Taux de churn',
                color='Tranche d\'âge',
                text_auto='.1f',
                labels={'Taux de churn': 'Taux de churn (%)'}
            )
            
            fig.update_layout(
                title="Taux de churn par tranche d'âge",
                xaxis_title="Tranche d'âge",
                yaxis_title="Taux de churn (%)",
                showlegend=False,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Ancienneté vs Churn
        tenure_churn = data.groupby('Tenure')['Exited'].agg(['count', 'mean']).reset_index()
        tenure_churn.columns = ['Ancienneté', 'Nombre de clients', 'Taux de churn']
        tenure_churn['Taux de churn'] = tenure_churn['Taux de churn'] * 100
        
        fig = px.line(
            tenure_churn,
            x='Ancienneté',
            y='Taux de churn',
            markers=True,
            labels={'Taux de churn': 'Taux de churn (%)', 'Ancienneté': 'Ancienneté (années)'}
        )
        
        fig.update_layout(
            title="Taux de churn par ancienneté",
            xaxis_title="Ancienneté (années)",
            yaxis_title="Taux de churn (%)",
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Onglet 3: Analyse financière
    with tab3:
        st.markdown('<h3 class="section-title">Analyse financière</h3>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Balance vs Churn
            fig = px.box(
                data,
                x="Exited",
                y="Balance",
                color="Exited",
                color_discrete_map={0: "#0052CC", 1: "#FF5252"},
                labels={"Exited": "A quitté la banque", "Balance": "Solde du compte"}
            )
            
            fig.update_layout(
                title="Distribution du solde par statut",
                xaxis_title="Statut (0=Fidèle, 1=Churné)",
                yaxis_title="Solde du compte",
                showlegend=False,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Score de crédit vs Churn
            fig = px.violin(
                data,
                x="Exited",
                y="CreditScore",
                color="Exited",
                box=True,
                color_discrete_map={0: "#0052CC", 1: "#FF5252"},
                labels={"Exited": "A quitté la banque", "CreditScore": "Score de crédit"}
            )
            
            fig.update_layout(
                title="Distribution du score de crédit par statut",
                xaxis_title="Statut (0=Fidèle, 1=Churné)",
                yaxis_title="Score de crédit",
                showlegend=False,
                template="plotly_white"
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Nombre de produits vs Churn
        products_churn = data.groupby('NumOfProducts')['Exited'].agg(['count', 'mean']).reset_index()
        products_churn.columns = ['Nombre de produits', 'Nombre de clients', 'Taux de churn']
        products_churn['Taux de churn'] = products_churn['Taux de churn'] * 100
        
        fig = px.bar(
            products_churn,
            x='Nombre de produits',
            y='Taux de churn',
            color='Nombre de produits',
            text_auto='.1f',
            labels={'Taux de churn': 'Taux de churn (%)'}
        )
        
        fig.update_layout(
            title="Taux de churn par nombre de produits",
            xaxis_title="Nombre de produits",
            yaxis_title="Taux de churn (%)",
            showlegend=False,
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Onglet 4: Corrélations
    with tab4:
        st.markdown('<h3 class="section-title">Matrice de corrélation</h3>', unsafe_allow_html=True)
        
        # Préparation des données pour la corrélation
        # CORRECTION: Sélectionner uniquement les colonnes numériques pour éviter l'erreur
        numeric_data = data.select_dtypes(include=['number'])
        
        # Calcul de la matrice de corrélation sur les données numériques uniquement
        corr_matrix = numeric_data.corr()
        
        # Création de la heatmap avec Plotly
        fig = px.imshow(
            corr_matrix,
            text_auto='.2f',
            aspect="auto",
            color_continuous_scale='RdBu_r',
            zmin=-1, zmax=1
        )
        
        fig.update_layout(
            title="Matrice de corrélation des variables numériques",
            width=800,
            height=800,
            template="plotly_white"
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Explication des corrélations importantes
        st.markdown(
            """
            <div class="info-box">
                <h4>Interprétation des corrélations</h4>
                <p>Les corrélations les plus fortes avec le churn (Exited) sont :</p>
                <ul>
                    <li><strong>Âge</strong> : Corrélation positive modérée de 0.29. Cela indique que les clients plus âgés ont une tendance légèrement plus forte à quitter la banque, suggérant que l'âge est un facteur contributif au churn.</li>
    
            </div>
            """,
            unsafe_allow_html=True
        )

if __name__ == "__main__":
    # Pour test local
    data = pd.read_csv("data/data.csv")
    afficher_visualisation(data)

