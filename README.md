HELP_THE_BLID_SCANNER

Temat : Skaner kodów kreskowych z bazą produktów i syntezatorem mowy oraz jej rozpoznawaniem

Osoba realizująca: Jakub Rozkosz

W zamyśle projekt kierowany jest dla osób niewidomych. Ociemniałym ciężko może byd rozróżnid 
przedmioty o identycznym kształcie. Bez zmysłu wzroku wyzwaniem jest rozpoznad czy np. puszka 
jest z ananasem czy brzoskwiniami. Pomysłem jest stworzenie programu, który za pomocą kamerki z 
laptopa będzie odczytywał kod kreskowy z produktu, odszukiwał jego nazwę w bazie kodów 
kreskowych, a następnie za pomocą syntezatora mowy komunikował użytkownikowi czym jest dany 
produkt. Projekt może byd wykorzystywany przez każdego we własnym celu.

Klasa CodeScanner:
”””
Klasa służy do skanowania i odszyfrowania kodów kreskowych z wykorzystaniem kamerki laptopa.
Args:
 scanned_code (int): zeskanowany kod kreskowy podczas skanowania.
Jeśli uda się zeskanowad produkt (co głównie zależy od jakości kamerki, oświetlenia, wielkości kodu 
kreskowego) to wokół niego zostaną narysowane czerwone kontury prostokąta wraz z numerem 
kodu kreskowego.
"""
*do obsługi obrazu w czasie rzeczywistym służy biblioteka OpenCV
*do odszyfrowania wyłapanego kodu kreskowego służy biblioteka Zbar
*należy pobrad: bibliotekę OpenCV i Zbar oraz moduł pyzbar

Klasa Database:
”””
Klasa służy do pobierania nazwy zeskanowanego produktu z bazy ( metoda get_product_name)
lub do dodawania produktu (kodu kreskowego i opisu) do bazy (metoda add_product).
Args:
name (str): zadana nazwa przypisana produktowi.
Jeśli kod kreskowy lub nadawana nazwa produktu jest pusta podnoszone są wyjątki. 
”””
*baza została stworzona w pliku json w następującym schemacie: 
 { „barcode”: 5900483922310,
 „product”: „marmolada brzoskwiniowa” }
 
Klasa SpeechSynthesizer:
”””
Klasa służy do przetwarzania tekstu na mowę (metoda saythename) oraz do rozpoznawania mowy 
(metoda getthename).
Jeśli tekst do odczytania przez syntezator mowy jest pusty zostaje podniesiony wyjątek.
”””
*do syntezowania mowy służy moduł gTTS (google text-to-speech), który wykorzystuje 
syntezator mowy google
*do rozpoznawania mowy – moduł speech_recognition też od google’a
*podsumowując trzeba pobrad następujące moduły: gTTS, playsound, pyaudio i 
SpeechRecognition

Klasa IdentifyProduct:
”””
Klasa jest odpowiedzialna za cały proces skanowania, importowania i odczytywania nazwy 
zeskanowanego produktu.
Args:
code_to_scan (CodeScanner): obiekt klasy CodeScanner – zostanie wykorzystany w metodzie 
scan_import _speak
Wykorzystuje ona obiekty i metody klas poprzednich (CodeScanner, Datatbase, SpeechSynthesizer). 
Jeśli produkt nie został zeskanowany – zostaje zwrócony taki komunikat głosowy. 
”””

Klasa AddProductByVoice:
”””
Klasa jest odpowiedzialna za cały proces skanowania, głosowego nadawania opisu produktowi i 
dodawania go do bazy.
Args:
code_to_scan (CodeScanner): obiekt klasy CodeScanner – zostanie wykorzystany w metodzie 
scan_name_add
Wykorzystuje ona obiekty i metody klas poprzednich (CodeScanner, Datatbase, SpeechSynthesizer). 
Jeśli nie udało się rozpoznad głosu lub zeskanowad produktu – zostają zwrócone takie komunikaty 
głosowe.
”””

Klasa Interface:
”””
Klasa, która tworzy interfejs graficzny użytkownika.
Jest to graficzna reprezentacja całego projektu skanera – tworzy menu z tłem, tekstem informującym.
Udostępnia widżety, do których są skróty klawiszowe.
Args:
master (Tk): obiekt klasy tkinter.Tk
”””
def introduction(self, event):
"""Jest pod spacją - włącza audioprzewodnik"""
def identify(self, event):
"""Jest pod lewą strzałką - włącza proces identyfikacji produktu, korzystając z metody klasy 
IdentiyProduct"""
def identify(self, event):
"""Jest pod lewą strzałką - włącza proces identyfikacji produktu, korzystając z metody klasy 
IdentifyProduct"""
def close_window(self, event):
 """Jest pod escape - wyłącza menu"""
 
Testy jednostkowe przy wykorzystaniu ‘pytest’ zostały wykonane do wszystkich tych elementów 
kodu, do których dało się takowe przeprowadzid. 
