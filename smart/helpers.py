import logging
import pandas as pd

logger = logging.getLogger(__name__)


def get_hate_terms_from_file_system(csv_file_name: str) -> list:
    result = []
    if csv_file_name:
        try:
            csv_file = pd.read_csv(csv_file_name, encoding='utf')
            csv_file.drop_duplicates(keep='first', inplace=True)
            result = csv_file['terms'].astype(str).values.tolist()
        except (FileNotFoundError, ValueError):
            logger.error(f"Invalid file or filepath submitted: {csv_file_name} not found")
        except KeyError:
            logger.error(f"Submitted file {csv_file_name} does not contain csv header `terms`")
    else:
        logger.error(f"{csv_file_name} file or filepath is empty")

    return result
