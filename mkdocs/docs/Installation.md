### Requirements
- Python >=3.7, <3.9
- SSH key for github organization


### 설치
- SoMLier를 다운로드 합니다 <br>

**pip 사용**
 
    $ pip install --user git+https://github.com/socar-inc/socar-data-soMLier.git@develop
    $ pip install --user git+https://github.com/socar-inc/socar-data-soMLier.git@$version이름


**From source**

    # clone
    $ git clone git@github.com:socar-inc/socar-data-soMLier.git
    
    # or
    $ git clone https://github.com/socar-inc/socar-data-soMLier.git
    
    # and move to the directory
    $ cd socar-data-soMLier

    # install
    $ pip install -e .
    
    # or use poetry
    $ poetry install
