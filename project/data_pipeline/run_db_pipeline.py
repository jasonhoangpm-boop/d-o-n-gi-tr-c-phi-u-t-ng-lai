from __future__ import annotations

import argparse
import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import text

from project.data_pipeline.fetch_data import fetch_vnindex_data
from project.data_pipeline.store_data import store_vnindex_data
from project.database.db_config import get_db_engine
from project.utils.logger import get_logger


logger = get_logger(__name__)


def create_table_if_needed() -> None:
    sql_path = Path(__file__).resolve().parents[1] / "database" / "create_table.sql"
    create_table_sql = sql_path.read_text(encoding="utf-8")

    engine = get_db_engine()
    with engine.begin() as conn:
        conn.execute(text(create_table_sql))


def count_rows() -> int:
    engine = get_db_engine()
    with engine.begin() as conn:
        result = conn.execute(text("SELECT COUNT(*) FROM vnindex_prices"))
        total = result.scalar_one()
    return int(total)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run VNINDEX data pipeline and store input data in PostgreSQL")
    parser.add_argument("--db-user", dest="db_user")
    parser.add_argument("--db-password", dest="db_password")
    parser.add_argument("--db-name", dest="db_name")
    parser.add_argument("--db-host", dest="db_host")
    parser.add_argument("--db-port", dest="db_port")
    return parser.parse_args()


def apply_db_env_from_args(args: argparse.Namespace) -> None:
    if args.db_user:
        os.environ["POSTGRES_USER"] = args.db_user
    if args.db_password:
        os.environ["POSTGRES_PASSWORD"] = args.db_password
    if args.db_name:
        os.environ["POSTGRES_DB"] = args.db_name
    if args.db_host:
        os.environ["POSTGRES_HOST"] = args.db_host
    if args.db_port:
        os.environ["POSTGRES_PORT"] = args.db_port


def run() -> None:
    args = parse_args()

    # Load optional .env from workspace root if present.
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    apply_db_env_from_args(args)

    create_table_if_needed()
    raw_df = fetch_vnindex_data()
    
    store_vnindex_data(raw_df)
    total_rows = count_rows()

    logger.info("Database pipeline completed successfully. Total rows in vnindex_prices: %s", total_rows)


if __name__ == "__main__":
    run()