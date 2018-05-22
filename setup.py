from setuptools import setup

setup(name='aiocsv',
      version='0.0.1',
      description='A Python csv parser for asyncio',
      url='https://github.com/AndrewLester/aiocsv',
      author='Andrew Lester',
      license='MIT',
      packages=['aiocsv'],
      install_requires=['aiofiles'],
      zip_safe=False)
