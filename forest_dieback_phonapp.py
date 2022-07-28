import numpy as np
import streamlit as st

from funDBapp import *

col1, col2, col3 = st.columns([1, 5,2])

with col2:
    st.image("https://forgemia.inra.fr/ludovic.mailleret/figures/-/raw/master/forest_dieback/forest_dieback.png")#, width = 300)

st.markdown("## Dépérissement des forêts et points de basculement")

st.markdown("### Modèle de [Ritchie *et al.* 2021](https://www.nature.com/articles/s41586-021-03263-2)")
st.markdown("$$ \dot v = g(.) v (1-v) - \gamma v $$")
st.markdown(" - $v$ est la proportion de végétation dans l'environnement")
st.markdown("- $g(.)$ le taux de croissance de la végétation")
st.markdown("- $\gamma$ un taux de perturbation")

st.markdown("### Calculs et simulations")

v0 = st.slider(' Proportion de végétation initiale', min_value=0., max_value=1., value = .3, step=0.05)  
gamma = st.slider(' Taux de perturbation', min_value=.1, max_value=.7, value = .3, step=0.05) 
T_f =  st.slider(' Température de forçage', min_value=16., max_value=30., value = 22., step=0.5)  

params_sim = np.array([g_0, T_opt, beta, T_f, a, gamma])

plotChoice = st.radio("Que voulez vous tracer ?",
                ("Dynamiques", "Synthèse des dynamiques", "Équilibres", "Bifurcations / perturbations", "Bifurcations / température"),
                index=0
                )

if plotChoice == "Bifurcations / température" or plotChoice == "Bifurcations / perturbations":
        plotTraj = st.checkbox("Tracer la trajectoire")
    
if plotChoice == "Bifurcations / température":
    climChange = st.checkbox("Simuler une augmentation de la température ?")
    Tslope = st.slider("Vitesse d'accroissement de la Température",  min_value=0., max_value=.15, value = .08, step=0.01, disabled = not climChange)  

if plotChoice == "Dynamiques":
    plotSim(v0 = v0, gamma = gamma, T_f = T_f, params = params_sim)
elif plotChoice == "Synthèse des dynamiques":
    plotSimAll(gamma = gamma, T_f = T_f, params = params_sim)
elif plotChoice == "Équilibres":
    plotEqs(gamma = gamma, T_f = T_f, params = params_sim)
elif plotChoice == "Bifurcations / perturbations":
    plotBifGamma(v0 =v0, gamma = gamma, T_f = T_f, params = params_sim, plotTraj = plotTraj)
elif plotChoice == "Bifurcations / température":
    plotBifTf(v0 = v0, gamma = gamma, T_f = T_f, params = params_sim, plotTraj = plotTraj, climChange = climChange, Tslope = Tslope)
