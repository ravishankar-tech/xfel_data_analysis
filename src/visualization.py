
from pathlib import Path

import matplotlib.pyplot as plt

# Plot XGM intensity
def plot_beam_intensity(
    beam,
    output_path: str | Path,
):
    
    values = beam["xgm"]["intensity"].values

    fig, ax = plt.subplots()

    ax.plot(values.ravel())

    ax.set_title("XGM Beam Intensity")
    ax.set_xlabel("Measurement")
    ax.set_ylabel("Intensity")

    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)

# Plot the representative detector image
def plot_detector_image(
    detector,
    output_path: str | Path,
):
    
    image = detector["image"]

    values = image.values

    if values.ndim == 3:
        values = values[0]

    fig, ax = plt.subplots()

    ax.imshow(values)

    ax.set_title("Representative LPD Detector Image")
    ax.set_xlabel("Pixel X")
    ax.set_ylabel("Pixel Y")

    fig.tight_layout()
    fig.savefig(output_path)
    plt.close(fig)


def create_figures(
    prepared: dict,
    output_dir: str | Path,
) -> dict:
    """Create the small MVP figure set."""

    output_dir = Path(output_dir)
    output_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    paths = {}

    intensity_path = (
        output_dir / "beam_intensity.png"
    )

    detector_path = (
        output_dir / "detector_image.png"
    )

    plot_beam_intensity(
        prepared["beam"],
        intensity_path,
    )

    plot_detector_image(
        prepared["detector"],
        detector_path,
    )

    paths["beam_intensity"] = intensity_path
    paths["detector_image"] = detector_path

    return paths