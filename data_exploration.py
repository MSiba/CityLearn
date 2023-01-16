import pandas as pd

DATA_PATH = "./citylearn/data/"
PHASE1 = DATA_PATH + "citylearn_challenge_2022_phase_1/"

B1csv = pd.read_csv(PHASE1 + "Building_1.csv")
#%%
B1csv.head(10)
#%%
B1header = B1csv.columns.values.tolist()
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
# interpretation: in some months, in some days, in some hours, the solar generation can be at its highest/lowest value