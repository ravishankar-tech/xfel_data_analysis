
from src.dataset import XFELDataset


XGM_SOURCE = "SA1_XTD2_XGM/DOOCS/MAIN:output"

HIREX_MASTER_SOURCE = (
    "SA1_XTD9_HIREX/CAL/MASTER:daqOutput"
)

GOTTHARD_MASTER_SOURCE = (
    "SA1_XTD9_HIREX/DAQ/GOTTHARD_MASTER:daqOutput"
)

DETECTOR_SOURCE = (
    "FXE_DET_LPD1M-1/DET/0CH0:xtdf"
)


XGM_MEASUREMENTS = {
    "intensity": "data.intensityTD",
    "intensity_uncertainty": "data.intensitySigmaTD",
    "x": "data.xTD",
    "x_uncertainty": "data.xSigmaTD",
    "y": "data.yTD",
    "y_uncertainty": "data.ySigmaTD",
}


def prepare_beam_measurements(
    dataset: XFELDataset,
) -> dict:
    """Prepare the selected beam measurements."""

    beam = {
        "xgm": {},
        "hirex_master": None,
        "gotthard_master": None,
    }

    for name, measurement in XGM_MEASUREMENTS.items():
        beam["xgm"][name] = dataset.get_measurement(
            "raw",
            XGM_SOURCE,
            measurement,
        )

    beam["hirex_master"] = dataset.get_measurement(
        "raw",
        HIREX_MASTER_SOURCE,
        "data.image.pixels",
    )

    beam["gotthard_master"] = dataset.get_measurement(
        "raw",
        GOTTHARD_MASTER_SOURCE,
        "data.adc",
    )

    return beam


def prepare_detector_measurement(
    dataset: XFELDataset,
) -> dict:
    
    return {
        "image": dataset.get_detector_sample(
            DETECTOR_SOURCE,
            "image.data",
            max_trains=1,
        )
    }


def prepare_for_analysis(
    dataset: XFELDataset,
) -> dict:
    
    return {
        "beam": prepare_beam_measurements(dataset),
        "detector": prepare_detector_measurement(dataset),
    }