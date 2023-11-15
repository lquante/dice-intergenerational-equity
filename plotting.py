from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import MinMaxScaler

#TODO: adjust these path to your data
basepath = "/home/quante/Documents/projects/IAM-stochasticity-discounting/"
datapath = os.path.join(basepath,"data")

fileident = "20231113_averages_CostOverTime"
datadict = {"DICE-2016-R":"full","Abatement cost funding":"funding20","Non-linear discounting": "non-linear-discounting", "GDP limit":"non-linear-discounting-per-gdp"}
datafiles = {key: f"{fileident}-{value}.csv" for key, value in datadict.items()}


figurepath = os.path.join(basepath,"figures")
#create figure dir if it does not exist
if not os.path.exists(figurepath):
    os.makedirs(figurepath)


#color and size definitions for plots

fontsize_normal = 6
plt.rcParams.update({
    'text.usetex': False,
    'svg.fonttype': 'none',
    'font.family': 'sans-serif',
    'font.serif': 'FreeSerif',
    'font.monospace': 'Computer Modern Typewriter',
    'text.latex.preamble': r'\usepackage{sansmath}\sansmath',
    'font.size': fontsize_normal
})

centimeter = 1 / 2.54

maxfigurewidth = 18 * centimeter
smallfigurewidth = maxfigurewidth / 3
mediumfigurewidth = maxfigurewidth / 2

#colors as in schematic figure
teal = (60/255, 147/255, 194/255, 1)
green = (108/255, 188/255, 144/255, 1)
grey = (160/255, 160/255, 160/255, 1)
orange = (253/255, 141/255, 60/255, 1)

colordict = {"DICE-2016-R":grey, "Abatement cost funding":orange,"Non-linear discounting": teal, "GDP limit":green}

# make a plot with just a legend showing these 4 colors from the colordict
fig, ax = plt.subplots(figsize=(maxfigurewidth, 0.25))
for label, color in colordict.items():
    ax.plot([], [], color=color, label=label)
ax.legend(loc='center', ncol=4, frameon=False, fontsize=fontsize_normal)
ax.axis('off')
plt.tight_layout()
plt.savefig(os.path.join(figurepath, "legend.pdf"), dpi=300)

timelimit=250

#plot figure panel of emission, abatement, damages and total GDP relative cost in for panels a-d, plotting results for the several data in each subplot
fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(maxfigurewidth, maxfigurewidth))

# plot emission
axs[0, 0].set_xlabel('Year')
axs[0, 0].set_ylabel('Emissions [GT CO$_2$]')
axs[0, 0].set_xlim([0, timelimit])
axs[0, 0].text(-0.05, 1.05, 'a', transform=axs[0, 0].transAxes, fontweight='bold', fontsize=fontsize_normal)
for key, value in datadict.items():
    data = pd.read_csv(os.path.join(datapath, datafiles[key]))
    axs[0, 0].plot(data['time'][:timelimit], data['emission'][:timelimit], color=colordict[key])

# plot abatement
axs[0, 1].set_xlabel('Year')
axs[0, 1].set_ylabel('Abatement [%]')
axs[0, 1].set_xlim([0, timelimit])
axs[0, 1].text(-0.05, 1.05, 'b', transform=axs[0, 1].transAxes, fontweight='bold', fontsize=fontsize_normal)
for key, value in datadict.items():
    data = pd.read_csv(os.path.join(datapath, datafiles[key]))
    axs[0, 1].plot(data['time'][:timelimit], data['abatement'][:timelimit]*100, color=colordict[key])

# plot damages
axs[1, 0].set_xlabel('Year')
axs[1, 0].set_ylabel('Damages [%]')
axs[1, 0].set_xlim([0, timelimit])
axs[1, 0].text(-0.05, 1.05, 'c', transform=axs[1, 0].transAxes, fontweight='bold', fontsize=fontsize_normal)
for key, value in datadict.items():
    data = pd.read_csv(os.path.join(datapath, datafiles[key]))
    axs[1, 0].plot(data['time'][:timelimit], data['damage'][:timelimit]*100, color=colordict[key])

# plot total GDP relative cost
axs[1, 1].set_xlabel('Year')
axs[1, 1].set_ylabel('Total GDP Relative Cost [%]')
axs[1, 1].set_xlim([0, timelimit])
axs[1, 1].text(-0.05, 1.05, 'd', transform=axs[1, 1].transAxes, fontweight='bold', fontsize=fontsize_normal)
for key, value in datadict.items():
    data = pd.read_csv(os.path.join(datapath, datafiles[key]))
    total_gdp_relative_cost = (data['costAbatement'] + data['costDamage'])/data['gdp']
    axs[1, 1].plot(data['time'][:timelimit], total_gdp_relative_cost[:timelimit]*100, color=colordict[key])

# create a 5th axis for the legend
legend_ax = fig.add_axes([0, -0.075, 1, 0.1])

# plot the legend on the 5th axis
for label, color in colordict.items():
    legend_ax.plot([], [], color=color, label=label)
legend_ax.legend(loc='center', ncol=2, frameon=False, fontsize=fontsize_normal)
legend_ax.axis('off')
plt.tight_layout()
plt.savefig(os.path.join(figurepath, "pathways_panel.pdf"), dpi=300, bbox_inches='tight')


# next figure including generational exposure

#load population shares from materials directory
materialpath = os.path.join(basepath,"material")
population_shares = pd.read_csv(os.path.join(materialpath, "population_shares_by_birth_year.csv"), index_col=0)

# create plot up to 2100, showing on x axis year born, on y axis damage weighted by share of population alive born in x year
# calculate the share of the population alive born in each year
population_shares = pd.read_csv(os.path.join(materialpath, "population_shares_by_birth_year.csv"), index_col=0).T


start_weighting_year = 2015
end_weighting_year = 2100
index_of_weighting_years = end_weighting_year - start_weighting_year

# plot damage average by generation year for each key into one plot, showing damage average for 1 generation after the other as a square with the value inside

start_year = 1975

import matplotlib.cm as cm
import matplotlib.colors as colors

cmap = cm.get_cmap('Reds')
norm = colors.Normalize(vmin=0.0, vmax=1)


# create a figure with three subplots
fig, axs = plt.subplots(nrows=3, ncols=1, figsize=(maxfigurewidth, maxfigurewidth))

# plot the damage average by generation year for each key
key_index=0
generation_weighted_damage = {}
for key, value in datadict.items():
    data = pd.read_csv(os.path.join(datapath, datafiles[key]))
    # calculate the damage weighted by share of population alive born in year
    damage_weighted_by_share_alive = {}
    for generation_year in range(start_year,2075):
        damage_weighted_by_share_alive[generation_year] = data['costDamage'][0:index_of_weighting_years] * population_shares[generation_year].values

    # assuming damage_weighted_by_share_alive is a dictionary with generation year as keys and damage weighted by share of population alive born in year as values
    df = pd.DataFrame.from_dict(damage_weighted_by_share_alive, orient='index')
    df.columns = range(start_weighting_year,end_weighting_year)
    df.index.name = 'generation_year'

    #summarize damage along lifetime by averaging along time
    generation_weighted_damage[key] = df.mean(axis=1)

scaler = MinMaxScaler()

generation_weighted_damage_concatenated = np.concatenate(list(generation_weighted_damage.values()))
generation_weighted_damage_scaled = scaler.fit_transform(generation_weighted_damage_concatenated.reshape(-1, 1)).reshape(-1)
for key in generation_weighted_damage:
    generation_weighted_damage_scaled_key = generation_weighted_damage_scaled[0:len(generation_weighted_damage[key])]
    generation_weighted_damage[key] = generation_weighted_damage_scaled_key
    generation_weighted_damage_scaled = generation_weighted_damage_scaled[len(generation_weighted_damage[key]):]

for key, value in datadict.items():
    for i, damage in enumerate(generation_weighted_damage[key]):
        axs[0].add_patch(Rectangle((i+start_year, key_index-0.5), 1, 1, fill=True, color=cmap(norm(damage))))
        #ax.text(i+0.5, key_index+0.5, f"{damage:.2f}", ha='center', va='center', color='white')
    # add a horizontal line at the bottom of the subplot
    axs[0].axhline(y=key_index-0.5, color='black', linewidth=0.5)
    key_index+=1

# set the x and y axis labels and limits
axs[0].set_xlabel('Generation Year')
axs[0].set_ylabel('Scenario')
axs[0].set_xlim([1975, 2050])
axs[0].set_ylim([-0.5, len(datadict)-0.5])
axs[0].set_yticks(range(len(datadict)))
axs[0].set_yticklabels(datadict.keys())
axs[0].text(-0.05, 1.05, 'a', transform=axs[0].transAxes, fontweight='bold', fontsize=fontsize_normal)

# plot the abatement cost average by generation year for each key
key_index=0
generation_weighted_abatement_cost = {}
for key, value in datadict.items():
    data = pd.read_csv(os.path.join(datapath, datafiles[key]))
    # calculate the abatement cost weighted by share of population alive born in year
    abatement_cost_weighted_by_share_alive = {}
    for generation_year in range(start_year,2075):
        abatement_cost_weighted_by_share_alive[generation_year] = data['costAbatement'][0:index_of_weighting_years] * population_shares[generation_year].values

    # assuming abatement_cost_weighted_by_share_alive is a dictionary with generation year as keys and abatement cost weighted by share of population alive born in year as values
    df = pd.DataFrame.from_dict(abatement_cost_weighted_by_share_alive, orient='index')
    df.columns = range(start_weighting_year,end_weighting_year)
    df.index.name = 'generation_year'

    #summarize abatement cost along lifetime by averaging along time
    generation_weighted_abatement_cost[key] = df.mean(axis=1)

scaler = MinMaxScaler()

generation_weighted_abatement_cost_concatenated = np.concatenate(list(generation_weighted_abatement_cost.values()))
generation_weighted_abatement_cost_scaled = scaler.fit_transform(generation_weighted_abatement_cost_concatenated.reshape(-1, 1)).reshape(-1)
for key in generation_weighted_abatement_cost:
    generation_weighted_abatement_cost_scaled_key = generation_weighted_abatement_cost_scaled[0:len(generation_weighted_abatement_cost[key])]
    generation_weighted_abatement_cost[key] = generation_weighted_abatement_cost_scaled_key
    generation_weighted_abatement_cost_scaled = generation_weighted_abatement_cost_scaled[len(generation_weighted_abatement_cost[key]):]

for key, value in datadict.items():
    for i, abatement_cost in enumerate(generation_weighted_abatement_cost[key]):
        axs[1].add_patch(Rectangle((i+start_year, key_index-0.5), 1, 1, fill=True, color=cmap(norm(abatement_cost))))
        #ax.text(i+0.5, key_index+0.5, f"{abatement_cost:.2f}", ha='center', va='center', color='white')
    # add a horizontal line at the bottom of the subplot
    axs[1].axhline(y=key_index-0.5, color='black', linewidth=0.5)
    key_index+=1

# set the x and y axis labels and limits
axs[1].set_xlabel('Generation Year')
axs[1].set_ylabel('Scenario')
axs[1].set_xlim([1975, 2050])
axs[1].set_ylim([-0.5, len(datadict)-0.5])
axs[1].set_yticks(range(len(datadict)))
axs[1].set_yticklabels(datadict.keys())
axs[1].text(-0.05, 1.05, 'b', transform=axs[1].transAxes, fontweight='bold', fontsize=fontsize_normal)

# plot the total cost relative to GDP average by generation year for each key
key_index=0
generation_weighted_total_cost_relative_to_gdp = {}
for key, value in datadict.items():
    data = pd.read_csv(os.path.join(datapath, datafiles[key]))
    # calculate the total cost relative to GDP weighted by share of population alive born in year
    total_cost_relative_to_gdp_weighted_by_share_alive = {}
    for generation_year in range(start_year,2075):
        total_cost_relative_to_gdp_weighted_by_share_alive[generation_year] = (data['costAbatement'][0:index_of_weighting_years] + data['costDamage'][0:index_of_weighting_years]) / data['gdp'][0:index_of_weighting_years] * population_shares[generation_year].values

    # assuming total_cost_relative_to_gdp_weighted_by_share_alive is a dictionary with generation year as keys and total cost relative to GDP weighted by share of population alive born in year as values
    df = pd.DataFrame.from_dict(total_cost_relative_to_gdp_weighted_by_share_alive, orient='index')
    df.columns = range(start_weighting_year,end_weighting_year)
    df.index.name = 'generation_year'

    #summarize total cost relative to GDP along lifetime by averaging along time
    generation_weighted_total_cost_relative_to_gdp[key] = df.mean(axis=1)

scaler = MinMaxScaler()

generation_weighted_total_cost_relative_to_gdp_concatenated = np.concatenate(list(generation_weighted_total_cost_relative_to_gdp.values()))
generation_weighted_total_cost_relative_to_gdp_scaled = scaler.fit_transform(generation_weighted_total_cost_relative_to_gdp_concatenated.reshape(-1, 1)).reshape(-1)
for key in generation_weighted_total_cost_relative_to_gdp:
    generation_weighted_total_cost_relative_to_gdp_scaled_key = generation_weighted_total_cost_relative_to_gdp_scaled[0:len(generation_weighted_total_cost_relative_to_gdp[key])]
    generation_weighted_total_cost_relative_to_gdp[key] = generation_weighted_total_cost_relative_to_gdp_scaled_key
    generation_weighted_total_cost_relative_to_gdp_scaled = generation_weighted_total_cost_relative_to_gdp_scaled[len(generation_weighted_total_cost_relative_to_gdp[key]):]

for key, value in datadict.items():
    for i, total_cost_relative_to_gdp in enumerate(generation_weighted_total_cost_relative_to_gdp[key]):
        axs[2].add_patch(Rectangle((i+start_year, key_index-0.5), 1, 1, fill=True, color=cmap(norm(total_cost_relative_to_gdp))))
        #ax.text(i+0.5, key_index+0.5, f"{total_cost_relative_to_gdp:.2f}", ha='center', va='center', color='white')
    # add a horizontal line at the bottom of the subplot
    axs[2].axhline(y=key_index-0.5, color='black', linewidth=0.5)
    key_index+=1

# set the x and y axis labels and limits
axs[2].set_xlabel('Generation Year')
axs[2].set_ylabel('Scenario')
axs[2].set_xlim([1975, 2050])
axs[2].set_ylim([-0.5, len(datadict)-0.5])
axs[2].set_yticks(range(len(datadict)))
axs[2].set_yticklabels(datadict.keys())
axs[2].text(-0.05, 1.05, 'c', transform=axs[2].transAxes, fontweight='bold', fontsize=fontsize_normal)

plt.tight_layout()
plt.savefig(os.path.join(figurepath, "generational_square_panel.pdf"), dpi=300, bbox_inches='tight')