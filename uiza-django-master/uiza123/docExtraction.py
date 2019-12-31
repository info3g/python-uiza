import zipfile
import xml.etree.ElementTree

with zipfile.ZipFile('C:\Users\as\Downloads\Amarjitsinghresume.docx') as docx:
    tree = xml.etree.ElementTree.XML(docx.read('word/document.xml'))

print(tree)    