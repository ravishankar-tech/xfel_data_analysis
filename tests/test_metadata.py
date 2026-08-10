
from pathlib import Path

from src.dataset import XFELDataset
from src.metadata import RunMetadata, collect_metadata


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


def test_metadata_type():
    metadata = collect_metadata(
        build_dataset(),
        "raw",
    )

    assert isinstance(
        metadata,
        RunMetadata,
    )


def test_dataset_type():
    metadata = collect_metadata(
        build_dataset(),
        "raw",
    )

    assert metadata.dataset_type == "RAW"


def test_source_count():
    metadata = collect_metadata(
        build_dataset(),
        "raw",
    )

    assert metadata.source_count == (
        len(metadata.instrument_sources)
        + len(metadata.control_sources)
    )


def test_instrument_sources_present():
    metadata = collect_metadata(
        build_dataset(),
        "raw",
    )

    assert metadata.instrument_sources


def test_control_sources_present():
    metadata = collect_metadata(
        build_dataset(),
        "raw",
    )

    assert metadata.control_sources