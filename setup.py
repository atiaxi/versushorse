try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

# Important distutils stuff:
#   This file from https://docs.python.org/2/distutils/
#   https://python-packaging-user-guide.readthedocs.org/en/latest/distributing.html

setup(
    name="versushorse",
    version="1.0",
    description= "What can fight a horse and win?",
    author="Roger Ostrander",
    author_email="atiaxi@gmail.com",
    url="http://itcamefromwritingprompts.com",
    packages=['versushorse'],
    install_requires=[
        'flask>=0.10.1',
    ],
)
