ReceiptDeskewer
==============================
This app takes images of receipts as input from the `input_data`-folder and rotates them that the text is readable.

Installation
------------
* Install [Google Tesseract OCR](https://github.com/tesseract-ocr/tesseract) and please check if the variable `pytesseract.pytesseract.tesseract_cmd` points to your Tesseract Installation.
By default it is set to `C:/Program Files/Tesseract-OCR/tesseract.exe`.
The variable can be found in the `image_manipulation.py` file

* Create new virtual environment `python -m venv <name_of_virtualenv>`
* Activate virtual environment `.\venv\Scripts\activate`
* Install requirements with `pip install -r requirements.txt`

Getting started
------------
Move image files to the `input_data`-folder and run the app with `python main.py`.
Optionally you can define a custom input folder by adding the path as an argument. For example: `python main.py --path "./raw_data/"`
By default intermediate results are stored. This can be changed by adding `--no-intermediate_results` as an argument. 

Example usage
------------
```commandline
python main.py
python main.py --path ./path_to_custom_folder/
python main.py --intermediate_results 
```