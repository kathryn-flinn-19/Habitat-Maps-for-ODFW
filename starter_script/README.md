# Setup instructions:
## Setting up Anaconda on your computer
- [Download Anaconda3 or Miniconda 3](https://www.anaconda.com/download)
- Open an Anaconda command prompt and enter `where conda` to find paths to your Anaconda installations. 
- Open `Edit System Environment Variables` in your computer's control panel.
- Click environment variables, select "Path" under User variables, and hit edit. 
- Using the output from `where conda, add the following paths to your Path environment variable:
    - C:/Users/<your_username>/miniconda3
    - C:/Users/<your_username>/miniconda3/Library/bin
    - C:/Users/<your_username>/miniconda3/Scripts

## Adding a Conda virtual environment to your code
- Add a Conda virtual environment to manage this folder. To make it easier to reference the virtual environment in future steps, it is recommended to give it an actual name, such as `conda_env`. 
- Relaunch your terminal session, then call `conda activate conda_env` to activate your virtual environment. If this is successful, the next prompt to be printed will be your cwd path, prefaced with (`conda_env`).

## Install dependencies
- Call `conda install conda-forge::matplotlib` to install matplotlib.
    - Note: this should also install `numpy`.
- Call `conda install geopandas` to install geopandas.
    - Note: this should also install `pandas`.
- Call `conda install rasterio` to install rasterio.
- Troubleshooting: these commands may fail at first if you have not accepted the Anaconda terms of service. The error message will tell you what commands to run to accept the terms of service; simply copy and paste these into an Anaconda prompt, then restart your shell session.

## Download and set up required data
- [Download the data for the USGS National Gap Land Cover in the Northwest and Southwest regions.](https://www.sciencebase.gov/catalog/item/5540e2d7e4b0a658d79395db)
- Unzip these folders and put them into your `data/gap_map` folder.
- [Download the data for USGS Hydrography data.](https://www.sciencebase.gov/catalog/item/5540eb44e4b0a658d7939624)
- Unzip this folder and put it into your `data/hydrography` folder.
- [Download the data for USGS elevation in the Northwest and Southwest regions.](https://www.sciencebase.gov/catalog/item/5540e111e4b0a658d79395d9)
- Unzip these folders and put them into your `data/elevation` folder. 
- Unzip the `hucs.zip` folder and keep it in `\starter_script`.

## Set your data paths
### In script.py/RegionalDataLayers():
- Set your `northwest.gap_land_cover` to the path to `data/gap_map/northwest/lcgap_nw`
- Set your `northwest.elevation` to the path to `data/gap_map/northwest/lcgap_nw`
- Set your `northwest.hydrography` to the path to `data/hydrography/GAPHydroData/nw`
- Set your `southwest.gap_land_cover` to the path to `data/gap_map/southwest/lcgap_sw`
- Set your `southwest.elevation` to the path to `data/elevation/southwest/elev_sw`
- Set your `state_boundaries` variable to the path to `data/boundaries/cb_2024_us_state_20m.shp`.

### In data/species/kitfox/kit_fox.yaml:
- Set your `habitat_model` variable to the path to `data\species\kit_fox\mKIFOx_CONUS_HabModel_2001v1.json`
- Set your `species_range` variable to the path to `data\species\kit_fox\mKIFOx_CONUS_Range_2001v1.shp`
- Set your `inaturalist_observations` variable to the path to `data\species\kit_fox\inaturalist\observations-758741.csv`