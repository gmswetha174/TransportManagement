import configparser
import os

class DBPropertyUtil:
    @staticmethod
    def get_connection_string(file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Properties file not found: {file_path}")

        config = configparser.ConfigParser()
        config.read(file_path, encoding='utf-8')

        if 'database' not in config:
            raise KeyError("Missing [database] section in properties file")

        db_config = config['database']
        return {
            'host': db_config.get('host'),
            'port': int(db_config.get('port')),
            'user': db_config.get('user'),
            'password': db_config.get('password'),
            'database': db_config.get('database')
        }
