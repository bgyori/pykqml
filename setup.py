from setuptools import setup

setup(name='pykqml',
    version='1.2',
    packages=['kqml'],
    keywords=['kqml', 'agent', 'nlp', 'communication', 'dialogue'],
    url='http://github.com/bgyori/pykqml',
    author='Benjamin M. Gyori',
    author_email='benjamin_gyori@hms.harvard.edu',
    description='KQML messaging classes in Python.',
    long_description=open('README.rst', 'r').read(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        ]
)
