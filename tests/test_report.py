

from pathlib import Path
from types import SimpleNamespace

from src.report import generate_report


def test_generate_report(tmp_path):
    results = {
        "beam": SimpleNamespace(
            intensity_mean=10.0,
            intensity_std=2.0,
            intensity_relative_variation=0.2,
            x_mean=1.0,
            x_std=0.1,
            y_mean=2.0,
            y_std=0.2,
            hirex_mean=3.0,
            gotthard_mean=4.0,
        ),
        "detector": SimpleNamespace(
            mean_signal=5.0,
            signal_std=1.0,
            bad_pixel_fraction=0.01,
        ),
    }

    metadata = SimpleNamespace(
        dataset_type="RAW",
        source_count=18,
    )

    output = tmp_path / "report.md"

    result = generate_report(
        results,
        metadata,
        output_path=output,
    )

    assert result == output
    assert output.exists()

    content = output.read_text(
        encoding="utf-8"
    )

    assert "XFEL Characterization Report" in content
    assert "Beam Characterization" in content
    assert "Detector Characterization" in content
    assert "Mean intensity" in content