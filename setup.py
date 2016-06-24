
from setuptools import setup, find_packages

version = open('facsimile/VERSION').read().strip()
requirements = open('facsimile/requirements.txt').read().split("\n")
test_requirements = open('facsimile/requirements-test.txt').read().split("\n")


setup(
    name='pluginmgr',
    version=version,
    author='20C',
    author_email='code@20c.com',
    description='lightweight python plugin system supporting config inheritance',
    long_description='',
    license='LICENSE.txt',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
    ],
    packages = find_packages(),
    include_package_data=True,


    url='https://github.com/20c/pluginmgr',
    download_url='https://github.com/20c/pluginmgr/%s' % version,


    install_requires=requirements,
    test_requires=test_requirements,

    zip_safe=True
)
