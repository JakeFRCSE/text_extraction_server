from fastapi import FastAPI
from pydantic import BaseModel
from libs import text_extraction

file_processor = text_extraction.FileProcessor()

app = FastAPI()

class URL(BaseModel):
    url: str

@app.get("/texts")
async def texts_only(url:URL):
    texts = file_processor.extract_texts(url.url)
    file_processor.clear()
    return { "extracted_texts" : texts }


@app.get("/tables")
async def tables_only(url:URL):
    tables = file_processor.extract_tables(url.url)
    file_processor.clear()
    return {"extracted_tables" : tables}


@app.get("/texts_tables")
async def texts_tables(url:URL):
    (texts, tables) = file_processor.extract_texts_tables(url.url)
    file_processor.clear()
    response =  {
        "extracted_texts" : texts, 
        "extracted_tables" : tables,
        }
    return response