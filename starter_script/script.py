import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path

import geopandas as gpd
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import rasterio
from rasterio.features import rasterize
from rasterio.transform import from_bounds
from matplotlib.colors import BoundaryNorm, ListedColormap
from rasterio.enums import Resampling
from rasterio.windows import from_bounds as bounds_window
from typing import Optional, Union


class Region(str, Enum):
    NORTHWEST = "northwest"
    SOUTHWEST = "southwest"

"""
    used to organize habitat details of a species' habitat into one object.
    information included:
    - ecosystem ids
    - elevation range where species is expected to be found
    - water features in that environment
"""
@dataclass(frozen=True)
class RegionalHabitat:
    # ids of the ecosystems where the species is primarily found
    prim_eco_sys_ids: list[int]
    # elevation range the species is expected to be found in
    elevation: tuple[int, int]
    # fw = flowing water data, ow = open/standing water, wv = wet vegetation
    into_buff_fw: Optional[float]
    into_buff_ow: Optional[float]
    into_buff_wv: Optional[float]
    from_buff_fw: Optional[float]
    from_buff_ow: Optional[float]
    from_buff_wv: Optional[float]

    """
        takes a dict (loaded from a json file or similar) and uses it to initialize
        RegionalHabitat attrs.
    """
    @staticmethod
    def from_species_model(species_model: dict) -> "RegionalHabitat":
        min_elevation = species_model["intElevMin"]
        max_elevation = species_model["intElevMax"]
        prim_eco_sys_ids = [eco_sys[0] for eco_sys in species_model["PrimEcoSys"]]
        return RegionalHabitat(
            prim_eco_sys_ids=prim_eco_sys_ids,
            elevation=(min_elevation, max_elevation),
            into_buff_fw=species_model["intIntoBuffFW"],
            into_buff_ow=species_model["intIntoBuffOW"],
            into_buff_wv=species_model["intIntoBuffWV"],
            from_buff_fw=species_model["intFromBuffFW"],
            from_buff_ow=species_model["intFromBuffOW"],
            from_buff_wv=species_model["intFromBuffWV"],
        )

"""
    combines two different regional habitats where a species
    can be found into one object. includes, for our purposes,
    the habitat object for the northwestern US and southwestern
    US.
"""
@dataclass(frozen=True)
class SpeciesHabitat:
    northwest: RegionalHabitat
    southwest: RegionalHabitat

    """
        takes a json, returns a SpeciesHabitat object with RegionalHabitats 
        built by the data within the json  
    """
    @staticmethod
    def from_json(path: Path) -> "SpeciesHabitat":
        with open(path, "r") as f:
            species_info = json.load(f)

        regional_models: dict[Region, RegionalHabitat] = {}
        for species_model in species_info["models"].values():
            region = species_model["Region"].lower()
            # notice: we're only filling out northwest and southwest habitats
            if region in (Region.NORTHWEST, Region.SOUTHWEST):
                regional_models[Region(region)] = RegionalHabitat.from_species_model(species_model)

        return SpeciesHabitat(
            northwest=regional_models[Region.NORTHWEST],
            southwest=regional_models[Region.SOUTHWEST],
        )

"""
    holds local paths to the data folders we use to create the maps
    notice that we need the following paths:
    - gap land cover
    - elevation
    - hydrography data
"""
@dataclass(frozen=True)
class RegionPaths:
    gap_land_cover: Path
    elevation: Path
    hydrography: Optional[Path] = None

"""
    a class to hold the ACTUAL to the folders containing the data layers necessary to 
    create the habitat maps.
    also includes path to shp file of state lines, to overlay on our generated habitat map
"""
@dataclass(frozen=True)
class RegionalDataLayers:
    northwest: RegionPaths = RegionPaths(
        gap_land_cover=Path("C:/Users/super/Desktop/capstone/Habitat-Maps-for-ODFW/starter_script/data/gap_map/northwest/lcgap_nw"),
        elevation=Path("C:/Users/super/Desktop/capstone/Habitat-Maps-for-ODFW/starter_script/data/elevation/northwest/elev_nw"),
        hydrography=Path("C:/Users/super/Desktop/capstone/Habitat-Maps-for-ODFW/starter_script/data/hydrography/GAPHydroData/nw"),
    )
    southwest: RegionPaths = RegionPaths(
        gap_land_cover=Path("C:/Users/super/Desktop/capstone/Habitat-Maps-for-ODFW/starter_script/data/gap_map/southwest/lcgap_sw"),
        elevation=Path("C:/Users/super/Desktop/capstone/Habitat-Maps-for-ODFW/starter_script/data/elevation/southwest/elev_sw"),
    )
    state_boundaries: Path = Path("C:/Users/super/Desktop/capstone/Habitat-Maps-for-ODFW/starter_script/data/boundaries/cb_2024_us_state_20m.shp")

"""
    parses a given yaml file to return the values it included for habitat_model,
    species_range, and inaturalist_observations. habitat_model is required, but the
    other two paths are optional.
"""
@dataclass(frozen=True)
class SpeciesPaths:
    habitat_model: Path
    species_range: Optional[Path] = None
    inaturalist_observations: Optional[Path] = None

    """
        parses the config yaml file for a species and returns the paths included there.
        note: habitat_model path is required, species_range and inaturalist_observations
        are optional
    """
    @staticmethod
    def from_json(path: Path = Path("data/species/kit_fox/kit_fox.yaml")) -> "SpeciesPaths":
        values = {}
        with open(path, "r") as f:
            for raw_line in f:
                line = raw_line.split("#", 1)[0].strip()
                if not line:
                    continue
                key, value = line.split(":", 1)
                values[key.strip()] = value.strip()

        return SpeciesPaths(
            habitat_model=Path(values["habitat_model"]),
            species_range=Path(values["species_range"]) if values.get("species_range") else None,
            inaturalist_observations=(Path(values["inaturalist_observations"]) if values.get("inaturalist_observations") else None),
        )

"""
    specifies height, width, and absolute bounds for our outputted grid
"""
@dataclass(frozen=True)
class GridSpec:
    height: int
    width: int
    bounds: rasterio.coords.BoundingBox

    """
        specifies the absolute bounds for our outputted grid, based on 
        the rasters we're using
    """
    @classmethod
    def from_rasters(cls, paths: Union[Path, list[Path]], preview_height: int = 2100) -> "GridSpec":
        if isinstance(paths, Path):
            paths = [paths]

        bounds = []
        heights = []
        # find the appropriate bounds based on the min and max bounds for our rasters
        for path in paths:
            with rasterio.open(path) as src:
                bounds.append(src.bounds)
                heights.append(src.height)

        left = min(bound.left for bound in bounds)
        bottom = min(bound.bottom for bound in bounds)
        right = max(bound.right for bound in bounds)
        top = max(bound.top for bound in bounds)
        scale = preview_height / max(heights)
        preview_width = max(int((right - left) / 30 * scale), 1)

        return cls(
            height=preview_height,
            width=preview_width,
            bounds=rasterio.coords.BoundingBox(
                left=left,
                bottom=bottom,
                right=right,
                top=top,
            ),
        )

    def transform(self) -> rasterio.Affine:
        return from_bounds(
            self.bounds.left,
            self.bounds.bottom,
            self.bounds.right,
            self.bounds.top,
            self.width,
            self.height,
        )

"""
    this is the map size specifications plus the data
"""
@dataclass(frozen=True)
class RasterMap:
    data: np.ma.MaskedArray
    grid: GridSpec

    @property
    def bounds(self) -> rasterio.coords.BoundingBox:
        return self.grid.bounds

    """
        making sure any RasterMaps we layer on top of each other use the
        same grid
    """
    def validate_compatible(self, other: "RasterMap") -> None:
        if self.grid != other.grid:
            raise ValueError("Raster maps must use the same grid")

"""
    reads a data file, turns it into a RasterMap with the specified
    height, width, and bounds
"""
def read_raster(
    path: Path,
    grid: GridSpec,
    resampling: Resampling = Resampling.nearest,
) -> RasterMap:
    with rasterio.open(path) as src:
        # we don't need super granular data, so we can resample / downsample to reduce
        # the quality of the final raster map
        data = src.read(
            1,
            window=bounds_window(*grid.bounds, transform=src.transform),
            out_shape=(grid.height, grid.width),
            resampling=resampling,
            masked=True,
            boundless=True,
            fill_value=src.nodata,
        )

    return RasterMap(data=data, grid=grid)

"""
    read our gap land cover data file and turn it into a RasterMap with 
    the specified height, width, and bounds
"""
def gap_land_cover_map(habitat: RegionalHabitat, paths: RegionPaths, grid: GridSpec) -> RasterMap:
    land_cover = read_raster(paths.gap_land_cover, grid)
    # check if our land cover is any of the ecosystems our species can be found in
    candidate = np.isin(land_cover.data, habitat.prim_eco_sys_ids).astype(np.uint8)
    # ignore invalid values
    candidate = np.ma.array(candidate, mask=np.ma.getmaskarray(land_cover.data))
    return RasterMap(candidate, grid)

"""
    turn our elevation data into a RasterMap with the specified height, width, and bounds
"""
def elevation_map(habitat: RegionalHabitat, paths: RegionPaths, grid: GridSpec) -> RasterMap:
    elevation = read_raster(paths.elevation, grid)
    low, high = habitat.elevation
    # check whether each piece of elevation data is within our expected elevation bounds
    candidate = ((elevation.data >= low) & (elevation.data <= high)).astype(np.uint8)
    # mask any invalid values
    candidate = np.ma.array(candidate, mask=np.ma.getmaskarray(elevation.data))
    return RasterMap(candidate, grid)

"""
    create a raster map out of our hydrography data, if we have it
"""
def hydrography_map(habitat: RegionalHabitat, paths: RegionPaths, grid: GridSpec) -> RasterMap:
    # if no hydrography data is provided, just use our gap land cover data
    if paths.hydrography is None:
        region = read_raster(paths.gap_land_cover, grid)
        return RasterMap(
            np.ma.array(
                np.ones((grid.height, grid.width), dtype=np.uint8),
                mask=np.ma.getmaskarray(region.data),
            ),
            grid,
        )
    
    def exterior_classes(max_meters: float) -> set[int]:
        # "from" meters --- i.e., the initial / source elevation of that water feature?
            # need to double check
        class_meters = {
            0: 9999.0,
            1: 4000.0,
            2: 2000.0,
            3: 1000.0,
            4: 500.0,
            5: 250.0,
            6: 120.0,
            7: 60.0,
            8: 30.0,
        }
        return {code for code, meters in class_meters.items() if meters <= max_meters}

    # "into" meters --- i.e., the final / terminal elevation of that water feature?
        # need to double check
    def interior_classes(max_meters: float) -> set[int]:
        class_meters = {
            9: 30.0,
            10: 60.0,
            11: 120.0,
            12: 250.0,
            13: 500.0,
            14: 1000.0,
            15: 2000.0,
            16: 4000.0,
            17: 9999.0,
        }
        return {code for code, meters in class_meters.items() if meters <= max_meters}

    """
        notice that we only care about a couple of types of hydrography types:
        s0t1v0n0 = "All types of flowing water with no masks" (i.e., our fw layer)
        s0t2v0n0 = "All types of standing (open) water with no masks" (i.e., our ow layer)
        s0t3v0n0 = "All types of wet veg with no masks" (i.e., our wv layer)

        additional note on the codes:
        - s = salinity
            - s0 = all
            - s1 = fresh
            - s2 = brackish
        - t = type
            - t1 = flowing
            - t2 = standing
            - t3 = wet veg
        - v = velocity
            - v0 = all / n/a
                - note that n/a is used for standing water (t2) 
                  or wet veg (t3), since, by definition, those 
                  water types wouldn't have a velocity
            - v1 = fast only
            - v2 = slow only
        - n = null
    """
    hydro_layers = [
        ("s0t1v0n0", habitat.from_buff_fw, habitat.into_buff_fw),
        ("s0t2v0n0", habitat.from_buff_ow, habitat.into_buff_ow),
        ("s0t3v0n0", habitat.from_buff_wv, habitat.into_buff_wv),
    ]
    candidate = np.zeros((grid.height, grid.width), dtype=bool)
    candidate_mask = np.ones((grid.height, grid.width), dtype=bool)
    for layer_name, from_meters, into_meters in hydro_layers:
        hydro = read_raster(paths.hydrography / layer_name, grid)
        valid = ~np.ma.getmaskarray(hydro.data)
        candidate_mask &= ~valid

        # seeing if the water types we want, in the elevation range we want, 
        # are in our data?
        if from_meters is not None:
            candidate |= valid & np.isin(hydro.data, list(exterior_classes(float(from_meters))))
        if into_meters is not None:
            candidate |= valid & np.isin(hydro.data, list(interior_classes(float(into_meters))))

    return RasterMap(np.ma.array(candidate.astype(np.uint8), mask=candidate_mask), grid)

"""
    make a range map based on the given path, returns its created RasterMap
"""
def species_range_map(range_path: Path, grid_spec: GridSpec) -> RasterMap:
    range_gdf = gpd.read_file(range_path).to_crs("EPSG:5070")
    # grab only the things within our specified bounds
    range_gdf = range_gdf.cx[
        grid_spec.bounds.left : grid_spec.bounds.right,
        grid_spec.bounds.bottom : grid_spec.bounds.top,
    ]

    # creating an array of raster data
    candidate = rasterize(
        [(geometry, 1) for geometry in range_gdf.geometry if geometry is not None],
        out_shape=(grid_spec.height, grid_spec.width),
        transform=grid_spec.transform(),
        fill=0,
        dtype=np.uint8,
    )
    candidate = np.ma.masked_where(candidate == 0, candidate)

    return RasterMap(data=candidate, grid=grid_spec)

"""
    combining multiple "candidate" maps into one 
"""
def combine_candidate_maps(*candidate_maps: RasterMap) -> RasterMap:
    if not candidate_maps:
        raise ValueError("At least one candidate habitat map is required")

    # make sure all maps can be layered
    first = candidate_maps[0]
    for other in candidate_maps[1:]:
        first.validate_compatible(other)

    # masking any invalid data entries across all the layers
    combined_mask = np.ma.getmaskarray(first.data)
    combined = first.data.filled(0).astype(bool)
    for other in candidate_maps[1:]:
        combined_mask |= np.ma.getmaskarray(other.data)
        combined = np.logical_and(combined, other.data.filled(0))

    combined = combined.astype(np.uint8)
    combined = np.ma.masked_where(combined_mask, combined)

    return RasterMap(data=combined, grid=first.grid)

"""
    combining multiple regional maps into one
"""
def merge_regional_maps(*regional_maps: RasterMap) -> RasterMap:
    if not regional_maps:
        raise ValueError("At least one regional map is required")
    if len(regional_maps) == 1:
        return regional_maps[0]

    first = regional_maps[0]
    for other in regional_maps[1:]:
        first.validate_compatible(other)

    merged_mask = np.ma.getmaskarray(first.data).copy()
    merged = first.data.filled(0).astype(bool)
    for other in regional_maps[1:]:
        merged_mask &= np.ma.getmaskarray(other.data)
        merged = np.logical_or(merged, other.data.filled(0))

    merged = merged.astype(np.uint8)
    merged = np.ma.masked_where(merged_mask, merged)

    return RasterMap(data=merged, grid=first.grid)

"""
    plotting states on a grid
"""
def add_state_lines(
    ax: plt.Axes,
    states_path: Path,
    displayed_states: list[str],
    bounds: rasterio.coords.BoundingBox,
) -> None:
    if not states_path.exists():
        return

    states = gpd.read_file(states_path)
    states = states[states["NAME"].isin(displayed_states)]
    states = states.to_crs("EPSG:5070")
    states = states.cx[bounds.left : bounds.right, bounds.bottom : bounds.top]
    states.boundary.plot(ax=ax, color="black", linewidth=0.6, alpha=0.8)

"""
    adding a scatterplot of inaturalist observation data within the bounds of our
    graph
"""
def add_inaturalist_observations(
    ax: plt.Axes,
    observations_path: Optional[Path],
    bounds: rasterio.coords.BoundingBox,
) -> None:
    if observations_path is None or not observations_path.exists():
        return

    observations = pd.read_csv(observations_path, usecols=["latitude", "longitude"])
    # only include observations that are attached to a latitude, longitude pair
    observations = observations.dropna(subset=["latitude", "longitude"])

    observation_points = gpd.GeoDataFrame(
        observations,
        geometry=gpd.points_from_xy(observations["longitude"], observations["latitude"]),
        crs="EPSG:4326",
    ).to_crs("EPSG:5070")
    observation_points = observation_points.cx[
        bounds.left : bounds.right,
        bounds.bottom : bounds.top,
    ]

    # make a scatter plot of the observations over the given axes
    ax.scatter(
        observation_points.geometry.x,
        observation_points.geometry.y,
        s=10,
        color="#EF2D56",
        alpha=0.9,
        linewidths=0,
    )

"""
    putting all of our layer maps together, with the inaturalist observations,
    to form a habitat map for the specified states. 
    note: since we're only looking for maps for the ODFW, we might be able to
    slim this down to just displaying the oregon map
"""
def plot_species_habitat(species_config_path: Path, title: str, output_path: Path) -> None:
    regional_data_layers = RegionalDataLayers()
    species_paths = SpeciesPaths.from_json(species_config_path)
    displayed_states = [
        "Washington",
        "Oregon",
        "Idaho",
        "California",
        "Nevada",
        "Utah",
        "Arizona",
        "New Mexico",
        "Colorado",
        "Wyoming",
    ]
    species_habitat = SpeciesHabitat.from_json(species_paths.habitat_model)
    grid_spec = GridSpec.from_rasters(
        [
            regional_data_layers.northwest.gap_land_cover,
            regional_data_layers.southwest.gap_land_cover,
        ],
        preview_height=3500,
    )
    range_candidates = species_range_map(species_paths.species_range, grid_spec) if species_paths.species_range is not None else None
    regional_maps = []

    # make combined maps for the sw and nw
    for region in (Region.NORTHWEST, Region.SOUTHWEST):
        if region == Region.NORTHWEST:
            regional_habitat = species_habitat.northwest
            regional_paths = regional_data_layers.northwest
        elif region == Region.SOUTHWEST:
            regional_habitat = species_habitat.southwest
            regional_paths = regional_data_layers.southwest

        land_cover_candidates = gap_land_cover_map(
            regional_habitat,
            regional_paths,
            grid_spec,
        )
        elevation_candidates = elevation_map(
            regional_habitat,
            regional_paths,
            grid_spec,
        )
        hydrography_candidates = hydrography_map(
            regional_habitat,
            regional_paths,
            grid_spec,
        )
        regional_maps.append(
            combine_candidate_maps(
                land_cover_candidates,
                elevation_candidates,
                hydrography_candidates,
                *(candidate for candidate in [range_candidates] if candidate is not None),
            )
        )

    # combine all maps into one
    true_habitat_map = merge_regional_maps(*regional_maps)

    cmap = ListedColormap(["white", "#C2CBEE"])
    cmap.set_bad("white")
    norm = BoundaryNorm([-0.5, 0.5, 1.5], cmap.N)

    # building out our figure: display the habitat map, then
    # add state lines, then add inaturalist data
    fig, ax = plt.subplots(figsize=(12, 10))
    ax.imshow(
        true_habitat_map.data,
        extent=[
            true_habitat_map.bounds.left,
            true_habitat_map.bounds.right,
            true_habitat_map.bounds.bottom,
            true_habitat_map.bounds.top,
        ],
        origin="upper",
        cmap=cmap,
        norm=norm,
        interpolation="nearest",
    )
    add_state_lines(
        ax,
        regional_data_layers.state_boundaries,
        displayed_states,
        true_habitat_map.bounds,
    )
    add_inaturalist_observations(
        ax,
        species_paths.inaturalist_observations,
        true_habitat_map.bounds,
    )
    ax.set_title(title)
    ax.set_axis_off()
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)
    print(f"Saved {output_path}")


def yuma_bat_main() -> None:
    plot_species_habitat(Path("species/bat.yaml"), "", Path("figures/bat_habitat_map.png"))


def kit_fox_main() -> None:
    plot_species_habitat(Path("data/species/kit_fox/kit_fox.yaml"), "", Path("figures/kit_fox_habitat_map-updated2.png"))


def western_toad_main() -> None:
    plot_species_habitat(Path("species/western_toad.yaml"), "", Path("figures/western_toad_habitat_map.png"))


def main() -> None:
    #yuma_bat_main()
    kit_fox_main()


if __name__ == "__main__":
    main()

