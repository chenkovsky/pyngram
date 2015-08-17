__author__ = 'chenkovsky'

from setuptools import setup, find_packages,Extension
module_ngram = Extension('libngram',
                    sources = ['murmur_hash.c', "hash_vocab.c", "ngram.c",'murmur_hash.h', "hash_vocab.h", "ngram.h"])

setup(
    name = "pyngram",
    version = "1.0",
    keywords = ('ngram', 'language model'),
    description = 'high performance language model query',
    license = 'MIT License',
    url = 'http://github.com/chenkovsky/pyngram',

    author = 'chenkov',
    author_email = 'chenkov@yeah.net',

    packages = find_packages(),
    package_data = {'': ['*.*']},
    include_package_data = True,
    platforms = 'any',
    install_requires = [],
    ext_modules = [module_ngram]
)