import logging
from db.init_db import init_db

# from app.s3.init_minio import init_minio
# from app.s3.client import s3client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    # TODO: place to initialize data into database and storage
    init_db(logger)
    # try:
    #     init_minio(s3client)
    # except FileExistsError as exc:
    #     logger.warning(f"Error occured while initializing minio: {exc}")

    pass


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
