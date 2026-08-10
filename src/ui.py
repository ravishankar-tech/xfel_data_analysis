
from pathlib import Path
from typing import Any
import sys



PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))



# Run configuration

RUN_ROOT = (
    PROJECT_ROOT
    / "data"
    / "XMPL"
    / "201750"
    / "p700000"
)

RAW_PATH = RUN_ROOT / "raw" / "r0299"
PROC_PATH = RUN_ROOT / "proc" / "r0299"

EXPERIMENT = "XMPL"
PROPOSAL = "201750"
PROCESSING_RUN = "p700000"
RUN = "r0299"

DETECTOR_SOURCE = "FXE_DET_LPD1M-1/DET/0CH0:xtdf"

OUTPUT_DIR = PROJECT_ROOT / "outputs"

BEAM_FIGURE = OUTPUT_DIR / "beam_intensity.png"
DETECTOR_FIGURE = OUTPUT_DIR / "detector_image.png"
REPORT_PATH = OUTPUT_DIR / "characterization_report.md"


# Pipeline

def run_pipeline() -> dict[str, Any]:
    
    from src.analysis import analyze
    from src.dataset import XFELDataset
    from src.metadata import collect_metadata
    from src.processing import prepare_for_analysis
    from src.report import generate_report
    from src.visualization import create_figures

    dataset = None

    try:
        dataset = XFELDataset(
            raw_path=RAW_PATH,
            proc_path=PROC_PATH,
        )

        metadata = collect_metadata(
            dataset,
            "raw",
        )

        prepared = prepare_for_analysis(dataset)

        results = analyze(prepared)

        figure_paths = create_figures(
            prepared,
            OUTPUT_DIR,
        )

        report_path = generate_report(
            results,
            metadata,
            figure_paths,
            REPORT_PATH,
        )

        return {
            "metadata": metadata,
            "results": results,
            "figure_paths": figure_paths,
            "report_path": Path(report_path),
        }

    finally:
        if dataset is not None:
            dataset.close()



# Report assistance

def refresh_report(
    results: dict[str, Any],
    metadata: Any,
    figure_paths: dict[str, Path] | None = None,
) -> Path:
    
    from src.report import generate_report
    return Path(
        generate_report(
            results,
            metadata,
            figure_paths,
            REPORT_PATH,
        )
    )


def load_report(
    path: str | Path = REPORT_PATH,
) -> str:
    
    report_path = Path(path)

    if not report_path.exists():
        raise FileNotFoundError(
            f"Report not found: {report_path}"
        )

    return report_path.read_text(
        encoding="utf-8"
    )


# Display

def format_value(
    value: Any,
    precision: int = 4,
) -> str:
    
    if value is None:
        return "Not available"

    try:
        numeric = float(value)
    except (TypeError, ValueError):
        return "Not available"

    if numeric != numeric:
        return "Not available"

    return f"{numeric:.{precision}g}"


def display_metric(
    st,
    label: str,
    value: Any,
) -> None:
    
    st.metric(
        label,
        format_value(value),
    )



# Streamlit application

def main() -> None:
    import streamlit as st

    st.set_page_config(
        page_title="XFEL Data Analysis",
        page_icon="🔬",
        layout="wide",
    )

    
    # Header
    st.title("XFEL Data Analysis")
    st.caption("Beam & Detector Characterization")

   
    # Run information
   
    st.header("Run Information")

    run_col1, run_col2, run_col3 = st.columns(3)

    run_col1.write(
        f"**Experiment:** {EXPERIMENT}"
    )
    run_col1.write(
        f"**Proposal:** {PROPOSAL}"
    )

    run_col2.write(
        f"**Processing:** {PROCESSING_RUN}"
    )
    run_col2.write(
        f"**Run:** {RUN}"
    )

    run_col3.write(
        "**Input datasets:** RAW + PROC"
    )
    run_col3.write(
        f"**Detector:** `{DETECTOR_SOURCE}`"
    )


    # Session state

    if "analysis_output" not in st.session_state:
        st.session_state.analysis_output = None

    if "analysis_status" not in st.session_state:
        st.session_state.analysis_status = "Idle"


    # Run analysis

    if st.button(
        "Run Analysis",
        type="primary",
    ):
        st.session_state.analysis_status = (
            "Running analysis..."
        )

        try:
            with st.spinner(
                "Running the existing XFEL analysis pipeline..."
            ):
                st.session_state.analysis_output = (
                    run_pipeline()
                )

            st.session_state.analysis_status = (
                "Analysis completed successfully."
            )

            st.success(
                st.session_state.analysis_status
            )

        except Exception as exc:
            st.session_state.analysis_output = None

            st.session_state.analysis_status = (
                "Analysis failed."
            )

            st.error(
                "The analysis could not be completed. "
                f"Reason: {exc}"
            )


    # Analysis status

    st.header("Analysis Status")

    if (
        st.session_state.analysis_status
        == "Analysis completed successfully."
    ):
        st.success(
            st.session_state.analysis_status
        )

    elif (
        st.session_state.analysis_status
        == "Analysis failed."
    ):
        st.error(
            st.session_state.analysis_status
        )

    else:
        st.info(
            st.session_state.analysis_status
        )


    # Display analysis results

    output = st.session_state.analysis_output

    if output is not None:

        results = output["results"]

        beam = results["beam"]
        detector = results["detector"]


        # Beam characterization

        st.header("Beam Characterization")

        beam_columns = st.columns(4)

        display_metric(
            beam_columns[0],
            "Mean intensity",
            beam.intensity_mean,
        )

        display_metric(
            beam_columns[1],
            "Intensity variation",
            beam.intensity_relative_variation,
        )

        display_metric(
            beam_columns[2],
            "Mean X position",
            beam.x_mean,
        )

        display_metric(
            beam_columns[3],
            "X-position variation",
            beam.x_std,
        )

        beam_columns = st.columns(4)

        display_metric(
            beam_columns[0],
            "Mean Y position",
            beam.y_mean,
        )

        display_metric(
            beam_columns[1],
            "Y-position variation",
            beam.y_std,
        )

        display_metric(
            beam_columns[2],
            "HIREX diagnostic mean",
            beam.hirex_mean,
        )

        display_metric(
            beam_columns[3],
            "Gotthard diagnostic mean",
            beam.gotthard_mean,
        )


        # Beam visualization

        beam_path = Path(
            output["figure_paths"]["beam_intensity"]
        )

        if beam_path.exists():

            st.subheader(
                "XGM Beam Intensity"
            )

            st.image(
                str(beam_path),
                caption="XGM Beam Intensity",
                use_container_width=True,
            )


        # Detector characterization

        st.header("Detector Characterization")

        st.write(
            f"**Representative detector:** "
            f"`{DETECTOR_SOURCE}`"
        )

        detector_columns = st.columns(3)

        display_metric(
            detector_columns[0],
            "Mean signal",
            detector.mean_signal,
        )

        display_metric(
            detector_columns[1],
            "Signal standard deviation",
            detector.signal_std,
        )

        display_metric(
            detector_columns[2],
            "Non-finite fraction",
            detector.bad_pixel_fraction,
        )


        # Detector visualization

        detector_path = Path(
            output["figure_paths"]["detector_image"]
        )

        if detector_path.exists():

            st.subheader(
                "Representative LPD Detector Image"
            )

            st.image(
                str(detector_path),
                caption="Representative LPD Detector Image",
                use_container_width=True,
            )


        # Report

        st.header("Report")

        if st.button(
            "Generate / Refresh Report"
        ):
            try:
                report_path = refresh_report(
                    output["results"],
                    output["metadata"],
                    output["figure_paths"],
                )

                output["report_path"] = report_path

                st.success(
                    "Report generated successfully."
                )

            except Exception as exc:
                st.error(
                    f"Report generation failed: {exc}"
                )

        try:
            report_text = load_report(
                output["report_path"]
            )

            st.markdown(report_text)

        except (
            FileNotFoundError,
            OSError,
        ) as exc:

            st.error(
                f"Generated report could not be loaded: {exc}"
            )


    # Scope and limitations

    st.header("Scope / Limitations")

    st.markdown(
        """
- Representative detector subset
- RAW beam diagnostics + PROC detector data
- Minimal MVP characterization, not a production XFEL calibration pipeline
- No unsupported reconstruction
- No full detector data loaded into memory
        """
    )



# Entry point

if __name__ == "__main__":
    main()