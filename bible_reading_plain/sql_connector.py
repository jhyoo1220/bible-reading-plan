import sqlite3
from reading import Reading


class SQLConnector(object):
    QUERY = """
        SELECT * FROM {book}
        WHERE chapter IN ({chapters})
        ORDER BY chapter ASC, verse ASC, verseIdx ASC
    """

    def __init__(self, db_file: str):
        self._conn = sqlite3.connect(db_file)
        self._cursor = self._conn.cursor()

    def _parse_row(self, row: object) -> dict:
        try:
            return {
                "chapter": int(row[1]),
                "verse": int(row[2]),
                "divided_verse": int(row[3]),
                "type": int(row[4]),
                "text": row[5],
            }

        except KeyError:
            return None

    def read_text_list(self, reading: Reading) -> list:
        db_params = reading.get_db_params()
        formatted_query = self.QUERY.format(**db_params)
        self._cursor.execute(formatted_query)

        results = []
        for row in self._cursor:
            curr_result = self._parse_row(row)

            if reading.is_target(curr_result["chapter"], curr_result["verse"]):
                results.append(curr_result)

        return results

    def close_connection(self):
        self._conn.close()
