from setuptools import setup, find_packages
from sys import version

if version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

setup(
    name='aweber_api',
    version='1.1.4',
    author='AWeber Dev Team',
    author_email='api@aweber.com',
    maintainer='AWeber API Team',
    maintainer_email='api@aweber.com',
    url='https://github.com/aweber/AWeber-API-Python-Library',
    download_url='http://pypi.python.org/pypi/aweber_api',
    description='A python client library for the AWeber API.',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: BSD License',
    ],
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'httplib2>=0.7.0,<=0.8.0',
        'oauth2>=1.2',
    ],
    tests_require=[
        'dingus',
        'coverage',
    ],
    setup_requires=[
        'nose',
    ],
    include_package_data=True
)
