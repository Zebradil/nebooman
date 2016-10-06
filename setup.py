# vim:fileencoding=utf-8:noet

from setuptools import setup

setup(
    name='nebooman',
    description='Netscape Bookmark Manager',
    version='0.1',
    keywords='netscape bookmark manager',
    license='MIT',
    author='German Lashevich',
    author_email='german.lashevich@gmail.com',
    url='https://github.com/zebradil/nebooman',
    download_url='https://github.com/zebradil/nebooman/tarball/0.1',
    packages=['nebooman'],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Topic :: Terminals',
    ],
    scripts=[
        'scripts/nebooman',
    ]
)
