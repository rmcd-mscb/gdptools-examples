import os

import pandas as pd
from gdptools.helpers import calc_weights_catalog

print(os.getcwd())
param_json = "https://mikejohnson51.github.io/opendap.catalog/cat_params.json"
grid_json = "https://mikejohnson51.github.io/opendap.catalog/cat_grids.json"
params = pd.read_json(param_json)
grids = pd.read_json(grid_json)


dm = "daymet4"
grid_id = 3.0
tmx = "tmax"
daymet = params.query("id == @dm & grid_id == @grid_id")
print(type(daymet), len(daymet))

# Create a dictionary of dataframes for each variable
dm_vars = ["prcp", "srad", "swe", "tmax", "tmin", "vp"]
# dm_vars = ["tmax", "tmin"]
dm_var_params = []
for _var in dm_vars:
    dm_var_params.append(
        params.query("id == @dm & grid_id == @grid_id & variable == @_var")
    )
dm_param_dict = dict(zip(dm_vars, dm_var_params))
dm_param_dict.get("tmax")


# Create a dictionary of dataframes for each variable
dm_var_grid = []
for var in dm_vars:
    gridid = dm_param_dict.get(var)["grid_id"].values[0]
    dm_var_grid.append(grids.query("grid_id == @gridid"))
dm_grid_dict = dict(zip(dm_vars, dm_var_grid))
dm_grid_dict.get("tmax")

wghtf = calc_weights_catalog(
    params_json=dm_param_dict.get("tmax"),
    grid_json=dm_grid_dict.get("tmax"),
    shp_file="~/data/NHM_19/NHM_19_nhrus_c.shp",
    wght_gen_file="~/data/NHM_19/cc_dm_wght_file_2.csv",
    wght_gen_proj=6931,
)
