from chalice_mail import __version__ as version

from setuptools import setup


with open("README.md", "r") as f:
    long_description = f.read()


setup(
    name="chalice-mail",
    version=version,
    url="https://github.com/marktennyson/chalice-mail",
    license="MIT",
    author="Aniket Sarkar",
    author_email="aniketsarkar@yahoo.com",
    description="SMTP and SES mail integration with AWS Chalice",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["chalice", "email", "smtp mail", 'aws', 'ses'],
    packages=["chalice_mail"],
    zip_safe=False,
    platforms="any",
    install_requires=[ 
        'appdirs==1.4.4',
        'attrs==20.3.0',
        'blessed==1.17.6',
        'blessings==1.7',
        'boto3==1.17.52',
        'botocore==1.20.52',
        'certifi==2020.12.5',
        'chalice==1.22.3',
        'chardet==4.0.0',
        'click==7.1.2',
        'codecov==2.1.11',
        'coloredlogs==15.0',
        'colour-runner==0.1.1',
        'coverage==5.5',
        'deepdiff==5.2.3',
        'distlib==0.3.1',
        'filelock==3.0.12',
        'humanfriendly==9.1',
        'idna==2.10',
        'inquirer==2.7.0',
        'Jinja2==2.11.3',
        'jmespath==0.10.0',
        'MarkupSafe==1.1.1',
        'mypy-extensions==0.4.3',
        'ordered-set==4.0.2',
        'packaging==20.9',
        'pluggy==0.13.1',
        'py==1.10.0',
        'Pygments==2.8.1',
        'pyparsing==2.4.7',
        'python-dateutil==2.8.1',
        'python-editor==1.0.4',
        'PyYAML==5.4.1',
        'readchar==2.0.1',
        'requests==2.25.1',
        'rootpath==0.1.1',
        's3transfer==0.3.7',
        'six==1.15.0',
        'termcolor==1.1.0',
        'toml==0.10.2',
        'tox==3.23.0',
        'urllib3==1.26.4',
        'virtualenv==20.4.3',
        'wcwidth==0.2.5',
    ],
    extras_require={},
    python_requires=">=3.6,<4",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)