from app import schemas, crud
from logging import Logger


def init_db(logger: Logger) -> None:

    INITIAL_DATA = {
        "example_corpus": {
            "name": "example_corpus"
        }
    }

    for corpus in INITIAL_DATA:
        if not crud.corpus.get_by_name(corpus):
            corpus_in = schemas.CorpusCreate(**INITIAL_DATA[corpus])
            corpus = crud.corpus.create(obj_in=corpus_in)
            logger.debug(corpus.to_json())
