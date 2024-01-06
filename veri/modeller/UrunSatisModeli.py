from veri.modeller.TemelVeriModeli import TemelVeriModeli
from datetime import date,datetime
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy import ForeignKey

class UrunSatisModeli(TemelVeriModeli):
    __tablename__="urun_siparis"

    urun_tarih:Mapped[date]=mapped_column(default=datetime.now().date())
    urun_firma:Mapped[str]=mapped_column(nullable=False)
    urun_musteri:Mapped[str]=mapped_column(nullable=False)
    urun_id:Mapped[int]=mapped_column(ForeignKey('urunler.id'))

