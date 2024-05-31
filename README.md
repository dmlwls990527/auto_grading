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
[!상용기술비교](https://github.com/dmlwls990527/auto_grading/blob/master/images/%EC%83%81%EC%9A%A9%EA%B8%B0%EC%88%A0%20%EB%B9%84%EA%B5%90.PNG)
Google Vision Api의 경우 위 2개의 Api와 비교했을 때 좀 더 정확한 텍스트 인식률을 확인할 수 있었다. 

시나리오
---

1. 홈페이지에서 답안지 형식을 다운받는다.

2. 답안지 입력 란에 실제 답안들을 입력한다.

3. 답안지들을 스캔해서 홈페이지에 업로드한다.

4. 서버에서 api 를 요청해서 OCR 을 진행 한 후 , 채점을 한다

5. 채점 결과를 csv 파일로 사용자에게 제공한다.

6. 사용자는 자동으로 파일을 다운받는다.

전처리 과정 
--- 

스캔한 답안지는 다음과 같은 구성으로 전처리 된다.

영역 분할

텍스트 추출

답안 후처리

채점 및 결과 반환

채점 소요시간은 시험지 하나에 15문항이라고 했을때 시험지 하나 당 8.3 초가 걸렸다. 학생 100명의 답안지를 채점하기 위해 필요한 예상 시간은 약 13.8분이다.


