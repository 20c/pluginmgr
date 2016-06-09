
from setuptools import find_packages, setup

version = open('facsimile/VERSION').read().strip()
requirements = open('facsimile/requirements.txt').read().split("\n")
test_requirements = open('facsimile/requirements-test.txt').read().split("\n")

setup(
    name='pluginmgr',
    version=version,
    author='20C',
    author_email='code@20c.com',
    description='a simple dynamic module manager',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages = find_packages(),
    url='https://github.com/20c/pluginmgr',
    download_url='https://github.com/20c/pluginmgr/%s' % version,
    install_requires=requirements,
    test_requires=test_requirements,
    zip_safe=True,
)

