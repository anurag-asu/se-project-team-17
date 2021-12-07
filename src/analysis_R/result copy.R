library(ggplot2)
library(cowplot)
library(ggstatsplot)
library(mlbench)
library(MASS)
library(pROC)

## Box plot no outlier only status Graduated and Retired
# 1. Frequency
Q <- quantile(df_no_I_na$frequency, probs=c(.25, .75), na.rm = FALSE)
iqr <- IQR(df_no_I_na$frequency)
up <-  Q[2]+1.5*iqr  
low <- Q[1]-1.5*iqr
freq_df <- subset(df_no_I_na, df_no_I_na$frequency > (Q[1] - 1.5*iqr) & df_no_I_na$frequency < (Q[2]+1.5*iqr))
boxplot(frequency ~ status, data = freq_df)
summary(freq_df$frequency)

# 2. Dimensional
Q <- quantile(df_no_I_na$dimensionality, probs=c(.25, .75), na.rm = FALSE)
iqr <- IQR(df_no_I_na$dimensionality)
up <-  Q[2]+1.5*iqr  
low <- Q[1]-1.5*iqr
dem_df <- subset(df_no_I_na, df_no_I_na$dimensionality > (Q[1] - 1.5*iqr) & df_no_I_na$dimensionality < (Q[2]+1.5*iqr))
boxplot(dimensionality ~ status, data = dem_df)
summary(dem_df)

# 3. Ratio of duplicate PRs [Not working]
Q <- quantile(df_no_I_na$ratio_of_duplicate_prs, probs=c(.25, .75), na.rm = FALSE)
iqr <- IQR(df_no_I_na$ratio_of_duplicate_prs)
up <-  Q[2]+1.5*iqr  
low <- Q[1]-1.5*iqr
ratio_dup_df <- subset(df_no_I_na, df_no_I_na$ratio_of_duplicate_prs > (Q[1] - 1.5*iqr) & df_no_I_na$ratio_of_duplicate_prs < (Q[2]+1.5*iqr))
ratio_dup_df$ratio_of_duplicate_prs
boxplot(ratio_of_duplicate_prs ~ status, data = ratio_dup_df)
df_no_na$ratio_of_duplicate_prs

# 4. Central Management
Q <- quantile(df_no_I_na$cntr_management, probs=c(.25, .75), na.rm = FALSE)
iqr <- IQR(df_no_I_na$cntr_management)
up <-  Q[2]+1.5*iqr  
low <- Q[1]-1.5*iqr
cntr_df <- subset(df_no_I_na, df_no_I_na$cntr_management > (Q[1] - 1.5*iqr) & df_no_I_na$cntr_management < (Q[2]+1.5*iqr))
boxplot(cntr_management ~ status, data = cntr_df)

# 5. Additive contribution index
Q <- quantile(df_no_I_na$additive_contribution_index, probs=c(.25, .75), na.rm = FALSE)
iqr <- IQR(df_no_I_na$additive_contribution_index)
up <-  Q[2]+1.5*iqr  
low <- Q[1]-1.5*iqr
add_df <- subset(df_no_I_na, df_no_I_na$additive_contribution_index > (Q[1] - 1.5*iqr) & df_no_I_na$additive_contribution_index < (Q[2]+1.5*iqr))
boxplot(additive_contribution_index ~ status, data = add_df)

# 6. Logic-coupling index
Q <- quantile(df_no_I_na$logic_coupling_index, probs=c(.25, .75), na.rm = FALSE)
iqr <- IQR(df_no_I_na$logic_coupling_index)
up <-  Q[2]+1.5*iqr  
low <- Q[1]-1.5*iqr
log_df <- subset(df_no_I_na, df_no_I_na$logic_coupling_index > (Q[1] - 1.5*iqr) & df_no_I_na$logic_coupling_index < (Q[2]+1.5*iqr))
boxplot(logic_coupling_index ~ status, data = log_df)

## Histogram ##
hist(freq_df[,8][freq_df$status=='G' | freq_df$status=='R'], main = colnames(freq_df)[8],xlab = colnames(freq_df)[8], col = 'blue')
hist(dem_df[,9][df$status=='G' | df$status=='R'], main = colnames(dem_df)[9],xlab = colnames(dem_df)[9], col = 'blue')
hist(ratio_dup_df[,10][df$status=='G' | df$status=='R'], main = colnames(ratio_dup_df)[10],xlab = colnames(ratio_dup_df)[10], col = 'blue')
hist(cntr_df[,13][df$status=='G' | df$status=='R'], main = colnames(cntr_df)[13],xlab = colnames(cntr_df)[13], col = 'blue')
hist(add_df[,14][df$status=='G' | df$status=='R'], main = colnames(add_df)[14],xlab = colnames(add_df)[14], col = 'blue')
hist(log_df[,15][df$status=='G' | df$status=='R'], main = colnames(log_df)[15],xlab = colnames(log_df)[15], col = 'blue')

## Normalization ##


## Logistic Regression ##
xtabs(~status + frequency, data = freq_df)
xtabs(~status + has_hard_fork, data = df_no_I_na)

# 1. Frequency
logistic_f <- glm(status ~ frequency, data=freq_df, family="binomial")
summary(logistic_f)

# 2. Dimensional
logistic_d <- glm(status ~ dimensionality, data=dem_df, family="binomial")
summary(logistic_d)

# 3. Ratio of Duplicate PRs
RDP <- glm(status ~ ratio_of_duplicate_prs, data=df_no_I_na, family="binomial")
summary(RDP)

# 4. Present of hard fork
hard_fork <- glm(status ~ has_hard_fork, data=df_no_I_na, family="binomial")
summary(hard_fork)

####-------------------------------------------------------------------------------------------
# 5. Central management
logistic_cm <- glm(status ~ cntr_management, data=cntr_df, family="binomial")
summary(logistic_cm)

#"Pseudo R-squared" and its p-value
ll.null <- logistic_cm$null.deviance/-2
ll.proposed <- logistic_cm$deviance/-2

## McFadden's Pseudo R^2 = [ LL(Null) - LL(Proposed) ] / LL(Null)
(ll.null - ll.proposed) / ll.null
## chi-square value = 2*(LL(Proposed) - LL(Null))
1 - pchisq(2*(ll.proposed - ll.null), df=1)
## p-value = 1 - pchisq(chi-square value, df = 2-1)
1 - pchisq((logistic_cm$null.deviance - logistic_cm$deviance), df=1)

####-------------------------------------------------------------------------------------------
# 6. Additive contribution index
logistic_ac <- glm(status ~ additive_contribution_index, data=add_df, family="binomial")
summary(logistic_ac)

#"Pseudo R-squared" and its p-value
ll.null <- logistic_ac$null.deviance/-2
ll.proposed <- logistic_ac$deviance/-2

## McFadden's Pseudo R^2 = [ LL(Null) - LL(Proposed) ] / LL(Null)
(ll.null - ll.proposed) / ll.null
## chi-square value = 2*(LL(Proposed) - LL(Null))
1 - pchisq(2*(ll.proposed - ll.null), df=1)
## p-value = 1 - pchisq(chi-square value, df = 2-1)
1 - pchisq((logistic$null.deviance - logistic$deviance), df=1)

####-------------------------------------------------------------------------------------------

# 7. Logic-coupling index
logistic_lc <- glm(status ~ logic_coupling_index, data=log_df, family="binomial")
summary(logistic_lc)

#"Pseudo R-squared" and its p-value
ll.null <- logistic_lc$null.deviance/-2
ll.proposed <- logistic_lc$deviance/-2

## McFadden's Pseudo R^2 = [ LL(Null) - LL(Proposed) ] / LL(Null)
(ll.null - ll.proposed) / ll.null
## chi-square value = 2*(LL(Proposed) - LL(Null))
1 - pchisq(2*(ll.proposed - ll.null), df=1)
## p-value = 1 - pchisq(chi-square value, df = 2-1)
1 - pchisq((logistic_lc$null.deviance - logistic_lc$deviance), df=1)

####-------------------------------------------------------------------------------------------

# Modularity
tmp <- df_no_I_na[,c("status","additive_contribution_index","logic_coupling_index")]
logistic_m <- glm(status~., data=tmp, family="binomial")
summary(logistic_m)

#"Pseudo R-squared" and its p-value
ll.null <- logistic_m$null.deviance/-2
ll.proposed <- logistic_m$deviance/-2

## McFadden's Pseudo R^2 = [ LL(Null) - LL(Proposed) ] / LL(Null)
(ll.null - ll.proposed) / ll.null
## chi-square value = 2*(LL(Proposed) - LL(Null))
1 - pchisq(2*(ll.proposed - ll.null), df=1)
## p-value = 1 - pchisq(chi-square value, df = 2-1)
1 - pchisq((logistic$null.deviance - logistic$deviance), df=1)

####-------------------------------------------------------------------------------------------

# All Metric
tmp <- df_no_I_na[,c("status","frequency","dimensionality","ratio_of_duplicate_prs","cntr_management","additive_contribution_index","logic_coupling_index","has_hard_fork")]
all <- glm(status~., family = binomial,data = tmp)
summary(all)

#"Pseudo R-squared" and its p-value
ll.null <- all$null.deviance/-2
ll.proposed <- all$deviance/-2

## McFadden's Pseudo R^2 = [ LL(Null) - LL(Proposed) ] / LL(Null)
(ll.null - ll.proposed) / ll.null
## chi-square value = 2*(LL(Proposed) - LL(Null))
1 - pchisq(2*(ll.proposed - ll.null), df=1)
## p-value = 1 - pchisq(chi-square value, df = 2-1)
1 - pchisq((logistic$null.deviance - logistic$deviance), df=1)
####-------------------------------------------------------------------------------------------

## Logistic -> AIC
all2 <- stepAIC(all)
summary(all2)
summary(all2$fitted.values)
hist(all2$fitted.values,main = " Histogram ",xlab = "Probability", col = 'light blue')

logistic_ac2 <- stepAIC(logistic_ac)
summary(logistic_ac2)
summary(logistic_ac2$fitted.values)
hist(logistic_ac2$fitted.values,main = " Histogram ",xlab = "Probability", col = 'light blue')

logistic_lc2 <- stepAIC(logistic_lc)
summary(logistic_lc2)
summary(logistic_ac2$fitted.values)
hist(logistic_ac2$fitted.values,main = " Histogram ",xlab = "Probability", col = 'light blue')

tmp <- df_no_I_na[,c("status","additive_contribution_index","logic_coupling_index")]
all <- glm(status~., family = binomial,data = tmp)
all2 <- stepAIC(all)
summary(all2)


### Logistic Regression Plot ###
ggplot(df_, aes(x=additive_contribution, y=status)) + 
  geom_point(alpha=.5) +
  stat_smooth(method="glm", se=FALSE, method.args = list(family=binomial))

#fit logistic regression model
model <- glm(status ~ has_hard_fork, data=df_no_I_na, family=binomial)

#define new data frame that contains predictor variable
newdata <- data.frame(has_hard_fork=seq(min(df_no_I_na$has_hard_fork), max(df_no_I_na$has_hard_fork),len=300))

#use fitted model to predict values of vs
newdata$status = predict(model, newdata, type="response")

#plot logistic regression curve
plot(status ~ has_hard_fork, data=has_hard_fork, col="steelblue")
lines(status ~ has_hard_fork, newdata, lwd=2)




