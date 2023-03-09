from pyzbar import pyzbar
import time
import cv2

import os
import speech_recognition as sr
import playsound
from gtts import gTTS
import json

import tkinter as tk
from tkinter.constants import INSERT


class WrongTypeOfObject(Exception):
    def __init__(self):
        super().__init__("Obiekt powinien być instancją klasy CodeScanner")

class ExWrongBarcodeType(Exception):
    def __init__(self, barcode):
        self.barcode = type(barcode)
        super().__init__(f"Kod kreskowy powinien mieć typ integer a ma {self.barcode}")

class ExEmptyBarcode(Exception):
    def __init__(self):
        super().__init__("Kod kreskowy nie może być pusty")

class ExEmptyProductName(Exception):
    def __init__(self):
        super().__init__("Nadawana produktowi nazwa nie może być pusta")

class ExEmptyText(Exception):
    def __init__(self):
        super().__init__("Tekst przeznaczony do odczytania nie może być pusty")

class ExNotTkinterObject(Exception):
    def __init__(self):
        super().__init__('''Obiekt tworzenia klasy ScannerInterface musi 
                        być obiektem klasy tkinter.Tk''')


class CodeScanner():

    """
    Klasa służy do skanowania i odszyfrowania kodów kreskowych 
    z wykorzystaniem kamerki laptopa.

    Args:
        scanned_code (int): zeskanowany kod kreskowy podczas skanowania
    """

    def __init__(self):
        self._scanned_code = None

    @property
    def scanned_code(self):
        return self._scanned_code

    def __str__(self):
        text = f"Ostatnio zeskanowany kod kreskowy to: {self._scanned_code}."
        return text
    
    def scan_barcode(self):
        print("[INFO] włączanie kamerki...")
        vc = cv2.VideoCapture(0)
        time.sleep(1.0)

        while True:
            ret, frame = vc.read()
            if not ret:
                print("Brak dostępu do kamerki. Wychodzenie...")
                break
            width = vc.get(3)
            height = vc.get(4)
            frame = cv2.resize(frame, (int(width*1.5), int(height*1.5)))
            barcodes = pyzbar.decode(frame)
            if barcodes:
                for barcode in barcodes:
                    (x, y, w, h) = barcode.rect
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
                    barcodeData = barcode.data.decode("utf-8")
                    barcodeType = barcode.type
                    text = "{} ({})".format(barcodeData, barcodeType)
                    cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX,
                                0.5, (0, 0, 255), 2)
                    self._scanned_code = int(barcodeData)
                    
            cv2.imshow("Barcode Scanner", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break

        print("[INFO] wyłączanie kamerki...")
        vc.release()
        cv2.destroyAllWindows()

        if self._scanned_code:
            return self._scanned_code
        else:
            return "Nie udało się zeskanować kodu kreskowego z produktu"

    def erase_scanned_code(self):
        self._scanned_code = None
        return


class Database():

    """
    Klasa służy do pobierania nazwy zeskanowanego produktu z bazy
    (get_product_name)
    lub do dodawania produktu (kodu kreskowego i opisu) do bazy
    (add_product).

    Args:
        name (str): zadana nazwa przypisana produktowi
    """

    def __init__(self):
        self._name = None

    @property   
    def name(self):
        return self._name
    
    def __str__(self):
        text = f"Ostatnio używany produkt z bazy to: {self._name}."
        return text

    def get_product_name(self, barcode):
        if not barcode:
            raise ExEmptyBarcode()
        if not isinstance(barcode, int):
            raise ExWrongBarcodeType(barcode)
        with open("baza_produktow.json", "r", encoding="utf-8") as jsonfile:
            data = json.load(jsonfile)
            for item in data:
                if barcode == item['barcode']:
                    self._name = item['product']
                    break
                else:
                    self._name = "Produktu nie ma w bazie"
        return self._name

    def add_product(self, barcode, name):
        if not name:
            raise ExEmptyProductName()
        if not barcode:
            raise ExEmptyBarcode()
        self._name = name
        if not isinstance(barcode, int):
            raise ExWrongBarcodeType(barcode)
        with open ("baza_produktow.json", "r+", encoding="utf-8") as jsonfile:
            data = json.load(jsonfile)
            data.append({'barcode': barcode, 'product': name})
            jsonfile.seek(0)
            json.dump(data, jsonfile, indent = 4)


class SpeechSynthesizer():

    """
    Klasa służy do przetwarzania tekstu na mowę
    (say_the_name) oraz do rozpoznawania mowy (get_the_name).
    """

    def say_the_name(self, text):
        if not text:
            raise ExEmptyText()
        tts = gTTS(text=text, lang="pl")
        filename = "voice.mp3"
        tts.save(filename)
        playsound.playsound(filename)
        os.remove("voice.mp3")
    
    def get_the_name(self):
        rec = sr.Recognizer()
        with sr.Microphone() as source:
            audio = rec.listen(source)
            said = ""

            try:
                said = rec.recognize_google(audio, language="pl")
                print(said)
            except Exception:
                print("ExVoiceNotRecognized")

        return said


class IdentifyProduct():

    """
    Klasa jest odpowiedzialna za cały proces skanowania, 
    importowania i odczytywania nazwy zeskanowanego produktu.
    Wykorzystuje ona obiekty i metody klas poprzednich
    (CodeScanner, Datatbase, SpeechSynthesizer).

    Args:
        code_to_scan (CodeScanner): obiekt klasy CodeScanner
    """

    def __init__(self, code_to_scan):
        if not isinstance(code_to_scan, CodeScanner):
            raise WrongTypeOfObject()
        self.code_to_scan = code_to_scan

    def scan_import_speak(self):
        self.code_to_scan.scan_barcode()
        scanned_code = self.code_to_scan.scanned_code
        speak = SpeechSynthesizer()
        if scanned_code:
            product = Database()
            product.get_product_name(scanned_code)
            speak.say_the_name(product.name)
        else:
            speak.say_the_name("Produkt nie został zeskanowany")
        self.code_to_scan.erase_scanned_code()


class AddProductByVoice():

    """
    Klasa jest odpowiedzialna za cały proces skanowania, 
    głosowego nadawania opisu produktowi i dodawania go do bazy.
    Wykorzystuje ona obiekty i metody klas poprzednich
    (CodeScanner, Datatbase, SpeechSynthesizer).

    Args:
        code_to_scan (CodeScanner): obiekt klasy CodeScanner
    """

    def __init__(self, code_to_scan):
        if not isinstance(code_to_scan, CodeScanner):
            raise WrongTypeOfObject()
        self.code_to_scan = code_to_scan
    
    def scan_name_add(self):
        product = Database()
        self.code_to_scan.scan_barcode()
        scanned_code = self.code_to_scan.scanned_code
        speech = SpeechSynthesizer()
        if scanned_code:
            speech.say_the_name("Po 2 sekundach proszę podać nazwę produktu")
            product_name = speech.get_the_name()
            if not product_name:
                speech.say_the_name("Nie udało się rozpoznać głosu")
            else:
                product.add_product(scanned_code, product_name)
        else:
            speech.say_the_name("Produkt nie został zeskanowany")
        self.code_to_scan.erase_scanned_code()


class ScannerInterface():

    """
    Klasa, która tworzy interfejs graficzny użytkownika.
    Jest to graficzna reprezentacja całego projektu skanera.
    Udostępnia widżety, do których są skróty klawiszowe.

    Args:
        master (Tk): obiekt klasy tkinter.Tk
    """

    def __init__(self, master):
        if not isinstance(master, tk.Tk):
            raise ExNotTkinterObject
        self.master = master
        master.title("Barcode Scanner")
        master.geometry('884x590')

        # umieszczenie zdjęcia jako tło
        self.img = tk.PhotoImage(file='kod_kreskowy_skaner.png')
        self.my_label = tk.Label(master, image=self.img)
        self.my_label.place(x=0, y=0, relwidth=1, relheight=1)

        # poniżej w okienku umieszczane są wiadomości, widżety
        title = "SKANER KODÓW KRESKOWYCH\nZ SYNTEZATOREM MOWY"
        self.my_text = tk.Label(master, text=title, font='Times 24', 
                            relief='solid', bd=2, bg='pink')
        self.my_text.pack(pady=32)

        self.identification = tk.Button(master, text="IDENTYFIKACJA\nPRODUKTU", 
                            font='Times 18', bg='gray50', height=4, padx=13,
                            command = self.identify)
        self.identification.place(x=80, y=370)

        self.adding = tk.Button(master, text="DODAWANIE\nPRODUKTU\nDO BAZY", 
                            font='Times 18', bg='gray50', height=4, padx=31,
                            command = self.add_to_database)
        self.adding.place(x=565, y=368)

        self.audioguide = tk.Text(master, height=1, width=24)
        self.audioguide.insert(INSERT, "spacja - audioprzewodnik")
        self.audioguide.place(x=350, y=570)

        self.right = tk.Text(master, height=1, width=24)
        self.right.insert(INSERT, "kliknij strzałkę w prawo")
        self.right.place(x=580, y=499)

        self.left = tk.Text(master, height=1, width=23)
        self.left.insert(INSERT, "kliknij strzałkę w lewo")
        self.left.place(x=98, y=500)

        self.esc = tk.Text(master, height=1, width=14)
        self.esc.insert(INSERT, "esc żeby wyjść")
        self.esc.place(x=765, y=0)

        # event-driven programming - keyboard shortcuts
        master.bind("<Escape>", self.close_window)
        master.bind("<Left>", self.identify)
        master.bind("<Right>", self.add_to_database)

        master.bind("<space>", self.introduction)

    def introduction(self, event):

        """Jest pod spacją - włącza audioprzewodnik"""

        audio_intr = SpeechSynthesizer()
        text = '''Witamy w skanerze kodów kreskowych z syntezatorem mowy. 
        Podaję skróty klawiszowe: 
        strzałka w lewo - identyfikacja produktu,
        strzałka w prawo - dodawanie produktu do bazy,
        escape - wyjście z programu,
        klawisz 'Ku' - wyłączenie kamerki podczas skanowania'''
        audio_intr.say_the_name(text)

    def identify(self, event=None):

        """Jest pod lewą strzałką - włącza proces identyfikacji
        produktu, korzystając z metody klasy IdentifyProduct"""

        scanning = CodeScanner()
        identify = IdentifyProduct(scanning)
        identify.scan_import_speak()
        speech = SpeechSynthesizer()
        time.sleep(0.3)
        speech.say_the_name("Powrót do menu")

    def add_to_database(self, event=None):

        """Jest pod prawą strzałką - włącza proces dodawania
        produktu do bazy, korzystając z metody klasy
        AddProductByVoice"""

        scanning = CodeScanner()
        addbyvoice = AddProductByVoice(scanning)
        addbyvoice.scan_name_add()
        speech = SpeechSynthesizer()
        time.sleep(0.3)
        speech.say_the_name("Powrót do menu")

    def close_window(self, event):

        """Jest pod escape - wyłącza menu"""

        self.master.destroy()


# wywołanie programu:

# root = tk.Tk()
# app = ScannerInterface(root)
# root.mainloop()
