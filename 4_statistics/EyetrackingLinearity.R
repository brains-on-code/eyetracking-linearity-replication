library(lme4)
library(car)

# check whether you use the same package version
packageVersion("lme4") # 1.1.21
packageVersion("car") # 3.0.6

eyetracking_df <- read.csv("Metrics_Data_for_LMM.csv", sep=",")
View(eyetracking_df)

# Replace VerticalNext with the metric you want to model (VerticalNext, VerticalLater, Regression, HorizontalLater, LineRegression, SaccadeLength, StoryOrder_Naive_Score, StoryOrder_Dynamic_Score, ExecOrder_Naive_Score, ExecOrder_Dynamic_Score)
lmm = lmer(formula = VerticalNext ~ Expert + Scrambled + Linearity + (1|Participant), data = eyetracking_df)
summary(lmm)

Anova(lmm)