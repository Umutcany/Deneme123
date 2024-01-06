from veri.modeller.TemelVeriModeli import TemelVeriModeli
from sqlalchemy.orm import mapped_column, Mapped

class UrunMusteri(TemelVeriModeli):
    __tablename__="urun_musteri"

    urun_kisiselbilgiler:Mapped[str]=mapped_column(nullable=False)


