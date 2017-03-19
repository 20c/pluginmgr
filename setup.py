
from setuptools import setup, find_packages

VERSION = open('facsimile/VERSION').read().strip()
REQUIREMENTS = open('facsimile/requirements.txt').read().split("\n")
TEST_REQUIREMENTS = open('facsimile/requirements-test.txt').read().split("\n")


setup(
    name='pluginmgr',
    version=VERSION,
    author='20C',
    author_email='code@20c.com',
    description='lightweight python plugin system supporting config inheritance',
    long_description='',
    license='LICENSE.txt',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(),
    include_package_data=True,

    url='https://github.com/20c/pluginmgr',
    download_url='https://github.com/20c/pluginmgr/%s' % VERSION,

    install_requires=REQUIREMENTS,
    test_requires=TEST_REQUIREMENTS,

    zip_safe=True
)
