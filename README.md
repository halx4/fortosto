# fortosto

Easily import CSV/JSONL files into PostgreSQL.
This tool automates the process of dumping data from a file into a database.

### Features:

- Automatic table creation
- Batch import folder
- table name prefix

## Install

**Windows**

download the latest executable [here](https://github.com/halx4/fortosto/releases/latest).

**Linux**

TODO...

## Usage

### Basic Usage

### Full Parameters Reference

```shell script
fortosto [-h] -f TARGET [-H HOST] [-P PORT] [-u USERNAME] [-p PASSWORD]
               [-d DATABASE] [-s SCHEMA] [-t TABLE] [-D DELIMITER]
               [-tp TABLE_PREFIX] [-pk PRIMARY_KEY]
               [--filename-pattern FILENAME_PATTERN] [--drop-if-exists]
               [--cast-numbers] [--verbose] [-v]


  -f TARGET, --target TARGET
#               target file name (required)

  -H HOST, --host HOST
#               Db Host 
#               (default: localhost)

  -P PORT, --port PORT
#               TCP Port 
#               (default: 5432)

  -u USERNAME, --username USERNAME
#               Db username 
#               (default: postgres)

  -p PASSWORD, --password PASSWORD
#               Db password 
#               (default: "")

  -d DATABASE, --database DATABASE
#               The db name 
#               (default: postgres)

  -s SCHEMA, --schema SCHEMA
#               The schema name.
#               (default: public)

  -t TABLE, --table TABLE
#               table name (must match [a-z0-9_]* )
#               (default: the filename lowercased and normalised)

  -D DELIMITER, --delimiter DELIMITER
#               delimiter used in csv files.
#               Ignored when targeting jsonl files.
#               (default: ',')

  -tp TABLE_PREFIX, --table-prefix TABLE_PREFIX
#               table name prefix 
#               (default: "")

  -pk PRIMARY_KEY, --primary-key PRIMARY_KEY
#               primary key column name to be added 
#               (default: )

  --filename-pattern FILENAME_PATTERN
#               Glob-style lookup pattern. 
#               Ignored when the target is a file.
#               (default: "*.csv")

  -die, --drop-if-exists      
#               drop table if it already exists in the db
#               (default: False)

  --cast-numbers        
#               try casting number columns after importing 
#               (default: False)

  --verbose             
#               enable verbose logging 
#               (default: False)

  -v, --version         
#               print version info and exit the application

  -h, --help
#               show usage instructions
```

### Examples

#### Custom delimiter

#### Batch import


## Limitations

- Csv must have headers
- Jsonl: all lines must have the same keys

## Build