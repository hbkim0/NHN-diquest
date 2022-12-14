# docker 실행 및 그 외 명령어
'''
docker run ubuntu:20.04 # 다운로드 및 실행 후 바로 죽음-> 아무것도 하라는 명령어가 없어서

docker run --rm -it ubuntu:20.04 /bin/sh # shell command로 접근 (ubuntu의 shell)
    # --rm 옵션이 없으면 컨테이너 종료되더라도 남아있어서 수동으로 삭제해야 함
    
docker run -d --rm -p 1111:1112 hashicorp/http-echo -text="hello world"
    # hashicorp 컨테이너와 pc 5678가 연결 
    # -d : 컨테이너를 background 실행

docker exec -it mysql mysql 
    # exec 명령어는 run과 달리 실행중인 도커 컨테이너에 접속할 때 사용
    # mysql의 mysql 클라이언트를 실행
    # show databases
    
docker ps
    # docker 컨테이너 리스트 보여줌
    # -a 옵션을 주면 중지된 컨테이너도 보여줌
    
docker stop [container_ID(여러 개 붙여서 사용 가능)]
    # 컨테이너 멈춤
    
docker rm [container_ID(여러 개 붙여서 사용 가능)]
    # 컨테이너 삭제
    
docker logs [options] [container_ID]
    # log 확인
    # -f 옵션을 붙이면 추가적인 log들도 볼 수 있음

docker images [options]
    # 도커가 다운로드한 이미지 목록 보여줌

docker pull [options] NAME[:TAG]
    # 도커 이미지 다운로드

docker rmi [options] [IMAGE_ID]
    # 도커 이미지 삭제

docker network create [OPTIONS] NETWORK
    # 도커 컨테이너끼리 이름으로 통신할 수 있는 가상 네트워크 생성
    
-v /my/own/datadir:/var/lib/mysql 
    # 볼륨 마운트
    
### Exam 1. nginx 컨테이너 만들기

    **index.html**
        hello world
    
    **run**
        $ docker run -d --rm \
        -p 50000:80 \
        -v $(pwd)/index.html:/usr/share/nginx/html/index.html \
        nginx

'''


# docker compose (docker-compose.yml)
'''
docker-compose up
    # 실행
    
docker-compose down
    # 종료하고 삭제
    
docker-compose start or start xx
    # 멈춘 컨테이너 실행 / xx 컨테이너만 실행

docker-compose restart or restart xx
    # 멈춘 컨테이너 재실행 / xx 컨테이너만 재실행

docker-compose stop
    # 정지

docker-compose logs or logs -f
    # 컨테이너의 로그 / 로그 follow
    
docker-compose ps
    # 컨테이너 목록
    
docker-compose exec {컨테이너 이름} {명령어}
    # 실행 중인 컨테이너에서 명령어 실행
    
version: '2' # docker-compose.yml 버전
services: # 실행할 컨테이너 정의 -> docker run --name xx 와 같다고 생각하면 됨
    db:
        image: mariadb:10.9 # 이미지가 없으면 자동으로 pull / 태그가 없으면 latest
        volumes: # 데이터가 유실되지 않도록
            - ./mysql:/var/lib/mysql {호스트 디렉토리}:{컨테이너 디렉토리}
        restart: always # 컨테이너가 죽게 되면 자동으로 띄워줌
        environment: # 컨테이너에 사용할 환경변수들
            MYSQL_ROOT_PASSWORD: wordpress
            MYSQL_DATABASE: wordpress
            MYSQL_USER: wordpress
            MYSQL_PASSWORD: wordpress
    wordpress:
        image: wordpress:latest
        volumes:
            - ./wp:/var/www/html
        ports:
            - "8000:80" # {호스트 포트}:{컨테이너 포트}
        restart: always
        environment:
            WORDPRESS_DB_HOST: db:3306
            WORDPRESS_DB_PASSWORD: wordpress
    django:
        build:
            context: .
            dockerfile: ./compose/django/Dockerfile-dev
'''

# docker 이미지
'''
이미지는 프로세스가 실행되는 파일들의 집합(환경)

Base Image는 수정 불가능

docker commit git ubuntu:git 
    # git이라는 컨테이너를 이미지로 변경

이미지 만들기 순서
    1. Base Image
    2. Container 화 시키기
    3. docker commit을 통해 Custom Image 만듦

Dockerfile 핵심 명령어
    FROM : Base image
    RUN : 쉘 명령어 실행
    CMD : 컨테이너 기본 실행 명령어(Entrypoint 인자로 사용)
    EXPOSE : 오픈되는 포트 정보
    ENV : 환경변수 설정
    ADD : 파일 또는 디렉토리 추가
    COPY : 파일 또는 디렉토리 추가
    ENTRYPOINT : 컨테이너 기본 실행 명령어
    VOLUME : 외부 마운트 포인트 생성
    USER : RUN, CMD, ENTRYPOINT를 실행하는 사용자
    WORKDIR : 작업 디렉토리 설정
    ARGS : 빌드타임 환경변수 설정
    LABEL : key-value 데이터
    ONBUILD : 다른 빌드의 베이스로 사용될 때 사용하는 명령어

이미지 빌드하기

    docker build -t {이미지명:이미지태그} {빌드 컨텍스트}
        # 현재 디렉토리의 dockerfile로 빌드
    
    dockerignore
        # .gitignore와 비슷한 역할
'''