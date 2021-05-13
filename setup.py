# from distutils.core import setup
# from setuptools import find_packages
from setuptools import setup, find_packages

setup(
    name='fortosto',  # How you named your package folder (MyLib)
    #packages=find_packages(),  # Chose the same as "name"
    packages=['fortosto', 'fortosto.commons'],
    version='1.1.0',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description='csv 2 pg loader',  # Give a short description about your library
    author='halx4',  # Type in your name
    author_email='foivoschrist@outlook.com',  # Type in your E-Mail
    url='https://github.com/halx4/fortosto',  # Provide either the link to your github or to your website
    download_url='https://github.com/halx4/fortosto/archive/refs/tags/v1.0.0.tar.gz',  # I explain this later on
    keywords=['CSV', 'POSTGRES', 'LOAD'],  # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'psycopg2',
        'Unidecode',
        'dateparser',
    ],
    python_requires='>=3.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package

        'Intended Audience :: Developers',  # Define that your audience are developers
        'Intended Audience :: System Administrators',
        'Intended Audience :: Information Technology',

        'Topic :: Database',
        'Topic :: Software Development',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
