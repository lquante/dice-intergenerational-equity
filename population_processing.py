import os
import pandas as pd


#TODO: adjust these path to your data
basepath = "/home/quante/Documents/projects/IAM-stochasticity-discounting/"

# get data mapping damages from years 2020 onwards onto generations being born in 1950 or later
materialpath = os.path.join(basepath,"material")

relevant_columns =  ["Year","Total Population, as of 1 January (thousands)","Births (thousands)","Life Expectancy at Birth, both sexes (years)","Infant Mortality Rate (infant deaths per 1,000 live births)","Under-Five Deaths, under age 5 (thousands)"]


population_data = {}
population_data["Estimates"] = pd.read_excel(os.path.join(materialpath, "WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx"), sheet_name="Estimates", header=0, skiprows=range(0,16), nrows=72)
population_data["Medium variant"] = pd.read_excel(os.path.join(materialpath, "WPP2022_GEN_F01_DEMOGRAPHIC_INDICATORS_COMPACT_REV1.xlsx"), sheet_name="Medium variant", header=0, skiprows=range(0,16), nrows=79)


# combine population data frames by year
combined_population_data = pd.concat([population_data["Estimates"][relevant_columns], population_data["Medium variant"][relevant_columns]], ignore_index=True)

# sort the combined data frame by year
combined_population_data = combined_population_data.sort_values(by="Year")

#combined_population_data["Births adjusted for five year mortality"] = combined_population_data["Births (thousands)"]-combined_population_data["Under-Five Deaths, under age 5 (thousands)"]
#combined_population_data["Births adjusted for infant mortality"] = combined_population_data["Births (thousands)"]*(1000-combined_population_data["Infant Mortality Rate (infant deaths per 1,000 live births)"])/1000
combined_population_data["Generational Lifetime Estimate"] = (combined_population_data["Year"] + combined_population_data["Life Expectancy at Birth, both sexes (years)"]).astype(int)

  
# use relavant population data to calculate the fraction of population alive that was born in 1950 or later, starting 2020combined_population_data_1950 = combined_population_data[combined_population_data['Year'] >= 2020]

shares_by_comparison_year = {}
for comparison_year in range(2015,2100):
    total_population = combined_population_data[combined_population_data['Year'] == comparison_year]["Total Population, as of 1 January (thousands)"].values[0]
    # calculate share of previous years population that is still alive
    share_alive_population = {}
    for year in range(1960,2101):
        year_data = combined_population_data[combined_population_data['Year'] == year]
        if year > comparison_year:
            share_generation = 0.0
        else:
            if year_data["Generational Lifetime Estimate"].values[0] >= comparison_year:
                share_generation = year_data["Births (thousands)"].values[0]/total_population
            else:
                share_generation = 0.0
        share_alive_population[year] = share_generation
    shares_by_comparison_year[comparison_year] = pd.DataFrame.from_dict(share_alive_population, orient='index')
#merge all shares into one dataframe
shares = pd.concat(shares_by_comparison_year, axis=1)
shares.to_csv(os.path.join(materialpath, "population_shares_by_birth_year.csv"))