import logging
import numpy as np
import pandas as pd
from sqlalchemy import text
from sqlalchemy.engine import Engine

logger = logging.getLogger(__name__)

def write_indmeldelser(table: str, file: str, engine: Engine) -> None:
    '''
    Description:
        Truncates the target table and writes enrollment data from a
        CSV file into it.

    Flow:
        1. Read CSV file into a DataFrame.
        2. Clean infinite values and fill NaN with empty string.
        3. Select and rename relevant columns.
        4. Truncate target table and insert DataFrame rows.

    Args:
        table (str): Name of the target SQL table.
        file (str): Full path to the CSV file containing enrollment data.
        engine (Engine): SQLAlchemy engine connected to the target database.

    Returns:
        None.

    Raises:
        FileNotFoundError: If the CSV file does not exist.
        KeyError: If expected columns are missing from the CSV file.
        SQLAlchemyError: If the database operation fails.
    '''
    
    df = pd.read_csv(file, encoding='utf-8', sep=';', dtype=str)
    df.replace({np.inf: np.nan, -np.inf: np.nan}, inplace=True)
    df = df.fillna('')
    df = df[[
        'CPR', 'År', 'Måned', 'Indmeldelse', 'Udmeldelse',
        'InstitutionID', 'Kommune', 'Alder', 'Navn',
        'Dobbelttæller', 'Stuetilknytning', 'Plejebarn']]
    
    df.columns = [
        'cpr', 'year', 'month', 'start_date', 'end_date',
        'institution_id', 'municipality_id', 'age_in_months', 'child_name',
        'double_count', 'group_id', 'foster_care']
    
    with engine.begin() as conn:
        conn.execute(text(f'DELETE FROM {table}'))
        df.to_sql(table, con=conn, if_exists='append', index=False)
    logger.info('write_indmeldelser completed')