from setuptools import setup

# Hackishly inject a constant into builtins to enable importing of the
# package before the library is built.
import sys, os
if sys.version_info[0] < 3:
    import __builtin__ as builtins
else:
    import builtins
builtins.__KEPUTILS_SETUP__ = True
import keputils
version = keputils.__version__


# Publish the library to PyPI.
if "publish" in sys.argv[-1]:
    os.system("python setup.py sdist upload")
    sys.exit()

# Push a new tag to GitHub.
if "tag" in sys.argv:
    os.system("git tag -a {0} -m 'version {0}'".format(version))
    os.system("git push --tags")
    sys.exit()


def readme():
    with open('README.rst') as f:
        return f.read()

setup(name = "keputils",
    version = version,
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
