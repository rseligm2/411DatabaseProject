from pathlib import Path

SOURCE_DIR: Path = Path(__file__).parent
APP_ROOT_DIR: Path = SOURCE_DIR.parent

DATA_DIR: Path = APP_ROOT_DIR/'data/sql'

SQL_DB_FILE: Path = DATA_DIR/'football.db'