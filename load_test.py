"""
This script sends many requests to the database in quick succession using multithreading.

Example usage:
    python load_test.py -n 50 -r -w
"""

import argparse
from collections import defaultdict
import concurrent.futures
import json
import random
import sqlite3
import string
import time
from typing import Iterator

RELEASE_YEAR_MIN: int = 1990
RELEASE_YEAR_MAX: int = 2024
GENRES: tuple[str, ...] = (
    "rpg",
    "fps",
    "puzzle",
    "racing",
    "sport",
    "simulation",
    "trivia",
    "educational",
)

parser = argparse.ArgumentParser()
parser.add_argument(
    "-n",
    "--n_requests",
    help="number of requests to make to the database",
    type=int,
    required=True,
)
parser.add_argument(
    "-w",
    "--write",
    help="make write requests to the database",
    action="store_true",  # if user doesn't provide this flag, give it the value False
)
parser.add_argument(
    "-r",
    "--read",
    help="make read requests to the database",
    action="store_true",  # if user doesn't provide this flag, give it the value False
)
args = parser.parse_args()

potential_actions: list[str] = []
if args.write:
    potential_actions.append("write")
if args.read:
    potential_actions.append("read")


def call_db(actions: list[str]) -> str:
    """Makea random read/write on the database"""
    chosen_action: str = random.choice(actions)
    print(chosen_action[0], end="")
    try:
        sql = sqlite3.connect("database.db")

        sql.execute("PRAGMA journal_mode = WAL;")
        sql.execute("PRAGMA synchronous = normal;")
        sql.execute("PRAGMA temp_store = memory;")
        sql.execute("PRAGMA mmap_size = 30000000000;")

        if chosen_action == "read":
            sql_cursor = sql.cursor()
            required_genres: list[str] = random.sample(
                GENRES, k=random.randint(1, len(GENRES))
            )
            sql_cursor.execute(
                f"""
    SELECT * FROM games 
    WHERE release_year {random.choice([">=","<="])} ? 
    AND name LIKE ? 
    AND genre IN ({", ".join(["?"]*len(required_genres))})
    """,
                #     """,
                (
                    random.randint(RELEASE_YEAR_MIN, RELEASE_YEAR_MAX),
                    random.choice(string.ascii_lowercase) + "%",
                    *required_genres,
                ),
            )
            for row in sql_cursor.fetchall():
                #print(row)
                pass
        elif chosen_action == "write":
            sql.execute(
                """
                INSERT INTO games (release_year, name, genre)
                VALUES (?, ?, ?)
                """,
                (
                    random.randint(RELEASE_YEAR_MIN, RELEASE_YEAR_MAX),
                    "".join([random.choice(string.ascii_lowercase) for _ in range(10)]),
                    random.choice(GENRES),
                ),
            )
        sql.commit()

        sql.close()
        return f"{chosen_action}_SUCCESS"
    except Exception as err:
        return f"{chosen_action}_{err}"


response_hist: dict[str, int] = defaultdict(int)

if __name__ == "__main__":
    start_time = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results: Iterator = executor.map(
            call_db, (potential_actions for _ in range(args.n_requests))
        )
    for result in results:
        response_hist[result] += 1
    print(json.dumps(response_hist, indent=4))
    end_time = time.perf_counter()
    print(f"time elapsed: {end_time-start_time:.2f} seconds")
