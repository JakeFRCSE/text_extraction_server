# How to use

1. Initialize FileProcessor Instance with TableExtractionStrategy enum type.
```
strategy = TableExtractionStrategy.PDFPLUMBER
file_processor = FileProcessor(table_exctraction_strategy=strategy)
```
2. Put url into the following code.
```
texts = file_processor.extract_texts(url)
```
# Output
1. If the url contains hwp, ppt, pptx and pdf, it returns a list comprised of a serise of string and a list of table(for PDFPLUMBER strategy).
Example Output:
```
[' 1 \n〔별지  제1호 서식〕\n편입학생 학점인정 총괄표\n', ' 2 \n〔별지 제2호 서식〕\n편입학생 개인별 학점 및 성적 인정표\n1. 인적사항\n2. 학점  및 성적 인정 내역\n가. 교양과목\n※ 공학인증의 경우 “전문교양”으로 인정할 수 있음.\n나. 전공(실용영어)과목\n※ 본교 인정 성적은 "S" 표시, 공학인증의 경우 비고란은 “전공(설계학점)”, “MSC”로\n구분하여 인정할 수 있음.\n다. 일반선택 과목\n※ 교과목명 없이 학점만 인정하고자 할 경우에는 본교 인정성적란의 교과목명에\n“인정학점”으로 하고 총학점 수만 기재하며, 교과목 인정시 성적은 "S" 표시.\n비  고\n', ' 3 \n라. 교직과목\n※ 본교 인정 성적은 "S" 표시 \n3. 추가이수 교양과목 [교양필수, 교양선택 구분 작성]\n첨부 : 전적학교 성적표(국문, 영문)  1부. \n20  ...\n\n작성자 :\n(인)\n상기와 같이 학과소속 교수회의 심의 결과에 따라 정히 인정함. \n(학과교수회의록 사본 첨부)\n\n학과(부)장\n(인)\n대학장 귀하\n', [['대학', '학과\n(전공)', '편입학\n년', '학번', '성 명', '학 점 인 정 내 역', 'None', 'None', 'None', 'None', 'None', 'None', 'None', '추가이수\n교양과목 내역', 'None', 'None', '비\n고'], ['None', 'None', 'None', 'None', 'None', '교 양', 'None', '전 공', 'None', 'None', '일반\n선택', '교직', '계', 'None', 'None', 'None', 'None'], ['None', 'None', 'None', 'None', 'None', '교양\n필수', '교양\n선택\n(기초\n교양)', '전공\n기초', '전공\n필수', '전공\n선택', 'None', 'None', 'None', '교양\n필수', '교양\n선택\n(기초\n교양)', '계', 'None'], ['', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '']], [['대 학', '학부(과, 전공)', '학 번', '성 명', '비 고'], ['', '', '', '', 'None']], [['전적대학 이수 성적', 'None', '본교 인정 성적', 'None', '계'], ['교과구분', '이수과목 및 학점', '교양필수', '교양선택\n(기초교양)', 'None'], ['', '', '', '', '']], [['전 적 대 학 이 수 성 적', 'None', 'None', 'None', 'None', 'None', '본 교 인 정 성 적', 'None', 'None', 'None', '본교과목\n(교과목코드)'], ['교과\n구분', '교과목명\n(국문, 영문)', '학\n년', '학\n기', '학\n점', '성\n적', '교과\n구분', '교과목명\n(국문, 영문)', '학\n점', '성\n적', 'None'], ['', '', '', '', '', '', '', '', '', '', '']], [['전 적 대 학 이 수 성 적', 'None', 'None', 'None', 'None', 'None', '본 교 인 정 성 적', 'None', 'None', 'None', '비 고'], ['교과\n구분', '교과목명\n(국문, 영문)', '학\n년', '학\n기', '학\n점', '성\n적', '교과\n구분', '교과목명\n(국문, 영문)', '학\n점', '성\n적', 'None'], ['', '', '', '', '', '', '', '', '', '', '']], [['전 적 대 학 이 수 성 적', 'None', 'None', 'None', 'None', 'None', '본 교 인 정 성 적', 'None', 'None', 'None', '비 고'], ['교과\n구분', '교과목명\n(국문, 영문)', '학\n년', '학\n기', '학\n점', '성\n적', '교과\n구분', '교과목명\n(국문, 영문)', '학\n점', '성\n적', 'None'], ['', '', '', '', '', '', '', '', '', '', '']], [['교과구분', '교과목코드번호', '교 과 목 명', '학 점', '비 고'], ['', '', '', '', '']]]
```
2. If not, it returns an empty list.
Example Output:
```
[]
```

# Caution
For automatication, automation of the process, refer to the following link.

[Reference](https://employeecoding.tistory.com/67)
