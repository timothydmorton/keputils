from setuptools import setup

def readme():
    with open('README.rst') as f:
        return f.read()

setup(name = "keputils",
    version = "0.2.1",
    description = "Basic module for interaction with KOI and Kepler-stellar tables.",
    long_description = readme(),
    author = "Timothy D. Morton",
    author_email = "tim.morton@gmail.com",
    url = "https://github.com/timothydmorton/keputils",
    packages = ['keputils'],
    scripts = ['scripts/koiquery'],
    #entry_points = {'console_scripts' : ['koiquery = koiquery:main']},
    classifiers=[
      'Development Status :: 3 - Alpha',
      'Intended Audience :: Science/Research',
      'Operating System :: OS Independent',
      'Programming Language :: Python',
      'Topic :: Scientific/Engineering',
      'Topic :: Scientific/Engineering :: Astronomy'
      ],
    install_requires=['pandas>=0.13','simpledist'],
    zip_safe=False
) 
