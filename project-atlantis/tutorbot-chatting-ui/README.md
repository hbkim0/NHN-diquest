# INFOCHATTER3-ANSWER-CHAT

- INFOCHATTER3-ANSWER-CHAT 개발 관련 내용을 기술한다.

# 이력

- v0.0.1

  - 2020.07.28

    - 최초 등록

# 구성

  <!-- blank line -->

- 환경

  - windows 10, mac
  - visual studio code
  - node 12.5.0
  - npm 6.9.0

  <!-- blank line -->

- 라이브러리

  - axios / 0.19.0
  - crypto-js / 4.0.0
  - es6-promise / 4.2.8
  - jquery / 3.4.1
  - moment / 2.24.0
  - url-loader / 4.1.0
  - vue / 2.5.11
  - vue-flatpickr-component / 8.1.5
  - vue-js-modal / 1.3.33
  - vue-owl-carousel / 2.0.3
  - vue-router / 3.1.6
  - vue-virtual-scroller / 1.0.10

- 자체개발 라이브러리
  - infochatter3-answer-uikit / 0.2.8

# 실행

- 설정 - API Config 먼저 수행
- Visual Studio Code 실행
  - npm install
  - npm run dev
  - npm run local // 로컬에서 개발 모드로 실행

## CROSS Origin

CROSS Origin 문제 발생시 크롬을 개발자 버전으로 실행후 확인하면 됩니다.

### OSX

```
open -n -a /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --args --user-data-dir="/tmp/chrome_dev_test" --disable-web-security
```

### Winodws

```
"[PATH_TO_CHROME]\chrome.exe" --disable-web-security --disable-gpu --user-data-dir=~/chromeTemp
"[PATH_TO_CHROME]\chrome.exe --user-data-dir="C://Chrome dev session" --disable-web-security"
```

### Linux

```
google-chrome --disable-web-security
```

# 배포

- Visual Studio Code 실행
  - npm run dev // 개발 버전
  - npm run build // 운영 버전

```
아래 경로에 있는 폴더,파일을 배포 하고자 하는 서버에 업로드

root
├── /dist // npm run dev, build 를 통해 생성되는 폴더
├── /src
│   └── /assets
└── /index.html

Apache 기준
htdocs/

Tomcat 기준
webapp/public/
```

# 개발

## 암호화

/src/api/crypto.js

```
key : b0f48588efef1cc7
iv : 1234567890123456
```

## 설정

### 아이콘

/src/assets/favicon

아이콘 교채

### 홈페이지 정보

/index.html

홈페이지 정보 교체 ( ex: title )

### API Config

/src/config/config.js

| key               | type    | description                       |
| ----------------- | ------- | --------------------------------- |
| REST_URL          | string  | 기본 API URL                      |
| PATH              | string  | 빌드 경로                         |
| REST_API_PATH     | string  | 챗봇(인포채터) 관련 REST API 경로 |
| MBR_REST_API_PATH | string  | 로그인,회원 관련 REAT API 경로    |
| REPO_ID           | string  | 저장소 아이디                     |
| AGENT_NAME        | string  | 에이전트명                        |
| FAQ_CATEGORY_NAME | string  | FQA 카테고리                      |
| LOGIN_USE         | boolean | 로그인 필요 여부 ( true / false ) |
| USER_ID           | string  | 유저 아이디                       |

배포시 운영 rest api url 이 챗봇이 배포되는 url 과 다를 경우 REST_URL 을 운영 url 로 설정후 배포해 줍니다.

```
// 예시

{
    "REST_URL": "", // rest api 도메인 ( url )
    "PATH": "/chatbot", // domain.com/chatbot 접속시 챗봇 화면이 보임
    "REST_API_PATH": "/restapi", // 으로 챗봇 관련 REAT API를 요청함
    "MBR_REST_API_PATH": "/restapi-mbr", // 로그인,회원 관련 REAT API 없음
    "REPO_ID": "TP", // 저장소 아이디
    "AGENT_NAME": "사학연금챗봇", // 에이전트명
    "FAQ_CATEGORY_NAME": "", // 카테고리 없음
    "LOGIN_USE": false, // 로그인 필수 아님
    "USER_ID": "" // 유저 아이디 없음
}
```

## 개발 프로세스

- 이슈 단계
  issues - boards(open, todo, doing, merged develop, merged master, close)
  - 'open' 단계에 앞으로 진행 될 이슈 생성(마일스톤, 작업자, 일정, 내용)
  - 스프린트 단위로 한 주가 시작되기 전 'open' -> 'todo' 상태 변경하여 해당 주의 스프린트가 시작 됨을 알림
  - 해당 작업자는 이슈 상태 'doing' 변경하여 이슈 해결 시작을 알림
  - /develop 브랜치를 기반으로 /feature/이슈번호 브랜치 생성하여 개발 시작
  - 개발 완료 후 /feature/이슈번호에 commit/push 후 merge request 생성
  - /feature/이슈번호 맞는 merge request 를 해당 팀원은 모두 코드를 확인하고 변경사항이 있다면 소스 위치에 수정내용 작성, 없다면 '확인 완료' 커맨트 작성
  - 작업자는 merge request 의 모든 커맨트를 확인하고 변경 작업 후에 완료했다는 커맨트를 등록, 'mark as resolved' 선택,
    만약 '확인 완료' 만 있다면 'mark as resolved' 선택하고 병합
  - 변경요청 한 팀원은 변경 된 내용을 확인하고 작업자의 커맨트에 'mark as resolved'
  - 모든 작업이 완료되었다면 /develop 브랜치로 병합
  - 해당 프로젝트의 빌드전(배포서버에서) slack의 해당 채널에 배포 시작을 모든 팀원에게 알리고, 해당 프로젝트 deploy를 시작
  - deploy가 모두 완료되면 slack의 해당 채널에 배포 완료를 모든 팀원에게 알림
  - 해당 테스크 상태 'merged develop' 변경
  - 테스트 진행
  - 위 내용은 스프린트(단위:1주) 단위로 이루어 지며 모든 이슈에 대해서 위와 같이 동일하게 반복

## 소스 버전 관리

- 해당 브랜치 구조는 git-flow 정책을 따름

- 브랜치 구조  
  feature - develop - release - tag - master - hotfix
  - feature : 테스크 단위 브랜치
  - develop : 전체 개발 단위 브랜치
  - release : 릴리즈 단위 브랜치
  - master : 전체 운영 단위 브랜치
  - hotfix : 전체운영 핫픽스 단위 브랜치
