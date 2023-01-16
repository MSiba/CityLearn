import pandas as pd

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
