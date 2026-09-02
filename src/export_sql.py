import os
import urllib.parse
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, inspect
import pyarrow as pa
import pyarrow.parquet as pq

# 1. 환경변수 로드
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
TARGET_TABLES_ENV = os.getenv("TARGET_TABLES", "").strip()

encoded_password = urllib.parse.quote_plus(DB_PASSWORD)
db_url = f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(db_url)

# 결과 저장 폴더 생성
OUTPUT_DIR = "output_parquet"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 2. 대상 테이블 목록 결정
inspector = inspect(engine)
all_tables = inspector.get_table_names()

if TARGET_TABLES_ENV:
    # .env에 지정된 테이블만 필터링
    target_tables = [t.strip() for t in TARGET_TABLES_ENV.split(",") if t.strip() in all_tables]
else:
    # 비어있으면 DB 내 전체 테이블 대상
    target_tables = all_tables

print(f"총 {len(target_tables)}개 테이블 추출 시작: {target_tables}\n")

# 3. 테이블별 순회 추출
CHUNK_SIZE = 100000

for table_name in target_tables:
    output_file = os.path.join(OUTPUT_DIR, f"{table_name}.parquet")
    print(f"▶ [{table_name}] 추출 시작...")

    query = f"SELECT * FROM `{table_name}`"
    writer = None
    total_rows = 0

    try:
        for chunk in pd.read_sql(query, engine, chunksize=CHUNK_SIZE):
            table = pa.Table.from_pandas(chunk)
            if writer is None:
                writer = pq.ParquetWriter(output_file, table.schema, compression="snappy")
            writer.write_table(table)
            total_rows += len(chunk)

        # 데이터가 0건인 빈 테이블 대응
        if writer is None:
            empty_df = pd.read_sql(f"SELECT * FROM `{table_name}` LIMIT 0", engine)
            table = pa.Table.from_pandas(empty_df)
            pq.write_table(table, output_file, compression="snappy")

        print(f"✔ [{table_name}] 완료 -> {output_file} (총 {total_rows:,} 행)")

    except Exception as e:
        print(f"✖ [{table_name}] 추출 실패: {e}")

    finally:
        if writer:
            writer.close()

print(f"\n모든 테이블 추출 작업이 완료되었습니다. 저장 위치: ./{OUTPUT_DIR}/")