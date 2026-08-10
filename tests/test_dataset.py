
from pathlib import Path

import pytest
import xarray as xr

from src.dataset import (
    XFELDataset,
    DatasetNotFoundError,
    SourceNotFoundError,
    MeasurementNotFoundError,
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


def test_paths_exist():
    dataset = build_dataset()

    assert dataset.has_raw()
    assert dataset.has_proc()


def test_raw_sources():
    dataset = build_dataset()

    sources = dataset.sources("raw")

    assert sources
    assert (
        "SA1_XTD2_XGM/DOOCS/MAIN:output"
        in sources
    )


def test_proc_sources():
    dataset = build_dataset()

    sources = dataset.sources("proc")

    assert sources

    lpd_sources = [
        source
        for source in sources
        if "LPD" in source.upper()
    ]

    assert len(lpd_sources) == 15


def test_measurements():
    dataset = build_dataset()

    source = (
        "FXE_DET_LPD1M-1/DET/0CH0:xtdf"
    )

    measurements = dataset.measurements(
        "proc",
        source,
    )

    assert "image.data" in measurements


def test_small_beam_measurement():
    dataset = build_dataset()

    data = dataset.get_measurement(
        "raw",
        "SA1_XTD2_XGM/DOOCS/MAIN:output",
        "data.intensityTD",
    )

    assert isinstance(data, xr.DataArray)
    assert data.size > 0


def test_invalid_source():
    dataset = build_dataset()

    with pytest.raises(SourceNotFoundError):
        dataset.measurements(
            "raw",
            "INVALID",
        )


def test_invalid_measurement():
    dataset = build_dataset()

    with pytest.raises(MeasurementNotFoundError):
        dataset.get_measurement(
            "raw",
            "SA1_XTD2_XGM/DOOCS/MAIN:output",
            "INVALID",
        )


def test_invalid_dataset():
    dataset = build_dataset()

    with pytest.raises(ValueError):
        dataset.sources("invalid")


def test_missing_path():
    with pytest.raises(DatasetNotFoundError):
        XFELDataset(
            raw_path=PROJECT_ROOT / "missing"
        )


def test_detector_sample_is_small():
    dataset = build_dataset()

    data = dataset.get_detector_sample(
        "FXE_DET_LPD1M-1/DET/0CH0:xtdf"
    )

    assert isinstance(data, xr.DataArray)
    assert data.ndim == 3
    assert data.shape[1:] == (256, 256)


def test_close():
    dataset = build_dataset()

    dataset.raw()
    dataset.proc()

    dataset.close()

    assert dataset._raw is None
    assert dataset._proc is None