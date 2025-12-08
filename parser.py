import re
from dataclasses import dataclass
from typing import List, Optional, Any


class SqlSyntaxError(Exception):
    """Raised when the SQL query has invalid syntax."""
    pass


@dataclass
class WhereClause:
    column: str
    operator: str
    value: Any


@dataclass
class Aggregate:
    func: str
    arg: str   # "*" or column name


@dataclass
class ParsedQuery:
    select_columns: Optional[List[str]]
    aggregate: Optional[Aggregate]
    from_table: str
    where_clause: Optional[WhereClause]


class SimpleSQLParser:
    """
    Simple SQL parser supporting:
    SELECT *, SELECT col1, col2
    SELECT COUNT(*), COUNT(col)
    Optional WHERE clause
    """

    SELECT_REGEX = re.compile(
        r"^\s*SELECT\s+(?P<select>.+?)\s+FROM\s+(?P<from>[A-Za-z0-9_]+)"
        r"(?:\s+WHERE\s+(?P<where>.+))?\s*;?\s*$",
        re.IGNORECASE
    )

    WHERE_REGEX = re.compile(
        r"^(?P<col>[A-Za-z0-9_]+)\s*"
        r"(?P<op>=|!=|>=|<=|>|<)\s*"
        r"(?P<val>.+)$",
        re.IGNORECASE
    )

    COUNT_REGEX = re.compile(
        r"^COUNT\s*\(\s*(?P<arg>\*|[A-Za-z0-9_]+)\s*\)$",
        re.IGNORECASE
    )

    def parse(self, sql: str) -> ParsedQuery:
        sql = sql.strip()
        if not sql:
            raise SqlSyntaxError("Empty SQL query.")

        match = self.SELECT_REGEX.match(sql)
        if not match:
            raise SqlSyntaxError("Invalid SQL format.")

        select_part = match.group("select").strip()
        from_table = match.group("from").strip()
        where_part = match.group("where")

        where_clause = self._parse_where(where_part) if where_part else None

        aggregate = None
        select_columns = None

        count_match = self.COUNT_REGEX.match(select_part)
        if count_match:
            aggregate = Aggregate(func="COUNT", arg=count_match.group("arg"))
        else:
            if select_part == "*":
                select_columns = ["*"]
            else:
                select_columns = [c.strip() for c in select_part.split(",")]

        return ParsedQuery(
            select_columns=select_columns,
            aggregate=aggregate,
            from_table=from_table,
            where_clause=where_clause
        )

    def _parse_where(self, where_str: str) -> WhereClause:
        match = self.WHERE_REGEX.match(where_str.strip())
        if not match:
            raise SqlSyntaxError("Invalid WHERE clause.")

        col = match.group("col")
        op = match.group("op")
        val = match.group("val").strip()

        # Remove trailing semicolon if it exists
        if val.endswith(";"):
            val = val[:-1].strip()

        # Remove quotes safely for both 'value' and "value"
        if (val.startswith("'") and val.endswith("'")) or \
           (val.startswith('"') and val.endswith('"')):
            val = val[1:-1].strip()

        # Try integer
        try:
            return WhereClause(column=col, operator=op, value=int(val))
        except:
            pass

        # Try float
        try:
            return WhereClause(column=col, operator=op, value=float(val))
        except:
            pass

        # Keep as lowercase string for safe comparison
        return WhereClause(column=col, operator=op, value=val.lower())
