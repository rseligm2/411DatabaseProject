import sqlite3 as sql
from typing import List, Dict, Any, Union, Optional
from dataclasses import asdict, dataclass, is_dataclass, make_dataclass, astuple

from src.config import SQL_DB_FILE

connection = sql.connect(str(SQL_DB_FILE))

