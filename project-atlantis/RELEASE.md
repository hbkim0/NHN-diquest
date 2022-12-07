# Release
> project-atlantis의 relase 방법

**(Step 1)** release branch 생성

* github에서 `release/vx.y.z` 로 branch 생성
* 각 service, ui에 `vx.y.z-rc`로 versioning

**(Step 2)** clone and checkout

* local에서 `project-atlantis` clone 및 release branch로 checkout
```console
$ git clone git@github.com:ai-dq/project-atlantis.git
$ cd project-atlantis
project-atlantis$ git checkout -t origin/release/vx.y.z
```

**(Step 3)** tutorbot-chatting-ui의 config 수정

* local에서 실행되는 `scoring-service`와 `tutorbot-auth-serivce`를 사용하기 위해서 config를 아래와 같이 수정
* `tutorbot-chatting-ui/src/config/config.json`
```json
{
    ...,
    "IMAGE_API_URL":"http://localhost:9980",
    "TUTORBOT_AUTH_API_URL": "http://localhost:9950"
}
```

**(Step 4)** install *(and build)*

* `scoring-service` and `tutorbot-auth-serivce`
```console
project-atlantis$ cd scoring-service ; poetry install ; cd -
project-atlantis$ cd tutorbot-auth-service ; poetry install ; cd -
```

* `scoring-admin`
```console
project-atlantis$ cd scoring-admin-ui ; npm install ; cd -
```

* `tutorbot-chatting-ui`
```console
project-atlantis$ cd tutorbot-chatting-ui ; npm install ; npm run dev ; cd -
```

**(Step 5)** run dev servers

* 4개의 terminal을 실행하여 아래 command를 각각 실행 함.
```console
$ cd project-atlantis/scoring-service ; poetry run python manage.py runserver
$ cd project-atlantis/tutorbot-auth-service ; poetry run python manage.py runserver
$ cd project-atlantis/scoring-admin-ui ; npm run serve
$ cd project-atlantis/tutorbot-chatting-ui ; npm run local
```

**(Step 6)** Sanity Test

* Test case: https://diquest.dooray.com/project/pages/3351462441237337835
* Test results: `vx.y.z-rc` 로 페이지를 생성하고, 테스트 결과를 작성
  * 테스트 결과 NG인 경우, issue를 생성함.
  * 참조: https://diquest.dooray.com/project/pages/3355703668469797166

**(Step 7)** Bug fix 및 확인

* 이전 단계에서 issue가 있다면, 담당자는 수정하고 `release/vx.y.z` 에 push 함.

**(Step 8)** release condidate 검토 및 merge

* 모든 issue가 해결(fixed, diferred, 등)되면, <br>
  release branch를 `master` 및 `production` branch로 merge
* `production` branch에 tag(`vx.y.z`) 생성
