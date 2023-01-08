from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
long_description = (here / 'README.md').read_text(encoding='utf-8')

setup(
    name='imageconverter',
    version='1.0.0',
    description='Convert images from different format to selected one.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Arnaldo Ono',
    author_email='git@onoarnaldo.com',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.11',
    ],

    keywords='image converter',
    package_dir={'': 'src', 'imageconverter': 'src/imageconverter'},
    packages=find_packages(where='src'),
    python_requires='~=3.11',

    install_requires=['Pillow'],
    extras_require={
        'test': ['pytest'],
    },
)
