import pandas
import researchpy as rp

import statsmodels.api as sm
import statsmodels.formula.api as smf
import statsmodels.stats.multicomp


def run_anova_analysis():
    full_df = pandas.read_csv("../output/AOI/Metrics_Data_for_Anova.csv")

    #print(df.mean(axis=0))

    #metrics = ['HitsLine', 'HitsBlocks', 'HitsAnswer',
    #           'VerticalNext', 'VerticalLater', 'Regression', 'HorizontalLater', 'LineRegression', 'SaccadeLength',
    #           'StoryOrder_Naive_Score', 'StoryOrder_Dynamic_Score', 'StoryOrder_Dynamic_Repetitions', 'ExecOrder_Naive_Score', 'ExecOrder_Dynamic_Score', 'ExecOrder_Dynamic_Repetitions']

    metrics = ['VerticalNext', 'VerticalLater', 'Regression', 'HorizontalLater', 'LineRegression', 'SaccadeLength']

    grouped1 = full_df.groupby(['Expert']).mean()
    grouped1.to_csv('../output/AOI/results_grouped_expert.csv')

    grouped2 = full_df.groupby(['Scrambled']).mean()
    grouped2.to_csv('../output/AOI/results_grouped_scrambled.csv')

    grouped3 = full_df.groupby(['Linearity']).mean()
    grouped3.to_csv('../output/AOI/results_grouped_linearity.csv')

    # todo test all metrics and write in separate files?
    for metric_to_be_tested in metrics:
        with open('../output/AOI/results_stats_anova_' + metric_to_be_tested + '.txt', 'w') as file_output:
            df = full_df.drop(full_df.columns.difference(['Expert', 'Scrambled', 'Linearity', metric_to_be_tested]), 1)

            print(df.head(5))

            #print(rp.summary_cont(df.groupby(['Expert', 'Scrambled', 'Linearity']))[metric_to_be_tested])

            model = smf.ols(metric_to_be_tested + ' ~ C(Expert) * C(Scrambled) * C(Linearity)', df).fit()

            # only if interaction effect is insignificant, we can remove it from the model
            #model = ols(metric_to_be_tested + ' ~ C(Expert) + C(Scrambled) + C(Linearity)', df).fit()

            #model = smf.mixedlm(metric_to_be_tested + ' ~ C(Expert) * C(Scrambled) * C(Linearity)', df).fit()

            file_output.write(str(model.summary()))
            file_output.write(str(model.diagn))

            #result = sm.regression.mixed_linear_model.MixedLM(model, typ=2)
            result = sm.stats.anova_lm(model, typ=2)
            file_output.write(str(result))

            # post-hoc testing
            try:
                file_output.write('\n### POST-HOC: EXPERTISE')
                mc = statsmodels.stats.multicomp.MultiComparison(df[metric_to_be_tested], df['Expert'])
                mc_results = mc.tukeyhsd()
                file_output.write(str(mc_results))

                file_output.write('\n### POST-HOC: COMPREHENSION STRATEGY')
                mc = statsmodels.stats.multicomp.MultiComparison(df[metric_to_be_tested], df['Scrambled'])
                mc_results = mc.tukeyhsd()
                file_output.write(str(mc_results))

                file_output.write('\n### POST-HOC: LINEARITY')
                mc = statsmodels.stats.multicomp.MultiComparison(df[metric_to_be_tested], df['Linearity'])
                mc_results = mc.tukeyhsd()
                file_output.write(str(mc_results))
            except:
                file_output.write('post-hoc testing with tukeyhsd failed...')


if __name__ == "__main__":
    run_anova_analysis()