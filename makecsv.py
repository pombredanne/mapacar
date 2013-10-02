#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
generate a csv similar to the table that is available at 
http://monitoramento.sema.mt.gov.br/navegador_mapa_lau/MapaLau.html
"""

import os
import unicodecsv

from lxml import etree

output = unicodecsv.writer(open("data.csv", "wb"), encoding="utf-8")
output.writerow([u"Propriedade", u"Municipio", u"Lau Emitido", u"Car Emitido",
u"Proprietários", "uProcessos", u"CodAprt", u"Shape"])

for dirpath, dirnames, filenames in os.walk("data"):
    for f in filenames:
        if not f.endswith(".xml"):
            continue

        metadata_xml = os.path.join(dirpath, f)
        item = etree.parse(metadata_xml)
        row = []
        row.append(item.find('./{http://tempuri.org/}Id').text)
        row.append(item.find('./{http://tempuri.org/}Propriedade').text)
        row.append(item.find('./{http://tempuri.org/}Municipio').text)
        row.append(item.find('./{http://tempuri.org/}Lau').text)
        row.append(item.find('./{http://tempuri.org/}Car').text)
        row.append(item.find('./{http://tempuri.org/}Proprietarios').text)
        row.append(item.find('./{http://tempuri.org/}Processos').text)
        row.append(item.find('./{http://tempuri.org/}CodAprt').text)

        shape = metadata_xml.replace(".xml", ".zip")
        if os.path.isfile(shape):
            row.append(shape)
        else:
            row.append(None)

        output.writerow(row)

