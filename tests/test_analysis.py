
import numpy as np
import xarray as xr

from src.analysis import (
    analyze_beam,
    analyze_detector,
)


def beam_data():
    return {
        "xgm": {
            "intensity": xr.DataArray(
                [10.0, 20.0, 30.0]
            ),
            "intensity_uncertainty": xr.DataArray(
                [1.0, 1.0, 1.0]
            ),
            "x": xr.DataArray(
                [1.0, 2.0, 3.0]
            ),
            "x_uncertainty": xr.DataArray(
                [0.1, 0.1, 0.1]
            ),
            "y": xr.DataArray(
                [4.0, 5.0, 6.0]
            ),
            "y_uncertainty": xr.DataArray(
                [0.1, 0.1, 0.1]
            ),
        },
        "hirex_master": xr.DataArray(
            [1.0, 2.0, 3.0]
        ),
        "gotthard_master": xr.DataArray(
            [4.0, 5.0, 6.0]
        ),
    }


def test_beam_analysis():
    result = analyze_beam(
        beam_data()
    )

    assert result.intensity_mean == 20.0
    assert result.x_mean == 2.0
    assert result.y_mean == 5.0


def test_relative_intensity_variation():
    result = analyze_beam(
        beam_data()
    )

    expected = (
        np.std([10.0, 20.0, 30.0])
        / 20.0
    )

    assert np.isclose(
        result.intensity_relative_variation,
        expected,
    )


def test_detector_analysis():
    detector = {
        "image": xr.DataArray(
            [
                [1.0, 2.0],
                [3.0, np.nan],
            ]
        )
    }

    result = analyze_detector(
        detector
    )

    assert result.mean_signal == 2.0
    assert result.bad_pixel_fraction == 0.25


def test_detector_no_finite_values():
    detector = {
        "image": xr.DataArray(
            [[np.nan, np.nan]]
        )
    }

    try:
        analyze_detector(detector)
    except ValueError:
        pass
    else:
        raise AssertionError(
            "Expected ValueError"
        )