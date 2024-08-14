from setuptools import setup, find_packages

setup(
    name='sage_sdk',
    version='1.0',
    packages=find_packages(),
    install_requires=[],
    author='Nyasha Chizampeni',
    author_email='nchizampeni@gmail.com',
    description='Description of your package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/Petalm-Africa/sage-sdk.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
