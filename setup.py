from setuptools import setup, find_packages

requires = [
    'tropofy',
]

setup(
    name='tropofy-anagram',
    version='1.0',
    description='This is a Tropofy example package',
    author='Elizabeth Alpert; Tropofy',
    url='http://www.tropofy.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires,
)
