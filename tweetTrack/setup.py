from setuptools import setup


setup(
    name='tweetTrack',
    version='0.1-dev',
    description='tweetTrack',
    long_description='A Flask app that uses sentiment analysis',
    url='https://github.com/lnhubbell/tweetTrack',
    # Author details
    author='Ian Auld, Nathan Hubbell, Corinne ',
    author_email='imauld@gmail.com',
    # Choose your license
    #   and remember to include the license text in a 'docs' directory.
    license='MIT',
    packages=['tweetTrack'],
    install_requires=[
            'setuptools',
            'Flask',
            'Flask-WTF',
            'Flask-SQLAlchemy',
            'requests',
            'pytest'
    ]
)
