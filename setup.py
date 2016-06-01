from distutils.core import setup

setup(name='momobot',
      version='1.0',
      packages=[''],
      description='Slack bot to manage Polls',
      long_description=long_description,
      license='MIT',
      url='https://github.com/axelroy/slackMomoBot',
      packages=find_packages(),
      install_requires=['aiohttp']
      )
