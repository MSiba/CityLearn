import os
import pandas as pd
import numpy as np
import calendar
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import seaborn as sns
import scipy.stats
from exploration_utils import plot_heatmap


DATA_PATH = "./citylearn/data/"
PHASE1 = DATA_PATH + "citylearn_challenge_2022_phase_1/"

"""
------------------------- Building1 Inspection -------------------------
"""
B1csv = pd.read_csv(PHASE1 + "Building_1.csv")
#%%
B1csv.head(10)
#%%
B1header = B1csv.columns.values.tolist()
"""
['Month',
 'Hour',
 'Day Type',
 'Daylight Savings Status',
 'Indoor Temperature [C]',
 'Average Unmet Cooling Setpoint Difference [C]',
 'Indoor Relative Humidity [%]',
 'Equipment Electric Power [kWh]',
 'DHW Heating [kWh]',
 'Cooling Load [kWh]',
 'Heating Load [kWh]',
 'Solar Generation [W/kW]']
 """
# 12 columns
#%%
B1csv.shape
# (8760, 12)
#%%
B1csv["Month"].value_counts()
# datatype float (1.0-12.0)
# it appears 744 times if the month is 31 days,
# 720 if 30 days
# 672 if 28 days (Feb.)
# This means: each day of the month is represented by each hour of that day
#%%
B1csv["Hour"].value_counts()
# datatype int64 (1.0 - 24.0) -each 365
# it means that each hour appears once a day

#%%
B1csv["Day Type"].value_counts()
# represents whether it is a Monday- Sunday
# encoded as 1.0 - 7.0
# type: int64

#%%
B1csv["Daylight Savings Status"].value_counts()
# only 0, maybe it doesn't have any PV

#%%
B1csv["Indoor Temperature [C]"].value_counts()
# empty [] of type int64

#%%
B1csv["Average Unmet Cooling Setpoint Difference [C]"].value_counts()
# empty [] of type int64

#%%
B1csv["Indoor Relative Humidity [%]"].value_counts()
# empty [] of type int64

#%%
B1csv["Equipment Electric Power [kWh]"].value_counts()
# 8556 different numbers of type int64
#%%
B1csv["Equipment Electric Power [kWh]"].describe()

"""
count    8760.000000
mean        1.208145
std         0.968270
min         0.057000
25%         0.570167
50%         0.812079
75%         1.530529
max         7.987483
"""
# interpretation: in some months, in some days, in specific hours of the day,
# the equipment electricity power is higher/lower than others
#%%
# Test the correlation between Month, Hour, and electricity power
cov_e = B1csv[["Month", "Hour", "Equipment Electric Power [kWh]"]].corr()
sns.set(style='ticks', color_codes=True)

sns.heatmap(cov_e,
            xticklabels=cov_e.columns,
            yticklabels=cov_e.columns)
plt.show()
# The Equipment Electric Power is much more correlated with the Hour of the day than the month
# corr(electric Power, Hour) = 0.22589
# corr(electric Power, Month) = 0.05421
#%%
# At which hour of the day the Equipment Electric Power is highest/lower?
ep_hour = B1csv[["Hour", "Equipment Electric Power [kWh]"]]
sns.boxplot(data=ep_hour, x="Hour", y="Equipment Electric Power [kWh]")
plt.xticks(rotation=45)
plt.show()
# The exact hours of maximum electric Power:
# from 9-12 am and from 16-21 pm
#The exact hours of lowest electric Power consumption
# from 1-5 am, NOTE: with many outliers.
# This can maybe be explained by considering the month also,
#since at some months, some occasions occur.
#%%
ep_month = B1csv[["Month", "Equipment Electric Power [kWh]"]]
sns.boxplot(data=ep_month, x="Month", y="Equipment Electric Power [kWh]")
plt.show()
# Interpretation: In July and August, the EEP is max
# In March, April, October, and November it is lowest
#%%
# combine the month-Day Type Hour index in one column + order
all_col = B1csv[["Month", "Day Type", "Hour", "Equipment Electric Power [kWh]"]]
all_col["datetime"] = (all_col["Month"].astype(str) + "-" + all_col["Day Type"].astype(str) + "-" + all_col["Hour"].astype(str) + " " + all_col.index.astype(str))
#%%
all_col.plot(y="Equipment Electric Power [kWh]", style='.')
plt.xticks(rotation=90)
plt.show()
#%%
# for each month
    # for each day
        # for each hour
            # plot the electricity
january = B1csv.loc[B1csv["Month"] == 1.0]

#%%
january.loc[january["Month"] == 1.0]["Day Number"] = ((january.index - 3673) / 24 + 1).astype(int)
jan_pivot = january.pivot(index='Hour', columns='Day Number', values='Equipment Electric Power [kWh]')
jan_ax = sns.heatmap(jan_pivot, annot=False)
plt.yticks(rotation=45)
plt.title("January EEP(KWh)")
plt.savefig("./January_EEP")
plt.show()
#%%
february = B1csv.loc[B1csv["Month"] == 2.0]
#%%
february.loc[february["Month"] == 2.0]["Day Number"] = ((february.index - 4417) / 24 + 1).astype(int)
#%%
feb_pivot = february.pivot(index='Hour', columns='Day Number', values='Equipment Electric Power [kWh]')
feb_ax = sns.heatmap(feb_pivot, annot=False)
plt.yticks(rotation=45)
plt.title("February EEP (kWh)")
plt.savefig("./February_EEP.png")
plt.show()

#%%
def plot_heatmap(df, month_nb, month_name, value_name, saveto):

    month = df.loc[df["Month"] == month_nb]

    #month.loc[month["Month"] == month_nb]["Day Number"] = ((month.index - month.index[0]) / 24 + 1).astype(int)
    month.loc[:, "Day Number"] = ((month.index - month.index[0]) / 24 + 1).astype(int)
    print(month["Day Number"])
    month_pivot = month.pivot(index='Hour', columns='Day Number', values=value_name)
    month_ax = sns.heatmap(month_pivot, annot=False)
    plt.yticks(rotation=45)
    plt.title("{} - {}".format(month_name, value_name))
    plt.savefig(os.path.join(saveto, month_name)) #"{}/{}_{}.png".format(saveto, month_name, value_name))
    plt.show()
# when exactly does the eq. electricity power at its
# highest?
# lowest?
#%%
months = np.arange(1.0, 13.0, 1.0)
months_name = calendar.month_name[1:]
val_n = 'Equipment Electric Power [kWh]'
dest_file = "./EEP_B1"
for i in range(len(months)):
    plot_heatmap(df=B1csv, month_nb=months[i], month_name=months_name[i], value_name=val_n, saveto=dest_file)
#%%
B1csv["DHW Heating [kWh]"].value_counts()
# here, the hot water is 0 for B1

#%%
B1csv["Cooling Load [kWh]"].value_counts()
# here, the cooling load is 0 for all entries

#%%
B1csv["Heating Load [kWh]"].value_counts()
# also, 0 for all entries

#%%
B1csv["Solar Generation [W/kW]"].value_counts()
# 4168 different entries for solar generation
#%%
B1csv["Solar Generation [W/kW]"].describe()
# range: 0.0 - 976.25
"""
count    8760.000000
mean      205.836089
std       290.977786
min         0.000000
25%         0.000000
50%         0.000000
75%       412.108333
max       976.250000"""
# interpretation: in some months, in some days, in some hours,
# the solar generation can be at its highest/lowest value
#%%
# Test the correlation between Month, Hour, and solar generation
cov_sg = B1csv[["Month", "Hour", "Solar Generation [W/kW]"]].corr()
sns.set(style='ticks', color_codes=True)

sns.heatmap(cov_sg,
            xticklabels=cov_sg.columns,
            yticklabels=cov_sg.columns)
plt.show()
# Interpretation: there is a negative correlation with hour and Month, meaning
# when the hour/month increases, the solar generation decreases?
# however, the negative correlation is almost negligeable, because it is almost 0
# ==> no correlation
# corr(Month, Solar Generation) = -0.016115
# corr(Hour, Solar Generation) = -0.045765
# corr(EEP, Solar Generation) = 0.011268
#%%
months = np.arange(1.0, 13.0, 1.0)
months_name = calendar.month_name[1:]
sg = "Solar Generation [W/kW]"
path = os.path.dirname(os.path.abspath(__file__))
sg_file = "SolarGeneration_B1"
for i in range(len(months)):
    plot_heatmap(df=B1csv, month_nb=months[i], month_name=months_name[i], value_name=sg, saveto=os.path.join(path, sg_file))

# which months produce the highest solar generation?

#%%
"""
------------------------- carbon_intensity.csv Inspection -------------------------
"""
ci = pd.read_csv(PHASE1 + "carbon_intensity.csv")
# unit kg_CO2/kWh
#%%
ci.describe()
"""
        kg_CO2/kWh
count  8760.000000
mean      0.156531
std       0.035370
min       0.070383
25%       0.131080
50%       0.154263
75%       0.178429
max       0.281796
"""
# interpretation: for each month of the year, for each day of the month, for each hour of the day
# ci is the actual CO2 emission rate from grid mix.
# range: between 0.07 - 0.28
#%%

"""
------------------------- pricing.csv Inspection -------------------------
"""
pricing = pd.read_csv(PHASE1 + "pricing.csv")

#%%
pricingheader = pricing.columns.values.tolist()
"""
'Electricity Pricing [$]',
 '6h Prediction Electricity Pricing [$]',
 '12h Prediction Electricity Pricing [$]',
 '24h Prediction Electricity Pricing [$]'
 """
#%%
pricing["Electricity Pricing [$]"].value_counts()

# electricity pricing is different for entries
# Time-of-Use (TOU) electricity cost.
"""
0.21    4617
0.22    2318
0.50    1215
0.54     440
0.40     170
"""
#%%
pricing["6h Prediction Electricity Pricing [$]"].value_counts()
# like before

#%%
pricing["12h Prediction Electricity Pricing [$]"].value_counts()

#%%
pricing["24h Prediction Electricity Pricing [$]"].value_counts()
# all same

"""
------------------------- weather.csv Inspection -------------------------
['Outdoor Drybulb Temperature [C]',
 'Relative Humidity [%]',
 'Diffuse Solar Radiation [W/m2]',
 'Direct Solar Radiation [W/m2]',
 '6h Prediction Outdoor Drybulb Temperature [C]',
 '12h Prediction Outdoor Drybulb Temperature [C]',
 '24h Prediction Outdoor Drybulb Temperature [C]',
 '6h Prediction Relative Humidity [%]',
 '12h Prediction Relative Humidity [%]',
 '24h Prediction Relative Humidity [%]',
 '6h Prediction Diffuse Solar Radiation [W/m2]',
 '12h Prediction Diffuse Solar Radiation [W/m2]',
 '24h Prediction Diffuse Solar Radiation [W/m2]',
 '6h Prediction Direct Solar Radiation [W/m2]',
 '12h Prediction Direct Solar Radiation [W/m2]',
 '24h Prediction Direct Solar Radiation [W/m2]']
"""
#%%
weather = pd.read_csv(PHASE1 + "weather.csv")
#(one year) of actual meteorological weather data for the buildings' location used to provide observation values to the environment.
#%%
weatherheader = weather.columns.values.tolist()
#%%
weather.shape
# (8760, 16)
#%%
weather["Outdoor Drybulb Temperature [C]"].value_counts()
# unit:     C
# range: 5.6 - 32.2
#%%
weather["Outdoor Drybulb Temperature [C]"].describe()
"""
count    8760.000000
mean       16.837454
std         3.564816
min         5.600000
25%        14.400000
50%        17.200000
75%        19.400000
max        32.200000
"""
#%%
weather["Relative Humidity [%]"].value_counts()
#%%
weather["Relative Humidity [%]"].describe()
"""
count    8760.000000
mean       73.004224
std        16.480251
min        10.000000
25%        65.000000
50%        76.000000
75%        84.000000
max       100.000000
"""
#%%
weather["Diffuse Solar Radiation [W/m2]"].describe()
"""
count    8760.000000
mean      208.282192
std       292.799407
min         0.000000
25%         0.000000
50%        10.000000
75%       382.000000
max      1017.000000
"""

#%%
weather["Direct Solar Radiation [W/m2]"].describe()
"""
count    8760.000000
mean      201.231507
std       296.193301
min         0.000000
25%         0.000000
50%         0.000000
75%       424.000000
max       953.000000
"""

#%%
"""
------------------------- schema.json Inspection -------------------------
"""
#%%
ALL_B1 = pd.concat([B1csv, ci, pricing, weather], axis=1)
ALL_B1.shape # (8760, 33)
#%%
ALL_B1.columns.values.tolist()
#%%
# Test Correlation between all non-nan columns of the whole dataset
cols = ['Month',
 'Hour',
 'Equipment Electric Power [kWh]',
 'Solar Generation [W/kW]',
 'kg_CO2/kWh',
 'Electricity Pricing [$]',
 'Outdoor Drybulb Temperature [C]',
 'Relative Humidity [%]',
 'Diffuse Solar Radiation [W/m2]',
 'Direct Solar Radiation [W/m2]']

cov_all = ALL_B1[cols].corr()
sns.set(style='ticks', color_codes=True)
sns.set(font_scale=0.7)
sns.heatmap(cov_all,
            xticklabels=cov_all.columns,
            yticklabels=cov_all.columns,
            annot=True)
plt.xticks(rotation=45)
plt.title("Correlation of main attributes")
plt.savefig("./Correlation_all")
plt.show()