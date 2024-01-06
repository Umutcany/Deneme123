from flask_sqlalchemy import SQLAlchemy
from veri.modeller.TemelVeriModeli import TemelVeriModeli

db=SQLAlchemy(model_class=TemelVeriModeli)
