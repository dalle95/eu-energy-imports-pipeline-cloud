from pathlib import Path

try:
    from ingestion.eurostat.upload.upload_data_to_gcp import upload_data_to_gcp
except ImportError:  # pragma: no cover - allow running as a script
    from upload_data_to_gcp import upload_data_to_gcp


def upload_dimensions_data_to_gcp():
    bucket = "eu-energy-imports-pipeline-raw-data-bucket"
    source_dir = Path("./data/processed/eurostat/dimensions/")
    destination_prefix = "eurostat/dimensions/"
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

    # Upload the value data to GCP
    source_dir = Path("./data/processed/eurostat/dimensions/")
    destination_prefix = "eurostat/dimensions/"
    upload_data_to_gcp(
        bucket=bucket,
        source_dir=source_dir,
        destination_prefix=destination_prefix,
        file_extension=file_extension,
        dry_run=dry_run,
    )

if __name__ == "__main__":
    upload_dimensions_data_to_gcp()