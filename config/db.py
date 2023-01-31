from sqlalchemy import create_engine, MetaData

engine = create_engine('mysql+pymysql://root@localhost:3306/fastapi_1')
meta = MetaData()
con = engine.connect()
"""
    konfigurace pro připojení k db
"""
