import numpy as np
import streamlit as st

from utils.funDBapp import *

st.set_page_config(layout="wide", page_title = "Simulations")

st.sidebar.header("Simulations")

col2, col3 = st.columns([5, 15], gap = "large")

with col2:
    st.image("https://forgemia.inra.fr/ludovic.mailleret/figures/-/raw/master/forest_dieback/forest_dieback.png", width=300)
with col3:
    st.markdown("$~$")
    st.markdown("# Dépérissement des forêts et points de basculement")
