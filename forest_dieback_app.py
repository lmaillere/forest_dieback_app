import numpy as np
import streamlit as st

from funDBapp import *

st.set_page_config(layout="wide")

col1, col2, col3 = st.columns([3, 5, 15], gap = "large")

with col2:
    st.image("https://forgemia.inra.fr/ludovic.mailleret/figures/-/raw/master/forest_dieback/forest_dieback.png", width=300)
with col3:
    st.markdown("$~$")
    st.markdown("# Dépérissement des forêts et points de basculement")

col11, col12, col13 = st.columns([3,11, 10],gap = "large")

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
    
col111, col121, col131 = st.columns([3,11, 10],gap = "large")
with col121:
    st.markdown("#### Dépendance de $g(.)$ en fonction de $T$")
    plotg(g_0, T_opt, beta)
    st.image("img/fig_g.png")

with col131:
    st.markdown("#### Dépendance de $T$ en fonction de $v$")
    plotTofv(T_fbase, a)
    st.image("img/fig_T.png")

with col121:
    st.markdown("### Calculs et simulations")
    st.markdown("Saisissez les paramètres")

col21, col22, col23, col24 = st.columns([3, 7, 7, 7], gap = "large")
with col22:
    v0 = st.slider(' Proportion de végétation initiale', min_value=0., max_value=1., value = .3, step=0.05, disabled = False)  

with col23:
    gamma = st.slider(' Taux de déforestation', min_value=0.1, max_value=.7, value = .3, step=0.05) 

with col24:
    T_f =  st.slider(' Température de l\'environnement à l\'ombre', min_value=16., max_value=30., value = T_fbase, step=0.5)  

# encapsulation
params_sim = np.array([g_0, T_opt, beta, T_f, a, gamma])

col31, col32, col3b, col33, col34 = st.columns([3.5, 5.5, .5, 12, 2.5],gap = "large")
with col32:
    plotChoice = st.selectbox("Que voulez vous tracer ?",
                ("Dynamiques", "Synthèse des dynamiques", "Équilibres", "Bifurcations / perturbations", "Bifurcations / température"),
                index=0
                )
    
    if plotChoice == "Bifurcations / température" or plotChoice == "Bifurcations / perturbations":
        plotTraj = st.checkbox("Tracer la trajectoire")
    
    if plotChoice == "Bifurcations / température":
        climChange = st.checkbox("Simuler une augmentation de la température ?")
        Tslope = st.slider("Vitesse d'accroissement de la Température",  min_value=0., max_value=.15, value = .08, step=0.01, disabled = not climChange)  


with col33:
    if plotChoice == "Dynamiques":
        fig_sim = plotSim(v0 = v0, gamma = gamma, T_f = T_f, params = params_sim)
        st.pyplot(fig_sim)
    elif plotChoice == "Synthèse des dynamiques":
        fig_all = plotSimAll(gamma = gamma, T_f = T_f, params = params_sim)
        st.pyplot(fig_all)
    elif plotChoice == "Équilibres":
        fig_eqs = plotEqs(gamma = gamma, T_f = T_f, params = params_sim)
        st.pyplot(fig_eqs)
    elif plotChoice == "Bifurcations / perturbations":
        fig_gam = plotBifGamma(v0 =v0, gamma = gamma, T_f = T_f, params = params_sim, plotTraj = plotTraj)
        st.pyplot(fig_gam)
    elif plotChoice == "Bifurcations / température":
        fig_T = plotBifTf(v0 = v0, gamma = gamma, T_f = T_f, params = params_sim, plotTraj = plotTraj, climChange = climChange, Tslope = Tslope)
        st.pyplot(fig_T)
