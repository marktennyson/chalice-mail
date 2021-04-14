import io
import re
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
    description="SMTP mail integration with AWS Chalice",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["chalice", "email", "smtp mail", 'aws'],
    packages=["chalice_mail"],
    zip_safe=False,
    platforms="any",
    install_requires=[ 
    ],
    extras_require={},
    python_requires=">=3.6,<4",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        # "Framework :: chalice",
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