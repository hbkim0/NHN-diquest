# LAI (Legacy Application Interface)

* KEY-VALUE 방식의 웹서비스
* 챗봇에서 대외서비스 연계를 사용하기 위해 개발됨
* 챗봇지식 구축시 LAI KEY 를 답변내에 사용하고 엔진에서는 LAI KEY 를 추츨하여 LAI 모듈에 값을 조회한다.
* LAI 는 KEY 기준으로 Method 맵핑되며 일반적인 웹서비스에서 URL PATH 맵핑과 비슷하다.

## LAI KEY

![LAI_KEY](docs/files/LAI_KEY.PNG)

* 예시
  * LAI KEY: 시작.시간.현재.time
  * Endpoint Name: 시작.시간.현재
  * Module Name: 시작
  * Endpoint Mapping : 시간.현재
  * Output Param: name
* 설명
  * '시작' 모듈에
  * '시간.현재' 와 맵핑되는 메서드를 호출하여 실행하고
  * 응답객체에 'time' 값을 반환한다.
