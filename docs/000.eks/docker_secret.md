
# 문제점

- Data collection 서비스 설정정보에 비밀번호 등 평문 저장은 security risk 이다.
- 환경변수는 에러 발생 후 디버깅 할때 로그에 노출 될 수 있고, 모든 process가 접근 가능하기 때문에
에 환경변수에 비밀번호 등을 평문 저장을 피해야함.

- 개선방법 1. my_secret.txt 텍스트파일에 분리하여 정의
- 개선방법 2. .env 파일에 분리하여 정의 (개선방법1.에 비해 취약)

## 개선방법 1.

- my_secret.txt 텍스트파일로 분리하여 정의
- https://docs.docker.com/compose/use-secrets/#simple

```
cat my_secret.txt
pa55w0rd_1
```

```yaml
version: '3.5'
services:
  data-collector:
    container_name: data-collector
    hostname: data-collector-001
    image: nginx:latest
    ports:
    - "11300:11300"
    - "11400:11400"
    environments:
      - FILE_SERVER_PASSWORD_FILE1: /run/secrets/my_secret
    volumes:
    - ./etc/my_rsa:/rsa_tv/my_rsa:rw
    secrets:
      - my_secret
secrets:
  my_secret:
    file: ./my_secret.txt
```


이렇게 정의하면 FILE_SERVER_PASSWORD_FILE1 이라는 환경변수에
/run/secrets/my_secret 경로가 저장이 되고, 애플리케이션은 이 경로를 통해
password등 정보에 접근하는 방식이다. 불가피하게 애플리케이션 코드의 수정이 필요하다.


## 개선방법 2.

1. .env 파일을 docker-compose.yaml와 같은 디렉토리에 정의

- docker-compse.yaml 파일은 default로 같은 디렉토리의 .env 파일을 로드하여 환경변수로 저장한다.
- 환경변수에 직접 password를 평문으로 저장하므로 개선방법 1. secret에 비해 취약하다.
- 기존과 같이 환경변수로 사용하므로, 애플리케이션 코드 수정은 필요없다.

- https://docs.docker.com/compose/environment-variables/set-environment-variables/#substitute-with-an-env-file

2.1. 환경변수를 .env파일에 정의

- .env 파일

```
FILE_SERVER_PASSWORD1=pa55w0rd
```

- docker-compose.yaml

```yaml
version: '3.5'
services:
  data-collector:
    container_name: data-collector
    hostname: data-collector-001
    image: nginx:latest
    ports:
    - "11300:11300"
    - "11400:11400"
    volumes:
    - ./etc/my_rsa:/rsa_tv/my_rsa:rw
    environment:
    - FILE_SERVER_PASSWORD1=${FILE_SERVER_PASSWORD1}
```

2.2. 파일명으로 환경변수 로드

- ssh-variable.env

```
FILE_SERVER_PASSWORD1=pa55w0rd_1
```

- ssh-variable.env.override

```
FILE_SERVER_PASSWORD1=pa55w0rd_2
```

```yaml
version: '3.5'
services:
  data-collector:
    container_name: data-collector
    hostname: data-collector-001
    image: nginx:latest
    ports:
    - "11300:11300"
    - "11400:11400"
    volumes:
    - ./etc/my_rsa:/rsa_tv/my_rsa:rw
    env_file:
    - ssh.variable.env
    - ssh-variable.env.override
```



# 결론


개선방안1.의 경우 모두 yaml에 평문으로 저장하는것을 다른 파일로 저장하는것 외에는 큰 차이는 없지만,
secret으로 정의하여 환경변수로 데이터가 노출되는 것을 방지 할 수 있으며, 로그로 노출도 방지 할 수 있다.
