from pathlib import Path

APP_ROOT_DIR: Path = Path(__file__).parent

DATA_DIR: Path = APP_ROOT_DIR/'data/'

SQL_DB_FILE: Path = DATA_DIR/'football.db'