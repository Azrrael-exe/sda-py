import psycopg2
from settings import Settings

settings = Settings()

def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except psycopg2.OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

connection = create_connection(
    db_name=settings.PG_DB,
    db_user=settings.PG_USER,
    db_password=settings.PG_PASSWORD,
    db_host=settings.PG_HOST,
    db_port=settings.PG_PORT,
)

def add_read(connection, variable: str, value: float):
    insert_query = "INSERT INTO reads (variable, value) VALUES ('{variable}', {value})".format(variable=variable, value=value)
    cursor = connection.cursor()
    cursor.execute(insert_query)
    connection.commit()

add_read(connection, variable="Voltage", value=1023)

connection.close()
