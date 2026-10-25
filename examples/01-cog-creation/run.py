#!/usr/bin/env python3
"""Example 01: create a Cloud-Optimized GeoTIFF and index its footprint in GeoParquet.

Install the optional raster dependencies with:
    pip install -e ".[cog]"
"""

from pathlib import Path

import geopandas as gpd
import numpy as np
from shapely.geometry import box

OUTPUT_DIR = Path("output")


def main() -> None:
    try:
        import rasterio
        from rasterio.transform import from_origin
        from rio_cogeo.cogeo import cog_translate, cog_validate
        from rio_cogeo.profiles import cog_profiles
    except ImportError as exc:
        raise SystemExit(
            'This example requires optional raster dependencies. '
            'Install them with: pip install -e ".[cog]"'
        ) from exc

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    source_path = OUTPUT_DIR / "synthetic-dem-source.tif"
    cog_path = OUTPUT_DIR / "synthetic-dem-cog.tif"
    footprint_path = OUTPUT_DIR / "raster-footprint.parquet"

    # Small deterministic raster in geographic coordinates, suitable for a demo.
    width = height = 256
    transform = from_origin(-80.95, 29.05, 0.0001, 0.0001)
    rows, cols = np.indices((height, width))
    elevation = (100 + rows + cols).astype(np.uint16)

    profile = {
        "driver": "GTiff",
        "width": width,
        "height": height,
        "count": 1,
        "dtype": "uint16",
        "crs": "EPSG:4326",
        "transform": transform,
        "nodata": 0,
    }
    with rasterio.open(source_path, "w", **profile) as dataset:
        dataset.write(elevation, 1)

    cog_translate(
        str(source_path),
        str(cog_path),
        cog_profiles.get("deflate"),
        in_memory=False,
        quiet=True,
    )

    is_valid, errors, warnings = cog_validate(str(cog_path), strict=True)
    if not is_valid:
        raise RuntimeError(f"COG validation failed: {errors}")

    with rasterio.open(cog_path) as dataset:
        if dataset.driver != "GTiff" or dataset.width != width or dataset.height != height:
            raise AssertionError("COG raster dimensions or driver changed unexpectedly")
        if dataset.crs.to_epsg() != 4326:
            raise AssertionError(f"Unexpected COG CRS: {dataset.crs}")
        bounds = dataset.bounds
        raster_crs = dataset.crs

    footprint = gpd.GeoDataFrame(
        {
            "asset_href": [cog_path.name],
            "width": [width],
            "height": [height],
            "crs": [raster_crs.to_string()],
            "cog_valid": [True],
        },
        geometry=[box(bounds.left, bounds.bottom, bounds.right, bounds.top)],
        crs=raster_crs,
    )
    footprint.to_parquet(footprint_path, index=False)

    # Verify that the companion vector index is readable and spatially aligned.
    round_trip = gpd.read_parquet(footprint_path)
    if len(round_trip) != 1 or round_trip.crs.to_epsg() != 4326:
        raise AssertionError("GeoParquet footprint failed its round-trip check")
    if round_trip.geometry.iloc[0].is_empty or not round_trip.geometry.iloc[0].is_valid:
        raise AssertionError("GeoParquet footprint geometry is invalid")

    print(f"COG created and validated: {cog_path}")
    print(f"GeoParquet footprint written: {footprint_path}")
    print(f"Strict COG validation warnings: {len(warnings)}")


if __name__ == "__main__":
    main()
