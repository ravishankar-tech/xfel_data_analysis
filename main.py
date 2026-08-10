
from pathlib import Path

from src.dataset import XFELDataset
from src.metadata import collect_metadata
from src.processing import prepare_for_analysis
from src.analysis import analyze
from src.visualization import create_figures
from src.report import generate_report


PROJECT_ROOT = Path(__file__).resolve().parent

RUN_ROOT = (
    PROJECT_ROOT
    / "data"
    / "XMPL"
    / "201750"
    / "p700000"
)

RAW_PATH = RUN_ROOT / "raw" / "r0299"
PROC_PATH = RUN_ROOT / "proc" / "r0299"

# Run the main characterization pipeline
def main():
    

    dataset = XFELDataset(
        raw_path=RAW_PATH,
        proc_path=PROC_PATH,
    )

    metadata = collect_metadata(
        dataset,
        "raw",
    )

    prepared = prepare_for_analysis(
        dataset
    )

    results = analyze(
        prepared
    )

    figure_paths = create_figures(
        prepared,
        PROJECT_ROOT / "outputs",
    )

    report_path = generate_report(
        results,
        metadata,
        figure_paths,
        PROJECT_ROOT
        / "outputs"
        / "characterization_report.md",
    )

    print(
        f"Report generated: {report_path}"
    )


if __name__ == "__main__":
    main()