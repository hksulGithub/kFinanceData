
from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='kfinancedata',
    url='https://github.com/hksulGithub/kFinanceData',
    author='Hong Kee Sul',
    author_email='hksul@cau.ac.kr',
    # Needed to actually package something
    packages=['kFinanceData'],
    # Needed for dependencies
    install_requires=['pandas', 'pytz', 'requests'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='Python Package for Korean Financial Market Data',
    # We will also need a readme eventually (there will be a warning)
    # long_description=open('README.txt').read(),
)
