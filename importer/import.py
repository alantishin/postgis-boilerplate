import pandas as pd
from sqlalchemy import create_engine
import argparse
import json
import os
import pathlib

"""
Import files to db
"""

parser = argparse.ArgumentParser()

parser.add_argument("--user", help="db user", default=os.environ.get('POSTGRES_USER'))
parser.add_argument("--password", help="db password", default=os.environ.get('POSTGRES_PASSWORD'))
parser.add_argument("--db", help="db name", default=os.environ.get('POSTGRES_DB'))
parser.add_argument("--host", help="db host", default=os.environ.get('POSTGRES_HOST'))
parser.add_argument("--port", help="db port", type=int, default=5432)

parser.add_argument("--filename", help="Import filename", required=True)

parser.add_argument("--schema", help="Schema", required=True)
parser.add_argument("--table", help="Table name", required=True)

args = parser.parse_args()


engine = create_engine( 'postgresql://{}:{}@{}:{}/{}'.format(args.user, args.password, args.host, args.port, args.db) )


ext = pathlib.Path(args.filename).suffix
dataframe = None

if(ext == '.xlsx'):
    dataframe = pd.read_excel( './data/{}'.format(args.filename), engine='openpyxl')
elif(ext == '.csv'):
    dataframe = pd.read_csv('./data/{}'.format(args.filename))
else:
    raise Exception('Unknown format', ext)


dataframe.to_sql(
    name=args.table,
    con=engine,
    schema=args.schema,
    if_exists='append',
    index=False,
)

print('successfully imported')