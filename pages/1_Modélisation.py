import numpy as np
import streamlit as st

from utils.funDBapp import *


st.set_page_config(layout="wide", page_title = "Modélisation")

st.sidebar.header("Modélisation")

col2, col3 = st.columns([5, 15], gap = "large")

with col2:
    st.image("https://forgemia.inra.fr/ludovic.mailleret/figures/-/raw/master/forest_dieback/forest_dieback.png", width=300)
with col3:
    st.markdown("$~$")
    st.markdown("# Dépérissement des forêts et points de basculement")

col12, col13 = st.columns([11, 10],gap = "large")

with col12:
    st.markdown("### D'après le modèle de [Ritchie *et al.* 2021](https://www.nature.com/articles/s41586-021-03263-2)")
    st.markdown(" - $v$ est la proportion de végétation dans l'environnement")
    st.markdown("- $g(.)$ le taux de croissance de la végétation")
    st.markdown("- $\gamma$ un taux de déforestation")
    st.markdown("Le modèle s'écrit :")
    st.markdown("$$ \dot v = g(.) v (1-v) - \gamma v $$")
    st.markdown("##")

with col13:
    st.markdown("##")
    st.markdown("Le taux de croissance a un maximum par rapport à la température locale $T$ :")
    st.markdown(r"$$ g(T) = g_0 \left[1-\left(\frac{T_{opt}-T}{\beta}\right)^2\right]$$")
    st.markdown("Par ailleurs, la température locale $T$ décroît avec la végétation :")
    st.markdown("$$ T = T_f + a (1-v) $$")
    st.markdown(r"Les paramètres $a$ et $\beta$ caractérisent la sensibilité de $g(.)$ et $T$ à la température locale et à la végétation, respectivement. $T_f$, est la valeur de la température de l'environnement à l'ombre.")
    st.markdown("###")

with st.expander(""):    
    col121, col131 = st.columns([11, 10],gap = "large")
    with col121:
        st.markdown("#### Dépendance de $g(.)$ en fonction de $T$")
        plotg(g_0, T_opt, beta)
        st.image("img/fig_g.png")

    with col131:
        st.markdown("#### Dépendance de $T$ en fonction de $v$")
        plotTofv(T_fbase, a)
        st.image("img/fig_Tofv.png")
