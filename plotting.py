import matplotlib.colors as colors
import matplotlib.cm as cm
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from matplotlib import cm, colors, colorbar

# color and size definitions for plots

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

centimeter = 1 / 2.54  # convert inches to cm

maxfigurewidth = 18 * centimeter
smallfigurewidth = maxfigurewidth / 3
mediumfigurewidth = maxfigurewidth / 2

# TODO: adjust these path to your data
basepath = "/home/quante/Documents/projects/intergenerational-inequality-financing-cost/"
datapath = os.path.join(basepath, "data")

figurepath = os.path.join(basepath, "figures")
# create figure dir if it does not exist
if not os.path.exists(figurepath):
    os.makedirs(figurepath)

# plot on cost sensitivity data
file = "202312_CostSensitivity-reduced.csv"
sensitivity_data = pd.read_csv(os.path.join(datapath, file))

timelimit = 350

abatementSensitivity = sensitivity_data["abatementSensitivityWeighted mean"][:timelimit]
damageSensitivity = sensitivity_data["damageSensitivityWeighted mean"][:timelimit]

abatementColor = (108/255, 188/255, 144/255, 1)
damageColor = (253/255, 141/255, 60/255, 1)

# plot abatement and damage sensitivity weighted by cost to value weight and discount factor in the same plot, using a darkish green and darkish red color
fig, ax = plt.subplots(figsize=(maxfigurewidth, maxfigurewidth/2))
ax.plot(abatementSensitivity, color=abatementColor)
ax.plot(damageSensitivity, color=damageColor)

# Fill area below the curves with a light shade
ax.fill_between(range(timelimit), abatementSensitivity,
                color=abatementColor, alpha=0.3)
ax.fill_between(range(timelimit), damageSensitivity,
                color=damageColor, alpha=0.3)

# add a vertical line at the maxima of the curves
ax.axvline(x=abatementSensitivity.idxmin(),
           color=abatementColor, linestyle='--', linewidth=0.5)
ax.axvline(x=damageSensitivity.idxmax(), color=damageColor,
           linestyle='--', linewidth=0.5)

# Draw horizontal line between min and max
min_x = abatementSensitivity.idxmin()
max_x = damageSensitivity.idxmax()
min_y = abatementSensitivity[min_x]
max_y = damageSensitivity[max_x]
ax.hlines(0, min_x, max_x, color='black', linewidth=0.5)

# Draw small vertical lines at min and max
ax.vlines(min_x, -20, 20, color='black', linewidth=0.5)
ax.vlines(max_x, -20, 20, color='black', linewidth=0.5)

ax.annotate("abatement-damage shift", xy=((abatementSensitivity.idxmin() +
            damageSensitivity.idxmax()) / 2, -60), ha='center', va='center')

ax.set_xlim([0, timelimit])
ax.set_xlabel('Time t')
ax.set_ylabel(
    'Cost sensitivity: $\\frac{d C}{d T} \\frac{d V}{d C} \\frac{N(0)}{N(t)}$')

plt.savefig(os.path.join(
    figurepath, "cost_sensitivity_abatement_damage_weighted.pdf"), dpi=300, bbox_inches='tight')


# plots on simulation data

fileident = "202312_CostOverTime"
datadict = {"DICE-2016-R": "full", "Abatement cost funding": "funding20",
            "Non-linear discounting": "non-linear-discounting", "3% GDP limit": "non-linear-discounting-per-gdp"}
datadict_stochastic = {"Stochastic DICE": "stochastic-model-reduced", "Stochastic abatement cost funding": "stochastic-model-funding20",
                       "Stochastic non-linear discounting": "stochastic-model-non-linear-discounting", "Stochastic 3% GDP limit": "stochastic-model-non-linear-discounting-per-gdp"}
# todo: use stochastic 20y funding + stochastic gdp limit
combined_datadict = {**datadict, **datadict_stochastic}
datafiles = {key: f"{fileident}-{value}.csv" for key,
             value in combined_datadict.items()}

variables = ["damage", "abatement", "emission",
             "gdp", "costAbatement", "costDamage"]
sub_keys = ["mean", "stddev", "5pc", "10pc", "90pc", "95pc"]

keys = {}
for variable in variables:
    keys[variable] = {}
    for sub_key in sub_keys:
        keys[variable][sub_key] = "{} {}".format(variable, sub_key)

# colors as in schematic figure
teal = (60/255, 147/255, 194/255, 1)
green = (108/255, 188/255, 144/255, 1)
grey = (160/255, 160/255, 160/255, 1)
orange = (253/255, 141/255, 60/255, 1)
purple = (75/255, 59/255, 85/255, 1)  # hex 4b3b55

colordict = {"DICE-2016-R": grey, "Stochastic DICE": green, "Abatement cost funding": orange, "Non-linear discounting": teal,
             "3% GDP limit": purple, "Stochastic abatement cost funding": orange, "Stochastic non-linear discounting": teal, "Stochastic 3% GDP limit": purple}
# same colors for stochastic abatement, stochastic discounting and gdp limit as for non-stochastic

# make a plot with just a legend showing these 4 colors from the colordict
fig, ax = plt.subplots(figsize=(maxfigurewidth, 0.25))
for label, color in colordict.items():
    ax.plot([], [], color=color, label=label)
ax.legend(loc='center', ncol=4, frameon=False, fontsize=fontsize_normal)
ax.axis('off')
plt.tight_layout()
plt.savefig(os.path.join(figurepath, "legend.pdf"), dpi=300)


# plot figure panel of emission, abatement, damages and total GDP relative cost in for panels a-d, plotting results for the several data in each subplot

def plot_subplots(scenario_inputs, timelimit=250):
    fig, axs = plt.subplots(nrows=2, ncols=2, figsize=(
        maxfigurewidth, maxfigurewidth))

    # add small letters to the subplots
    for row in range(2):
        for col in range(2):
            axs[row, col].set_xlabel('Year')
            axs[row, col].set_xlim([0, timelimit])
            axs[row, col].text(-0.05, 1.05, chr(97 + row * 2 + col), transform=axs[row,
                               col].transAxes, fontweight='bold', fontsize=fontsize_normal)

    for scenario in scenario_inputs:
        key = scenario
        data = pd.read_csv(os.path.join(datapath, datafiles[key]))

        axs[0, 0].plot(data['time'][:timelimit], data[keys["emission"]
                       ["mean"]][:timelimit], color=colordict[key])
        axs[0, 0].set_ylabel('Emission (GtCO2)')
        axs[0, 1].plot(data['time'][:timelimit], data[keys["abatement"]
                       ["mean"]][:timelimit]*100, color=colordict[key])
        axs[0, 1].set_ylabel('Abatement (percent)')
        axs[1, 0].plot(data['time'][:timelimit], data[keys["damage"]
                       ["mean"]][:timelimit]*100, color=colordict[key])
        axs[1, 0].set_ylabel('Damage (percent)')
        total_gdp_relative_cost = (
            data[keys["costAbatement"]["mean"]] + data[keys["costDamage"]["mean"]])/data[keys["gdp"]["mean"]]
        axs[1, 1].plot(data['time'][:timelimit],
                       total_gdp_relative_cost[:timelimit]*100, color=colordict[key])
        axs[1, 1].set_ylabel('Total cost (percent of GDP)')

        # add ci based on 10pc and 90pc
        if "Stochastic" in key:
            axs[0, 0].fill_between(data['time'][:timelimit], data[keys["emission"]["10pc"]][:timelimit],
                                   data[keys["emission"]["90pc"]][:timelimit], color=colordict[key], alpha=0.2)
            axs[0, 1].fill_between(data['time'][:timelimit], data[keys["abatement"]["10pc"]][:timelimit]
                                   * 100, data[keys["abatement"]["90pc"]][:timelimit]*100, color=colordict[key], alpha=0.2)
            axs[1, 0].fill_between(data['time'][:timelimit], data[keys["damage"]["10pc"]][:timelimit]
                                   * 100, data[keys["damage"]["90pc"]][:timelimit]*100, color=colordict[key], alpha=0.2)
            # slightly inaccurate for total cost but for now ok?!
            axs[1, 1].fill_between(data['time'][:timelimit], ((data[keys["costAbatement"]["10pc"]] + data[keys["costDamage"]["10pc"]])/data[keys["gdp"]["10pc"]])[:timelimit]
                                   * 100, ((data[keys["costAbatement"]["90pc"]] + data[keys["costDamage"]["90pc"]])/data[keys["gdp"]["90pc"]])[:timelimit]*100, color=colordict[key], alpha=0.2)

    legend_ax = fig.add_axes([0, -0.075, 1, 0.1])

    # plot the legend on the 5th axis
    for label in scenario_inputs:
        legend_ax.plot([], [], color=colordict[label], label=label)
    legend_ax.legend(loc='center', ncol=3, frameon=False,
                     fontsize=fontsize_normal)
    legend_ax.axis('off')
    plt.tight_layout()
    return fig


scenariosets = {"deterministic_stochastic": ["DICE-2016-R", "Stochastic DICE"], "deterministic": ["DICE-2016-R", "Abatement cost funding", "3% GDP limit"],
                "stochastic": ["Stochastic DICE", "Stochastic abatement cost funding", "Stochastic 3% GDP limit"]}


materialpath = os.path.join(basepath, "material")
generation_lifetime = pd.read_csv(os.path.join(
    materialpath, "LifeExpectancyByBirthYear.csv"), index_col=0)

# plot lifetime damage by birth year
start_year = 2015
end_year = 2200
start_aggregation_year = 2015

def calculate_lifetime_aggregate(variable, start_year, end_year, generation_lifetime, data, start_aggregation_year, relative_gdp=False, gdp_share=1, average=False):
    lifetime_aggregate = {}
    for generation_year in range(start_year, end_year):
        if generation_year > 2100:
            end_lifetime = int(generation_lifetime.loc[2100].values[0]) + generation_year  # just extending with static life expectancy
        else:
            end_lifetime = int(generation_lifetime.loc[generation_year].values[0]) + generation_year
        
        if end_lifetime >= start_aggregation_year:
            start_index = max(0,generation_year-start_aggregation_year)
            end_index = end_lifetime-start_aggregation_year
            if relative_gdp:
                lifetime_aggregate[generation_year] = np.nansum(
                    data[variable][start_index:end_index]/(data["gdp mean"][start_index:end_index]*gdp_share))*100
            else:
                lifetime_aggregate[generation_year] = np.nansum(
                    data[variable][start_index:end_index])
        else:
            lifetime_aggregate[generation_year] = 0.0
    if average:
        lifetime_aggregate = {
            key: value/(end_index-start_index) for key, value in lifetime_aggregate.items()}
    df = pd.DataFrame.from_dict(lifetime_aggregate, orient='index')
    df.index.name = 'generation_year'
    return df


# simpler plot, just plotting total cost relative to 3% of GDP per timestep, summed along lifetime of generation


def plot_total_cost_relative_to_gdp(scenario_keys):
    fig, axs = plt.subplots(nrows=1, ncols=1, figsize=(
        maxfigurewidth, maxfigurewidth/4))
    new_cmap = plt.cm.get_cmap('seismic', 256)
    new_norm = colors.TwoSlopeNorm(vmin=0.0, vcenter=3.0, vmax=6.0)

    total_cost_relative_to_gdp = {}
    for key in scenario_keys:
        data = pd.read_csv(os.path.join(datapath, datafiles[key]))
        abatement_cost_relative_to_gdp = calculate_lifetime_aggregate(
            "costAbatement mean", start_year, end_year, generation_lifetime, data, start_aggregation_year, relative_gdp=True, gdp_share=1, average=True)
        damage_cost_relative_to_gdp = calculate_lifetime_aggregate(
            "costDamage mean", start_year, end_year, generation_lifetime, data, start_aggregation_year, relative_gdp=True, gdp_share=1, average=True)
        total_cost_relative_to_gdp[key] = abatement_cost_relative_to_gdp + \
            damage_cost_relative_to_gdp

    key_index = len(scenario_keys)-1
    for key in scenario_keys:
        for i, damage in enumerate(total_cost_relative_to_gdp[key].values):
            axs.add_patch(Rectangle((i+start_year, key_index-0.5),
                                    1, 1, fill=True, color=new_cmap(new_norm(damage))))
        # add a horizontal line at the bottom of the subplot
        axs.axhline(y=key_index-0.5, color='black', linewidth=0.5)
        key_index -= 1

    axs.set_xlabel('Birth Year')
    axs.set_ylabel('Scenario')
    axs.set_xlim([start_year, end_year])
    axs.set_ylim([-0.5, len(scenario_keys)-0.5])
    axs.set_yticks(range(len(scenario_keys)))
    axs.set_yticklabels(reversed(scenario_keys))

    # Add colorbar
    cax = fig.add_axes([1.0125, 0.25, 0.03, 0.7])
    cb = colorbar.ColorbarBase(
        cax, cmap=new_cmap, norm=new_norm, orientation='vertical')
    cb.set_label('Total Cost relative to GDP')

    plt.tight_layout()
    return fig


deterministic_scenario_keys = ["DICE-2016-R",
                               "Abatement cost funding", "3% GDP limit"]

plot_total_cost_relative_to_gdp(deterministic_scenario_keys)
plt.savefig(os.path.join(
    figurepath, "deterministic_total_cost_relative_to_gdp.pdf"), dpi=300, bbox_inches='tight')

stochastic_scenario_keys = [
    "Stochastic DICE", "Stochastic abatement cost funding", "Stochastic 3% GDP limit", "3% GDP limit"]
plot_total_cost_relative_to_gdp(stochastic_scenario_keys)
plt.savefig(os.path.join(
    figurepath, "stochastic_total_cost_relative_to_gdp.pdf"), dpi=300, bbox_inches='tight')