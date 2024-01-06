from flask import Flask
from flask_migrate import Migrate
from veri import *
from sqlalchemy import select
from flask import request
from flask import Blueprint
from sqlalchemy import Select
from veri import SiteModel

ticaret_bp=Blueprint('ticaret_bp',__name__)

@ticaret_bp.route('',methods=['GET'])
@ticaret_bp.route('/',methods=['GET'])

def index():
    sorgu=select(SiteModel)

    cevap=db.session.scalars(sorgu).all()
    
    return [ticaret.to_dict() for ticaret in cevap]


@ticaret_bp.route("/",methods=["POST"])
@ticaret_bp.route('',methods=["POST"])
def ekle():
    ticaret=SiteModel()

    ticaret.adi=request.json['adi']
    ticaret.adres=request.json['adres']
    ticaret.telefon=request.json['telefon']

    db.session.add(ticaret)
    db.session.commit()

    return ticaret.to_dict()

@ticaret_bp.route('/<int:id>',methods=["GET"])
def getir(id:int):
    sorgu=select(SiteModel).where(SiteModel.id==id)
    cevap=db.session.scalars(sorgu).one()

    return cevap.to_dict()


@ticaret_bp.route('/<int:id>',methods=["PUT","PATCH"])
def duzenle(id:int):
    sorgu=select(SiteModel).where(SiteModel.id==id)
    ticaret=db.session.scalars(sorgu).one()

    ticaret.adi=request.json["adi"]
    ticaret.adres=request.json["adres"]
    ticaret.telefon=request.json["telefon"]

    db.session.commit()

    return ticaret.to_dict()

@ticaret_bp.route("/<int:id>",methods=["DELETE"])
def sil(id:int):
    sorgu=select(SiteModel).where(SiteModel.id==id)
    ticaret=db.session.scalars(sorgu).one()

    db.session.delete(ticaret)
    db.session.commit()

    return {'silinen':ticaret.to_dict()}
