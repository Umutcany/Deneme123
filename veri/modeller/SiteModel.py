from sqlalchemy.orm import Mapped, mapped_column
from veri.modeller.TemelVeriModeli import TemelVeriModeli

class SiteModel(TemelVeriModeli):
    __tablename__='ticaret'

    ticaret_telefon:Mapped[str]=mapped_column(nullable=True)
    ticaret_adi:Mapped[str]=mapped_column(nullable=False)
    ticaret_adres:Mapped[str]=mapped_column(nullable=True)
    ticaret_yetkiliKisi:Mapped[str]=mapped_column(nullable=True)

