from sqlalchemy import Select
from sqlalchemy import inspect
from flask import request
from datetime import date
from os import abort
from sqlalchemy import func
from datetime import datetime

def sorgula(sorgu: Select, veri_sinifi: type, sayfa_no: int = 0, kayit_sayisi: int = 10):
    # Sorgulama Dilini Çalıştıracak Fonsksiyon

    # 1-Sayfalama ve Kayıt Sayısı
    # Bu bilgiler parametrik olarak gelecek ve url içinde http://xyz.com/api/v1/ticaret/<sayfa_no>/<kayit_sayisi>
    # şeklinde yer alacaktır.

    if sayfa_no>=0:
        sorgu = sorgu.limit(kayit_sayisi)
        sorgu = sorgu.offset(sayfa_no * kayit_sayisi)


    # 2-Sıralama
    # Sıralama query string ile yapılır
    # http://xyz.com/api/v1/ticaret?sirala=ar_<alanadi1>&sirala=az_<alanadi2>
    # Eğer alan adı ar_ ile başlarsa artan az_ile başlarsan azalan sıralama demektir.

    siralama_alanlari = request.args.getlist("sirala")
    sutunlar = [col.key for col in inspect(veri_sinifi).mapper.column_attrs]
    for alan_adi in siralama_alanlari:
        if alan_adi.startswith('ar_'):
            gercek_alan_adi = alan_adi[3:]
            sorgu = sorgu.order_by(getattr(veri_sinifi, gercek_alan_adi).asc())
        elif alan_adi.startswith('az_'):
            gercek_alan_adi = alan_adi[3:]
            sorgu = sorgu.order_by(getattr(veri_sinifi, gercek_alan_adi).desc())



    #FİLTRELEME
    #1- Filtre Listesini elde edelim
    filtre= request.args.getlist('f')
    if len(filtre)>0:
         #2-her filtreyi Alan, Operatör ve Değer olarak üçe ayıralım.
        operator_karakterleri=list('<>=~!|')
        ayrilmis_filtreler=[]

        for filtre_metni in filtre:
            alan_adi = []
            operator= []
            deger = []

            adim= 0
            for karakter in filtre_metni:
                if adim == 0 and karakter not in operator_karakterleri:
                    alan_adi.append(karakter)
                elif adim == 0 and karakter in operator_karakterleri:
                    adim = 1
                    operator.append(karakter)
                elif adim == 1 and karakter in operator_karakterleri:
                    operator.append(karakter)
                elif adim == 1 and karakter not in operator_karakterleri:
                    adim = 2
                    deger.append(karakter)
                else:
                    deger.append(karakter)

            alan_adi_str=''.join(alan_adi)
            operator_str=''.join(operator)
            deger_str=''.join(deger)

            ayrilmis_filtreler.append((alan_adi_str,operator_str,deger_str))

        #filtreyi çalıştırmak
        tablo_alanlari=inspect(veri_sinifi).mapper.column_attrs

        for alan, op, deger in ayrilmis_filtreler:
            #1-alanın veri türünü bulalım.
            tablo_alani=tablo_alanlari[alan]
            if tablo_alani.class_attribute.type.python_type in [int]:
                #Tamsayı filtrelemesi
                kabul_edilen_operatorler=['>','>=','<','<=','=','~']
                if op not in kabul_edilen_operatorler:
                    abort(500)
                else:
                    if op == '~':
                        degerler=[float(d) for d in deger.split(',')]
                        sorgu=sorgu.where(tablo_alani.between(degerler[0],degerler[1]))
                    else:
                        if op == '>':
                            sorgu=sorgu.where(tablo_alani>float(deger))
                        elif op == '<':
                            sorgu=sorgu.where(tablo_alani<float(deger))
                        elif op == '>=':
                            sorgu=sorgu.where(tablo_alani>=float(deger))
                        elif op == '<=':
                            sorgu=sorgu.where(tablo_alani<=float(deger))
                        elif op == '=':
                            sorgu=sorgu.where(tablo_alani==float(deger))
            elif tablo_alani.class_attribute.type.python_type in [str]:
                #Metin Filtrelenmesi
                kabul_edilen_operatorler=['|=','=|','|=|','!=','=!','!=!']
                if op not in kabul_edilen_operatorler:
                    abort(500)
                else:
                    if op == '|=':
                        sorgu = sorgu.where(func.lower(tablo_alani).like(f"{deger.lower()}%"))
                    elif op == '=|':
                        sorgu = sorgu.where(func.lower(tablo_alani).like(f"%{deger.lower()}"))
                    elif op == '|=|':
                        sorgu = sorgu.where(func.lower(tablo_alani).like(f"%{deger.lower()}%"))
                    elif op == '!=':
                        sorgu = sorgu.where(~func.lower(tablo_alani).like(f"{deger.lower()}%"))
                    elif op == '=!':
                        sorgu = sorgu.where(~func.lower(tablo_alani).like(f"%{deger.lower()}"))
                
            elif tablo_alani.class_attribute.type.python_type in [date]:
                # Tarih Filtrelenmesi
                kabul_edilen_operatorler = ['>', '<', '=', '~']
                if op not in kabul_edilen_operatorler:
                    abort(500)
                else:
                    if op == '~':
                        degerler = [datetime.strptime(d, "%Y-%m-%d") for d in deger.split(',')]
                        sorgu = sorgu.where(tablo_alani.between(func.date(degerler[0]), func.date(degerler[1])))
                    else:
                            # Tek bir tarih
                            deger = datetime.strptime(deger, "%Y-%m-%d")
                            if op == '>':
                                sorgu = sorgu.where(tablo_alani > func.date(deger))
                            elif op == '<':
                                sorgu = sorgu.where(tablo_alani < func.date(deger))
                            elif op == '=':
                                sorgu = sorgu.where(tablo_alani == func.date(deger))

    return sorgu