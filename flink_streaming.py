from pyflink.table import EnvironmentSettings, TableEnvironment
import os


# Create a batch TableEnvironment
env_settings = EnvironmentSettings.in_streaming_mode()
table_env = TableEnvironment.create(env_settings)

# Get the current working directory
CURRENT_DIR = os.getcwd()

# Define a list of JAR file names you want to add
jar_files = [
    "flink-sql-connector-postgres-cdc-3.0.1.jar",
    "postgresql-42.6.0.jar",
    "flink-connector-jdbc-3.3.0-1.20.jar"
]

# Build the list of JAR URLs by prepending 'file:///' to each file name
jar_urls = [f"file:///{CURRENT_DIR}/{jar_file}" for jar_file in jar_files]

table_env.get_config().get_configuration().set_string(
    "pipeline.jars",
    ";".join(jar_urls)
)

postgres_sink = f"""
CREATE TABLE test_data_e (
    id BIGINT,
    name STRING,
    vals INT,
   PRIMARY KEY (id) NOT ENFORCED
 ) WITH (
   'connector' = 'postgres-cdc',
   'hostname' = 'localhost',
   'port' = '5432',
   'username' = 'paimon',
   'password' = 'paimon123',
   'database-name' = 'postgres',
   'schema-name' = 'public',
    'slot.name' = 'sales',
    'decoding.plugin.name' = 'pgoutput',
   'table-name' = 'test_data_e'
 );
"""

table_env.execute_sql(postgres_sink)


table_env.execute_sql(f"SELECT * FROM test_data_e ").print()