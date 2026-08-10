# XFEL Data Analysis

A Python project for characterizing beam and detector data from a European XFEL run using the `EXtra-data` library.

## Idea

I built this project to work with European XFEL data and understand how the data can be analyzed using Python.

The project uses RAW beam data and PROC detector data. It prepares selected measurements, calculates basic beam and detector characteristics, and presents the results as figures, a report, and an optional Streamlit dashboard.

The project is a small MVP. It was built to understand the data and the tools rather than to build a production scale pipeline.

A separate case study in [`case_study.md`](case_study.md) explains the general path from an XFEL experiment to HDF5 data. This README focuses on what this project does with that data.

## Objective

The objective is to build a small analysis pipeline using the available RAW and PROC data.

The project has two analysis paths:

- **RAW → Beam characterization**
- **PROC → Detector characterization**

The beam analysis uses XGM, HIREX and Gotthard measurements.

The detector analysis uses data from an LPD detector.

Both paths use the same project structure and produce analysis results that are used for the figures and report.

## Scope

The project includes:

- Beam characterization from RAW data.
- Detector characterization from PROC data.
- XGM intensity and position measurements.
- HIREX diagnostic data.
- Gotthard diagnostic data.
- A representative LPD detector sample.
- Figures and a Markdown report.
- An optional Streamlit interface.

The project does not include:

- Analysis of every source and measurement available in the dataset.
- Full-run detector analysis.

The project uses a selected set of measurements from the available dataset.

## Architecture

The project is split into separate parts.

```text
HDF5 Data
    │
    ▼
Dataset Access
    │
    ▼
Metadata
    │
    ▼
Processing
    │
    ├───────────────┐
    ▼               ▼
Beam Analysis   Detector Analysis
    │               │
    └───────┬───────┘
            ▼
       Visualization
            │
            ▼
          Report
            │
            ▼
       Streamlit UI
```

### Dataset Access

`dataset.py` handles access to the XFEL data.

It opens the RAW and PROC datasets, discovers the available sources and measurements, and loads the measurements used by the project.

It uses `EXtra-data` to access the XFEL data.

Dataset access does not perform the analysis.

### Metadata

`metadata.py` reads information about the dataset.

It provides information such as the dataset type and source counts.

### Processing

`processing.py` selects the measurements used by the project.

The RAW beam branch uses:

- `SA1_XTD2_XGM/DOOCS/MAIN:output`
- `SA1_XTD9_HIREX/CAL/MASTER:daqOutput`
- `SA1_XTD9_HIREX/DAQ/GOTTHARD_MASTER:daqOutput`

The PROC detector branch uses:

- `FXE_DET_LPD1M-1/DET/0CH0:xtdf`

The XGM measurements are:

```python
XGM_MEASUREMENTS = {
    "intensity": "data.intensityTD",
    "intensity_uncertainty": "data.intensitySigmaTD",
    "x": "data.xTD",
    "x_uncertainty": "data.xSigmaTD",
    "y": "data.yTD",
    "y_uncertainty": "data.ySigmaTD",
}
```

HIREX uses:

```text
data.image.pixels
```

Gotthard uses:

```text
data.adc
```

The detector analysis uses:

```text
image.data
```

Processing prepares the data for analysis. It does not calculate the results.

### Analysis

`analysis.py` calculates the beam and detector characterization results.

It works on the data prepared by `processing.py`.

It does not access `EXtra-data` directly.

### Visualization

`visualization.py` creates the figures used by the project.

It creates the beam intensity figure and the detector image figure.

### Report

`report.py` creates the Markdown characterization report.

The report contains the run information, beam results, detector results and references to the generated figures.

### Streamlit UI

`ui.py` provides the Streamlit interface.

It uses the existing project pipeline and presents the results interactively.

The UI does not contain the data access or analysis logic.

## Project Structure

```text
.
├── main.py
├── requirements.txt
├── src/
│   ├── dataset.py
│   ├── metadata.py
│   ├── processing.py
│   ├── analysis.py
│   ├── visualization.py
│   ├── report.py
│   └── ui.py
├── tests/
└── outputs/
```

### Source Files

`dataset.py` handles access to the RAW and PROC datasets.

`metadata.py` reads dataset and run information.

`processing.py` selects and prepares the measurements used by the project.

`analysis.py` calculates the beam and detector characterization results.

`visualization.py` creates the analysis figures.

`report.py` creates the Markdown report.

`ui.py` provides the Streamlit dashboard.

### Tests

The `tests/` directory contains tests for the project modules.

The tests cover the dataset access, processing and analysis parts of the project.

### Outputs

The `outputs/` directory contains the figures and report generated by the project.

## Data Used

### Data Source

The data used by the project comes from a European XFEL example run. The example data is provided for working with European XFEL data and the `EXtra-data` tools.

The required example data needs to be available locally before running the project.

### Dataset

The run used by the project is:

- **Experiment:** `XMPL`
- **Proposal:** `201750`
- **Processing run:** `p700000`
- **Run:** `r0299`

The RAW dataset contains the beam and diagnostic sources used by the project. The PROC dataset contains the LPD detector sources. The project does not use every source in the run. It selects the sources and measurements needed for the two analysis paths.

### Local Data Structure

The expected data structure is:

```text
data/
└── XMPL/
    └── 201750/
        └── p700000/
            ├── raw/
            │   └── r0299/
            └── proc/
                └── r0299/
```

### RAW Beam Data

The project uses the following RAW sources and measurements:

| Source | Measurement | Used for |
|---|---|---|
| `SA1_XTD2_XGM/DOOCS/MAIN:output` | `data.intensityTD` | XGM intensity |
| `SA1_XTD2_XGM/DOOCS/MAIN:output` | `data.intensitySigmaTD` | Intensity uncertainty |
| `SA1_XTD2_XGM/DOOCS/MAIN:output` | `data.xTD` | X position |
| `SA1_XTD2_XGM/DOOCS/MAIN:output` | `data.xSigmaTD` | X-position uncertainty |
| `SA1_XTD2_XGM/DOOCS/MAIN:output` | `data.yTD` | Y position |
| `SA1_XTD2_XGM/DOOCS/MAIN:output` | `data.ySigmaTD` | Y-position uncertainty |
| `SA1_XTD9_HIREX/CAL/MASTER:daqOutput` | `data.image.pixels` | HIREX diagnostic data |
| `SA1_XTD9_HIREX/DAQ/GOTTHARD_MASTER:daqOutput` | `data.adc` | Gotthard diagnostic data |

### PROC Detector Data

The project uses:

```text
FXE_DET_LPD1M-1/DET/0CH0:xtdf
```

and loads:

```text
image.data
```

The detector preparation uses a representative detector sample rather than loading the complete detector dataset.

## Beam Characterization

The beam analysis uses the selected XGM, HIREX and Gotthard measurements.

### XGM

The project calculates:

- Mean intensity.
- Intensity standard deviation.
- Relative intensity variation.
- Mean X position.
- X-position standard deviation.
- Mean Y position.
- Y-position standard deviation.

The relative intensity variation is calculated as:

```text
standard deviation / mean
```

Only finite values are used for the calculations.

### HIREX

The project loads the HIREX image data from:

```text
data.image.pixels
```

The current analysis calculates the mean HIREX signal.

The result is the mean of the recorded signal values. It is not converted into a calibrated physical quantity.

### Gotthard

The project loads the Gotthard ADC data from:

```text
data.adc
```

The current analysis calculates the mean Gotthard signal.

The result is the mean of the recorded ADC values. It is not converted into a calibrated physical quantity.

## Detector Characterization

The detector analysis uses the LPD detector data from the PROC dataset.

The detector processing uses:

```text
FXE_DET_LPD1M-1/DET/0CH0:xtdf
```

and reads:

```text
image.data
```

The detector sample is limited to one train for the current analysis.

The project calculates:

- Mean detector signal.
- Detector signal standard deviation.
- Non-finite pixel fraction.

The non-finite pixel fraction shows the proportion of pixels in the sample that do not contain finite values.

The other detector measurements are available in the PROC data, but they are not currently used:

```text
image.gain
image.mask
image.cellId
image.pulseId
```

## Output

Running the project produces the following outputs:

```text
outputs/
├── beam_intensity.png
├── detector_image.png
└── characterization_report.md
```

### Beam Intensity Figure

`beam_intensity.png` shows the XGM intensity over the loaded measurement range.

### Detector Image

`detector_image.png` shows the representative LPD detector sample as an image.

### Characterization Report

`characterization_report.md` contains:

- Run information.
- Beam characterization results.
- Detector characterization results.
- References to the generated figures.
- The scope of the analysis.

The project can also display the same information through the Streamlit interface.

## Setup & Execution

### Prerequisites

The project requires:

- Python 3.10 or newer.
- The European XFEL example data used by the project.

### Install the Dependencies

Install the Python dependencies from `requirements.txt`.

```bash
pip install -r requirements.txt
```

### Run the Analysis

Run the main program:

```bash
python main.py
```

The program loads the RAW and PROC data, prepares the selected measurements, runs the beam and detector analysis, creates the figures and writes the report.

### Start the Streamlit Interface

The project can also be started through Streamlit:

```bash
streamlit run src/ui.py
```

The Streamlit interface provides the same analysis through an interactive interface.

## Execution Flow

The project runs in the following order:

```text
RAW / PROC data
      ↓
Dataset access
      ↓
Dataset information
      ↓
Measurement preparation
      ↓
Beam analysis
      +
Detector analysis
      ↓
Figures
      ↓
Markdown report
      ↓
Streamlit interface
```

The dataset is opened first.

The required dataset information is then read.

The selected RAW and PROC measurements are prepared.

The beam and detector data are passed to the analysis functions.

The analysis results are used to create the figures and report.

The Streamlit interface can then present the same results interactively.

## Results / Example Output

The current example run produces the following characterization results:

| Metric | Value |
|---|---:|
| Mean intensity | 37.37 |
| Intensity standard deviation | 362 |
| Relative intensity variation | 9.688 |
| Mean X position | 1.012 |
| X-position variation | 0.3184 |
| Mean Y position | 0.978 |
| Y-position variation | 0.209 |
| HIREX diagnostic mean | -19.88 |
| Gotthard diagnostic mean | 2998 |
| Mean detector signal | -7.753 |
| Detector signal standard deviation | 1109 |
| Non-finite pixel fraction | 0.0000% |

These values are statistical characterizations of the selected measurements.

They are not calibrated physical quantities.

## Limitations

The current project has a limited scope.

The detector analysis uses one representative detector sample rather than the complete LPD detector data.

The current analysis does not use:

```text
image.gain
image.mask
image.cellId
image.pulseId
```

## Future Work

Possible next steps are:

- Analyze multiple LPD modules and multiple trains.
- Use `image.mask` for detector data quality handling.
- Use `image.gain`, `image.cellId` and `image.pulseId` in the detector analysis.
- Add more beam characterization measurements.
- Explore spectral analysis after understanding the required calibration and data processing.
- Add continuous integration for the test suite.

## Related

[`case_study.md`](case_study.md) explains the general path from an XFEL experiment to HDF5 data.

The case study is independent of this project's implementation. It provides the background needed to understand where the RAW and PROC data used by this project come from.