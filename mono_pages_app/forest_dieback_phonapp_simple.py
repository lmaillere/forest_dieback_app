import numpy as np
import streamlit as st

from utils.funDBapp import *

col1, col2, col3 = st.columns([0.5, 5, 1])

with col2:
    st.image("https://forgemia.inra.fr/ludovic.mailleret/figures/-/raw/master/forest_dieback/forest_dieback.png", width = 400)
    st.markdown("## Dépérissement des forêts et points de bascule")

with col2:
    tab1, tab2 = st.tabs(["Modèle", "Simulations"])

    with tab1: 
        st.markdown("### Modèle de [Ritchie *et al.* 2021](https://www.nature.com/articles/s41586-021-03263-2)")
        # st.markdown("$$ \dot v = g(.) v (1-v) - \gamma v $$")
        # st.markdown(" - $v$ est la proportion de végétation dans l'environnement")
        # st.markdown("- $g(.)$ le taux de croissance de la végétation")
        # st.markdown("- $\gamma$ un taux de perturbation")
        st.markdown(" - $v$ est la proportion de végétation dans l'environnement")
        st.markdown("- $g(.)$ le taux de croissance de la végétation")
        st.markdown("- $\gamma$ un taux de déforestation")
        st.markdown("Le modèle s'écrit :")
        st.markdown("$$ \dot v = g(.) v (1-v) - \gamma v $$")
        st.markdown("##")
        st.markdown("Le taux de croissance a un maximum par rapport à la température locale $T$ :")
        st.markdown(r"$$ g(T) = g_0 \left[1-\left(\frac{T_{opt}-T}{\beta}\right)^2\right]$$")
        st.markdown("Par ailleurs, la température locale $T$ décroît avec la végétation :")
        st.markdown("$$ T = T_f + a (1-v) $$")
        st.markdown(r"Les paramètres $a$ et $\beta$ caractérisent la sensibilité de $g(.)$ et $T$ à la température locale et à la végétation, respectivement. $T_f$ est la température de l'environnement à l'ombre.")

    with tab2:

        st.markdown("### Calculs et simulations")

        plotChoice = st.radio("Que voulez vous tracer ?",
                        ("Dynamiques", "Synthèse des dynamiques"),
                        index=0
                        )

        st.markdown("#### Paramètres")

        if plotChoice == "Dynamiques":
            v0 = st.slider(' Proportion de végétation initiale', min_value=0., max_value=1., value = .5, step=0.05)  
        
        gamma = st.slider(' Taux de déforestation', min_value=.1, max_value=.7, value = .1, step=0.1) 
        T_f =  st.slider(' Température de l\'environnement à l\'ombre', min_value=19., max_value=30., value = T_fbase, step=1.)  

        params_sim = np.array([g_0, T_opt, beta, T_f, a, gamma])

        st.markdown("#### Simulations")

        # plot of the figs
        if plotChoice == "Dynamiques":
            fig_sim = plotSim(v0 = v0, gamma = gamma, T_f = T_f, params = params_sim)
            st.pyplot(fig_sim)
        elif plotChoice == "Synthèse des dynamiques":
            fig_all = plotSimAll(gamma = gamma, T_f = T_f, params = params_sim)
            st.pyplot(fig_all)
