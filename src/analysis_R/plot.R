library(ggplot2)
library(cowplot)
library(ggstatsplot)
library(mlbench)
library(MASS)
library(pROC)

## Before removing outliers ##
boxplot(frequency ~ status, data = df_no_na)
boxplot(dimensionality ~ status, data = df_no_na)
boxplot(ratio_of_duplicate_prs ~ status, data = df_no_na)
boxplot(cntr_management ~ status, data = df_no_na)
boxplot(additive_contribution_index ~ status, data = df_no_na)
boxplot(logic_coupling_index ~ status, data = df_no_na)

## After removing outliers [Status all] ##
# 1. Frequency
Q <- quantile(df_no_na$frequency, probs=c(.25, .75), na.rm = FALSE)
iqr <- IQR(df$frequency)
up <-  Q[2]+1.5*iqr  
low <- Q[1]-1.5*iqr
freq_df <- subset(df_no_na, df_no_na$frequency > (Q[1] - 1.5*iqr) & df_no_na$frequency < (Q[2]+1.5*iqr))
boxplot(frequency ~ status, data = freq_df)
summary(freq_df$frequency)

# 2. Dimensional
Q <- quantile(df_no_na$dimensionality, probs=c(.25, .75), na.rm = FALSE)
iqr <- IQR(df_no_na$dimensionality)
up <-  Q[2]+1.5*iqr  
low <- Q[1]-1.5*iqr
dem_df <- subset(df_no_na, df_no_na$dimensionality > (Q[1] - 1.5*iqr) & df_no_na$dimensionality < (Q[2]+1.5*iqr))
boxplot(dimensionality ~ status, data = df)
boxplot(dimensionality ~ status, data = dem_df)
summary(dem_df)

# 3. Ratio of duplicate PRs
Q <- quantile(df_no_na$ratio_of_duplicate_prs, probs=c(.25, .75), na.rm = FALSE)
iqr <- IQR(df_no_na$ratio_of_duplicate_prs)
up <-  Q[2]+1.5*iqr  
low <- Q[1]-1.5*iqr
ratio_dup_df <- subset(df_no_na, df_no_na$ratio_of_duplicate_prs > (Q[1] - 1.5*iqr) & df_no_na$ratio_of_duplicate_prs < (Q[2]+1.5*iqr))
ratio_dup_df$ratio_of_duplicate_prs
boxplot(ratio_of_duplicate_prs ~ status, data = ratio_dup_df)
df_no_na$ratio_of_duplicate_prs

# 4. Central Management
Q <- quantile(df_no_na$cntr_management, probs=c(.25, .75), na.rm = FALSE)
iqr <- IQR(df_no_na$cntr_management)
up <-  Q[2]+1.5*iqr  
low <- Q[1]-1.5*iqr
cntr_df <- subset(df_no_na, df_no_na$cntr_management > (Q[1] - 1.5*iqr) & df_no_na$cntr_management < (Q[2]+1.5*iqr))
boxplot(cntr_management ~ status, data = cntr_df)

# 5. Additive contribution index
Q <- quantile(df_no_na$additive_contribution_index, probs=c(.25, .75), na.rm = FALSE)
iqr <- IQR(df_no_na$additive_contribution_index)
up <-  Q[2]+1.5*iqr  
low <- Q[1]-1.5*iqr
add_df <- subset(df_no_na, df_no_na$additive_contribution_index > (Q[1] - 1.5*iqr) & df_no_na$additive_contribution_index < (Q[2]+1.5*iqr))
boxplot(additive_contribution_index ~ status, data = add_df)

# 6. Logic-coupling index
Q <- quantile(df_no_na$logic_coupling_index, probs=c(.25, .75), na.rm = FALSE)
iqr <- IQR(df_no_na$logic_coupling_index)
up <-  Q[2]+1.5*iqr  
low <- Q[1]-1.5*iqr
log_df <- subset(df_no_na, df_no_na$logic_coupling_index > (Q[1] - 1.5*iqr) & df_no_na$logic_coupling_index < (Q[2]+1.5*iqr))
boxplot(logic_coupling_index ~ status, data = log_df)
