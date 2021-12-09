library(ggplot2)
library(cowplot)
library(ggstatsplot)
library(mlbench)
library(MASS)
library(pROC)

## Before removing outliers ##
boxplot(frequency ~ status, data = df_no_I_na)
boxplot(dimensionality ~ status, data = df_no_I_na)
boxplot(ratio_of_duplicate_prs ~ status, data = df_no_I_na)


par(cex.lab=1)
boxplot(cntr_management ~ status, data = df_no_I_na, main = "Central management index", cex.main = 2, xlab = "Before" , at = c(1,2), col = c("light green","pink"))
boxplot(additive_contribution_index ~ status, data = df_no_I_na, main = "Additive contribution index", cex.main = 2, xlab = "Before", at = c(1,2), col = c("light green","pink"))
boxplot(logic_coupling_index ~ status, data = df_no_I_na, main = "Logic coupling index", cex.main = 2, xlab = "Before", at = c(1,2), col = c("light green","pink"))






## After removing outliers [Status all] ##
# 1. Frequency
Q <- quantile(df_no_na$frequency, probs=c(.25, .75), na.rm = FALSE)
iqr <- IQR(df$frequency)
up <-  Q[2]+1.5*iqr  
low <- Q[1]-1.5*iqr
freq_df <- subset(df_no_na, df_no_na$frequency > (Q[1] - 1.5*iqr) & df_no_na$frequency < (Q[2]+1.5*iqr))
boxplot(frequency ~ status, data = freq_df, )
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


# 6. Pre-Communication index
Q <- quantile(df_no_na$pre_communication, probs=c(.25, .75), na.rm = FALSE)
iqr <- IQR(df_no_na$pre_communication)
up <-  Q[2]+1.5*iqr  
low <- Q[1]-1.5*iqr
pre_df <- subset(df_no_na, df_no_na$pre_communication > (Q[1] - 1.5*iqr) & df_no_na$pre_communication < (Q[2]+1.5*iqr))
boxplot(pre_communication ~ status, data = pre_df)
summary(pre_df)

# 7. Logic-coupling index
Q <- quantile(df_no_na$logic_coupling_index, probs=c(.25, .75), na.rm = FALSE)
iqr <- IQR(df_no_na$logic_coupling_index)
up <-  Q[2]+1.5*iqr  
low <- Q[1]-1.5*iqr
log_df <- subset(df_no_na, df_no_na$logic_coupling_index > (Q[1] - 1.5*iqr) & df_no_na$logic_coupling_index < (Q[2]+1.5*iqr))
boxplot(logic_coupling_index ~ status, data = log_df)

## Histogram ##
hist(log_df[,15][df$status=='G' | df$status=='R'], main = "Logic coupling index",xlab = colnames(log_df)[15], col = 'light blue', sub = "[i]", cex.main = 2)
hist(add_df[,14][df$status=='G' | df$status=='R'], main = "Additive contribution index",xlab = colnames(add_df)[14], col = 'light blue', sub = "[ii]" , cex.main = 2)
hist(df_no_I_na[,10][df$status=='G' | df$status=='R'], main = "Ratio of duplicate PRs",xlab = colnames(df_no_I_na)[10], col = 'light blue', sub = "[iii]", cex.main = 2)
ggplot(df_no_I_na,aes(factor(has_hard_fork))) + geom_bar(fill = "light blue",) + theme_classic() + labs(title = "Presence of hard fork", caption = "[iv]") + theme(plot.title = element_text(hjust = 0.5, size =  22, face = "bold"), plot.caption = element_text(hjust=0.5, size=12)) 
hist(cntr_df[,13][df$status=='G' | df$status=='R'], main = "Central management index",xlab = colnames(cntr_df)[13], col = 'light blue', sub = "[v]", cex.main = 2)
hist(pre_df[,19][df$status=='G' | df$status=='R'], main = "Pre-communication index",xlab = colnames(pre_df)[19], col = 'light blue', sub = "[vi]" ,cex.main = 2)
hist(dem_df[,9][df$status=='G' | df$status=='R'], main = "Dimensionality of commits",xlab = colnames(dem_df)[9], col = 'light blue', sub = "[vii]", cex.main = 2)
hist(freq_df[,8][df$status=='G' | df$status=='R'], main = "Frequency of PRs",xlab = colnames(freq_df)[8], col = 'light blue', sub = "[viii]", cex.main = 2)

