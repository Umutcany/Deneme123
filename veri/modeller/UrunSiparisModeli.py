from veri.modeller.TemelVeriModeli import TemelVeriModeli
from sqlalchemy.orm import mapped_column, Mapped

class UrunSiparisModeli(TemelVeriModeli):
    __tablename__="urun_siparismodeli"

    urun_siparis:Mapped[str]=mapped_column(nullable=False)
    urun_bilgi:Mapped[str]=mapped_column(nullable=False)
    urun_adet:Mapped[int]=mapped_column(nullable=False)
    urun_fiyat:Mapped[int]=mapped_column(nullable=False)


    @property 
    def toplam_fiyat(self) -> float:
        return self.urun_adet * self.urun_fiyat

