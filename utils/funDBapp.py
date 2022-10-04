import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import streamlit as st
import matplotlib.image as image

# nickname for Polynomial function
P = np.polynomial.Polynomial

#######################################
# parameters
g_0 = 1.
T_opt = 26.
beta = 8.5
a = 12.
T_fbase = 24.

#From Ritchie et al. 2021, adapted to Amazonian forest dieback
# g_0 = 2.
#T_opt = 28.
# beta = 10.
# a = 5.
#T_fbase = 26.

#########################################################
# general fonctions

# taux de croissance en fonction de la température
def g_of_T_climChg(T, g_0, T_opt, beta):
    return g_0*(1-((T_opt-T)/beta)**2)

# température en fonction de la végétation
def T_of_v_climChg(v, T_f, a):
    return T_f + a * (1-v)

# taux de croissance fonction de la végétation (et du temps si scenario accroissement temperature)
def g_of_v_climChg(v, t, params, Tslope):
    g_0, T_opt, beta, T_f, a, gamma = params
    return g_of_T_climChg(T_of_v_climChg(v, T_fChg(t, T_f, Tslope), a), g_0, T_opt, beta)

# Temperature de forcage, qui peut augmenter avec le temps
def T_fChg(t, T_f, Tslope): 
    return T_f + Tslope * t

#########################################################
# functions plotting g(T) and T(v)
def plotg(g_0, T_opt, beta):
    fig_g, ax_g = plt.subplots(figsize=(5, 3))

    Tplot = np.arange(T_opt - 8., T_opt + 8., .1)

    ax_g.plot(Tplot, g_of_T_climChg(Tplot, g_0, T_opt, beta))
    
    ax_g.set_xlabel("température $T$")
    ax_g.set_ylabel("taux de croissance $g(T)$")

    ax_g.grid()

    fig_g.savefig("img/fig_g.png",bbox_inches='tight')

def plotTofv(T_f, a):
    fig_T, ax_T = plt.subplots(figsize=(5, 3))

    v_plotT = np.arange(0, 1.01, .01)

    ax_T.plot(v_plotT, T_of_v_climChg(v_plotT, T_f, a))

    ax_T.set_ylabel("température $T$")
    ax_T.set_xlabel("proportion de végétation $v$")

    ax_T.grid()

    fig_T.savefig("img/fig_Tofv.png",bbox_inches='tight')
    

#########################################################
# partie intégration du modèle / dynamiques

# définition d'un vecteur tspan 
t_0 = 0             # temps initial
t_fin = 10.0        # temps final
pas_t = 0.01        # pas de temps de récupération des variables entre t_0 et t_fin
tspan = np.arange(t_0, t_fin, pas_t)
long_tspan = np.arange(t_0, 15*t_fin, pas_t)

#######################################################
# partie bifurcation vs T_f, scenario d'accroissement de la température

# modèle pouvant prendre en compte l'accroissement de la température
def modeleFDB_climChg(etat, t, params_sim, Tslope): 
    v = etat              # on recupere l'etat
    gamma = params_sim[-1]     # on récupère les paramètres
    vdot = g_of_v_climChg(v, t, params_sim, Tslope)*v*(1-v) - gamma * v # la derivee 
    return vdot

# fonction pour intégration et plot des dynamiques
@st.experimental_singleton
def plotSim(v0, gamma, T_f, params, tspan = tspan):
    g_0, T_opt, beta = params[0:3]
    a = params[4]
    params_sim = np.array([g_0, T_opt, beta, T_f, a, gamma])
    
    int_FDB = odeint(modeleFDB_climChg, v0, tspan, args=(params_sim, 0), hmax=pas_t)
    
    # figure
    fig1, ax1 = plt.subplots(figsize=(8, 6))  

    # tracé des simulations par rapport au temps
    ax1.plot(tspan, int_FDB, color='C0', label='proportion de végétation')

    # tracé des équilibres positifs
    v_roots = getEqs(gamma = gamma, T_f = T_f, params = params_sim)[0]

    mycolors = ['C3', 'C2']
    mylabels = ['équilibre instable', 'équilibre stable']

    for i in range(v_roots.size):
        ax1.plot(tspan, np.ones(tspan.shape)*v_roots[-1-i], color = mycolors[-1-i], label = mylabels[-1-i], linestyle = (0, (3, 7)))

    # tracé de l'équilibre nul
    col0, lab0 = 'C2', ''
    if v_roots.size == 1: col0, lab0 ='C3', "équilibre instable" 
    if v_roots.size == 0: lab0 = "équilibre stable"
    ax1.plot(tspan, np.ones(tspan.shape)*0, linestyle = (0, (3, 7)), color = col0, label = lab0)
    
    # ajout de petites imagettes
    im1 = image.imread("img/forest.png") 
    im2 = image.imread("img/desert.png") 
    
    if v_roots.size > 0:
        # put a new axes where you want the image to appear
        # (x, y, width, height)
        imax1 = fig1.add_axes([.77, (69+384*v_roots[-1])/510+.01, 0.1, 0.1])
        # remove ticks & the box from imax 
        imax1.set_axis_off()
        # print the logo with aspect="equal" to avoid distorting the logo
        imax1.imshow(im1, aspect="equal")
    
    imax2 = fig1.add_axes([.78, 0.17, 0.08, 0.08])
    imax2.set_axis_off()
    imax2.imshow(im2, aspect="equal")

    ax1.legend(fontsize='10', loc = 'upper left')
    ax1.set_xlabel('temps', fontsize='12')
    ax1.set_ylabel('proportion de végétation $v$', fontsize='12')
    fig1.suptitle(r'Proportion de végétation $v$', va='top', fontsize='14')
    ax1.set_ylim(bottom = -.05, top=1)
    ax1.grid()

    # returns the figure object
    return fig1
    
# fonction pour intégration et plot de toutes les dynamiques
@st.experimental_singleton
def plotSimAll(gamma, T_f, params, tspan = tspan):
    g_0, T_opt, beta = params[0:3]
    a = params[4]
    params_sim = np.array([g_0, T_opt, beta, T_f, a, gamma])

    v0_span = np.arange(.1, 1.1, .1)
    labSimAll = np.full(v0_span.shape, '')
    labSimAll = np.append(labSimAll, "proportion de végétation")
    labSimAll = np.delete(labSimAll, 0)

    # figure
    figS, axS = plt.subplots(figsize=(8, 6))  
    
    # redéfinition du cycle des couleurs pour un dégradé de bleu
    colorSimAll = plt.cm.Blues(np.linspace(.3, .8, v0_span.size))
    axS.set_prop_cycle(color = colorSimAll)

    # calcul des différentes dynamiques et plot
    for i in range(v0_span.size):
        int_FDB = odeint(modeleFDB_climChg, v0_span[i], tspan, args=(params_sim, 0), hmax=pas_t)
        axS.plot(tspan, int_FDB, label=labSimAll[i])
    
    v_roots = getEqs(gamma = gamma, T_f = T_f, params = params_sim)[0]

    mycolors = ['C3', 'C2']
    mylabels = ['équilibre instable', 'équilibre stable']

    for i in range(v_roots.size):
        axS.plot(tspan, np.ones(tspan.shape)*v_roots[-1-i], color = mycolors[-1-i], label = mylabels[-1-i], linestyle = (0, (3, 7)))

    # tracé de l'équilibre nul
    col0, lab0 = 'C2', ''
    if v_roots.size == 1: col0, lab0 ='C3', "équilibre instable" 
    if v_roots.size == 0: lab0 = "équilibre stable"
    axS.plot(tspan, np.ones(tspan.shape)*0, linestyle = (0, (3, 7)), color = col0, label = lab0)
    
    # test ajout de petites imagettes
    im1 = image.imread("img/forest.png") 
    im2 = image.imread("img/desert.png") 
    
    if v_roots.size > 0:
        # put a new axes where you want the image to appear
        # (x, y, width, height)
        imax1 = figS.add_axes([.77, (69+384*v_roots[-1])/510+.01, 0.1, 0.1])
        # remove ticks & the box from imax 
        imax1.set_axis_off()
        # print the logo with aspect="equal" to avoid distorting the logo
        imax1.imshow(im1, aspect="equal")
    
    imax2 = figS.add_axes([.78, 0.17, 0.08, 0.08])
    imax2.set_axis_off()
    imax2.imshow(im2, aspect="equal")

    axS.legend(fontsize='10', loc = "upper left")
    axS.set_xlabel('temps', fontsize='12')
    axS.set_ylabel('proportion de végétation $v$', fontsize='12')
    figS.suptitle(r'Proportion de végétation $v$', va='top', fontsize='14')
    axS.set_ylim(bottom = -.05, top=1)
    axS.grid()

    # returns the figure object
    return figS

##############################################################
# partie equilibres

# calcule les racines (équilibres v^* > 0)
def getEqs(gamma, T_f, params):
    # g_0, T_opt, beta, T_f, a, gamma = params est la structure attendue
    g_0, T_opt, beta = params[0:3]
    a = params[4]
    params_sim = np.array([g_0, T_opt, beta, T_f, a, gamma])
    
    v = P([0, 1]) # définition de monôme
    # def polynôme définissant les équilibres v^* > 0
    Q = g_of_v_climChg(v, t=0, params = params_sim, Tslope =0)*(1-v)-gamma 
    
    v_roots = Q.roots()[(np.isreal(Q.roots())) * (Q.roots() < 1) * (Q.roots() > 0) ] # on récupère seulement les racines entre 0 et 1
    y_roots = [gamma/(1-v) for v in v_roots] # ordonnée pour le plot des coursbes définissant les éqs
    
    return v_roots, y_roots

# plot les courbes définissant les eq positifs et plotte les équilibres positifs
@st.experimental_singleton
def plotEqs(gamma, T_f, params):
    g_0, T_opt, beta = params[0:3]
    a = params[4]
    params_sim = np.array([g_0, T_opt, beta, T_f, a, gamma]) 
    v_plot = np.arange(0, 1, .01)
    
    # plot
    fig0, ax0 = plt.subplots(figsize=(8, 6))  # création d'une figure, et d'un système d'axes
    
    # tracé de g(.) fonction de la température
    ax0.plot(v_plot, g_of_v_climChg(v_plot, t=0, params = params_sim, Tslope = 0), color='C0', label='taux de croissance') 
    ax0.plot(v_plot, gamma/(1-v_plot), color='C1', label=r'$\frac{\gamma}{1-v}$') 

    # tracé des intersections des courbes = équilibres
    v_roots, y_roots = getEqs(gamma = gamma, T_f = T_f, params = params_sim)

    mycolors = ['C3', 'C2']
    mylabels = ['équilibre instable', 'équilibre stable']

    for i in range(v_roots.size):
        ax0.plot(v_roots[-1-i], y_roots[-1-i], 'o', color = mycolors[-1-i], label = mylabels[-1-i]) # to be sure the latest elements of v_roots is plot in C0

    ax0.legend(fontsize='10')
    ax0.set_xlabel('proportion de végétation $v$', fontsize='12')
    ax0.set_ylabel('courbes', fontsize='12')
    fig0.suptitle('Équilibres aux intersections', va='top', fontsize='14')
    ax0.grid()
    ax0.set_ylim(bottom=-.1, top=1.5)

    # returns the figure object
    return fig0

#################################################################
# partie bifurcation vs gamma
@st.experimental_singleton
def plotBifGamma(v0, gamma, T_f,  params, plotTraj):
    g_0, T_opt, beta = params[0:3]
    a = params[4]
    params_sim = np.array([g_0, T_opt, beta, T_f, a, gamma])
    v_plot = np.arange(0, 1, .01)

    # création d'une figure, et d'un système d'axes
    fig13, ax13 = plt.subplots(figsize=(8, 6))  

    # plot de l'équilibre trivial avec la bonne stabilité
    gamma_trans = g_of_v_climChg(0, t=0, params = params_sim, Tslope = 0)
    if gamma_trans >= 0:
        gamma_plot1 = np.arange(0, gamma_trans, .001)
        gamma_plot2 = np.arange(gamma_trans, 1., .001)
        ax13.plot(gamma_plot1, np.ones(gamma_plot1.shape)*0, color = 'C3')
        ax13.plot(gamma_plot2, np.ones(gamma_plot2.shape)*0, color = 'C2', label = "équilibre stable")
    else:
        gamma_plot = np.arange(0, 1, .01)
        ax13.plot(gamma_plot, np.ones(gamma_plot.shape)*0, color = 'C2', label = "équilibre stable")

    # on trace la branche instable en rouge C3 et stable en vert C2
    # il faut recuperer le sommet : la derivee est nulle
    v = P([0, 1]) # définition de monôme
    # def polynôme définissant le lieu des équilibres v^* > 0
    QQ = g_of_v_climChg(v, t=0, params = params_sim, Tslope =0)*(1-v) # la courbe gamma(v), pourrait servir dans le plot du lieu lui-meme
    deriv0 = QQ.deriv().roots()  # les racines de sa dérivée
    pos_deriv0 = deriv0[QQ(deriv0)>0] # la racine correspondant seulement a gamma(v) > 0

    v_plot_uns = np.arange(0, pos_deriv0, .001) 
    v_plot_st = np.arange(pos_deriv0, 1, .001) 
    
    ax13.plot(QQ(v_plot_uns)[QQ(v_plot_uns)>0], v_plot_uns[QQ(v_plot_uns)>0], color = 'C3', label = "équilibre instable" ) # branche instable
    ax13.plot(QQ(v_plot_st)[QQ(v_plot_st)>0.], v_plot_st[QQ(v_plot_st)>0.], color = 'C2')  # branche stable
    ax13.plot(QQ(pos_deriv0), pos_deriv0, 'D', markersize = 5, color = 'C4', label = "bifurcation pli" )

    if plotTraj:
        # représentation de la trajectoire
        int_FDB = odeint(modeleFDB_climChg, v0, long_tspan, args=(params_sim, 0), hmax=pas_t)
        gamma_sim = np.ones(int_FDB.shape) * gamma
        ax13.plot(gamma_sim, int_FDB, color = 'C0', label = "trajectoire")
        ax13.plot(gamma, v0, 'o', color = 'C1', label = "végétation initiale")
        ax13.plot(gamma, int_FDB[-1], 'o', color = 'C0', label = "végétation finale")


    # test ajout de petites imagettes
    im1 = image.imread("img/forest.png") 
    im2 = image.imread("img/desert.png") 
       
    vplot_st2 = v_plot_st[QQ(v_plot_st)>0.01]
    # no it does not work as expected yet to put the forest in the right place
    y_im1 = (69+384*vplot_st2[-1])/510-.09
    imax1 = fig13.add_axes([.22, y_im1, 0.08, 0.08])
    imax1.set_axis_off()
    imax1.imshow(im1, aspect="equal")

    imax2 = fig13.add_axes([.79, 0.17, 0.07, 0.07])
    imax2.set_axis_off()
    imax2.imshow(im2, aspect="equal")

    ax13.legend(fontsize='10')
    ax13.set_xlabel('$\gamma$', fontsize='12')
    ax13.set_ylabel('proportion de végétation $v$', fontsize='12')
    fig13.suptitle(r'Proportion de végétation $v$', va='top', fontsize='14')

    # modification éventuelle des bornes des axes
    #ax13.set_xlim(left=0, right=1)

    # ajout d'une grille
    ax13.grid()
    
    # returns the figure object
    return fig13

################################################################
# partie bifurcation vs T_f
def Tf1(v, params):
    g_0, T_opt, beta, T_f, a, gamma = params
    return T_opt+a*(v-1)+beta*np.sqrt(1-gamma/(g_0*(1-v)))

def Tf2(v, params):
    g_0, T_opt, beta, T_f, a, gamma = params
    return T_opt+a*(v-1)-beta*np.sqrt(1-gamma/(g_0*(1-v)))

# bifurcations vs T
@st.experimental_singleton
def plotBifTf(v0, gamma, T_f, params, plotTraj, climChange, Tslope = 0):
    g_0, T_opt, beta = params[0:3]
    a = params[4]
    params_bif_tf = np.array([g_0, T_opt, beta, T_f, a, gamma])

    minv= 0
    maxv= 1-gamma/g_0
    step = 0.00001
    v_plot = np.arange(minv, maxv, step)
    
    fig20, ax20 = plt.subplots(figsize=(8, 6))  
    
    ax20.plot(Tf2(v_plot, params = params_bif_tf), v_plot, color = 'C2') # branche 2
    
    # on récupère plusieurs points d'intéret du diagramme pour pouvoir tracer correctement la stabilité de v = 0 (2 transcritiques)
    # c'est un peu laborieux...
    Tplot_min = Tf2(minv, params = params_bif_tf)-5
    Tplot_max = max(Tf1(v_plot, params = params_bif_tf))+5
    Ttranscrit1 = Tf2(minv, params = params_bif_tf)
    Ttranscrit2 = Tf1(minv, params = params_bif_tf)
    Tplot_st1 = np.arange(Tplot_min, Ttranscrit1, .1)
    Tplot_uns = np.arange(Ttranscrit1, Ttranscrit2, .1)
    Tplot_st2 = np.arange(Ttranscrit2, Tplot_max, .1)
    zero_plot_st1 = np.ones(Tplot_st1.shape) * 0
    zero_plot_uns = np.ones(Tplot_uns.shape) * 0
    zero_plot_st2 = np.ones(Tplot_st2.shape) * 0
    
    ax20.plot(Tplot_st1, zero_plot_st1, color = "C2", label = "équilibre stable")
    ax20.plot(Tplot_uns, zero_plot_uns, color = "C3", label = "équilibre instable")
    ax20.plot(Tplot_st2, zero_plot_st2, color = "C2")
    
    v_pli = v_plot[np.argmax(Tf1(v_plot, params = params_bif_tf))]
    v_plot_saddle = np.arange(minv, v_pli, .01)
    v_plot_stable = np.arange(v_pli, maxv, step)
    ax20.plot(Tf1(v_plot_stable, params = params_bif_tf), v_plot_stable, color = "C2") # branche 1
    ax20.plot(Tf1(v_plot_saddle, params = params_bif_tf), v_plot_saddle, color = "C3")
    ax20.plot(Tf1(v_pli, params = params_bif_tf), v_pli, 'D', markersize = 5, label = "bifurcation pli", color = "C4")

    # tracé trajectoire pour T_f fixe
    if plotTraj and not climChange:
        # représentation de la trajectoire
        int_FDB = odeint(modeleFDB_climChg, v0, long_tspan, args=(params_bif_tf, 0), hmax=pas_t)
        T_f_sim = np.ones(int_FDB.shape) * T_f
        ax20.plot(T_f_sim, int_FDB, color = 'C0', label = "trajectoire")
        ax20.plot(T_f, v0, 'o', color = 'C1', label = "végétation initiale")
        ax20.plot(T_f, int_FDB[-1], 'o', color = 'C0', label = "végétation finale")

    # tracé trajectoire pour T_f qui augmente
    if climChange:
        int_FDB_climChg = odeint(modeleFDB_climChg, v0, long_tspan, args=(params_bif_tf, Tslope), hmax=pas_t)
        T_f_simChg = T_fChg(long_tspan, T_f, Tslope)
        ax20.plot(T_f_simChg, int_FDB_climChg, color = 'C1', label = "trajectoire")
        ax20.plot(T_f, v0, 'o', color = 'C1', label = "végétation initiale")
        ax20.plot(T_f_simChg[-1], int_FDB_climChg[-1], 'o', color = 'C3', label = "végétation finale")
    
    # imagettes
    if not climChange:
        im1 = image.imread("img/forest.png") 
        y_im1 = (69+384*maxv/2)/510+.1
        x_im1 = Tf2(v_plot, params = params_bif_tf)[round(len(v_plot)/2)]/(Tplot_max-Tplot_min)-.05
        imax1 = fig20.add_axes([x_im1, y_im1, 0.08, 0.08])
        imax1.set_axis_off()
        imax1.imshow(im1, aspect="equal")

    im2 = image.imread("img/desert.png") 
    imax2 = fig20.add_axes([.78, 0.17, 0.07, 0.07])
    imax2.set_axis_off()
    imax2.imshow(im2, aspect="equal")

    ax20.legend(fontsize='10', loc = "upper left")
    ax20.set_xlabel('$T_f$', fontsize='12')
    ax20.set_ylabel('proportion de végétation $v$', fontsize='12')
    fig20.suptitle(r'Proportion de végétation $v$', va='top', fontsize='14')

    # modification éventuelle des bornes des axes
    ax20.set_ylim(bottom= -0.05, top=1)
    ax20.grid()

    # returns the figure object
    return fig20


# trajectoire contre le temps climate change
@st.experimental_singleton
def plotSimClimchg(v0, gamma, T_f, params, plotTraj, climChange, Tslope = 0):
    g_0, T_opt, beta = params[0:3]
    a = params[4]
    params_bif_tf = np.array([g_0, T_opt, beta, T_f, a, gamma])

    int_FDB_climChg = odeint(modeleFDB_climChg, v0, long_tspan, args=(params_bif_tf, Tslope), hmax=pas_t)
    
    fig21, ax21 = plt.subplots(figsize=(8, 6))  

    ax21.plot(long_tspan, int_FDB_climChg, color = 'C0', label = "proportion de végétation")
    ax21.set_xlabel("temps", fontsize='12')
    ax21.set_ylabel("proportion de végétation $v$", fontsize='12')
    #fig21.suptitle(r'Proportion de végétation $v$', va='top', fontsize='14')
    ax21.set_ylim(bottom = -.05, top=1)
    ax21.legend(fontsize='10', loc = "upper right")

    ax21.grid()

    return fig21
    