CREATE TABLE IF NOT EXISTS vnindex_prices (
    date TIMESTAMP NOT NULL,
    open DOUBLE PRECISION,
    high DOUBLE PRECISION,
    low DOUBLE PRECISION,
    close DOUBLE PRECISION,
    volume BIGINT,
    interval VARCHAR(10) NOT NULL
);

-- 🔥 bỏ primary key cũ nếu có
ALTER TABLE vnindex_prices
DROP CONSTRAINT IF EXISTS vnindex_prices_pkey;

-- 🔥 tạo primary key đúng chuẩn time-series
ALTER TABLE vnindex_prices
ADD CONSTRAINT vnindex_prices_pkey
PRIMARY KEY (date, interval);