import requests
from pathlib import Path
import datetime

from ingestion.eurostat.config.datasets import EUROSTAT_DATASETS


def update_gitignore():
    gitignore_path = Path(".gitignore")
    content = gitignore_path.read_text(encoding="utf-8") if gitignore_path.exists() else ""

    if "data/" not in content:
        with open(gitignore_path, "a", encoding="utf-8") as f:
            if content and not content.endswith("\n"):
                f.write("\n")
            f.write("# Data directory\ndata/\n")

def download_file(url: str, output_path: Path):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()  # solleva errore per 4xx / 5xx

        output_path.write_bytes(response.content)
        print(f"Downloaded: {output_path}")

    except requests.exceptions.HTTPError as e:
        print(f"HTTP error for {url}: {e}")

    except requests.exceptions.ConnectionError:
        print(f"Connection error while downloading {url}")

    except requests.exceptions.Timeout:
        print(f"Timeout while downloading {url}")

    except Exception as e:
        print(f"Unexpected error for {url}: {e}")


def download_gas_data():
    dataset = EUROSTAT_DATASETS["gas_imports"]

    dataset_id = dataset["dataset_id"]
    filters = dataset["filters"]
    freq = filters["freq"]
    geo = filters["geo"]

    year = datetime.datetime.now().year

    endpoint = "https://ec.europa.eu/eurostat/api/dissemination/sdmx/2.1"
    base_url = (
        f"{endpoint}/data/{dataset_id}/{freq}....{geo}"
        "?startPeriod=YEAR&endPeriod=YEAR&format=SDMX-CSV"
    )

    output_dir = Path("data/raw/eurostat/facts/gas_imports")
    output_dir.mkdir(parents=True, exist_ok=True)

    update_gitignore()

    for year in range(1990, year):
        url_parametrized = base_url.replace("YEAR", str(year))
        output_file = output_dir / f"gas_imports_{year}.csv"

        print(f"Downloading {year}...")
        print(url_parametrized)

        download_file(url_parametrized, output_file)

    print("Gas data download completed.")

