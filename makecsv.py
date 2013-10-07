#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import unicodecsv

from lxml import etree

output = unicodecsv.writer(open("data.csv", "wb"), encoding="utf-8")
output.writerow(["ProcessoNumero", "Interessado", "Nome/Razao", "Municipio", "Area APRT", "Perimetro APRT", "Shape"])

for dirpath, dirnames, filenames in os.walk("data"):
    for f in filenames:
        if not f.endswith(".xml"):
            continue

        metadata_xml = os.path.join(dirpath, f)
        item = etree.parse(metadata_xml)
        row = []
        row.append(item.find('./{http://tempuri.org/}ProcessoNumero').text)
        row.append(item.find('./{http://tempuri.org/}ProcessoInteressado').text)
        row.append(item.find('./{http://tempuri.org/}NomeRazao').text)
        row.append(item.find('./{http://tempuri.org/}Municipio').text)
        row.append(item.find('./{http://tempuri.org/}AreaAPRT').text)
        row.append(item.find('./{http://tempuri.org/}PerimetroAPRT').text)

        shape = metadata_xml.replace(".xml", ".zip")
        if os.path.isfile(shape):
            row.append(shape)
        else:
            row.append(None)

        output.writerow(row)

