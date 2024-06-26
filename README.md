﻿# auto_grading
 프로젝트 소개 
-----
짧은 단어들을 자동으로 채점해주는 프로그램을 개발하였다. 4명이서 진행한 팀 프로젝트이다. 

OCR 기술을 이용해서 시험지들을 OCR로 분석해서 자동으로 채점해주는 프로그램을 개발했다.

본 프로젝트의 목적은 OCR 기술을 이용하여 학생들이 제출한 단답형 형식의 답안에 대해 답안 인식 ,정답 비교 및 자동 점수 부여 시스템을 개발하는 것이다.

이를 통해 교육 기관이 기존의 수동 채점 방식에서 벗어나 시간과 노력을 크게 절약할 수 있을 것이라고 생각하였다.

💡 요구 및 필요 기술
--- 
1. OpenCV : 학생들이 제출한 답안지 이미지를 전처리하고 , 노이즈를 제거 하며 이미지의 품질을 향상시킨다.

2. Flask :  Flask 를 사용하여 웹 페이지를 구축하고 ,학생들이 답안지 PDF 를 업로드하고 정답을 입력할 수 있는 환경을 제공한다. 또한 이러한 웹 애플리케이션을 호스팅하고 서비스한다.

3. Google Vision Api : 답안지 이미지를 텍스트로 변환하여 컴퓨터가 읽을 수 있는 형식으로 제공한다. 손글씨 답안을 인식하고 해석하는 역할.

💡 상용 기술 비교
---
OCR 을 적용할 API 를 결정하는데 있어서 상용기술로 사용되는 OCR기술들을 비교대조 해볼 필요가 있었다. 
![상용기술비교](https://github.com/dmlwls990527/auto_grading/blob/master/images/%EC%83%81%EC%9A%A9%EA%B8%B0%EC%88%A0%20%EB%B9%84%EA%B5%90.PNG)
Google Vision Api의 경우 위 2개의 Api와 비교했을 때 좀 더 정확한 텍스트 인식률을 확인할 수 있었다. 

프로젝트 구성 
---
![아키텍처](https://github.com/dmlwls990527/auto_grading/blob/master/images/%EC%95%84%ED%82%A4%ED%85%8D%EC%B2%98.PNG)

a. 시험 답안 양식 다운로드 : 

웹 페이지에 시험 답안지 양식을 다운받을 수 있는 링크를 설정하여 시험 주최자가 답안 양식을 웹 페이지 또는 애플리케이션에서 다운로드할 수 있도록 제공한다. 시험 주최자는 시험 답안지 양식의 문항 수 및 배점 등을 수정하여 사용한다.

b. 답안 작성 및 업로드:

응시자들은 다운로드하고 수정된 답안 양식을 이용하여 각 문제에 대한 답안을 작성한다. 작성이 완료된 답안지는 PDF 파일로 저장한 후 시험 감독관 혹은 주최자에게 파일을 보낸다.

c. 웹 페이지 방문 및 답안 업로드:

PDF로 변환한 파일을 받은 주최자 혹은 감독관은 해당 파일을 웹 페이지에 업로드한다.

d. 정답 입력:

시험을 본 답안지의 문항 수 만큼 정답 입력필드를 생성한 후 각 문제의 정답을 웹 페이지의 입력 필드에 입력한다.

e. 답안 처리 및 OCR:

서버는 업로드된 PDF 파일과 입력된 정답을 POST 요청을 통해 받는다. 서버는 Google Vision API를 활용하여 OCR 처리를 수행하여 PDF 파일을 텍스트로 변환한다.

f. OCR 결과 처리:

OCR 결과를 배열로 변환하여 문제 번호, 학생의 답안, 정답, 배점 등을 추출한다.

g. 채점 및 결과 반환:

서버는 OCR로 받은 학생의 답안과 웹페이지의 입력필드에 적힌 정답의 값을 비교한 후 일치 여부에 따라 OCR로 받은 배점을 모두 더해서 최종 점수를 받아낸다. 이렇게 나온 채점 결과를 웹페이지에 Json 형식으로 나타내며 CSV 파일로 답안 작성 내용과 채점 결과표를 사용자 및 관리자에게 반환한다.

h. 최종 결과 확인:

사용자 또는 관리자는 채점 결과가 저장된 CSV 파일을 다운로드하여 확인한다.

프로젝트 설계
---
a. 답안 영역 분할 단계

답안지는 답안별로 영역들이 나뉘어져 있기에 답안지에 인식된 x축의 긴 선들을 기준으로 답안의 영역을 분할한다. 
![1단계](https://github.com/dmlwls990527/auto_grading/blob/master/images/%EC%A0%88%EC%B0%A81.PNG)

b. 학번,이름 추출 단계

어떤 학생의 시험지인지 판별하는 과정이다. 답안 영역 분할 단계를 통해 바디 (답안 표 영역 ) / 헤더 (과목정보,학번,이름 영역 ) 으로 나뉜다. 

헤더 부분을 통해서 학번과 이름 작성칸의 () 와 [] 안에 있는 텍스트를 인식할 수 있도록 지정하여 저장하는 방식으로 텍스트 정보를 저장하였다. 

![2단계](https://github.com/dmlwls990527/auto_grading/blob/master/images/%EC%A0%88%EC%B0%A82.PNG)

c. 문항번호 ,답안 , 배점 텍스트 추출

답안 영역 분할 단계를 통해 얻은 문항 별 이미지에서 텍스트를 추출한다. 그 후에

2차원 배열을 통해서 [번호][답안][배점] 으로 매핑하였다. 공백 답아느이 경우에는 " " 를 매핑하였다.

![3단계 예시](https://github.com/dmlwls990527/auto_grading/blob/master/images/%EC%A0%88%EC%B0%A83.PNG)

d. 답안 후처리 단계

텍스트를 인식하면서 주로 발생하는 오류들을 발견하였다. 주로 1과 l 이 잘못 인식되는 경우, 띄어쓰기 및 줄바꿈이 이루어지지 않았으나 인식이 되는 경우가 이에 해당한다. 

![4단계](https://github.com/dmlwls990527/auto_grading/blob/master/images/%EC%A0%88%EC%B0%A84.PNG)

위에있는 표가 후처리 전, 아래 표가 후처리 후의 답안 모습이다. 문제 5와,9 그리고 문제 10을 보면 띄어쓰기와 줄바꿈이 후처리 되었다.

e. 실제 답안을 이용한 학생 답안 채점 단계

답안 후처리 단계까지의 과정을 거친 이후 실질적인 채점이 이루어지는 단계이다. 사용자가 웹을 이용해 미리 입력한 실제 답안과 인식한 답안을 분항별로 비교하여 채점하였다.

f. 결과를 csv 파일로 변환하는 단계

![5단계,채점 완료 이미지](https://github.com/dmlwls990527/auto_grading/blob/master/images/%EC%A0%88%EC%B0%A85.PNG)
![csv파일](https://github.com/dmlwls990527/auto_grading/blob/master/images/%EC%B1%84%EC%A0%90%EA%B2%B0%EA%B3%BC%20csv%20%ED%8C%8C%EC%9D%BC.PNG)

프로젝트 결과
--- 
![웹페이지](https://github.com/dmlwls990527/auto_grading/blob/master/images/%EC%9B%B9%EC%8B%9C%EB%82%98%EB%A6%AC%EC%98%A4.PNG)

[시연 영상] (https://drive.google.com/file/d/18DOWlgIxsum1GLQoGY_jolcJsO8-oAkQ/view?resourcekey) 
채점 소요시간은 시험지 하나에 15문항이라고 했을때 시험지 하나 당 8.3 초가 걸렸다. 학생 100명의 답안지를 채점하기 위해 필요한 예상 시간은 약 13.8분이다.


