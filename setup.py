from setuptools import setup

with open("requirements.txt") as f:
    reqs = f.read().strip().split("\n")
    
setup(
    name='multigenai',
    version='1.2.0',
    description='A module for generating AI responses using Bard and ChatGPT',
    author='Omkar Patel',
    author_email='omkarvpatel1234@gmail.com',
    packages=['multigenai'],
    install_requires=reqs,
)
