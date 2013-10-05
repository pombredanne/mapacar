#!/usr/bin/env python

import os
import sys
import time
import datetime
import lxml.etree as et

import ptree
import requests

UA = "mapalau v0.0.1: http://github.com/edsu/mapacar"


request_xml = """<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/" xmlns:s="http://www.w3.org/2001/XMLSchema" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <SOAP-ENV:Body>
    <tns:BuscarInformacoesMapa xmlns:tns="http://tempuri.org/">
      <tns:busca></tns:busca>
      <tns:maior>%i</tns:maior>
      <tns:menor>%i</tns:menor>
    </tns:BuscarInformacoesMapa>
  </SOAP-ENV:Body>
</SOAP-ENV:Envelope>
"""

def get_items():
    url = "http://monitoramento.sema.mt.gov.br/simlamws/IntegracaoMapaLau.asmx"
    url = "http://monitoramento.sema.mt.gov.br/simlamws/IntegracaoMapaProjetoDigital.asmx"
    count = 0
    num_results = 100
    while True:
        response = requests.post(url, 
            headers={
                "Content-Type": "text/xml; charset=utf-8",
                "User-Agent": UA
            }, 
            data=request_xml % (count + num_results, count + 1)
        )
        doc = et.fromstring(response.content)
        found = False
        for i in doc.findall('.//{http://tempuri.org/}InformacoesMapaProjetoDigital'):
            found = True
            yield i
        if found != True:
            break
        count += num_results

def download():
    count = 0
    for item in get_items():
        count += 1

        id = item.find('./{http://tempuri.org/}MapaDigital').text
        if not id or id == "0":
            continue

        # write out metadata
        data_dir = 'data' + ptree.id2ptree(id)
        if not os.path.isdir(data_dir):
            os.makedirs(data_dir)
        et.cleanup_namespaces(item)
        xml = et.tostring(item, pretty_print=True)

	# no need to refetch
        metadata_file = os.path.join(data_dir, "%s.xml" % id)
        if os.path.isfile(metadata_file):
            continue
        open(metadata_file, "w").write(xml)

        # be nice :)
        time.sleep(1)

        # try to download shapefile
        zip_url = item.find('./{http://tempuri.org/}UrlZip').text
        if zip_url:
            r = requests.get(zip_url, headers={"User-Agent": UA})
            if r.headers['Content-Type'] == 'application/x-zip-compressed':
                zip_file = metadata_file.replace(".xml", ".zip")
                open(zip_file, "wb").write(r.content)
        	print "%s %s %s %s" % (datetime.datetime.now(), count, id, zip_file)

if __name__ == "__main__":
    download()
