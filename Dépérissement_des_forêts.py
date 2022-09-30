import numpy as np
import streamlit as st

from utils.funDBapp import *

st.set_page_config(layout="wide", page_title = "Introduction", page_icon ="📚")

st.sidebar.header("Introduction")

col2, col3 = st.columns([5, 15], gap = "large")

with col2:
    st.image("https://forgemia.inra.fr/ludovic.mailleret/figures/-/raw/master/forest_dieback/forest_dieback.png", width=300)
with col3:
    st.markdown("$~$")
    st.markdown("# Dépérissement des forêts et points de bascule")

st.markdown("## Introduction")
st.markdown("Cette application introduit un modèle très simple de dépérissement des forêts proposé dans l'article scientifique [(Ritchie *et al.* 2021)](https://www.nature.com/articles/s41586-021-03263-2). Elle permet de :")
st.markdown("- simuler les dynamiques et observer les changements impliqués par des conditions initiales différentes")
st.markdown("- étudier l'influence de différents paramètres ou processus comme la température ou la déforestation, par l'intermédiaire de diagrammes de bifurcation")
st.markdown("- simuler l'influence de scenarios de changement climatique correspondant à des augmentations de la température de l'environnement") 

