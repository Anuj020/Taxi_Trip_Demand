from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    trained_file_path: str
    test_file_path: str
    validation_file_path: str

@dataclass
class DataValidationArtifact:
    drift_report_file_path: str
    