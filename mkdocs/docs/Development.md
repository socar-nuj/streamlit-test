<p align="center">
  <img src="../images/soMLier_logo.png" width="200" />
</p>

<br>

## 개발

### 설치 및 세팅

```bash
# 소스 코드 Clone
$ git clone git@github.com:socar-inc/socar-data-soMLier.git
$ cd socar-data-soMLier

# 파이썬 버전 세팅
$ pyenv shell 3.8.7

# 필요한 패키지 설치
$ poetry install

# pre commit hook 설치
$ pre-commit install --hook-type commit-msg
```

<br>

### 브랜치 규칙

- 본인 브랜치를 만들어 작업합니다.
- PR & Merge로 작업한 내용을 합칩니다.
- 머지 규칙은 다음과 같습니다.
  - `develop` <- `feature` : Squash & Merge
  - `main` <- `develop` : Rebase & Merge

<br>

### 커밋 규칙

[Commitizen](https://commitizen-tools.github.io/commitizen/) 을 이용하여 개발합니다.
사용법은 다음과 같습니다.

```bash
$ git add ...
$ cz c
```

커밋 및 버지닝 방법은 [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) 규칙을 따릅니다.

<br>


### 배포 규칙

- 마찬가지로 [Commitizen](https://commitizen-tools.github.io/commitizen/) 을 이용하여 배포합니다.
- `main` 브랜치에 push 되면 GitHub Action이 동작하여 버전 태그와 `CHANGELOG.md` 를 만듭니다.
- 버전이 태그되면 BuddyWorks가 동작하여 GCR에 이미지를 빌드합니다.