from dataclasses import dataclass

import numpy as np
import xarray as xr


# Beam characterization results
@dataclass
class BeamAnalysisResult:
    

    intensity_mean: float
    intensity_std: float
    intensity_relative_variation: float

    x_mean: float
    x_std: float

    y_mean: float
    y_std: float

    hirex_mean: float
    gotthard_mean: float


#Detector characterization results

@dataclass
class DetectorAnalysisResult:
    

    mean_signal: float
    signal_std: float
    bad_pixel_fraction: float

# Return finite values from an xarray DataArray
def _finite_values(data: xr.DataArray) -> np.ndarray:
    
    values = np.asarray(data.values)

    values = values[np.isfinite(values)]

    if values.size == 0:
        raise ValueError("No finite values available.")

    return values

# Calculate the selected beam characterization metrics
def analyze_beam(
    beam: dict,
) -> BeamAnalysisResult:
    

    intensity = _finite_values(
        beam["xgm"]["intensity"]
    )

    x_position = _finite_values(
        beam["xgm"]["x"]
    )

    y_position = _finite_values(
        beam["xgm"]["y"]
    )

    hirex = _finite_values(
        beam["hirex_master"]
    )

    gotthard = _finite_values(
        beam["gotthard_master"]
    )

    intensity_mean = float(
        np.mean(intensity)
    )

    intensity_std = float(
        np.std(intensity)
    )

    relative_variation = (
        intensity_std / intensity_mean
        if intensity_mean != 0
        else float("nan")
    )

    return BeamAnalysisResult(
        intensity_mean=intensity_mean,
        intensity_std=intensity_std,
        intensity_relative_variation=relative_variation,
        x_mean=float(np.mean(x_position)),
        x_std=float(np.std(x_position)),
        y_mean=float(np.mean(y_position)),
        y_std=float(np.std(y_position)),
        hirex_mean=float(np.mean(hirex)),
        gotthard_mean=float(np.mean(gotthard)),
    )

# Calculate the selected detector characterization metrics
def analyze_detector(
    detector: dict,
) -> DetectorAnalysisResult:
    

    image = detector["image"]

    values = np.asarray(image.values)

    finite = np.isfinite(values)

    valid_values = values[finite]

    if valid_values.size == 0:
        raise ValueError(
            "Detector sample contains no finite values."
        )

    bad_pixel_fraction = float(
        1.0 - (
            valid_values.size / values.size
        )
    )

    return DetectorAnalysisResult(
        mean_signal=float(
            np.mean(valid_values)
        ),
        signal_std=float(
            np.std(valid_values)
        ),
        bad_pixel_fraction=bad_pixel_fraction,
    )

# Run the complete characterization
def analyze(
    prepared: dict,
) -> dict:
    

    return {
        "beam": analyze_beam(
            prepared["beam"]
        ),
        "detector": analyze_detector(
            prepared["detector"]
        ),
    }