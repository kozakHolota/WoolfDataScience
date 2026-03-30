from pathlib import Path

import click
import pandas as pd
from sqlalchemy import create_engine


@click.command()
@click.option('--host', default='localhost', help='Host to connect to')
@click.option('--port', default=3306, help='Port to connect to')
@click.option('--db_name', help='Database name to connect to', required=True)
@click.option('--user', help='User to connect with', required=True)
@click.option('--password', help='Password to connect with', required=True)
def main(host: str, port: int, db_name: str, user: str, password: str):
    engine = create_engine(f'mysql+pymysql://{user}:{password}@{host}:{port}/{db_name}')
    csv_dataset_path = Path(__file__).parent.parent / 'csv_dataset'
    for file in csv_dataset_path.glob('*.csv'):
        table_name = file.stem
        df = pd.read_csv(file)
        df.to_sql(table_name, engine, if_exists='replace', index=False)

if __name__ == '__main__':
    main()