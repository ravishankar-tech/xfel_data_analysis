
from pathlib import Path

import xarray as xr
from extra_data import RunDirectory


class DatasetError(Exception):
    """Base exception for dataset access errors."""

    pass


class DatasetNotFoundError(DatasetError):
    """Raised when a dataset cannot be found."""

    pass


class SourceNotFoundError(DatasetError):
    """Raised when a source cannot be found."""

    pass


class MeasurementNotFoundError(DatasetError):
    """Raised when a measurement cannot be found."""

    pass


class XFELDataset:
    """Access the RAW and PROC datasets for an XFEL run."""
    

    def __init__(
        self,
        raw_path: str | Path | None = None,
        proc_path: str | Path | None = None,
    ):
        self.raw_path = self._validate_path(raw_path, "RAW")
        self.proc_path = self._validate_path(proc_path, "PROC")

        self._raw = None
        self._proc = None

    @staticmethod
    def _validate_path(
        path: str | Path | None,
        dataset_name: str,
    ) -> Path | None:
        # Validate a dataset directory
        if path is None:
            return None

        path = Path(path)

        if not path.exists():
            raise DatasetNotFoundError(
                f"{dataset_name} dataset not found: {path}"
            )

        if not path.is_dir():
            raise DatasetNotFoundError(
                f"{dataset_name} dataset is not a directory: {path}"
            )

        return path.resolve()

    def has_raw(self) -> bool:
        # Return whether RAW data is available
        return self.raw_path is not None

    def has_proc(self) -> bool:
        # Return whether PROC data is available
        return self.proc_path is not None

    def raw(self):
        # Open and return the RAW dataset
        if self.raw_path is None:
            raise DatasetNotFoundError(
                "RAW dataset is not available."
            )

        if self._raw is None:
            self._raw = RunDirectory(str(self.raw_path))

        return self._raw

    def proc(self):
        # Open and return the PROC dataset
        if self.proc_path is None:
            raise DatasetNotFoundError(
                "PROC dataset is not available."
            )

        if self._proc is None:
            self._proc = RunDirectory(str(self.proc_path))

        return self._proc

# Return RAW or PROC dataset
    def _get_dataset(self, dataset: str):
        
        dataset = dataset.lower()

        if dataset == "raw":
            return self.raw()

        if dataset == "proc":
            return self.proc()

        raise ValueError(
            "dataset must be 'raw' or 'proc'"
        )

 # Return all sources in a dataset
    def sources(self, dataset: str) -> list[str]:
       
        run = self._get_dataset(dataset)

        return sorted(
            set(run.instrument_sources)
            | set(run.control_sources)
        )

# Return measurements available for a source
    def measurements(
        self,
        dataset: str,
        source: str,
    ) -> list[str]:
        
        run = self._get_dataset(dataset)

        if source not in run:
            raise SourceNotFoundError(
                f"Source not found: {source}"
            )

        return sorted(run[source].keys())

    def get_measurement(
        self,
        dataset: str,
        source: str,
        measurement: str,
    ) -> xr.DataArray:
       
        run = self._get_dataset(dataset)

        if source not in run:
            raise SourceNotFoundError(
                f"Source not found: {source}"
            )

        if measurement not in run[source].keys():
            raise MeasurementNotFoundError(
                f"Measurement not found: "
                f"{source}/{measurement}"
            )

        return run[source, measurement].xarray()

    def get_detector_sample(
        self,
        source: str,
        measurement: str = "image.data",
        max_trains: int = 1,
    ) -> xr.DataArray:
        
        if max_trains < 1:
            raise ValueError("max_trains must be at least 1")

        run = self.proc()

        if source not in run:
            raise SourceNotFoundError(
                f"Source not found: {source}"
            )

        if measurement not in run[source].keys():
            raise MeasurementNotFoundError(
                f"Measurement not found: "
                f"{source}/{measurement}"
            )

        selected = run.select(
            source,
            measurement,
        )

        arrays = []

        for _, train_data in selected.trains(
            require_all=True
        ):
            value = train_data[source][measurement]

            arrays.append(value)

            if len(arrays) >= max_trains:
                break

        if not arrays:
            raise DatasetError(
                f"No detector data available for "
                f"{source}/{measurement}"
            )

        import numpy as np

        data = np.concatenate(arrays, axis=0)

        return xr.DataArray(data)

    def close(self):
        
        self._raw = None
        self._proc = None