

from pathlib import Path

from src import ui


def test_ui_module_imports():
    assert callable(ui.main)
    assert callable(ui.run_pipeline)
    assert callable(ui.refresh_report)
    assert callable(ui.load_report)


def test_run_configuration():
    assert ui.EXPERIMENT == "XMPL"
    assert ui.PROPOSAL == "201750"
    assert ui.PROCESSING_RUN == "p700000"
    assert ui.RUN == "r0299"
    assert ui.DETECTOR_SOURCE == (
        "FXE_DET_LPD1M-1/DET/0CH0:xtdf"
    )


def test_format_value():
    assert ui.format_value(10.123456) == "10.12"
    assert ui.format_value(0.2) == "0.2"
    assert ui.format_value(float("nan")) == "Not available"
    assert ui.format_value(None) == "Not available"


def test_load_report(tmp_path):
    report = tmp_path / "report.md"
    report.write_text("# Test report", encoding="utf-8")

    assert ui.load_report(report) == "# Test report"


def test_load_report_missing(tmp_path):
    missing = tmp_path / "missing.md"

    try:
        ui.load_report(missing)
    except FileNotFoundError as exc:
        assert "Report not found" in str(exc)
    else:
        raise AssertionError("Expected FileNotFoundError")
