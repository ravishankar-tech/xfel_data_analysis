

from pathlib import Path


def generate_report(
    results: dict,
    metadata,
    figure_paths: dict | None = None,
    output_path: str | Path = "outputs/beam_detector_report.md",
):
    """Generate the characterization report."""

    output_path = Path(output_path)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    beam = results["beam"]
    detector = results["detector"]

    lines = [
        "# XFEL Characterization Report",
        "",
        "## Run Overview",
        "",
        f"- Dataset type: {metadata.dataset_type}",
        f"- Sources: {metadata.source_count}",
        "",
        "## Beam Characterization",
        "",
        f"- Mean intensity: "
        f"{beam.intensity_mean:.4g}",
        f"- Intensity standard deviation: "
        f"{beam.intensity_std:.4g}",
        f"- Relative intensity variation: "
        f"{beam.intensity_relative_variation:.4g}",
        f"- Mean X position: "
        f"{beam.x_mean:.4g}",
        f"- X-position variation: "
        f"{beam.x_std:.4g}",
        f"- Mean Y position: "
        f"{beam.y_mean:.4g}",
        f"- Y-position variation: "
        f"{beam.y_std:.4g}",
        f"- HIREX diagnostic mean: "
        f"{beam.hirex_mean:.4g}",
        f"- Gotthard diagnostic mean: "
        f"{beam.gotthard_mean:.4g}",
        "",
        "## Detector Characterization",
        "",
        f"- Mean detector signal: "
        f"{detector.mean_signal:.4g}",
        f"- Detector signal standard deviation: "
        f"{detector.signal_std:.4g}",
        f"- Non-finite pixel fraction: "
        f"{detector.bad_pixel_fraction:.4%}",
        "",
        "## Figures",
        "",
    ]

    if figure_paths:
        for name, path in figure_paths.items():
            lines.append(
                f"- {name}: `{path}`"
            )

    lines.extend(
        [
            "",
            "## Scope",
            "",
            "This report uses a minimal representative "
            "subset of the available XFEL data.",
            "",
            "No photon-flux reconstruction, spectral "
            "reconstruction, or unsupported calibration "
            "has been performed.",
            "",
        ]
    )

    output_path.write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    return output_path