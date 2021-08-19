from setuptools import setup

requires = [
    'requests>=2.19.1',
    'aiohttp>=3.7.4'
]

test_requirements = [
    'pytest-mock>=3.5.1',
    'pytest>=6.2.2',
    'pytest-asyncio>=0.14.0'
]

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='passpwnedcheck',
    version='2.0.0',
    description='Test for pwned password',
    author='Nguyen Thai Duong',
    author_email='duongnt.bk@gmail.com',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/duongntbk/passpwnedcheck',
    packages=['passpwnedcheck'],  #same as name
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=requires,
    tests_require=test_requirements,
)