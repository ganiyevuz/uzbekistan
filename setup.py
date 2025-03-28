from setuptools import setup, find_packages

VERSION = '2.7.2'

# Read requirements
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

# Development dependencies
dev_requirements = [
    'pytest>=7.4.3',
    'pytest-django>=4.7.0',
    'pytest-cov>=4.1.0',
    'black>=23.11.0',
    'flake8>=6.1.0',
    'mypy>=1.7.1',
    'isort>=5.12.0',
    'django-stubs>=4.2.7',
    'djangorestframework-stubs>=3.14.5',
    'types-redis>=4.6.0.20240106',
]

setup(
    name='uzbekistan',
    version=VERSION,
    description='Django app for Uzbekistan administrative divisions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Jakhongir Ganiev',
    author_email='ganiyevuz@gmail.com',
    url='https://github.com/ganiyevuz/uzbekistan',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    extras_require={
        'dev': dev_requirements,
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 5.0',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    python_requires='>=3.8,<4.0',
    keywords=['django', 'uzbekistan', 'regions', 'districts', 'villages', 'api'],
    project_urls={
        'Documentation': 'https://github.com/ganiyevuz/uzbekistan',
        'Source': 'https://github.com/ganiyevuz/uzbekistan',
        'Tracker': 'https://github.com/ganiyevuz/uzbekistan/issues',
    },
)
