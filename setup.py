# -*- coding: utf-8 -*-
from setuptools import setup

packages = [
    "somlier",
    "somlier.application",
    "somlier.application.ports",
    "somlier.application.ports.clients",
    "somlier.application.ports.repositories",
    "somlier.application.use_cases",
    "somlier.application.use_cases.offline",
    "somlier.application.use_cases.online",
    "somlier.application.use_cases.online.cleanup",
    "somlier.application.use_cases.online.deploy",
    "somlier.config",
    "somlier.config.bentoml",
    "somlier.config.mlflow",
    "somlier.core",
    "somlier.core.bentoml",
    "somlier.core.bentoml.mlflow",
    "somlier.external_interfaces",
    "somlier.external_interfaces.inbound",
    "somlier.external_interfaces.inbound.cli",
    "somlier.external_interfaces.inbound.web",
    "somlier.external_interfaces.outbound",
    "somlier.external_interfaces.outbound.clients",
    "somlier.external_interfaces.outbound.clients.cli",
    "somlier.external_interfaces.outbound.clients.rest",
    "somlier.external_interfaces.outbound.mlflow",
    "somlier.external_interfaces.outbound.repositories",
]

package_data = {"": ["*"]}

install_requires = [
    "BentoML>=0.13.0,<0.14.0",
    "dependency-injector>=4.37.0,<5.0.0",
    "fastapi[all]>=0.65.1,<0.66.0",
    "fire>=0.4.0,<0.5.0",
    "google-cloud-storage>=1.38.0,<2.0.0",
    "kubernetes>=17.17.0,<18.0.0",
    "loguru>=0.5.3,<0.6.0",
    "mlflow>=1.21.0,<2.0.0",
    "pandas>=1.2.0,<2.0.0",
    "pydantic>=1.8.1,<2.0.0",
    "python-dotenv>=0.17.1,<0.18.0",
    "scipy>=1.7.0,<1.8.0",
    "toml>=0.10.2,<0.11.0",
]

extras_require = {
    "all": [
        "socar-data-dag-builder @ " "git+ssh://git@github.com/socar-inc/socar-data-dag-builder.git@v0.3.14",
        "GitPython>=3.1.24,<4.0.0",
        "scikit-learn>=0.24.2,<0.25.0",
        "lightgbm==3.2.1",
        "torch>=1.8.0,<2.0.0",
    ],
    "lightgbm": ["lightgbm==3.2.1"],
    "offline": [
        "socar-data-dag-builder @ " "git+ssh://git@github.com/socar-inc/socar-data-dag-builder.git@v0.3.14",
        "GitPython>=3.1.24,<4.0.0",
    ],
    "sklearn": ["scikit-learn>=0.24.2,<0.25.0"],
    "torch": ["torch>=1.8.0,<2.0.0"],
}

entry_points = {"console_scripts": ["somlier = somlier.__main__:main"]}

setup_kwargs = {
    "name": "somlier",
    "version": "0.3.0",
    "description": "",
    "long_description": None,
    "author": "socar-hardy",
    "author_email": "hardy@socar.kr",
    "maintainer": None,
    "maintainer_email": None,
    "url": None,
    "packages": packages,
    "package_data": package_data,
    "install_requires": install_requires,
    "extras_require": extras_require,
    "entry_points": entry_points,
    "python_requires": ">=3.7.1,<3.9",
}

setup(**setup_kwargs)
