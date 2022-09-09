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
    st.markdown("# Dépérissement des forêts et points de basculement")

st.markdown("*Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.*")
