import os

from setuptools import setup, find_packages

from blogsley_setup.install import install
from blogsley_setup.develop import develop

with open("README.md", "r") as fh:
    long_description = fh.read()
    
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

datadir = 'share/blogsley'
data_files = [(d, [os.path.join(d,f) for f in files])
    for d, folders, files in os.walk(datadir)]

packages = find_packages(exclude=["__blogsley__", "tests"])

setup(
    name='blogsley',
    packages=packages,
    include_package_data=True,
    data_files=data_files,
    use_scm_version = {
        "local_scheme": "no-local-version",
        'write_to': 'blogsley/version.py',
        'write_to_template': 'version = "{version}"',
        'tag_regex': r'^(?P<prefix>v)?(?P<version>[^\+]+)(?P<suffix>.*)?$'
    },
    setup_requires=['setuptools_scm'],
    cmdclass={
        'install': install,
        'develop': develop
    },
    install_requires=requirements,
    entry_points={"console_scripts": ["blogsley = blogsley.command:cli"]},
    author="Kurtis Fields",
    author_email="kurtisfields@gmail.com",
    description="Web Publishing Evolved",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/blogsley/blogsley",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)