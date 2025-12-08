from parser import SimpleSQLParser, SqlSyntaxError
from engine import QueryEngine, SqlExecutionError
import os


def print_table(rows, columns):
    if not rows:
        print("(no rows)")
        return

    # Determine column widths
    widths = {col: len(col) for col in columns}
    for row in rows:
        for col in columns:
            widths[col] = max(widths[col], len(str(row.get(col, ""))))

    # Header
    header = " | ".join(f"{col:<{widths[col]}}" for col in columns)
    separator = "-+-".join("-" * widths[col] for col in columns)
    print(header)
    print(separator)

    # Rows
    for row in rows:
        print(" | ".join(f"{str(row.get(col, '')):<{widths[col]}}" for col in columns))


def main():
    print("Mini SQL Database Engine")
    print("========================")
    print("Type SQL queries, or 'exit' to quit.\n")

    parser = SimpleSQLParser()
    engine = QueryEngine()

    # LOAD CSV STEP
    while True:
        csv_path = input("Enter path to CSV file to load: ").strip()
        if csv_path.lower() in ("exit", "quit"):
            print("Goodbye!")
            return

        if not os.path.exists(csv_path):
            print("File not found. Try again.")
            continue

        table_name = os.path.splitext(os.path.basename(csv_path))[0]

        try:
            engine.load_csv(table_name, csv_path)
            print(f"Loaded table '{table_name}'. You can now run queries.\n")
            break
        except SqlExecutionError as e:
            print(f"Error loading CSV: {e}")

    # SQL REPL
    while True:
        sql = input("sql> ").strip()
        if not sql:
            continue

        if sql.lower() in ("exit", "quit"):
            print("Goodbye!")
            break

        try:
            parsed = parser.parse(sql)
            rows, columns = engine.execute(parsed)
            print_table(rows, columns)

        except SqlSyntaxError as e:
            print(f"Syntax error: {e}")

        except SqlExecutionError as e:
            print(f"Execution error: {e}")

        except Exception as e:
            print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
