#!/usr/bin/env python

import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt


def avg_and_error(y_cumulative):

    y_cumulative = np.array(y_cumulative)

    iterations = y_cumulative.shape[0]
    timesteps = y_cumulative.shape[1]
    components = y_cumulative.shape[2]

    y = []
    pos_err = []
    neg_err = []

    for i in range(timesteps):

        y_timestep = y_cumulative[:,i,:]

        means = []
        errors = []

        for j in range(components):

            mean = np.mean(y_timestep[:,j])
            sem = st.sem(y_timestep[:,j])
            ci95 = st.t.interval(0.95, iterations-1, loc=mean, scale=sem)
            means.append(mean)
            errors.append(ci95)

        y.append(np.array(means))
        pos_err.append(np.array(errors)[:,0])
        neg_err.append(np.array(errors)[:,1])

    y = np.array(y)
    pos_err = np.array(pos_err)
    neg_err = np.array(neg_err)

    return y, pos_err, neg_err


def plot_results(plot_list, species_dict, color_dict, y, pos_err, neg_err, t):

    plt.rc('text', usetex=True)
    plt.rc('font', family='sans-serif')

    # fig = plt.plot(dpi=300)
    fig, (ax1, ax2) = plt.subplots(nrows=1, ncols=2, sharex=True, figsize=(20,10), dpi=300)

    # theta( H2O(aq)      )
    # theta( H5O2(aq)     )
    # theta( COH*         )
    # theta( CO*          )
    # theta( H*           )
    # theta( COH-H2O*     )
    # theta( COH-H2O-H2O* )
    # theta( *            )

    for species_index in plot_list:

        if species_index <= 1:
            ax1.plot(t, y[:,species_index], color_dict[species_index], label=species_dict[species_index])
            ax1.fill_between(t, pos_err[:,species_index], neg_err[:,species_index], color=color_dict[species_index], alpha=0.2)

        elif species_index >= 2:
            ax2.plot(t, y[:,species_index], color_dict[species_index], label=species_dict[species_index])
            ax2.fill_between(t, pos_err[:,species_index], neg_err[:,species_index], color=color_dict[species_index], alpha=0.2)


    ax1.set(ylabel=r'Concentration [mol/L]')
    ax1.legend(loc='upper right', fontsize=12)

    ax2.set(xlabel=r't [s]', ylabel=r'Surface coverage, $\theta$ [ML]')
    ax2.legend(loc='upper right', fontsize=12)

    ax2.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.show()
