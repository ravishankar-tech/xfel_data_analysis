

from pathlib import Path

import xarray as xr

from src.dataset import XFELDataset
from src.processing import (
    XGM_MEASUREMENTS,
    prepare_beam_measurements,
    prepare_detector_measurement,
    prepare_for_analysis,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RUN_ROOT = (
    PROJECT_ROOT
    / "data"
    / "XMPL"
    / "201750"
    / "p700000"
)

RAW_PATH = RUN_ROOT / "raw" / "r0299"
PROC_PATH = RUN_ROOT / "proc" / "r0299"


def build_dataset():
    return XFELDataset(
        raw_path=RAW_PATH,
        proc_path=PROC_PATH,
    )


def test_prepare_beam_measurements():
    beam = prepare_beam_measurements(
        build_dataset()
    )

    assert set(beam) == {
        "xgm",
        "hirex_master",
        "gotthard_master",
    }

    assert set(beam["xgm"]) == set(
        XGM_MEASUREMENTS
    )

    for value in beam["xgm"].values():
        assert isinstance(
            value,
            xr.DataArray,
        )


def test_hirex_measurement():
    beam = prepare_beam_measurements(
        build_dataset()
    )

    assert isinstance(
        beam["hirex_master"],
        xr.DataArray,
    )


def test_gotthard_measurement():
    beam = prepare_beam_measurements(
        build_dataset()
    )

    assert isinstance(
        beam["gotthard_master"],
        xr.DataArray,
    )


def test_prepare_detector_measurement():
    detector = prepare_detector_measurement(
        build_dataset()
    )

    assert set(detector) == {
        "image"
    }

    assert isinstance(
        detector["image"],
        xr.DataArray,
    )

    assert detector["image"].ndim == 3


def test_prepare_for_analysis():
    prepared = prepare_for_analysis(
        build_dataset()
    )

    assert set(prepared) == {
        "beam",
        "detector",
    }

    assert prepared["beam"]
    assert prepared["detector"]