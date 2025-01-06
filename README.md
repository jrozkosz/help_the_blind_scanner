Topic: Barcode Scanner with Product Database, Speech Synthesis, and Recognition

Developer: Jakub Rozkosz

This project is designed for visually impaired individuals. For those who are blind, distinguishing between items with identical shapes can be challenging. Without the sense of sight, it may be difficult to tell if, for example, a can is filled with pineapple or peaches. The application uses the laptop's camera to read the barcode of the product, searches for its name in the barcode database, and then communicates the product's name to the user through a speech synthesizer. Additionally, the user can add a product to the database by scanning the barcode and verbally providing the product name, which will be saved in the database. The project can be used by anyone for their personal purposes.

Unit tests were conducted using the ‘pytest’ module.

This application utilizes OpenCV for barcode scanning functionality and Google libs for speech recognition and text-to-speech.
