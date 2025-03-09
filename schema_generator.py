import mysql.connector
import argparse
import sys


def get_table_info(connection, table_name):
    cursor = connection.cursor(dictionary=True)

    # Get table comment
    cursor.execute(f"""
        SELECT TABLE_COMMENT 
        FROM information_schema.TABLES 
        WHERE TABLE_SCHEMA = DATABASE() 
        AND TABLE_NAME = '{table_name}'
    """)
    table_comment = cursor.fetchone()['TABLE_COMMENT'] if cursor.rowcount > 0 else ""

    # Get columns info
    cursor.execute(f"""
        SELECT 
            c.COLUMN_NAME,
            c.DATA_TYPE,
            c.CHARACTER_MAXIMUM_LENGTH,
            c.NUMERIC_PRECISION,
            c.IS_NULLABLE,
            c.COLUMN_DEFAULT,
            c.COLUMN_COMMENT,
            c.ORDINAL_POSITION
        FROM 
            information_schema.COLUMNS c
        WHERE 
            c.TABLE_SCHEMA = DATABASE() 
            AND c.TABLE_NAME = '{table_name}'
        ORDER BY 
            c.ORDINAL_POSITION
    """)
    columns = cursor.fetchall()

    # Get constraints
    cursor.execute(f"""
        SELECT 
            k.CONSTRAINT_NAME,
            k.COLUMN_NAME,
            k.REFERENCED_TABLE_NAME,
            k.REFERENCED_COLUMN_NAME,
            t.CONSTRAINT_TYPE
        FROM 
            information_schema.KEY_COLUMN_USAGE k
        JOIN
            information_schema.TABLE_CONSTRAINTS t
        ON
            k.CONSTRAINT_NAME = t.CONSTRAINT_NAME
            AND k.TABLE_SCHEMA = t.TABLE_SCHEMA
            AND k.TABLE_NAME = t.TABLE_NAME
        WHERE 
            k.TABLE_SCHEMA = DATABASE() 
            AND k.TABLE_NAME = '{table_name}'
    """)
    constraints = cursor.fetchall()

    # Create a dictionary to map columns to their constraints
    column_constraints = {}
    for constraint in constraints:
        col_name = constraint['COLUMN_NAME']
        if col_name not in column_constraints:
            column_constraints[col_name] = []

        constraint_type = constraint['CONSTRAINT_TYPE']
        if constraint_type == 'PRIMARY KEY':
            column_constraints[col_name].append('PK')
        elif constraint_type == 'UNIQUE':
            column_constraints[col_name].append('UK')
        elif constraint_type == 'FOREIGN KEY':
            column_constraints[col_name].append('FK')

    cursor.close()
    return table_name, table_comment, columns, column_constraints


def format_schema(table_name, table_comment, columns, column_constraints):
    output = f"{table_name}:\n"
    if table_comment:
        output += f"{table_comment}\n\n"
    else:
        output += "\n"

    # Format header
    output += f"{'KEYS':<20}{'COLUMN_NAME':<20}{'DATA_TYPE':<20}{'NULLABLE':<20}{'COMMENT'}\n"

    # Format each column
    for col in columns:
        # Format constraints
        keys = ""
        if col['COLUMN_NAME'] in column_constraints:
            keys = ",".join(column_constraints[col['COLUMN_NAME']])

        # Format data type
        data_type = col['DATA_TYPE']
        if col['CHARACTER_MAXIMUM_LENGTH']:
            data_type += f"({col['CHARACTER_MAXIMUM_LENGTH']})"
        elif col['NUMERIC_PRECISION']:
            data_type += f"({col['NUMERIC_PRECISION']})"

        # Format nullable
        nullable = "NOT NULL" if col['IS_NULLABLE'] == 'NO' else ""

        # Format the row
        output += f"{keys:<20}{col['COLUMN_NAME']:<20}{data_type:<20}{nullable:<20}{col['COLUMN_COMMENT']}\n"

    return output


def main():

    try:
        # Connect to the database
        connection = mysql.connector.connect(
            host='35.184.138.61',
            user='root',
            password='chembl',
            database='chembl_35'
        )

        # Get all tables
        cursor = connection.cursor(dictionary=True)
        cursor.execute("""
            SELECT TABLE_NAME 
            FROM information_schema.TABLES 
            WHERE TABLE_SCHEMA = DATABASE()
            ORDER BY TABLE_NAME
        """)
        tables = cursor.fetchall()
        cursor.close()

        # Open output file if specified
        output_file = sys.stdout

        # Process each table
        for table in tables:
            table_name = table['TABLE_NAME']
            table_info = get_table_info(connection, table_name)
            formatted_schema = format_schema(*table_info)

            output_file.write(formatted_schema)
            output_file.write("\n" + "=" * 80 + "\n\n")

        # Close output file if needed
        # if args.output:
        #     output_file.close()
        #     print(f"Schema exported to {args.output}")

        connection.close()

    except mysql.connector.Error as error:
        print(f"Error connecting to MySQL: {error}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())