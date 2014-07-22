from setuptools import setup


setup(
    name='streamScript',
    version='0.1-dev',
    description='streamScript',
    long_description='A Flask app that uses sentiment analysis',
    url='https://github.com/lnhubbell/tweetTrack',
    # Author details
    author='Ian Auld, Nathan Hubbell, Corinne ',
    author_email='imauld@gmail.com',
    # Choose your license
    #   and remember to include the license text in a 'docs' directory.
    license='MIT',
    packages=['streamScript'],
    install_requires=[
            'setuptools',
            'Flask',
            'pytest'
    ]
)
