import json
import sqlite3
from pathlib import Path


def save_extra_info(gacha_type: str, info: dict) -> None:
    file_path = Path(f"extra_info_{gacha_type}.json")
    with file_path.open(mode="w", encoding="utf-8") as json_file:
        json.dump(info, json_file, indent=4)


def save_logs_to_db(gacha_type: str, signal_data: list) -> None:
    try:
        conn = sqlite3.connect(f"logs_{gacha_type}.db")
        cursor = conn.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS gacha_data (
            id TEXT PRIMARY KEY,
            uid TEXT,
            gacha_id TEXT,
            gacha_type TEXT,
            item_id TEXT,
            count INTEGER,
            time TEXT,
            name TEXT,
            lang TEXT,
            item_type TEXT,
            rank_type INTEGER,
            pity INTEGER
        )
        """)

        for entry in signal_data:
            cursor.execute(
                """
            SELECT time FROM gacha_data WHERE id = ?
            """,
                (entry["id"],),
            )

            existing_entry = cursor.fetchone()

            if existing_entry is None or entry["time"] > existing_entry[0]:
                cursor.execute(
                    """
                INSERT OR REPLACE INTO gacha_data (id, uid, gacha_id, gacha_type, item_id, count, time, name, lang, item_type, rank_type, pity)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,  # noqa: E501
                    (
                        entry["id"],
                        entry["uid"],
                        entry["gacha_id"],
                        entry["gacha_type"],
                        entry["item_id"],
                        int(entry["count"]),
                        entry["time"],
                        entry["name"],
                        entry["lang"],
                        entry["item_type"],
                        int(entry["rank_type"]),
                        int(entry["pity"]),
                    ),
                )
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    else:
        conn.commit()
    finally:
        conn.close()


def read_db(gacha_type: str) -> list[dict]:
    try:
        conn = sqlite3.connect(f"logs_{gacha_type}.db")
        cursor = conn.cursor()
        query = "SELECT * FROM gacha_data"
        cursor.execute(query)

        rows = cursor.fetchall()

        # Get the column names from the cursor description
        column_names = [description[0] for description in cursor.description]

        data = [dict(zip(column_names, row)) for row in rows]

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return None
    else:
        return data
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def read_extra_info(gacha_type: str) -> dict:
    file_path = Path(f"extra_info_{gacha_type}.json")
    if not file_path.exists():
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with file_path.open(encoding="utf-8") as json_file:
        return json.load(json_file)
