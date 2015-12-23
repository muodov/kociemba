from setuptools import setup


setup(
    name='kociemba',
    version='1.0',
    description='Python/C implementation of Herbert Kociemba\'s Two-Phase algorithm for solving Rubik\'s Cube',
    keywords='kociemba rubik cube solver twophase',
    url='https://github.com/muodov/kociemba',
    author='muodov',
    author_email='muodov@gmail.com',
    license='GPLv2',
    packages=['kociemba'],
    package_data={
        '': ['cprunetables/*', 'pykociemba/**/*'],
    },
    zip_safe=False,
    setup_requires=["cffi>=1.0.0"],
    cffi_modules=["kociemba/build_ckociemba.py:ffi"],
    install_requires=["cffi>=1.0.0"],
)
