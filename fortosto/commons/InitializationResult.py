from dataclasses import dataclass
from typing import Optional


@dataclass
class InitializationResult:
    dbname: Optional[str] = None
    user: Optional[str] = None
    password: Optional[str] = None
    host: Optional[str] = None
    port: Optional[str] = None
    schema: Optional[str] = None
    delimiter: Optional[str] = None

    tableNamePrefix: Optional[str] = None
    primaryKey: Optional[str] = None
    filenamePattern: Optional[str] = None
    dropTableIfExists: bool = False
    castNumbers: bool = False
    appendMode: bool = False

    target: Optional[str] = None
    table: Optional[str] = None
