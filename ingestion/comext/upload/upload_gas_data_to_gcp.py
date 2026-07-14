from pathlib import Path

try:
    from ingestion.comext.upload.upload_data_to_gcp import upload_data_to_gcp
except ImportError:  # pragma: no cover - allow running as a script
    from upload_data_to_gcp import upload_data_to_gcp

def upload_gas_data_to_gcp():
    bucket = "eu-energy-imports-pipeline-raw-data-bucket"
    source_dir = Path("./data/raw/comext/facts/gas_imports")
    destination_prefix = "comext/facts/gas_imports"
    file_extension = ".csv"
    dry_run = False

    # Upload the quantity data to GCP
    upload_data_to_gcp(
        bucket=bucket,
        source_dir=source_dir,
        destination_prefix=destination_prefix,
        file_extension=file_extension,
        dry_run=dry_run,
    )

if __name__ == "__main__":
    upload_gas_data_to_gcp()
    