from setuptools import setup

setup(
    name='TUDASummerSchool',
    version='0.1.2',    
    description='Support Code for TUDA FL Lab',
    url='https://github.com/MarcoChilese/TUDASummerSchool22',
    author='TUDA',
    license='BSD 2-clause',
    packages=['TUDASummerSchool22'],
    install_requires=['numpy',                     
                      "torch",
                      "datetime", "Pillow"],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)