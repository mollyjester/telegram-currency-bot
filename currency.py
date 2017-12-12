# -*- coding: utf-8 -*-
"""CBR http://www.cbr.ru/scripts/XML_daily.asp wrapper"""
import xml.etree.ElementTree as ElementTree

url_currency = 'http://www.cbr.ru/scripts/XML_daily.asp'


class CurrencyKeys(object):
    """XML nodes names"""
    Date = 'Date'
    Valute = 'Valute'
    ID = 'ID'
    NumCode = 'NumCode'
    CharCode = 'CharCode'
    Nominal = 'Nominal'
    Name = 'Name'
    Rate = 'Value'


class CurrencyItem(object):
    def __init__(self, id):
        self.id = id
        self._numcode = ''
        self._charcode = ''
        self._nominal = 0
        self._name = ''
        self._rate = 0

    @property
    def numcode(self):
        return self._numcode

    @numcode.setter
    def numcode(self, value):
        self._numcode = value

    @property
    def charcode(self):
        return self._charcode

    @charcode.setter
    def charcode(self, value):
        self._charcode = value

    @property
    def nominal(self):
        return self._nominal

    @nominal.setter
    def nominal(self, value):
        self._nominal = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, value):
        self._rate = value

    def __str__(self):
        return ' '.join([
            self.id,
            self.numcode,
            self.charcode,
            str(self.nominal),
            self.name,
            str(self.rate)
            ])


class CurrencyParser(object):
    def __init__(self, xmldata):
        self.xmldata = xmldata

    def parse(self):
        currency_items = []
        et = ElementTree.fromstring(self.xmldata)
        currency_items.append(et.attrib[CurrencyKeys.Date])

        for currency in et:
            if currency.tag == CurrencyKeys.Valute:
                ci = CurrencyItem(currency.attrib[CurrencyKeys.ID])
                for prop in currency:
                    if prop.tag == CurrencyKeys.NumCode:
                        ci.numcode = prop.text
                    elif prop.tag == CurrencyKeys.CharCode:
                        ci.charcode = prop.text
                    elif prop.tag == CurrencyKeys.Nominal:
                        ci.nominal = int(prop.text)
                    elif prop.tag == CurrencyKeys.Name:
                        ci.name = prop.text
                    elif prop.tag == CurrencyKeys.Rate:
                        ci.rate = float(prop.text.replace(',', '.'))
                currency_items.append(ci)
        return currency_items


if __name__ == '__main__':
    import urllib.request as request
    response = request.urlopen(url_currency, timeout=10)
    cp = CurrencyParser(response.read())
    for i in cp.parse():
        print(i)
