


import os
import pandas as pd

# TODO: adjust these path to your data
basepath = "/home/quante/Documents/projects/intergenerational-inequality-financing-cost/"
#basepath = "../../.././"

materialpath = os.path.join(basepath, "material")
relevant_columns = ["Year", "Total Population, as of 1 January (thousands)", "Births (thousands)", "Life Expectancy at Birth, both sexes (years)",
                    "Infant Mortality Rate (infant deaths per 1,000 live births)", "Under-Five Deaths, under age 5 (thousands)"]

population_data = {}
population_data["Estimates"] = pd.read_excel(os.path.join(
    materialpath, "WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx"), sheet_name="Estimates", header=0, skiprows=range(0, 16), nrows=72)
population_data["Medium variant"] = pd.read_excel(os.path.join(
    materialpath, "WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx"), sheet_name="Medium variant", header=0, skiprows=range(0, 16), nrows=79)
# combine population data frames by year
combined_population_data = pd.concat([population_data["Estimates"][relevant_columns],
                                     population_data["Medium variant"][relevant_columns]], ignore_index=True).sort_values(by="Year")
combined_population_data["Birth Year Life Expectancy Estimate"] = (
    combined_population_data["Life Expectancy at Birth, both sexes (years)"])

# extract df with generation lifeExpectancy expectation
generation_lifeExpectancy = combined_population_data[[
    "Year", "Birth Year Life Expectancy Estimate"]].set_index("Year")


# export generation lifeExpectancy as csv
generation_lifeExpectancy.to_csv(os.path.join(materialpath, "LifeExpectancyByBirthYear.csv"))
