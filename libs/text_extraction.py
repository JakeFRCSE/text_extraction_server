import requests
import os
import magic
import pythoncom
import win32com.client as win32
import re
import pdfplumber
import pymupdf
from typing import List, Dict, Tuple, Optional, Sequence
from pptxtopdf import convert
from enum import Enum, unique

@unique
class TableExtractionStrategy(Enum):
    PDFPLUMBER = 0
    YOLO = 1

class FileProcessor():
    def __init__(self, file_name:str = "temp", table_exctraction_strategy:TableExtractionStrategy = TableExtractionStrategy.PDFPLUMBER):
        self.url = None
        self.cwd = os.getcwd()
        self.file_name = file_name
        self.download_path = os.path.join(self.cwd, self.file_name)
        self.pdf_path = self.download_path + '.pdf'
        self.pdf_wo_table_path = self.download_path + "wo_table.pdf"
        self.table_exctraction_strategy = table_exctraction_strategy
        self.extension_path = None
        self.extension = None
        

    def clear_file_path(self, file_path)->None:
        if os.path.exists(file_path):
            os.remove(file_path)

    def download_file(self, url:str)->None:
        self.url = url
        try:
            with open(self.download_path, "wb") as file:
                response = requests.get(self.url)
                response.raise_for_status()
                file.write(response.content)
            print(f"Processing...\n{self.url}")
        except Exception as e:
            print(f"Failed to process: {self.url}\n{e}")
            return None    
        
    def detect_file_type(self)->None:
        try:
            mime = magic.Magic(mime=True)
            file_type = mime.from_file(str(self.download_path))
                
        except Exception as e:
            print(f"파일 형식 감지 중 오류 발생: {e}")
        
        else:
            mime_to_ext = {
                'application/pdf': '.pdf',
                'application/x-hwp': '.hwp',
                'image/jpeg': '.jpg',
                'image/png': '.png',
                'image/gif': '.gif',
                'application/vnd.ms-powerpoint':'.ppt',
                'application/vnd.openxmlformats-officedocument.presentationml.presentation':'.pptx',
            }
            self.extension = mime_to_ext.get(file_type, None)
            if self.extension:
                self.extension_path = self.download_path + self.extension
        
    def attach_extension(self)->None:
        if self.extension:
            os.rename(self.download_path, self.file_name + self.extension)

    def convert_hwp_to_pdf(self)->None:
        pdf_path = self.pdf_path
        hwp_path = self.extension_path
        try:
            pythoncom.CoInitialize()
            hwp = win32.gencache.EnsureDispatch("HWPFrame.HwpObject")
            hwp.RegisterModule("FilePathCheckDLL", "FilePathCheckerModule")
            hwp.XHwpWindows.Item(0).Visible = False
            hwp.Open(str(hwp_path))
            hwp.SaveAs(str(pdf_path), "PDF")
            hwp.Clear()
            self.extension = ".pdf"
        
        except Exception as e:
            print(f"HWP to PDF 변환 중 오류 발생: {e}")
            return None
            
        finally:
            try:
                hwp.Quit()
                
            except:
                pass
            pythoncom.CoUninitialize()

    def convert_ppt_to_pdf(self)->None:
        """pptx is also available"""
        convert(self.cwd, self.cwd)
        self.extension = ".pdf"


    def refine_text(self, text:str)->str:
        refined_text = re.sub(r"-{5,}","\n", text)
        refined_text = re.sub(r"[-*\x07\u20E7\u20E9\u0003\u00B7]", "", refined_text)
        refined_text = re.sub(r'[\u2027\u25CB\u3139]', '', refined_text)
        refined_text = re.sub(r"\u318d", "", refined_text)
        refined_text = re.sub(r"\u25A1", "", refined_text)
        refined_text = re.sub(r"\u007C{2,}", "", refined_text)
        refined_text = re.sub(r"\u25FE", " ", refined_text)
        refined_text = re.sub(r"\u3147", " ", refined_text)
        refined_text = re.sub(r"[\u3010]", "[", refined_text)
        refined_text = re.sub(r"[\u3011]", "]", refined_text)
        refined_text = re.sub(r"\u2018", "'", refined_text)
        refined_text = re.sub(r"\u2019", "'", refined_text)
        refined_text = re.sub(r"\t", "\n", refined_text)
        refined_text = re.sub(r" {3,}", "\n", refined_text)
        refined_text = re.sub(r"\n +", "\n", refined_text)
        refined_text = re.sub(r" \n ", "\n", refined_text)
        refined_text = re.sub(r"\n\n", "\n", refined_text)
        refined_text = re.sub(r'\n(.{1})\n', r'\1',refined_text)
        return refined_text

    def format_table(self, table:List[List[Optional[str]]])->List[str]:
        formatted_table = []
        for row in table:
            formatted_row = []
            for cell in row:
                cell = self.refine_text(str(cell))
                formatted_row.append(cell)
            formatted_table.append(formatted_row)
        return formatted_table

    def extract_tables_pdfplumber(self)->List[Dict[int, str]]:
        tables = []

        with pdfplumber.open(self.pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages):
                page_tables = page.extract_tables()

                for table in page_tables:
                    formatted_table = self.format_table(table)
                    tables.append({
                        'page': page_num + 1,
                        'table': formatted_table
                    })

        return tables

    def remove_tables(self)->None:
        doc = pymupdf.open(self.pdf_path)
        for page in doc:
            for tab in page.find_tables():
                page.add_redact_annot(tab.bbox) 
                page.apply_redactions(images=2, graphics=2, text= 0)
        doc.save(self.pdf_wo_table_path)
        doc.close()

    def get_texts_refined(self)->List[str]:
        doc = pymupdf.open(self.pdf_path)
        refined_extracted_text = [self.refine_text(page.get_text()) for page in doc]
        return refined_extracted_text
    
    def get_texts_refined_wo_table(self)->List[str]:
        doc = pymupdf.open(self.pdf_wo_table_path)
        refined_extracted_text = [self.refine_text(page.get_text()) for page in doc]
        return refined_extracted_text

    def clear(self)->None:
        paths = [self.download_path, self.extension_path, self.pdf_path, self.pdf_wo_table_path]
        for path in paths:
            if path:
                self.clear_file_path(path)
        self.extension = None
        self.extension_path = None

    def prepare_pdf(self, url:str)->bool:
        self.clear_file_path(self.download_path)
        self.download_file(url)
        self.detect_file_type()
        if self.extension is None:
            self.clear()
            return False
        self.clear_file_path(self.extension_path)
        self.attach_extension()


        if self.extension != ".pdf":
            self.clear_file_path(self.pdf_path)
        if self.extension == ".hwp":
            self.convert_hwp_to_pdf()
        elif self.extension == ".ppt" or self.extension == ".pptx":
            self.convert_ppt_to_pdf()
        if self.extension != ".pdf":
            self.clear()
            return False
        return True

    def extract_texts(self, url:str)->List | List[str]:
        texts = []
        if self.prepare_pdf(url):
            texts = self.get_texts_refined()
        return texts

    def extract_tables(self, url:str)->List[Optional[Dict[int, str]]]:
        tables_list = []
        if self.prepare_pdf(url):
            if self.table_exctraction_strategy == TableExtractionStrategy.PDFPLUMBER:
                tables = self.extract_tables_pdfplumber()
            elif self.table_exctraction_strategy == TableExtractionStrategy.YOLO:
                #Yolo extraction
                pass
            for table in tables:
                    tables_list.append(table.get('table', None))
        return tables_list

    def extract_texts_tables(self, url:str)->Tuple[List[Optional[str]], List[Optional[List[str]]]]:
        texts = []
        tables = []
        if self.prepare_pdf(url):
        
            tables = self.extract_tables(url)
            self.remove_tables()
            texts = self.get_texts_refined_wo_table()

        
        return (texts, tables)

    def set_table_strategy_yolo(self)->bool:
        self.table_exctraction_strategy = TableExtractionStrategy.YOLO
        print("Successfully Changed to YOLO strategy")
        return True

    def set_table_strategy_pdfplmbr(self)->bool:
        self.table_exctraction_strategy = TableExtractionStrategy.PDFPLUMBER
        print("Successfully Changed to PDFPLUMBER strategy")
        return True


if __name__ == "__main__":
    texts = []
    url_lists = ["https://me.pusan.ac.kr/new/sub05/download.asp?fileSeq=15919&type=hakbunotice", # xlsx
                 "https://me.pusan.ac.kr/new/sub05/download.asp?fileSeq=15920&type=hakbunotice", # hwp
                 "https://me.pusan.ac.kr/new/sub05/download.asp?fileSeq=15917&type=hakbunotice", # png
                 "https://me.pusan.ac.kr/new/sub05/download.asp?fileSeq=15901&type=hakbunotice", # jpg
                 "https://me.pusan.ac.kr/new/sub05/download.asp?fileSeq=15842&type=hakbunotice", # pdf
                 ]
    strategy = TableExtractionStrategy.PDFPLUMBER
    file_processor = FileProcessor(table_exctraction_strategy=strategy)
    for url_list in url_lists:
        texts = file_processor.extract_texts(url_list)
        if texts:
            print(texts)
        else:
            print("SKIPPED: This file is not text-extractable.\n")