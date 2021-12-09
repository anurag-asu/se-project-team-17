# 1. Load metrics value from csv file
df <- read.csv(file = 'all_metrics.csv')
df_no_I <- df[(df$status == 1) | (df$status == 2),]
str(df_no_I)
str(df)
summary(df)

# 2. Define "status" as categorical variable (Factor)
df[df$status == 0,]$status <- "I"
df[df$status == 1,]$status <- "G"
df[df$status == 2,]$status <- "R"
df$status <- as.factor(df$status)

df_no_I[df_no_I$status == 1,]$status <- 1
df_no_I[df_no_I$status == 2,]$status <- 0
head(df_no_I)
df_no_I$status <- as.factor(df_no_I$status)
df_no_I$has_hard_fork <- as.factor(df_no_I$has_hard_fork)
summary(df_no_I)
### Data cleaning ###
## 3. Remove NA values
df_no_na <- df[!(is.na(df$frequency) | is.na(df$dimensionality) | is.na(df$ratio_of_duplicate_prs) | is.na(df$cntr_management) | is.na(df$additive_contribution_index) | is.na(df$logic_coupling_index) | is.na(df$has_hard_fork)),]
summary(df_no_na)

df_no_I_na <- df_no_I[!(is.na(df_no_I$frequency) | is.na(df_no_I$dimensionality) | is.na(df_no_I$ratio_of_duplicate_prs) | is.na(df_no_I$cntr_management) | is.na(df_no_I$additive_contribution_index) | is.na(df_no_I$logic_coupling_index) | is.na(df_no_I$has_hard_fork)),]
summary(df_no_I_na)
