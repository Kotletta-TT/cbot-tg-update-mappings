from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session, declarative_base
from nums_mapping import BEELINE, ROSTELECOM

from models import Mapping

engine = create_engine('sqlite:///mappings.db')

Base = declarative_base()

test1 = Mapping(iccid='1234567890123456788', phone='79999999998', provider="BEELINE")
test2 = Mapping(iccid='89701205569000706191', phone='71112222111', provider="ROSTELECOM")

new_mappings = [test1, test2]

class MappingDB(Base):
    __tablename__ = "mappings"
    id = Column(Integer, primary_key=True)
    iccid = Column(String(20))
    phone = Column(String(11))
    provider = Column(String(30))


Base.metadata.create_all(engine)


with Session(engine) as session:

    for i in new_mappings:
        results = session.query(MappingDB).filter_by(iccid=i.iccid).one()
        if not results:
            results = MappingDB(**i.dict())
            session.add(results)
        else:
            results.phone = i.phone
        session.commit()
    # for i, k in BEELINE.items():
    #     session.add(MappingDB(iccid=i, phone=k, provider="BEELINE"))
    # for i, k in ROSTELECOM.items():
    #     session.add(MappingDB(iccid=i, phone=k, provider="ROSTELECOM"))
