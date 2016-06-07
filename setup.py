from setuptools import setup

setup(
    name='pycslog',
    version='0.0.1',
    description='Client-Server Ham Radio Contest Logger',
    url='http://github.com/neilmb/pycslog',
    author='Neil Martinsen-Burrell N0FN',
    author_email='neilmartinsenburrell@gmail.com',
    license='GPL',
    packages=['pycslog'],
    zip_safe=False,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Framework :: Flask",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Programming Language :: Python :: 2",
        "Topic :: Communications :: Ham Radio",
    ],
    install_requires=[
        'flask',
    ],
    test_require=[
        'nose',
        'rednose',
    ],
)
