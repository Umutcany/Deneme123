from veri.modeller.TemelVeriModeli import TemelVeriModeli
from datetime import date,datetime
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import ForeignKey

class UrunYorumModeli(TemelVeriModeli):
    __tablename__="urun_yorum"

    urun_siparis:Mapped[str]=mapped_column(nullable=False)
    urun_bilgi:Mapped[str]=mapped_column(nullable=False)
    urun_yorum:Mapped[str]=mapped_column(nullable=True)
    urun_puan:Mapped[int]=mapped_column(nullable=False)
