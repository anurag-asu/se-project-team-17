from numpy import NaN
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as stats
import pylab
import numpy as np

loc1 = "csvs/asfi_refined_with_metrics.csv"
loc2 = "csvs/asfi_refined_false_removed.csv"


def remove_ouliers(df, metric):
    Q1 = df[metric].quantile(0.25)
    Q3 = df[metric].quantile(0.75)

    IQR = Q3 - Q1  # IQR is interquartile range.

    filter = (df[metric] >= Q1 - 1.5 * IQR) & (df[metric] <= Q3 + 1.5 * IQR)
    df = df.loc[filter]

    return df


def pre_process_data_metric(df, metric):

    df = normalize_data(df, metric, False)
    df.replace([np.inf, -np.inf], 0, inplace=True)
    print(df[metric])
    mean = df[metric].mean()

    print("mean", mean)

    # catrgorize dataframe based on mean and remove status = 0, i.e still in incubation
    df_mean_high = df.loc[(df[metric] >= mean)]
    df_mean_low = df.loc[(df[metric] < mean)]

    print("projects with " + metric + " higher than mean ", len(df_mean_high))
    print("projects with " + metric + " lower than mean ", len(df_mean_low))

    df_mean_high_gtd = df_mean_high.loc[df["status"] == 1]
    df_mean_high_rtd = df_mean_high.loc[df["status"] == 2]

    print(
        "projects with " + metric + " higher than mean and graduated ",
        len(df_mean_high_gtd),
    )
    print(
        "projects with " + metric + " higher than mean and retired ",
        len(df_mean_high_rtd),
    )

    df_mean_low_gtd = df_mean_low.loc[df["status"] == 1]
    df_mean_low_rtd = df_mean_low.loc[df["status"] == 2]

    print(
        "projects with " + metric + " lower than mean and graduated ",
        len(df_mean_low_gtd),
    )
    print(
        "projects with " + metric + " lower than mean and retired ",
        len(df_mean_low_rtd),
    )

    chi_sq(
        len(df_mean_high_gtd),
        len(df_mean_low_gtd),
        len(df_mean_high_rtd),
        len(df_mean_low_rtd),
    )


def chi_sq(df_mean_high_gtd, df_mean_low_gtd, df_mean_high_rtd, df_mean_low_rtd):
    # chi-squared test with similar proportions
    from scipy.stats import chi2_contingency
    from scipy.stats import chi2

    # contingency table
    table = [[df_mean_high_gtd, df_mean_low_gtd], [df_mean_high_rtd, df_mean_low_rtd]]

    print(table)
    stat, p, dof, expected = chi2_contingency(table)

    print("dof=%d" % dof)
    print(expected)
    # interpret test-statistic

    prob = 0.95
    critical = chi2.ppf(prob, dof)

    print("probability=%.3f, critical=%.3f, stat=%.3f" % (prob, critical, stat))
    if abs(stat) >= critical:
        print("Dependent (reject H0)")
    else:
        print("Independent (fail to reject H0)")

    # interpret p-value
    alpha = 0.025

    print("significance=%.3f, p=%.3f" % (alpha, p))
    if p <= alpha:
        print("Dependent (reject H0)")
    else:
        print("Independent (fail to reject H0)")


def plot_outlier_and_distribution_graphs(df, metric):

    plt.subplot(2, 2, 1)
    plt.title(metric + " metric with outliers")
    plt.boxplot(df[metric])

    df = remove_ouliers(df, metric)

    plt.subplot(2, 2, 2)
    plt.title(metric + " metric after removing outliers")
    plt.boxplot(df[metric])

    # calculate std deviation and mean
    std = df[metric].std()
    mean = df[metric].mean()

    plt.subplot(2, 2, 3)

    # Plot pandas histogram from dataframe with df.plot.hist (not df.hist)
    ax = df[metric].plot.hist(bins=20, density=True, edgecolor="w", linewidth=0.5)

    # Save default x-axis limits for final formatting because the pandas kde
    # plot uses much wider limits which usually decreases readability
    xlim = ax.get_xlim()

    # Plot pandas KDE
    # df[metric].plot.kde(color='k', alpha=0.5, ax=ax) # same as df['var'].plot.kde()

    # # Reset x-axis limits and edit legend and add title
    # ax.set_xlim(xlim)
    # ax.legend(labels=['KDE'], frameon=False)
    # ax.set_title('Data distribution of ' + metric + ' metric', fontsize=14, pad=15)
    # ax.set_xlabel(metric + ' metric')
    # ax.text(0.7, 0.8, 'Mean = ' + str(mean) +'\nStd = ' + str(std), horizontalalignment='center',
    #     verticalalignment='center', transform=ax.transAxes)

    plt.subplot(2, 2, 4)
    stats.probplot(df[metric], dist="norm", plot=pylab)

    plt.show()
    pylab.show()


def normalize_data(df, metric, show_graph=False):
    df[metric] = np.log(df[metric])

    if show_graph:
        stats.probplot(df[metric], dist="norm", plot=pylab)
        pylab.show()

    return df


def pre_process_data(metric, location):
    df = pd.read_csv(location)
    df = df.loc[
        (df[metric] != NaN) & (df["correct_url_found"] != False) & (df["status"] != 0)
    ]
    pre_process_data_metric(df, metric)


def plot_graphs(metric, location):
    df = pd.read_csv(location)
    df = df.loc[
        (df[metric] != NaN) & (df["correct_url_found"] != False) & (df["status"] != 0)
    ]
    plot_outlier_and_distribution_graphs(df, metric)


def normalize_metrics(metric, location, show_graph=False):
    df = pd.read_csv(location)
    df = df.loc[
        (df[metric] != NaN) & (df["correct_url_found"] != False) & (df["status"] != 0)
    ]
    df = normalize_data(df, metric, show_graph)


def do_something(metric, location):
    df = df = pd.read_csv(location)
    df = df.loc[
        (df[metric] != NaN) & (df["correct_url_found"] != False) & (df["status"] != 0)
    ]

    mean = df[metric].mean()
    std = df[metric].std()

    print(mean)
    print(std)


# chi_sq()

# pre_process_data('frequency', loc1)
# pre_process_data('dimensionality', loc1)
# pre_process_data_frequency()

# plot_graphs('ratio_of_duplicate_prs', loc2)


# normalize_metrics('frequency', True)
# normalize_metrics('dimensionality', True)
# do_something('ratio_of_duplicate_prs', loc2)
