from ingestion.eurostat.config.download_dimensions import download_dimensions

from ingestion.eurostat.extract.download_oil_data import download_oil_data as download_oil_data_eurostat
from ingestion.eurostat.extract.download_gas_data import download_gas_data as download_gas_data_eurostat
from ingestion.eurostat.extract.download_electricity_data import download_electricity_data as download_electricity_data_eurostat

from ingestion.comext.extract.download_oil_data import download_oil_data as download_oil_data_comext
from ingestion.comext.extract.download_gas_data import download_gas_data as download_gas_data_comext

from ingestion.eurostat.upload.upload_dimensions_data_to_gcp import upload_dimensions_data_to_gcp as upload_dimensions_data_to_gcp
from ingestion.comext.upload.upload_gas_data_to_gcp import upload_gas_data_to_gcp as upload_gas_data_to_gcp
from ingestion.comext.upload.upload_oil_data_to_gcp import upload_oil_data_to_gcp as upload_oil_data_to_gcp


def run_ingestion():
    print("Ingestion phase started")

    print("Starting Eurostat dimensions ingestion")
    download_dimensions()
    print("Eurostat dimensions ingestion completed")

    print("Starting Eurostat oil ingestion")
    download_oil_data_eurostat()
    print("Eurostat oil ingestion completed")

    print("Starting Eurostat gas ingestion")
    download_gas_data_eurostat()
    print("Eurostat gas ingestion completed")

    print("Starting Eurostat electricity ingestion")
    download_electricity_data_eurostat()
    print("Eurostat electricity ingestion completed")

    print("Starting Comext oil ingestion")
    download_oil_data_comext()
    print("Comext oil ingestion completed")

    print("Starting Comext gas ingestion")
    download_gas_data_comext()
    print("Comext gas ingestion completed")

    print("Starting GCP upload")
    print("Starting Comext gas upload")
    upload_gas_data_to_gcp()
    print("Starting Comext oil upload")
    upload_oil_data_to_gcp()
    print("Starting Eurostat dimensions upload")
    upload_dimensions_data_to_gcp()
    print("GCP upload completed")

    print("Ingestion phase completed")

if __name__ == "__main__":
    run_ingestion()