from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import Session, declarative_base
from typing import List

from models import Mapping

engine = create_engine('sqlite:///mappings.db')

Base = declarative_base()


class MappingDB(Base):
    __tablename__ = "mappings"
    id = Column(Integer, primary_key=True)
    iccid = Column(String(20))
    phone = Column(String(11))
    provider = Column(String(30))


Base.metadata.create_all(engine)


def upd_db(new_mappings: List[Mapping]):
    with Session(engine) as session:
        for i in new_mappings:
            results = session.query(MappingDB).filter(
                MappingDB.iccid.like(f'{i.iccid}%')).first()
            if not results:
                results = MappingDB(**i.dict())
                session.add(results)
                print(f"New mapping added\niccid: {i.iccid}\nphone: {i.phone}")
            else:
                if results.phone == i.phone:
                    continue
                else:
                    print(
                        f"Update mapping\niccid: {i.iccid}\nnew phone: "
                        f"{i.phone}\nold phone: {results.phone}")
                    results.phone = i.phone
            session.commit()