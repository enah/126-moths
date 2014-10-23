from sim import simulate
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter

def prob_all_grey(num_samples=100, max_moths=50, prob_white=0.8):
    samples = []
    for num_moths in range(1, max_moths + 1):
        samples.append(
                sum(simulate({'ww':0, 'wg':num_moths, 'gg':0}, 
                        prob_white, fraction=False)
                for _ in range(num_samples)) / float(num_samples))
    plt.plot(samples)
    plt.title(
        'Probability All Moths Turn Grey (prob_white = {})'.format(prob_white))
    plt.xlabel('Number of moths')
    plt.ylabel('Probability')
    plt.show()

def prob_against_white_death(num_samples=100, num_moths=30, granularity=0.05):
    samples = []
    for prob_white_death in np.arange(0, 1 + granularity, granularity):
        samples.append(sum(
                simulate({'ww':0, 'wg':num_moths, 'gg':0}, prob_white_death)
                for _ in range(num_samples)) / float(num_samples))
    plt.plot(np.arange(0, 1 + granularity, granularity), samples)
    plt.title('Grey Moths Versus Probability of White Death')
    plt.xlabel('Probability of white death')
    plt.ylabel('Fraction of grey moths')
    plt.show()

def frac_grey_against_both(num_samples=50, max_moths=30, granularity=0.1):
    probs_white_death = np.arange(0, 1 + granularity, granularity)
    nums_moths = np.arange(1, max_moths + 1)
    results = np.zeros((len(nums_moths), len(probs_white_death)))
    probs_white_death, nums_moths = np.meshgrid(probs_white_death, nums_moths)
    stacked = np.dstack((probs_white_death, nums_moths))
    for i, group in enumerate(stacked):
        for j, pair in enumerate(group):
            prob_white_death, num_moths = pair[0], pair[1]
            results[i][j] = sum(
                simulate({'ww':0, 'wg':num_moths, 'gg':0}, prob_white_death)
                for _ in range(num_samples)) / float(num_samples)

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    surf = ax.plot_surface(probs_white_death, nums_moths, results, rstride=1, 
            cstride=1, cmap=cm.Greys, linewidth=0, antialiased=False)
    ax.set_zlim(0, 1.00)

    ax.zaxis.set_major_locator(LinearLocator(10))
    ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

    fig.colorbar(surf, shrink=0.5, aspect=5)

    plt.title('Fraction of Grey Moths')
    ax.set_xlabel('Probability of white moth death')
    ax.set_ylabel('Number of moths')
    ax.set_zlabel('Fraction of grey moths')

    plt.show()
