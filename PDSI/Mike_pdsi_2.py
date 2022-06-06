"""Test program to area-weight PDSI to gages2."""
import time
from pathlib import Path

import pandas as pd
from gdptools.helpers import calc_weights_catalog

# from gdptools.run_weights_engine import RunWghtEngine

p = Path("gages2/")
print(p.exists())
param_json = "https://mikejohnson51.github.io/opendap.catalog/cat_params.json"
grid_json = "https://mikejohnson51.github.io/opendap.catalog/cat_grids.json"
params = pd.read_json(param_json)
grids = pd.read_json(grid_json)

dm = "terraclim"
grid_id = 3.0
var = "PDSI"
tc = params.query("id == @dm & variable == @var")
print(type(tc), len(tc))

# Create a dictionary of dataframes for each variable
tc_vars = ["PDSI"]
# dm_vars = ["tmax", "tmin"]
tc_var_params = []
for _var in tc_vars:
    tc_var_params.append(params.query("id == @dm & variable == @_var"))
tc_param_dict = dict(zip(tc_vars, tc_var_params))
tc_param_dict.get("PDSI")

# Create a dictionary of dataframes for each variable
tc_var_grid = []
for var in tc_vars:
    gridid = tc_param_dict.get(var)["grid_id"].values[0]
    tc_var_grid.append(grids.query("grid_id == @gridid"))
tc_grid_dict = dict(zip(tc_vars, tc_var_grid))
tc_grid_dict.get("PDSI")

start_time = time.time()
wghtf = calc_weights_catalog(
    params_json=tc_param_dict.get("PDSI"),
    grid_json=tc_grid_dict.get("PDSI"),
    shp_file="../../../data/Mikes_basins/Mikes_basins_2.shp",
    wght_gen_file="../../../data/Mikes_basins/cwc_pdsi_wght_file_2.csv",
    wght_gen_proj=6931,
)
print(time.time() - start_time)
# eng = RunWghtEngine()
# eng.initialize(
#     param_dict=tc_param_dict,
#     grid_dict=tc_grid_dict,
#     wghts="../../../data/Mikes_basins/cwc_pdsi_wght_file_1.csv",
#     gdf="../../../data/Mikes_basins/Mikes_basins_2.shp",
#     start_date="1960-01-01",
#     end_date="2019-12-31",
# )

# ngdf, nvals = eng.run(numdiv=1)

# success = eng.finalize(
#     gdf=ngdf,
#     vals=nvals,
#     opath="../../../data/Mikes_basins",
#     prefix="pdsi_gages2_1960_2020",
# )
