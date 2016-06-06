from setuptools import setup


setup(
    name='kociemba',
    version='1.1',
    description='Python/C implementation of Herbert Kociemba\'s Two-Phase algorithm for solving Rubik\'s Cube',
    keywords='kociemba rubik cube solver twophase',
    url='https://github.com/muodov/kociemba',
    author='muodov',
    author_email='muodov@gmail.com',
    license='GPLv2',
    packages=['kociemba'],
    package_data={
        '': [
            'cprunetables/*',
            'pykociemba/*.py',
            'pykociemba/prunetables/*',
            'ckociemba/include/*.h',
            'ckociemba/*.c'],
    },
    classifiers=(
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
    ),
    entry_points = {
        'console_scripts': ['kociemba=kociemba.command_line:main'],
    },
    setup_requires=['pytest-runner', "cffi>=1.0.0"],
    tests_require=['pytest', ],
    zip_safe=False,
    cffi_modules=["kociemba/build_ckociemba.py:ffi"],
    install_requires=["cffi>=1.0.0", 'future'],
)
