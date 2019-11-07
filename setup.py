import setuptools
import versioneer
from distutils.sysconfig import get_python_lib

with open("README.md", "r") as fh:
    long_description = fh.read()

p = get_python_lib
setuptools.setup(
    name="fraudfeature",
    author="denise",
    author_email="fancm@craiditx.com",
    url="https://git.creditx.com/JH2019/fraudfeature",
    long_description=long_description,
    long_description_content_type="text/markdown",    
    packages=setuptools.find_packages(),
    package_data={'fraudfeature': ['util/district-*']},
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass())
