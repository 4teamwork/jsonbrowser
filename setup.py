from setuptools import setup, find_packages
import os

version = '0.1.dev0'

tests_require = [
    'unittest2',
]

setup(
    name='jsonbrowser',
    version=version,
    description='JSONBrowser',
    long_description=open('README.rst').read() + '\n' +
    open(os.path.join('docs', 'HISTORY.txt')).read(),

    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],

    keywords='',
    author='Lukas Graf',
    author_email='mailto:lukas.graf.bern+github@gmail.com',
    url='https://github.com/lukasgraf/jsonbrowser',
    license='GPL2',

    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=[],
    include_package_data=True,
    zip_safe=False,

    install_requires=[
        'setuptools',
        'Flask',
        'Flask-Bootstrap',
    ],

    tests_require=tests_require,
    extras_require=dict(tests=tests_require),

    entry_points='''
    # -*- Entry points: -*-
    [console_scripts]
    run-jsonbrowser = jsonbrowser.flask_app:run_server
    ''',
)
