

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import xarray as xr

from src.visualization import (
    create_figures,
)


def test_create_figures(tmp_path):
    prepared = {
        "beam": {
            "xgm": {
                "intensity": xr.DataArray(
                    [1.0, 2.0, 3.0]
                )
            }
        },
        "detector": {
            "image": xr.DataArray(
                [
                    [
                        [1.0, 2.0],
                        [3.0, 4.0],
                    ]
                ]
            )
        },
    }

    paths = create_figures(
        prepared,
        tmp_path,
    )

    assert "beam_intensity" in paths
    assert "detector_image" in paths

    assert Path(
        paths["beam_intensity"]
    ).exists()

    assert Path(
        paths["detector_image"]
    ).exists()