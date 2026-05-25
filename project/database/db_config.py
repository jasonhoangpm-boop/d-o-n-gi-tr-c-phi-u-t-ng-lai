import os

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def get_db_engine() -> Engine:
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    db_name = os.getenv("POSTGRES_DB")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")

    if not user or not password or not db_name:
        raise RuntimeError(
            "Missing required DB environment variables: POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB"
        )

    db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}"
    return create_engine(db_url, pool_pre_ping=True)


def create_stock_table(symbol: str) -> None:
    """🔥 Tự động tạo bảng {symbol}_prices nếu chưa tồn tại"""
    from sqlalchemy import text
    from project.utils.logger import get_logger
    
    logger = get_logger(__name__)
    table_name = f"{symbol.lower()}_prices"
    engine = get_db_engine()
    
    create_table_sql = text(f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            date TIMESTAMP NOT NULL,
            open DOUBLE PRECISION,
            high DOUBLE PRECISION,
            low DOUBLE PRECISION,
            close DOUBLE PRECISION,
            volume BIGINT,
            interval VARCHAR(10) NOT NULL
        );
    """)
    
    create_pk_sql = text(f"""
        ALTER TABLE {table_name}
        DROP CONSTRAINT IF EXISTS {table_name}_pkey;
        
        ALTER TABLE {table_name}
        ADD CONSTRAINT {table_name}_pkey
        PRIMARY KEY (date, interval);
    """)
    
    try:
        with engine.begin() as conn:
            conn.execute(create_table_sql)
            conn.execute(create_pk_sql)
        logger.info(f"✅ Table '{table_name}' created/verified successfully.")
    except Exception as exc:
        logger.error(f"Failed to create table '{table_name}': {exc}")
        raise RuntimeError(f"Table creation failed for {symbol}: {exc}") from exc
