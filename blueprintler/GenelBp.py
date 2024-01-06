from flask import Blueprint
from sqlalchemy import select
from veri import db
from flask import request
from sqlalchemy import inspect
from flask import abort
from blueprintler.VeriSorgulama import sorgula
from sqlalchemy import func

def genel_bp(veri_sinifi:type, bp_adi:str='genel_bp'):
    bp=Blueprint(bp_adi,__name__)

    @bp.route('/',methods=['GET'])
    @bp.route('',methods=['GET'])
    @bp.route('/sayfa/<int:sayfa>',methods=["GET"])
    @bp.route('/sayfa/<int:sayfa>/<int:kayit_sayisi>',methods=["GET"])

    def index(sayfa:int=1,kayit_sayisi:int=10):
        sorgu=select(veri_sinifi)
        sayfa =max(0,sayfa)

        sorgu=sorgula(sorgu,veri_sinifi,sayfa -1,kayit_sayisi)

        cevap = db.session.scalars(sorgu).all()

        return [veri.to_dict() for veri in cevap]

    @bp.route("/sayfa_sayisi",methods=["GET"])
    @bp.route("/sayfa_sayisi/<int:kayit_sayisi>",methods=["GET"])
    def sayfa_sayisi(kayit_sayisi:int=10):
        sorgu=select(func.count('*')).select_from(veri_sinifi)
        sorgu=sorgula(sorgu, veri_sinifi, -1, kayit_sayisi)
        cevap=db.session.scalars(sorgu).all()
        kalan=cevap[0] % kayit_sayisi
        sayfa_sayisi=cevap[0] // kayit_sayisi
        if kalan>0:
            sayfa_sayisi +=1
        return {"sayfa_sayisi":sayfa_sayisi}
    
    @bp.route("/",methods=['POST'])
    @bp.route('',methods=['POST'])

    def ekle():
        veri=veri_sinifi()

        sutunlar=[col.key for col in inspect(veri_sinifi).mapper.column_attrs]

        for sutun in request.json:
            if sutun in sutunlar:
                setattr(veri,sutun,request.json[sutun])
            else:
                return abort(500)
            
            
        db.session.add(veri)
        db.session.commit()

        return veri.to_dict()
    
    @bp.route('/<int:id>',methods=["PUT"])
    def getir(id:int):
        sorgu=select(veri_sinifi).where(veri_sinifi.id==id)
        cevap=db.session.scalars(sorgu).one()

        return cevap.to_dict()
    
    @bp.route('/<int:id>',methods=["PUT","PATCH"])
    def duzenle(id:int):
        sorgu=select(veri_sinifi).where(veri_sinifi.id==id)
        veri=db.session.scalars(sorgu).one()

        sutunlar=[col.key for col in inspect(veri_sinifi).mapper.column_attrs]

        for sutun in request.json:
            if sutun in sutunlar:
                setattr(veri,sutun,request.json[sutun])
            else:
                return abort(500)

        db.session.commit()   

        return veri.to_dict()
    
    @bp.route("/<int:id>",methods=["DELETE"])
    def sil(id:int):
        sorgu=select(veri_sinifi).where(veri_sinifi.id==id)
        veri=db.session.scalars(sorgu).one()

        db.session.delete(veri)
        db.session.commit()

        return {'silinen':veri.to_dict()}

    
    return bp
    


    
