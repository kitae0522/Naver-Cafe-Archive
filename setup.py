from setuptools import setup, find_packages
from spdlqj import NaverCafeArchive
import os


def long_description() -> str:
    with open(f'{os.getcwd()}/README.md', 'r', encoding='utf-8') as f:
        return f.read()


setup(
    name='spdlqj',
    version=NaverCafeArchive.__version__,
    url='https://github.com/kitae0522/Naver-Cafe-Archive',
    author='Ted Song',
    author_email='kitae040522''@''gmail.com',
    description='🇰🇷 Naver Cafe Archive Module',
    long_description=long_description(),
    long_description_content_type='text/markdown',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'setuptools',
        'requests',
        'pandas'
    ],
    classifiers=[]
)
