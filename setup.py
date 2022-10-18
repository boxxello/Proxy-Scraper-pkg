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

]

setup(
    name='getproxy',
    version=version,
    description="get proxy",
    long_description=readme,
    author="boxxello",
    author_email='francesco.boxxo@gmail.com',
    url='https://github.com/fate0/getproxy',
    packages=find_packages(),
    package_dir={},
    entry_points={
        'console_scripts': [
            'proxy_scraper=proxy_scraper.main:main'
        ]
    },
    include_package_data=True,
    install_requires=requirements,
    license="MIT license",
    zip_safe=False,
    keywords='proxy_scraper',
    classifiers=[
        'Development Status :: 0.1 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
