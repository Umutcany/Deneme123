from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from datetime import datetime
from sqlalchemy import inspect

class TemelVeriModeli(DeclarativeBase):
    id:Mapped[int]=mapped_column(autoincrement=True,primary_key=True)
    olusturulma_tarihi:Mapped[datetime]=mapped_column(default=datetime.now())
    guncelleme_tarihi:Mapped[datetime]=mapped_column(default=datetime.now(),onupdate=datetime.now())

    def to_dict(self)->dict:
        sonuc={col.key:getattr(self,col.key) for col in inspect(self).mapper.column_attrs}
        return sonuc
