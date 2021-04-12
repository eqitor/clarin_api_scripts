import logging

from tenacity import after_log, before_log, retry, stop_after_attempt, wait_fixed

from db.client import client
# from app.db.session import SessionLocal
# from app.s3.client import s3client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

max_tries = 60 * 5  # 5 minutes
wait_seconds = 1


@retry(
    stop=stop_after_attempt(max_tries),
    wait=wait_fixed(wait_seconds),
    before=before_log(logger, logging.INFO),
    after=after_log(logger, logging.WARN),
)
def init() -> None:
    try:
        # TODO: place to initialize other services like db, storage etc.
        # Try to create session to check if DB is awake
        server_info = client.server_info()
        logger.info(server_info)
        logger.info("MongoDb initialized")
        # s3 = s3client
        # s3.list_buckets()
        # logger.info("Minio initialized")
        pass
    except Exception as e:
        logger.error(e)
        raise e


def main() -> None:
    logger.info("Initializing service")
    init()
    logger.info("Service finished initializing")


if __name__ == "__main__":
    main()
