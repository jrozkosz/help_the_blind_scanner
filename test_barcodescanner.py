import barcodescanner as bs
from barcodescanner import Database, CodeScanner, SpeechSynthesizer, IdentifyProduct, AddProductByVoice, ScannerInterface
import pytest
import json
import cv2
import os

class TestDatabase:

    product = Database()

    def test_class_description_None(self, capsys):
        print(self.product)
        output = capsys.readouterr().out
        expected = "Ostatnio używany produkt z bazy to: None.\n"
        assert output == expected
    
    def test_class_description_used_name(self, capsys):
        self.product._name = "Kalafior brokułowy"
        print(self.product)
        output = capsys.readouterr().out
        expected = "Ostatnio używany produkt z bazy to: Kalafior brokułowy.\n"
        assert output == expected

    def test_get_product_name_empty_code(self):
        with pytest.raises(bs.ExEmptyBarcode):
            self.product.get_product_name(None)

    def test_get_product_name_wrong_code_type(self):
        with pytest.raises(bs.ExWrongBarcodeType):
            self.product.get_product_name("str_barcode")

    def test_get_existing_product_name(self):
        product_from_database = self.product.get_product_name(40084701)
        assert product_from_database == "Kinder Chocolate"
        assert self.product.name == "Kinder Chocolate"

    def test_get_nonexisting_product_name(self):
        product_not_from_database = self.product.get_product_name(101010101)
        assert product_not_from_database == "Produktu nie ma w bazie"


    def test_add_product_empty_name(self):
        with pytest.raises(bs.ExEmptyProductName):
            self.product.add_product(12345, None)
    
    def test_add_product_empty_name(self):
        with pytest.raises(bs.ExEmptyBarcode):
            self.product.add_product(None, "Name")

    def test_add_product_wrong_code_type(self):
        with pytest.raises(bs.ExWrongBarcodeType):
            self.product.add_product("str_barcode", "whatever")

    def test_add_product_not_from_database(self):
        with open("baza_produktow.json", "r", encoding="utf-8") as jsonfile:
            # zachowuję stan bazy przed dodaniem testowego produktu
            previous = json.load(jsonfile)

        added_code = 123456789
        added_name = "testowy produkt"

        self.product.add_product(added_code, added_name)
        i = 0
        with open("baza_produktow.json", "r", encoding="utf-8") as jsonfile:
            data = json.load(jsonfile)
            for item in data:
                if added_code == item['barcode'] and added_name == item['product']:
                    i += 1  # +1 jeśli wystąpił testowy produkt w bazie
        assert i != 0
        assert self.product.name == "testowy produkt"

        os.remove("baza_produktow.json")
        # teraz przywracam pierwotny stan bazy, sprzed testowania,
        # żeby nie mieć testowego produktu w bazie
        with open("baza_produktow.json", "w", encoding="utf-8") as jsonfile:
            json.dump(previous, jsonfile, indent = 4)


class TestCodeScanner:

    def test_class_description_None(self, capsys):
        scanner = CodeScanner()
        print(scanner)
        output = capsys.readouterr().out
        expected = "Ostatnio zeskanowany kod kreskowy to: None.\n"
        assert output == expected
    
    def test_class_description_scanned(self, capsys):
        scanner = CodeScanner()
        scanner._scanned_code = 10101010101
        print(scanner)
        output = capsys.readouterr().out
        expected = "Ostatnio zeskanowany kod kreskowy to: 10101010101.\n"
        assert output == expected
        
    def test_video_capture(self):
        cap = cv2.VideoCapture(0)
        assert cap.isOpened()

    def test_erase_scanned_code(self):
        scanning = CodeScanner()
        scanning._scanned_code = 123456789
        scanning.erase_scanned_code()
        assert scanning.scanned_code == None


class TestSpeechSynthesizer():
    
    def test_empty_text(self):
        speak = SpeechSynthesizer()
        with pytest.raises(bs.ExEmptyText):
            speak.say_the_name(None)


class TestIdentifyProduct():
    
    def test_wrong_object_type(self):
        with pytest.raises(bs.WrongTypeOfObject):
            identify = IdentifyProduct("whatever")


class TestAddProductByVoice():
    
    def test_wrong_object_type(self):
        with pytest.raises(bs.WrongTypeOfObject):
            identify = AddProductByVoice(999999999)


class TestScannerInterface():

    def test_wrong_object_type(self):
        with pytest.raises(bs.ExNotTkinterObject):
            interface = ScannerInterface("byle co")