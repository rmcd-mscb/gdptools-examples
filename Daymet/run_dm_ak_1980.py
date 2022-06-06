"""File for testing."""
from pathlib import Path

import pandas as pd
from gdptools.run_weights_engine import RunWghtEngine

p = Path("../../data/NHM_19")
print(p.exists())

t_start_series = pd.date_range(pd.to_datetime("1980-01-01"), periods=10, freq="AS")
t_end_series = pd.date_range(pd.to_datetime("1980-12-31"), periods=10, freq="A")
f_time_series = pd.date_range(pd.to_datetime("1980"), periods=10, freq="1Y")

time_start = [t.strftime("%Y-%m-%d") for t in t_start_series]
time_end = [t.strftime("%Y-%m-%d") for t in t_end_series]
file_time = [t.strftime("%Y") for t in f_time_series]

param_json = "https://mikejohnson51.github.io/opendap.catalog/cat_params.json"
grid_json = "https://mikejohnson51.github.io/opendap.catalog/cat_grids.json"
params = pd.read_json(param_json)
grids = pd.read_json(grid_json)

dm = "daymet4"
grid_id = 3.0
tmx = "tmax"
daymet = params.query("id == @dm & grid_id == @grid_id")
print(type(daymet), len(daymet))

daymet


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

for index, _ts in enumerate(time_start):
    print(time_start[index], time_end[index])

    eng = RunWghtEngine()
    eng.initialize(
        param_dict=dm_param_dict,
        grid_dict=dm_grid_dict,
        wghts="../../data/NHM_19/cc_dm_wght_file.csv",
        gdf="../../data/NHM_19/NHM_19_nhrus_c.shp",
        start_date=time_start[index],
        end_date=time_end[index],
    )

    ngdf, nvals = eng.run(numdiv=4)

    # eng = RunWghtEnginePerFeature('DEBUG')
    # eng.initialize(
    #     param_dict=dm_param_dict,
    #     grid_dict=dm_grid_dict,
    #     gdf="~/data/NHM_19/NHM_19_nhrus_c.shp",
    #     start_date="2019-01-01",
    #     end_date="2019-12-31",
    #     wght_gen_proj=6931
    # )

    # ngdf, nvals = eng.run_per_feature()
    # print(ngdf, nvals)
    dict_new = {
        "dims": {"feature": "nhru", "time": "time", "x": "lon", "y": "lat"},
        "feature": {
            "varname": "nhru",
            "long_name": "local model Hydrologic Response Unit ID (HRU)",
        },
        "lat": {
            "varname": "lat",
            "long_name": "Latitude of HRU centroid",
            "units": "degree_north",
            "standard_name": "latitude",
        },
        "lon": {
            "varname": "lon",
            "long_name": "Longitude of HRU centroid",
            "units": "degree_east",
            "standard_name": "longitude",
        },
        "tmax": {
            "varname": "tmax",
            "long_name": "Daily maximum temperature",
            "standard_name": "maximum_daily_air_temperature",
            "convert": True,
            "native_unit": "degC",
            "convert_unit": "degF",
        },
        "tmin": {
            "varname": "tmin",
            "long_name": "Daily minimum temperature",
            "standard_name": "minimum_daily_air_temperature",
            "convert": True,
            "native_unit": "degC",
            "convert_unit": "degF",
        },
        "prcp": {
            "varname": "prcp",
            "long_name": "Daily total precipitation",
            "standard_name": "prcp",
            "convert": True,
            "native_unit": "millimeter",
            "convert_unit": "inches",
        },
        "srad": {
            "varname": "srad",
            "long_name": "Daylight average incident shortwave radiation",
            "standard_name": "srad",
            "convert": False,
            "native_unit": "W m-2",
            "convert_unit": "None",
        },
        "swe": {
            "varname": "swe",
            "long_name": "Snow water equivalent",
            "standard_name": "swe",
            "convert": False,
            "native_unit": "kg m-2",
            "convert_unit": "None",
        },
        "vp": {
            "varname": "vp",
            "long_name": "Daily average vapor pressure",
            "standard_name": "vp",
            "convert": False,
            "native_unit": "Pa",
            "convert_unit": "None",
        },
    }

    success = eng.finalize(
        gdf=ngdf,
        vals=nvals,
        opath="../../data/NHM_19",
        prefix=f"{file_time[index]}_dm_ak",
        work_dict=dict_new,
    )


# from gdptools.helpers import calc_weights_catalog, calc_weights_catalog_test
# import os
# print(os.getcwd())
# wghtf = calc_weights_catalog(
#     params_json=dm_param_dict.get('tmax'),
#     grid_json=dm_grid_dict.get('tmax'),
#     shp_file='~/data/NHM_19/NHM_19_nhrus_c.shp',
#     wght_gen_file='~/data/NHM_19/cc_dm_wght_file.csv',
#     wght_gen_proj=6931)


# wghtf.to_csv('testwghts.csv')


# from gdptools.helpers import run_weights_catalog
# newgdf, vals = run_weights_catalog(
#     params_json=dm_param_dict.get('tmax'),
#     grid_json=dm_grid_dict.get('tmax'),
#     wght_file='~/data/NHM_19/cc_dm_wght_file.csv',
#     shp_file='~/data/NHM_19/NHM_19_nhrus_c.shp',
#     begin_date='2020-01-01',
#     end_date='2020-01-07'
# )


# In[ ]:
