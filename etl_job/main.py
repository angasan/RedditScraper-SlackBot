"""
Executable file for the ETL process
"""

import time

from etl_job import (
    extract,
    transform,
    load
)

if __name__ == '__main__':

    extracted_reddits = extract()
    transformed_reddits = transform(extracted_reddits)
    eng, con = load(transformed_reddits)
    
    con.close()
    eng.dispose()