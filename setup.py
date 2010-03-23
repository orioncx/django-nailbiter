from setuptools import setup, find_packages


setup(
    name='django-nailbiter',
    version='dev',
    description='thumbnail generation modeled after sorl-thumbnail, plays nice with storage backends',
    long_description=open('README.rst').read(),
    author='Matt Dennewitz, Image processors taken from sorl-thumbnail',
    author_email='mattdennewitz@gmail.com',
    url='http://github.com/blackbrrr/django-nailbiter',
    packages=find_packages(),
    zip_safe=False,
)

