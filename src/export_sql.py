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
    target_tables = [t.strip() for t in TARGET_TABLES_ENV.split(",") if t.strip() in all_tables]
else:
    target_tables = all_tables

print(f"총 {len(target_tables)}개 테이블 추출 시작: {target_tables}\n")

# 3. 테이블별 순회 추출
CHUNK_SIZE = 100000

for table_name in target_tables:
    output_file = os.path.join(OUTPUT_DIR, f"{table_name}.parquet")
    print(f"▶ [{table_name}] 추출 시작...")

    query = f"SELECT * FROM `{table_name}`"
    writer = None
    fixed_schema = None
    total_rows = 0

    try:
        # dtype_backend="pyarrow"를 적용하여 NULL 포함 정수 컬럼 등이 멋대로 float으로 바뀌는 현상 방지
        for chunk in pd.read_sql(query, engine, chunksize=CHUNK_SIZE, dtype_backend="pyarrow"):
            # index 컬럼 메타데이터 제외 (스키마 불일치 방지)
            table = pa.Table.from_pandas(chunk, preserve_index=False)
            
            # 첫 번째 청크에서 생성한 스키마를 고정
            if writer is None:
                fixed_schema = table.schema
                writer = pq.ParquetWriter(output_file, fixed_schema, compression="snappy")
            else:
                # 2번째 청크부터 타입 차이가 있더라도 초기 스키마로 강제 형변환(Cast)
                table = table.cast(fixed_schema)

            writer.write_table(table)
            total_rows += len(chunk)

        # 데이터가 0건인 빈 테이블 대응
        if writer is None:
            empty_df = pd.read_sql(f"SELECT * FROM `{table_name}` LIMIT 0", engine, dtype_backend="pyarrow")
            table = pa.Table.from_pandas(empty_df, preserve_index=False)
            pq.write_table(table, output_file, compression="snappy")

        print(f"✔ [{table_name}] 완료 -> {output_file} (총 {total_rows:,} 행)")

    except Exception as e:
        print(f"✖ [{table_name}] 추출 실패: {e}")
        # 실패 시 깨진 불완전 파일 정리
        if os.path.exists(output_file):
            try:
                os.remove(output_file)
            except OSError:
                pass

    finally:
        if writer:
            writer.close()

print(f"\n모든 테이블 추출 작업이 완료되었습니다. 저장 위치: ./{OUTPUT_DIR}/")