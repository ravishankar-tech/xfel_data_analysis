
from dataclasses import dataclass, field

from src.dataset import XFELDataset

# Basic metadata describing one XFEL run
@dataclass
class RunMetadata:
    
    proposal: str | None = None
    run: str | None = None
    dataset_type: str | None = None

    source_count: int = 0
    instrument_sources: list[str] = field(default_factory=list)
    control_sources: list[str] = field(default_factory=list)

#  Collect dataset metadata

def collect_metadata(
    dataset: XFELDataset,
    dataset_type: str = "raw",
) -> RunMetadata:
    
    run = dataset._get_dataset(dataset_type)

    instrument_sources = sorted(
        run.instrument_sources
    )

    control_sources = sorted(
        run.control_sources
    )

    return RunMetadata(
        dataset_type=dataset_type.upper(),
        source_count=(
            len(instrument_sources)
            + len(control_sources)
        ),
        instrument_sources=instrument_sources,
        control_sources=control_sources,
    )