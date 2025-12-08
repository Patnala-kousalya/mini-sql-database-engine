import csv
from typing import List, Dict, Any, Tuple

from parser import ParsedQuery, WhereClause, Aggregate, SqlSyntaxError


class SqlExecutionError(Exception):
    """Raised when SQL execution fails."""
    pass


class QueryEngine:
    """
    In-memory SQL execution engine:
    - Loads CSV into a table (list of dicts)
    - SELECT *, SELECT col1, col2
    - WHERE filtering with = != > < >= <=
    - COUNT(*) and COUNT(col)
    """

    def __init__(self):
        self.tables: Dict[str, List[Dict[str, Any]]] = {}

    # --------------------------------------------------
    # LOAD CSV
    # --------------------------------------------------
    def load_csv(self, table_name: str, csv_path: str):
        try:
            with open(csv_path, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                rows = [dict(row) for row in reader]
        except Exception as e:
            raise SqlExecutionError(f"Failed to load CSV: {e}")

        self.tables[table_name] = rows

    # --------------------------------------------------
    # EXECUTE QUERY
    # --------------------------------------------------
    def execute(self, query: ParsedQuery) -> Tuple[List[Dict[str, Any]], List[str]]:
        if query.from_table not in self.tables:
            raise SqlExecutionError(f"Table '{query.from_table}' not loaded.")

        rows = self.tables[query.from_table]

        # 1. WHERE filtering
        if query.where_clause:
            rows = self._apply_where(rows, query.where_clause)

        # 2. COUNT aggregation
        if query.aggregate:
            return self._execute_aggregate(rows, query.aggregate)

        # 3. SELECT projection
        return self._project(rows, query.select_columns)

    # --------------------------------------------------
    # WHERE Filtering (FINAL FIXED VERSION)
    # --------------------------------------------------
    def _apply_where(self, rows: List[Dict[str, Any]], where: WhereClause):
        op = where.operator
        result = []

        for row in rows:
            if where.column not in row:
                raise SqlExecutionError(f"Column '{where.column}' not found.")

            cell = row[where.column]

            left = str(cell).strip().lower()
            right = str(where.value).strip().lower()

            # DEBUG PRINT
            print("DEBUG:", row[where.column], "->", left, op, right)

            try:
                left_num = float(left)
                right_num = float(right)
                left, right = left_num, right_num
            except:
                pass

            if self._compare(left, op, right):
                result.append(row)

        return result

    # --------------------------------------------------
    # Comparison operator
    # --------------------------------------------------
    def _compare(self, a, op, b):
        try:
            if op == "=":
                return a == b
            if op == "!=":
                return a != b
            if op == ">":
                return a > b
            if op == "<":
                return a < b
            if op == ">=":
                return a >= b
            if op == "<=":
                return a <= b
        except:
            return False

        raise SqlExecutionError(f"Invalid operator: {op}")

    # --------------------------------------------------
    # COUNT Aggregation
    # --------------------------------------------------
    def _execute_aggregate(self, rows, agg: Aggregate):
        if agg.arg == "*":
            count = len(rows)
        else:
            col = agg.arg
            count = sum(1 for r in rows if r.get(col) not in (None, ""))

        return [{"COUNT": count}], ["COUNT"]

    # --------------------------------------------------
    # SELECT Projection
    # --------------------------------------------------
    def _project(self, rows, columns):
        # SELECT *
        if columns == ["*"]:
            if not rows:
                return [], []
            return rows, list(rows[0].keys())

        # Validate columns
        if rows:
            missing = [c for c in columns if c not in rows[0]]
            if missing:
                raise SqlExecutionError(f"Unknown columns: {missing}")

        # Build projected rows
        return (
            [{col: row.get(col) for col in columns} for row in rows],
            columns
        )
