from numpy import NaN
import pandas as pd
import matplotlib.pyplot as plt

def pre_process_data_frequency():
    df = pd.read_csv('csvs/asfi_refined_with_metrics.csv')
    df = df.loc[(df['frequency'] != NaN) & (df['correct_url_found'] != False)]

    print('initial projects ', len(df))

    # plt.subplot(1,2,1)
    # plt.title('frequency metric with outliers')
    # plt.boxplot(df['frequency'])
    
    # removing outliers
    # TO DO Plot boxplot before
    Q1 = df['frequency'].quantile(0.25)
    Q3 = df['frequency'].quantile(0.75)

    # print(Q1, Q3)

    IQR = Q3 - Q1    #IQR is interquartile range. 

    filter = (df['frequency'] >= Q1 - 1.5 * IQR) & (df['frequency'] <= Q3 + 1.5 *IQR) 
    
    df = df.loc[filter]
    # TO DO Plot boxplot after

    # plt.subplot(1,2,2)
    # plt.title('frequency metric after removing outliers')
    # plt.boxplot(df['frequency'])

    # plt.show()

    print('projects after removing outliers', len(df))

    # plot a histogram for visualisation

    # plt.xlabel('Frequency of commits')
    # plt.title('Data distribution for frequency metric')
    # plt.hist(x=df['frequency'], bins=20, rwidth=0.9)
    # plt.show()

    # calculate std deviation and mean
    std = df['frequency'].std()
    mean = df['frequency'].mean()

    # Plot pandas histogram from dataframe with df.plot.hist (not df.hist)
    ax = df['frequency'].plot.hist(bins=20, density=True, edgecolor='w', linewidth=0.5)

    # Save default x-axis limits for final formatting because the pandas kde
    # plot uses much wider limits which usually decreases readability
    xlim = ax.get_xlim()

    # Plot pandas KDE
    df['frequency'].plot.kde(color='k', alpha=0.5, ax=ax) # same as df['var'].plot.kde()

    # Reset x-axis limits and edit legend and add title
    ax.set_xlim(xlim)
    ax.legend(labels=['KDE'], frameon=False)
    ax.set_title('Data distribution of frequency metric', fontsize=14, pad=15)
    ax.set_xlabel('Frequency metric')
    ax.text(0.7, 0.8, 'Mean = ' + str(mean) +'\nStd = ' + str(std), horizontalalignment='center',
        verticalalignment='center', transform=ax.transAxes)
    plt.show()

    print('mean of frequency metric', mean)

    # catrgorize dataframe based on mean and remove status = 0, i.e still in incubation
    df_mean_high = df.loc[(df['frequency'] >= mean) & (df['status'] != 0)]
    df_mean_low = df.loc[(df['frequency'] < mean) & (df['status'] != 0)]

    print('projects with frequency higher than mean ', len(df_mean_high))
    print('projects with frequency lower than mean ', len(df_mean_low))

    df_mean_high_gtd = df_mean_high.loc[df['status'] == 1]
    df_mean_high_rtd = df_mean_high.loc[df['status'] == 2]

    print('projects with frequency higher than mean and graduated ', len(df_mean_high_gtd))
    print('projects with requency higher than mean and retired ', len(df_mean_high_rtd))

    df_mean_low_gtd = df_mean_low.loc[df['status'] == 1]
    df_mean_low_rtd = df_mean_low.loc[df['status'] == 2]

    print('projects with frequency lower than mean and graduated ', len(df_mean_low_gtd))
    print('projects with frequency lower than mean and retired ', len(df_mean_low_rtd))


def pre_process_data_dimensionality():
    df = pd.read_csv('csvs/asfi_refined_with_metrics.csv')
    df = df.loc[(df['dimensionality'] != NaN) & (df['correct_url_found'] != False)]

    print('initial projects ', len(df))

    # plt.subplot(1,2,1)
    # plt.title('dimensionality metric with outliers')
    # plt.boxplot(df['dimensionality'])
    
    # removing outliers
    # TO DO Plot boxplot before
    Q1 = df['dimensionality'].quantile(0.25)
    Q3 = df['dimensionality'].quantile(0.75)

    # print(Q1, Q3)

    IQR = Q3 - Q1    #IQR is interquartile range. 

    filter = (df['dimensionality'] >= Q1 - 1.5 * IQR) & (df['dimensionality'] <= Q3 + 1.5 *IQR) 
    
    df = df.loc[filter]
    # TO DO Plot boxplot after
    # plt.subplot(1,2,2)
    # plt.title('dimensionality metric with outliers')
    # plt.boxplot(df['dimensionality'])

    print('projects after removing outliers', len(df))

    # plot a histogram for visualisation

    # plt.xlabel('Dimensionality metric')
    # plt.title('Data distribution for dimensionality metric')
    # plt.hist(x=df['dimensionality'], bins=20, rwidth=0.9)
    # plt.show()

    

    # calculate std deviation and mean
    std = df['dimensionality'].std()
    mean = df['dimensionality'].mean()

    # Plot pandas histogram from dataframe with df.plot.hist (not df.hist)
    ax = df['dimensionality'].plot.hist(bins=20, density=True, edgecolor='w', linewidth=0.5)

    # Save default x-axis limits for final formatting because the pandas kde
    # plot uses much wider limits which usually decreases readability
    xlim = ax.get_xlim()

    # Plot pandas KDE
    df['dimensionality'].plot.kde(color='k', alpha=0.5, ax=ax) # same as df['var'].plot.kde()

    # Reset x-axis limits and edit legend and add title
    ax.set_xlim(xlim)
    ax.legend(labels=['KDE'], frameon=False)
    ax.set_title('Data distribution of dimensionality metric', fontsize=14, pad=15)
    ax.set_xlabel('Dimentionality metric')
    ax.text(0.7, 0.8, 'Mean = ' + str(mean) +'\nStd = ' + str(std), horizontalalignment='center',
        verticalalignment='center', transform=ax.transAxes)
    plt.show()


    print('mean of frequency metric', mean)

    # catrgorize dataframe based on mean and remove status = 0, i.e still in incubation
    df_mean_high = df.loc[(df['dimensionality'] >= mean) & (df['status'] != 0)]
    df_mean_low = df.loc[(df['dimensionality'] < mean) & (df['status'] != 0)]

    print('projects with dimensionality higher than mean ', len(df_mean_high))
    print('projects with dimensionality lower than mean ', len(df_mean_low))

    df_mean_high_gtd = df_mean_high.loc[df['status'] == 1]
    df_mean_high_rtd = df_mean_high.loc[df['status'] == 2]

    print('projects with dimensionality higher than mean and graduated ', len(df_mean_high_gtd))
    print('projects with dimensionality higher than mean and retired ', len(df_mean_high_rtd))

    df_mean_low_gtd = df_mean_low.loc[df['status'] == 1]
    df_mean_low_rtd = df_mean_low.loc[df['status'] == 2]

    print('projects with dimensionality lower than mean and graduated ', len(df_mean_low_gtd))
    print('projects with dimensionality lower than mean and retired ', len(df_mean_low_rtd))


# pre_process_data_dimensionality()
pre_process_data_frequency()




