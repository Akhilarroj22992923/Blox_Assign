from sqlalchemy import create_engine
import hashlib
from database_details import local_db_url, cloud_db_url  # Import the database URLs from the other file

def get_row_count(engine, table_name):
    query = f"SELECT COUNT(*) FROM {table_name}"
    with engine.connect() as conn:
        result = conn.execute(query)
        return result.scalar()

def get_table_checksum(engine, table_name):
    """
    Generate a checksum for the table by hashing all rows' data.
    """
    query = f"SELECT * FROM {table_name}"
    checksum = hashlib.sha256()
    with engine.connect() as conn:
        result = conn.execute(query)
        for row in result:
            row_data = ''.join(map(str, row))
            checksum.update(row_data.encode('utf-8'))
    return checksum.hexdigest()

def compare_databases(local_db_url, cloud_db_url, tables):
    local_engine = create_engine(local_db_url)
    cloud_engine = create_engine(cloud_db_url)

    for table in tables:
        local_row_count = get_row_count(local_engine, table)
        cloud_row_count = get_row_count(cloud_engine, table)
        if local_row_count != cloud_row_count:
            print(f"Row count mismatch in {table}: Local={local_row_count}, Cloud={cloud_row_count}")
            continue

        local_checksum = get_table_checksum(local_engine, table)
        cloud_checksum = get_table_checksum(cloud_engine, table)
        if local_checksum != cloud_checksum:
            print(f"Data mismatch in {table}. Checksums do not match.")
        else:
            print(f"Table {table} is consistent across both databases.")

# Example usage
tables_to_check = ["customers", "orders", "products"]
compare_databases(local_db_url, cloud_db_url, tables_to_check)
