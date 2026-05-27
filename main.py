#######################################################################

__maintainer__      = 'Anders H. Vestergaard'
__author__          = 'Anders H. Vestergaard'
__contributors__    = []
__email__           = 'anders.vestergaard@hjoerring.dk'
__version__         = '1.0.0'
__status__          = 'Production'

'''
Description:
    Reads CSV files from a mounted network share, writes the data to SQL
    Server, and archives the processed files.

Flow:
    1. Validate environment variables and file paths.
    2. Locate CSV files matching expected filename patterns.
    3. Establish a SQLAlchemy database engine.
    4. Write enrollment, institution and classroom data to SQL.
    5. Archive processed files.
'''

#######################################################################

import datetime
import logging
import os
import re
from dateutil.relativedelta import relativedelta
from dotenv import load_dotenv
from utils.archive_files import archive_files
from utils.get_engine import get_engine
from utils.write_indmeldelser import write_indmeldelser
from utils.write_institutioner import write_institutioner
from utils.write_stuer import write_stuer

load_dotenv()
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%m-%Y %H:%M:%S', level=logging.INFO)
logging.info('Libraries imported')

#######################################################################

# Standard variables
process_date = (datetime.datetime.now() - datetime.timedelta(days=1)).date()
logging.info('Standard variables set')

# Table names
indmeldelser_table  = os.getenv('DB_TABLE_INDMELDELSER')
institutioner_table = os.getenv('DB_TABLE_INSTITUTIONER')
stuer_table         = os.getenv('DB_TABLE_STUER')

if not all([indmeldelser_table, institutioner_table, stuer_table]):
    missing = [name for name, val in [
        ('DB_TABLE_INDMELDELSER', indmeldelser_table),
        ('DB_TABLE_INSTITUTIONER', institutioner_table),
        ('DB_TABLE_STUER', stuer_table)
    ] if not val]
    raise EnvironmentError(f'Missing required environment variables: {", ".join(missing)}')

# File paths
file_path = os.getenv('FILE_PATH')
if not file_path:
    raise EnvironmentError('Missing required environment variable: FILE_PATH')
if not os.path.isdir(file_path):
    raise FileNotFoundError(f'FILE_PATH does not exist or is not accessible: {file_path}')

files = os.listdir(file_path)

indmeldelser_file  = next((os.path.join(file_path, f) for f in files if re.match(r'^Indmeldelser_\d{8}\.csv$', f)), None)
institutioner_file = next((os.path.join(file_path, f) for f in files if re.match(r'^Institutioner_\d{8}\.csv$', f)), None)
stuer_file         = next((os.path.join(file_path, f) for f in files if re.match(r'^Stuer_\d{8}\.csv$', f)), None)

if not all([indmeldelser_file, institutioner_file, stuer_file]):
    missing = [name for name, f in [
        ('Indmeldelser', indmeldelser_file),
        ('Institutioner', institutioner_file),
        ('Stuer', stuer_file)
    ] if not f]
    raise FileNotFoundError(f'Missing CSV files in {file_path}: {", ".join(missing)}')

logging.info('Files retrieved')

#######################################################################

engine = get_engine()

write_indmeldelser(indmeldelser_table, indmeldelser_file, engine)
write_institutioner(institutioner_table, institutioner_file, engine)
write_stuer(stuer_table, stuer_file, engine)
logging.info('All data written to SQL')

archive_files(file_path)
logging.info('Done')