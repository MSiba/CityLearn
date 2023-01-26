import matplotlib.pyplot as plt
plt.style.use('ggplot')
import seaborn as sns

def plot_heatmap(df, month_nb, month_name, value_name, saveto):
    """
    plots a heatmap of a specific value, e.g. solar generation, w.r.t each hour of each month.
    :param df:
    :param month_nb:
    :param month_name:
    :param value_name:
    :param saveto:
    :return:
    """
    month = df.loc[df["Month"] == month_nb]

    #month.loc[month["Month"] == month_nb]["Day Number"] = ((month.index - month.index[0]) / 24 + 1).astype(int)
    month.loc[:, "Day Number"] = ((month.index - month.index[0]) / 24 + 1).astype(int)
    print(month["Day Number"])
    month_pivot = month.pivot(index='Hour', columns='Day Number', values=value_name)
    month_ax = sns.heatmap(month_pivot, annot=False)
    plt.yticks(rotation=45)
    plt.title("{} - {}".format(month_name, value_name))
    plt.savefig("{}/{}_{}.png".format(saveto, month_name, value_name))
    plt.show()