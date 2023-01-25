import pandas as pd
from sqlalchemy import create_engine


class DBManager:

    def __init__(self, host: str, port: str, db_name: str, username: str, password: str) -> None:
        """
            Creates an engine to connect to the database using SQLAlchemy

            Parameters:
                host (str): host address
                post (str): port number
                db_name (str): database name
                username (str): username for accessing the database
                password (str): password for accessing the database
        """

        # Initialize SQLalchemy engine
        # Engine instance
        self.engine = create_engine(f"postgresql://{username}:{password}@{host}:{port}/{db_name}")
        self.db_name = db_name


    def create_table(self, table_name: str, params: list):
        """ Create a table in corresponding database if not exists """
        sql = f'CREATE TABLE IF NOT EXISTS {table_name} ({", ".join([param[0]+" "+param[1] for param in params])});'
        self.engine.execute(sql)



    def df_to_table(self, df, table_name, if_exists='replace'):
        """Dump dataframe to psql database"""
        df.to_sql(table_name, self.engine, if_exists = if_exists, index = False)


if __name__=="__main__":
    obj = DBManager('localhost', 5432, 'scrabia', 'postgres', 'postgres')
    params = [('title', 'text'),
                ('company', 'text'),
                ('location', 'text'),
                ('apply', 'text'),
                ('description', 'text'),]
    obj.create_table('jobs', params)
    obj.df_to_table(pd.DataFrame([['1', '2', '3', '4', '5']], columns=['title', 'company', 'location', 'apply', 'description']), 'scrabia')
