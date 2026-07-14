import os
from pathlib import Path

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional dependency
    def load_dotenv() -> bool:
        return False

load_dotenv()


def upload_file(bucket, source_path: Path, destination_blob_name: str):
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(str(source_path))
    print(f"Uploaded {source_path} => gs://{bucket.name}/{destination_blob_name}")


def normalize_extensions(file_extension):
    if isinstance(file_extension, str):
        values = [file_extension]
    else:
        values = list(file_extension)

    normalized = []
    for value in values:
        value = str(value).strip()
        if not value:
            continue
        normalized.append(value if value.startswith(".") else f".{value}")
    return tuple(normalized)


def find_files(source_dir: Path, file_extensions):
    extensions = normalize_extensions(file_extensions)
    if not extensions:
        raise ValueError("At least one file extension must be provided")

    # Cerca tutti i file direttamente dentro la cartella passata, senza scendere nelle sotto-cartelle
    candidates = sorted(source_dir.glob("*"))

    return [
        path
        for path in candidates
        if path.is_file() and path.suffix.lower() in {ext.lower() for ext in extensions}
    ]

def upload_directory(
    bucket_name: str,
    source_dir: Path,
    destination_prefix: str = "",
    file_extension: str | tuple[str, ...] = ".parquet",
):
    try:
        from google.cloud import storage
    except ImportError as exc:
        raise ImportError(
            "Missing dependency 'google-cloud-storage'. Install it with `pip install google-cloud-storage`."
        ) from exc

    if not source_dir.exists() or not source_dir.is_dir():
        raise FileNotFoundError(f"Source directory not found: {source_dir}")

    files_to_upload = find_files(source_dir, file_extension)
    if not files_to_upload:
        raise FileNotFoundError(
            f"No files with extension {file_extension} found in {source_dir}"
        )

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    if not bucket.exists():
        raise ValueError(f"Bucket does not exist: {bucket_name}")

    for source_path in files_to_upload:
        relative_name = source_path.relative_to(source_dir)
        destination_blob_name = (
            f"{destination_prefix.rstrip('/')}/{relative_name.as_posix()}"
            if destination_prefix
            else relative_name.as_posix()
        )
        upload_file(bucket, source_path, destination_blob_name)


def upload_data_to_gcp(
    bucket: str = "REPLACE_WITH_BUCKET_NAME",
    source_dir: str | Path = "data/processed/gas_import",
    destination_prefix: str = "eurostat/gas_imports",
    file_extension: str | tuple[str, ...] = ".parquet",
    dry_run: bool = False,
) -> None:
    source_dir = Path(source_dir)
    files_to_upload = find_files(source_dir, file_extension)

    if dry_run:
        if not files_to_upload:
            raise FileNotFoundError(
                f"No files with extension {file_extension} found in {source_dir}"
            )
        print("Dry run: the following files would be uploaded:")
        for source_path in files_to_upload:
            relative_name = source_path.relative_to(source_dir)
            destination_blob_name = (
                f"{destination_prefix.rstrip('/')}/{relative_name.as_posix()}"
                if destination_prefix
                else relative_name.as_posix()
            )
            print(f"  {source_path} => gs://{bucket}/{destination_blob_name}")
        return

    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print(
            "Warning: GOOGLE_APPLICATION_CREDENTIALS is not set in the environment. "
            "dotenv will attempt to load it from .env if present."
        )

    upload_directory(bucket, source_dir, destination_prefix, file_extension)
