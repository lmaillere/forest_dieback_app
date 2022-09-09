import numpy as np
import streamlit as st

from utils.funDBapp import *

st.set_page_config(layout="wide", page_title = "Simulations", page_icon ="📈")

st.sidebar.header("Simulations")

col2, col3 = st.columns([5, 15], gap = "large")

with col2:
    st.image("https://forgemia.inra.fr/ludovic.mailleret/figures/-/raw/master/forest_dieback/forest_dieback.png", width=300)
with col3:
    st.markdown("$~$")
    st.markdown("# Dépérissement des forêts et points de basculement")


col121, col131 = st.columns([11, 10],gap = "large")

with col121:
    st.markdown("### Calculs et simulations")
    st.markdown("Saisissez les paramètres")

col22, col23, col24 = st.columns([7, 7, 7], gap = "large")
with col22:
    v0 = st.slider(' Proportion de végétation initiale', min_value=0., max_value=1., value = .3, step=0.05, disabled = False)  

with col23:
    gamma = st.slider(' Taux de déforestation', min_value=0.1, max_value=.7, value = .3, step=0.05) 

with col24:
    T_f =  st.slider(' Température de l\'environnement à l\'ombre', min_value=16., max_value=30., value = T_fbase, step=0.5)  

# encapsulation
params_sim = np.array([g_0, T_opt, beta, T_f, a, gamma])

col32, col33 = st.columns([10, 15],gap = "large")
with col32:
    plotChoice = st.selectbox("Que voulez vous tracer ?",
                ("Dynamiques", "Synthèse des dynamiques", "Équilibres", "Bifurcations / perturbations", "Bifurcations / température", "Simuler une augmentation de la température ?"), index=0)
    
    if plotChoice == "Bifurcations / température" or plotChoice == "Bifurcations / perturbations":
        Tslope = 0
        plotTraj = st.checkbox("Tracer la trajectoire")
        if plotTraj:
            fig_sim = plotSim(v0 = v0, gamma = gamma, T_f = T_f, params = params_sim)
            st.pyplot(fig_sim)
    
    
    if plotChoice == "Simuler une augmentation de la température ?":
        climChange = True
        plotTraj = True
        Tslope = st.slider("Vitesse d'accroissement de la Température",  min_value=0., max_value=.15, value = .02, step=0.01)  
        # il manque la sim contre le temps ici
        fig_sim_climChg = plotSimClimchg(v0 = v0, gamma = gamma, T_f = T_f, params = params_sim, plotTraj = plotTraj, climChange = climChange, Tslope = Tslope)
        st.pyplot(fig_sim_climChg)


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
        climChange = False
        fig_T = plotBifTf(v0 = v0, gamma = gamma, T_f = T_f, params = params_sim, plotTraj = plotTraj, climChange = climChange, Tslope = Tslope)
        st.pyplot(fig_T)
    elif plotChoice == "Simuler une augmentation de la température ?":
        climChange = True
        plotTraj = True
        fig_TclimChg = plotBifTf(v0 = v0, gamma = gamma, T_f = T_f, params = params_sim, plotTraj = plotTraj, climChange = climChange, Tslope = Tslope)
        st.pyplot(fig_TclimChg)