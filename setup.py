from setuptools import setup, find_packages

setup(
    name = 'iati.fetch',
    version = '0.1dev',
    description = 'IATI Python module for obtaining data and SSOT content using a network connection',
    author = 'IATI Technical Team and other authors',
    author_email = 'code@iatistandard.org',
    url='http://iatistandard.org/',
    packages = find_packages(exclude='iati/fetch/tests'),
    install_requires = [
        'iati.core==0.1dev'
        ],
    dependency_links=['https://github.com/IATI/iati.core/tarball/master#egg=iati.core-0.1dev'],
    classifiers = [
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Text Processing :: Markup :: XML'
        ],
)
