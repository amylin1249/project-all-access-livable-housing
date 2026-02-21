import csv
import sys
import shapefile
import geopandas as gpd
from pathlib import Path
from shapely.geometry import Point, Polygon


SF_CENSUS_PATH = "raw-data/census/sf_census_tracts_2020.csv"
POP_PATH = "raw-data/census/acs_sf_population_2020_24.csv"
RENT_PATH = "raw-data/census/acs_sf_median_rent_2020_24.csv"
HH_INC_PATH = "raw-data/census/acs_sf_median_hh_income_2020_24.csv"
RACE_PATH = "raw-data/census/acs_sf_race_2020_24.csv"

POP_ID = "AUO6E001"
RENT_ID = "AUWGE001"
HH_INC_ID = "AURUE001"
WHITE_POP_ID = "AUO7E002"

KEYS = ["geo_id", "geom", "population", "median_rent", "median_hh_income", "white_pct"]


def clean_acs_data(file_path: str, col_name: str) -> dict:
    """
    This function will load the data from the ACS files saved and
    return a list of CleanedData tuples.

    In each file:
    - Tracts will be identified by their GeoID ("TL_GEO_ID")
    - Data to be saved will be found in the column with the unique identifier

    Parameters:
        col_name: Identifier for the column with the relevant data in that file

    Returns:
        A dictionary of GeoID keys that map to their data fields
        (None if the original data is a negative value)
    """
    cleaned_data = {}

    with open(file_path) as f:
        reader = csv.DictReader(f)

        for row in reader:
            geo_id = row["TL_GEO_ID"]
            data = int(row[col_name])
            if data >= 0:
                cleaned_data[geo_id] = data
            else:
                cleaned_data[geo_id] = None

    return cleaned_data


def get_sf_geoid() -> list[str]:
    """
    Docstring
    """
    sf_geoid = []

    with open(SF_CENSUS_PATH) as f:
        reader = csv.DictReader(f)
        for row in reader:
            geom = row["the_geom"]
            geo_id = row["geoid"]

            if geom.startswith("MULTIPOLYGON") and geo_id:
                sf_geoid.append(geo_id)
    
    return sf_geoid


def filter_sf_tracts():
    """
    Docstring
    """
    gdf = gpd.read_file("raw-data/census/cali_tracts_shapefiles_")



def join_census_tracts():
    """
    Docstring for join_census_tracts
    """
    csv.field_size_limit(sys.maxsize)

    with open(SF_CENSUS_PATH) as f:
        reader = csv.DictReader(f)

        with open("clean-data/census_acs_join.csv", "w") as f:
            writer = csv.DictWriter(f, KEYS)
            writer.writeheader()

            for row in reader:
                geom = row["the_geom"]
                geo_id = row["geoid"]
                population = clean_acs_data(POP_PATH, POP_ID)[geo_id]

                if population > 0:
                    white_pct = (
                        clean_acs_data(RACE_PATH, WHITE_POP_ID)[geo_id] / population
                    )
                else:
                    white_pct = None

                if geom.startswith("MULTIPOLYGON") and geo_id:
                    writer.writerow(
                        {
                            KEYS[0]: geo_id,
                            KEYS[1]: geom,
                            KEYS[2]: population,
                            KEYS[3]: clean_acs_data(RENT_PATH, RENT_ID)[geo_id],
                            KEYS[4]: clean_acs_data(HH_INC_PATH, HH_INC_ID)[geo_id],
                            KEYS[5]: white_pct,
                        }
                    )


def load_shapefiles(path: Path) -> Tract:
    """
    Extract and parse polygons from Census shapefiles.
    """
    tracts = []
    with shapefile.Reader(path) as sf:
        # This iterates over all shapes with their associated data.
        for shape_rec in sf.shapeRecords():
            # the shape_rec object here has two properties of interest
            #    shape_rec.record - dict containing the data attributes
            #                       associated with the shape
            #    shape_rec.shape.points - list of WKT points, used to construct
            #                             a shapely.Polygon
            tracts.append(
                Tract(
                    id=shape_rec.record["TRACTCE"],
                    polygon=Polygon(shape_rec.shape.points),
                )
            )
    return tracts


if __name__ == "__main__":
    join_census_tracts()
