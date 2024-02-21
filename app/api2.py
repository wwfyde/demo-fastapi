from datetime import datetime

from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, String, JSON, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base, Session

app = FastAPI()

db_dns = "mysql+mysqlconnector://wufangyuan:wufangyuan@172.16.0.130:3306/moway_look"

engine = create_engine(db_dns)
SessionLocal = sessionmaker(autoflush=True, bind=engine)
Base = declarative_base()


class ModelWork(Base):
    __tablename__ = 'model_work'
    __table_args__ = {
        'comment': '模特作品'
    }
    id = Column(String(32), primary_key=True, index=True)
    model_id = Column(String(32), index=True, nullable=False, comment="模特ID")
    media = Column(JSON, comment="作品文件")
    tags = Column(JSON, comment="作品标签")
    content = Column(String(510), comment="作品内容")
    post = Column(Boolean, default=False, comment="是否发布")
    create_at = Column(DateTime, default=datetime.now, nullable=False, comment="创建时间")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get('/items')
def read_items(db: Session = Depends(get_db)):
    return db.query(ModelWork).all()


@app.post('/item')
def create_item(db: Session = Depends(get_db)):
    model_work = ModelWork(
        id=15,
        model_id='1',
        content='hello, 世界',
        media=["https://https://molook.oss-cn-beijing.aliyuncs.com/models/1.6165607c.png",
               "https://molook.oss-cn-beijing.aliyuncs.com/models/1.6165607c.png"],
        tags=['a', 'b']
    )
    db.add(model_work)
    db.commit()
    db.refresh(model_work)
    return model_work
