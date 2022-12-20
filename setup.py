from setuptools import setup, find_packages

setup(name='webScrap',
      version='3.0',
      url='https://github.com/ajcltm/webScrap',
      license='jnu',
      author='ajcltm',
      author_email='ajcltm@gmail.com',
      description='',
      packages=find_packages(exclude=['test']),
      zip_safe=False,
      setup_requires=['requests>=1.0'],
      test_suite='')