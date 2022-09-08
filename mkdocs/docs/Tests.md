<p align="center">
  <img src="../images/soMLier_logo.png" width="200" />
</p>

<br>

# TEST

## 프로젝트 구조
```shell
tests
├── e2e #1
├── integration #2
├── load #3
├── unit #4
└── config #5
```

- `#1`: 시스템 e2e 테스트를 담습니다. docker-compose 기반으로 테스트합니다
- `#2`: integration 테스트는 외부 시스템과 소통하는 객체를 테스트합니다
- `#3`: 부하 테스트 케이스를 모아놓습니다
- `#4`: 유닛 테스트를 담습니다. Usecase 레이어 부터 테스트합니다.
- `#5`: 모델이 SoMLier 환경에서 실행되는지 확인합니다.


## e2e 테스트 방법
```shell
# e2e 환경을 준비합니다
make prepare-e2e-environment

# 준비된 e2e 환경에 접근합니다
make attach-e2e-environment

# e2e 테스트를 실행합니다
pytest tests/e2e
```

## integration 테스트 방법
주의: 외부 시스템과 소통하기 때문에 VPN 연결이 필요할 수 있습니다
```shell
pytest tests/integration
# or
make run-integration-test
```

## load 테스트 방법
```shell
# locust server를 실행합니다
python3 -m locust -f tests/load/locustfile.py
# or
make run-load-test-server
```

## unit 테스트 방법
```shell
python3 -m pytest tests/unit
# or
make run-unit-test
```

## config 테스트 방법
- config 및 dependencies를 확인합니다.
```shell
cd tests/config

somlier config show
# or
somlier config show -d
```

- somlier 환경에서 main.py 를 실행합니다.
```shell
cd tests/config

somlier config run main
```