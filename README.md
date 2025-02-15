# FastAPI request format
|function|method|url|request|response|status|
|-------------|----|---------------|-----------|---------|--------------|
|extract_texts|GET|/texts|request body|{ "extracted_texts" : texts }|200:OK|
|extract_tables|GET|/tables|request body|{"extracted_tables" : tables}|200:OK|
|extract_texts_tables|GET|/texts_tables|request body|{"extracted_texts" : texts, "extracted_tables" : tables}|200:OK|

request body:
```
{
  "url":"..."
}
```


# How to use FileProcessor

1. Initialize FileProcessor Instance with TableExtractionStrategy enum type.
```
strategy = TableExtractionStrategy.PDFPLUMBER
file_processor = FileProcessor(table_exctraction_strategy=strategy)
```
2. Put url into the following code.

```
# Whole text in the file.
texts = file_processor.extract_texts(url)
```
```
# Only tables in the file
tables = file_processor.extract_tables(url)
```
```
# Text and tables in the file. Note that the content of table is not included in the text.
(texts, tables) = file_processor.extract_texts_tables(url) 
```
# Output
If the url contains hwp, ppt, pptx and pdf, it returns a list comprised of a serise of string for textand a list of table(for PDFPLUMBER strategy).
1. Example Output for texts:
```
# List[Optional[str]]
texts: [" 1 \n〔별지  제1호 서식〕\n편입학생 학점인정 총괄표\n대학\n학과\n(전공)편입학년\n학번\n성  명학점인정\n내 역\n추가이수 \n교양과목 내역비고교양전공\n일반\n선택교직계교양\n필수\n교양\n선택\n(기초\n교양)\n전공\n기초\n전공\n필수\n전공\n선택\n교양\n필수\n교양\n선택\n(기초\n교양)계"," 2 \n〔별지 제2호 서식〕\n편입학생 개인별 학점 및 성적 인정표\n1. 인적사항\n2. 학점 및 성적 인정 내역\n가. 교양과목\n※ 공학인증의 경우 “전문교양”으로 인정할 수 있음.\n나. 전공(실용영어)과목\n※ 본교 인정 성적은 \"S\" 표시, 공학인증의 경우 비고란은 “전공(설계학점)”, “MSC”로\n구분하여 인정할 수 있음.\n다. 일반선택 과목\n※ 교과목명 없이 학점만 인정하고자 할 경우에는 본교 인정성적란의 교과목명에\n“인정학점”으로 하고 총학점 수만 기재하며, 교과목 인정시 성적은 \"S\" 표시.\n대  학\n학부(과, 전공)\n학  번\n성  명\n비  고\n전적대학 이수 성적\n본교 인정 성적계교과구분\n이수과목 및 학점\n교양필수\n교양선택\n(기초교양)\n전 적 대 학  이 수 성 적\n본 교  인 정  성 적\n본교과목\n(교과목코드)\n교과\n구분\n교과목명\n(국문, 영문)학년학기학점성적\n교과\n구분\n교과목명\n(국문, 영문)학점성적\n전 적 대 학  이 수 성 적\n본 교  인 정  성 적\n비 고\n교과\n구분\n교과목명\n(국문, 영문)학년학기학점성적\n교과\n구분\n교과목명\n(국문, 영문)학점성적\n"," 3 \n라. 교직과목\n※ 본교 인정 성적은 \"S\" 표시 \n3. 추가이수 교양과목 [교양필수, 교양선택 구분 작성]\n첨부 : 전적학교 성적표(국문, 영문)  1부. \n20  ...\n\n작성자 :\n(인)\n상기와 같이 학과소속 교수회의 심의 결과에 따라 정히 인정함. \n(학과교수회의록 사본 첨부)\n\n학과(부)장\n(인)\n대학장 귀하\n교과구분\n교과목코드번호\n교 과 목 명\n학  점\n비  고\n전 적 대 학  이 수 성 적\n본 교  인 정  성 적\n비 고\n교과\n구분\n교과목명\n(국문, 영문)학년학기학점성적\n교과\n구분\n교과목명\n(국문, 영문)학점성적\n"]
```
2. Example output for tables
```
# List[Optional[List[str]]]
tables: [[["대학","학과\n(전공)","편입학\n년","학번","성 명","학 점 인 정 내 역","추가이수\n교양과목 내역","비\n고"],["교 양","전 공","일반\n선택","교직","계"],["교양\n필수","교양\n선택\n(기초\n교양)","전공\n기초","전공\n필수","전공\n선택","교양\n필수","교양\n선택\n(기초\n교양)","계"]],[["대 학","학부(과, 전공)","학 번","성 명","비 고"]],[["전적대학 이수 성적","본교 인정 성적","계"],["교과구분","이수과목 및 학점","교양필수","교양선택\n(기초교양)"]],[["전 적 대 학 이 수 성 적","본 교 인 정 성 적","본교과목\n(교과목코드)"],["교과\n구분","교과목명\n(국문, 영문)","학\n년","학\n기","학\n점","성\n적","교과\n구분","교과목명\n(국문, 영문)","학\n점","성\n적"]],[["전 적 대 학 이 수 성 적","본 교 인 정 성 적","비 고"],["교과\n구분","교과목명\n(국문, 영문)","학\n년","학\n기","학\n점","성\n적","교과\n구분","교과목명\n(국문, 영문)","학\n점","성\n적"]],[["전 적 대 학 이 수 성 적","본 교 인 정 성 적","비 고"],["교과\n구분","교과목명\n(국문, 영문)","학\n년","학\n기","학\n점","성\n적","교과\n구분","교과목명\n(국문, 영문)","학\n점","성\n적"]],[["교과구분","교과목코드번호","교 과 목 명","학 점","비 고"]]]
```   
3. Example output for texts and tables
```
# List[Optional[str]]
texts: [" 1 \n〔별지  제1호 서식〕\n편입학생 학점인정 총괄표\n"," 2 \n〔별지 제2호 서식〕\n편입학생 개인별 학점 및 성적 인정표\n1. 인적사항\n2. 학점 및 성적 인정 내역\n가. 교양과목\n※ 공학인증의 경우 “전문교양”으로 인정할 수 있음.\n나. 전공(실용영어)과목\n※ 본교 인정 성적은 \"S\" 표시, 공학인증의 경우 비고란은 “전공(설계학점)”, “MSC”로\n구분하여 인정할 수 있음.\n다. 일반선택 과목\n※ 교과목명 없이 학점만 인정하고자 할 경우에는 본교 인정성적란의 교과목명에\n“인정학점”으로 하고 총학점 수만 기재하며, 교과목 인정시 성적은 \"S\" 표시.\n비  고\n"," 3 \n라. 교직과목\n※ 본교 인정 성적은 \"S\" 표시 \n3. 추가이수 교양과목 [교양필수, 교양선택 구분 작성]\n첨부 : 전적학교 성적표(국문, 영문)  1부. \n20  ...\n\n작성자 :\n(인)\n상기와 같이 학과소속 교수회의 심의 결과에 따라 정히 인정함. \n(학과교수회의록 사본 첨부)\n\n학과(부)장\n(인)\n대학장 귀하\n"]

# List[Optional[List[str]]]
tables: [[["대학","학과\n(전공)","편입학\n년","학번","성 명","학 점 인 정 내 역","추가이수\n교양과목 내역","비\n고"],["교 양","전 공","일반\n선택","교직","계"],["교양\n필수","교양\n선택\n(기초\n교양)","전공\n기초","전공\n필수","전공\n선택","교양\n필수","교양\n선택\n(기초\n교양)","계"]],[["대 학","학부(과, 전공)","학 번","성 명","비 고"]],[["전적대학 이수 성적","본교 인정 성적","계"],["교과구분","이수과목 및 학점","교양필수","교양선택\n(기초교양)"]],[["전 적 대 학 이 수 성 적","본 교 인 정 성 적","본교과목\n(교과목코드)"],["교과\n구분","교과목명\n(국문, 영문)","학\n년","학\n기","학\n점","성\n적","교과\n구분","교과목명\n(국문, 영문)","학\n점","성\n적"]],[["전 적 대 학 이 수 성 적","본 교 인 정 성 적","비 고"],["교과\n구분","교과목명\n(국문, 영문)","학\n년","학\n기","학\n점","성\n적","교과\n구분","교과목명\n(국문, 영문)","학\n점","성\n적"]],[["전 적 대 학 이 수 성 적","본 교 인 정 성 적","비 고"],["교과\n구분","교과목명\n(국문, 영문)","학\n년","학\n기","학\n점","성\n적","교과\n구분","교과목명\n(국문, 영문)","학\n점","성\n적"]],[["교과구분","교과목코드번호","교 과 목 명","학 점","비 고"]]]
```
4. If no content extracted, it returns an empty list.
Example Output:
```
[]
```


# Caution
For automatication, automation of the process, refer to the following link.

[Reference](https://employeecoding.tistory.com/67)
