from veri.modeller.TemelVeriModeli import TemelVeriModeli
from sqlalchemy.orm import mapped_column, Mapped

class UrunKategori(TemelVeriModeli):
    __tablename__="urun_kategori"

    urun_kategori:Mapped[str]=mapped_column(nullable=True)


