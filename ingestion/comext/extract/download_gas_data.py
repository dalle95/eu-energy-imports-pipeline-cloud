import requests
from pathlib import Path
import datetime

from ingestion.comext.config.datasets import COMEXT_DATASETS


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
    dataset = COMEXT_DATASETS["gas_imports"]

    dataset_id = dataset["dataset_id"]
    filters = dataset["filters"]
    freq = filters["freq"]
    reporter = filters["reporter"]
    product = filters["product"]
    indicators = filters["indicators"]
    indicators_str = "+".join(indicators)

    current_year = datetime.datetime.now().year

    update_gitignore()

    for p in product:
       
        endpoint = "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1"
        base_url = (
            f"{endpoint}/data/{dataset_id}/{freq}.{reporter}..{p}.1.{indicators_str}"
            "?startPeriod=YEAR-01&endPeriod=YEAR-12&format=SDMX-CSV"
        )

        output_dir = Path("data/raw/comext/facts/gas_imports")
        output_dir.mkdir(parents=True, exist_ok=True)

        for year in range(1990, current_year+1):
            url_parametrized = base_url.replace("YEAR", str(year))
            output_file = output_dir / f"gas_{p}_imports_{year}.csv"

            print(f"Downloading {year}...")
            print(url_parametrized)

            download_file(url_parametrized, output_file)

        print("Gas data download completed.")

if __name__ == "__main__":
    download_gas_data()

