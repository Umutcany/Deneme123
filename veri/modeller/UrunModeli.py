from veri.modeller.TemelVeriModeli import TemelVeriModeli
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import List

class UrunModeli(TemelVeriModeli):
    __tablename__="urunler"

    urun_kodu:Mapped[str]=mapped_column(nullable=False,unique=True)
    urun_adi:Mapped[str]=mapped_column(nullable=False)
    urun_resim:Mapped[str]=mapped_column(nullable=True)
    urun_fiyat:Mapped[float]=mapped_column(nullable=False)
    urun_aciklama:Mapped[str]=mapped_column(nullable=False)

