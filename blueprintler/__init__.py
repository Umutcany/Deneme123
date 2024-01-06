from flask import Blueprint

from blueprintler.GenelBp import genel_bp
from veri import SiteModel,UrunModeli,UrunSiparisModeli,UrunSatisModeli

v1_bp=Blueprint("v1_bp",__name__)


v1_bp.register_blueprint(genel_bp(SiteModel,"ticaret_bp"),url_prefix="/ticaret")
v1_bp.register_blueprint(genel_bp(UrunModeli,"urun_bp"),url_prefix="/urun")
v1_bp.register_blueprint(genel_bp(UrunSiparisModeli,"urun_siparis_bp"),url_prefix="/urun_alis")
v1_bp.register_blueprint(genel_bp(UrunSatisModeli,"urun_satis_bp"),url_prefix="/urun_satis")


api_bp=Blueprint("api_bp",__name__)
api_bp.register_blueprint(v1_bp,url_prefix="/v1")