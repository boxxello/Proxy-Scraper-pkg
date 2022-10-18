import re
import ast
from setuptools import setup, find_packages

with open('README.md'.upper()) as readme_file:
    readme = readme_file.read()

_version_re = re.compile(r'__version__\s+=\s+(.*)')

with open('proxy_scraper/__init__.py', 'rb') as f:
    version = str(ast.literal_eval(_version_re.search(
        f.read().decode('utf-8')).group(1)))

requirements = [
    'geoip2==4.6.0',
    'gevent==22.10.1',
    'retrying==1.3.3',
    'fake-useragent==0.1.11',

]

setup(
    name='Proxy-Scraper-pkg',
    version=version,
    description="A simple but effective proxy scraper and validator ",
    long_description=readme,
    author="boxxello",
    author_email='francesco.boxxo@gmail.com',
    url='https://github.com/boxxello/Proxy-Scraper-pkg',
    packages=find_packages(),
    package_dir={},
    entry_points={
        'console_scripts': [
            'proxy_scraper=proxy_scraper.main:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License",
    platforms='any',
    zip_safe=False,
    keywords='proxy_scraper',
    classifiers=[
        'Development Status :: 0.1 - Alpha',
        'Intended Audience :: Developers',
        'Environment :: Console',
        'Operating System :: POSIX',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Topic :: Internet :: WWW/HTTP :: Indexing/Search',
        'Topic :: Internet :: Proxy Servers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
