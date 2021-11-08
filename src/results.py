from numpy import NaN
import pandas as pd
import matplotlib.pyplot as plt

def pre_process_data_frequency():
    df = pd.read_csv('csvs/asfi_refined_with_metrics.csv')
    df = df.loc[(df['frequency'] != NaN) & (df['correct_url_found'] != False)]

    print('initial projects ', len(df))
    
    # removing outliers
    # TO DO Plot boxplot before
    Q1 = df['frequency'].quantile(0.25)
    Q3 = df['frequency'].quantile(0.75)

    # print(Q1, Q3)

    IQR = Q3 - Q1    #IQR is interquartile range. 

    filter = (df['frequency'] >= Q1 - 1.5 * IQR) & (df['frequency'] <= Q3 + 1.5 *IQR) 
    
    df = df.loc[filter]
    # TO DO Plot boxplot after

    print('projects after removing outliers', len(df))

    # plot a histogram for visualisation

    # plt.xlabel('frequency_metric')
    # plt.hist(x=df['frequency'], bins=20, rwidth=0.9)
    # plt.show()

    # calculate std deviation and mean
    std = df['frequency'].std()
    mean = df['frequency'].mean()

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
    
    # removing outliers
    # TO DO Plot boxplot before
    Q1 = df['dimensionality'].quantile(0.25)
    Q3 = df['dimensionality'].quantile(0.75)

    # print(Q1, Q3)

    IQR = Q3 - Q1    #IQR is interquartile range. 

    filter = (df['dimensionality'] >= Q1 - 1.5 * IQR) & (df['dimensionality'] <= Q3 + 1.5 *IQR) 
    
    df = df.loc[filter]
    # TO DO Plot boxplot after

    print('projects after removing outliers', len(df))

    # plot a histogram for visualisation

    # plt.xlabel('frequency_metric')
    # plt.hist(x=df['frequency'], bins=20, rwidth=0.9)
    # plt.show()

    # calculate std deviation and mean
    std = df['dimensionality'].std()
    mean = df['dimensionality'].mean()

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


pre_process_data_dimensionality()
# pre_process_data_frequency()




