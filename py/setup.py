from setuptools import setup, find_packages
from os import path

def makePackage(prefix='',name='',keyword='',suffix='*'):
    
    here = path.abspath(path.curdir)
    with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
    scripts=[path.join(here,f'src/parse_{suffix}') ]
    
    packages=[x for x in find_packages('src') if x.startswith(prefix)]
    print(f'Packages is "{packages}"')

    setup(
        name=name,
        version='0.2.1',
        description=f'A simple {keyword} File parser',
        long_description=long_description,
        author='Julian Porter',
        author_email='julian@porternet.org',
        classifiers=[
            'Development Status :: 4 - Beta',
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Intended Audience :: Other Audience',
            'License :: OSI Approved :: MIT License',
            'Natural Language :: English',
            'Operating System :: MacOS',
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.6',
            'Programming Language :: Python :: 3.7',
            'Programming Language :: Python :: 3.8',
             'Programming Language :: Python :: 3.9',
            f'Topic :: Multimedia :: Sound/Audio :: {keyword}'
        ],
        keywords=keyword,
        packages=packages,
        python_requires='>=3.6, <4',
        package_dir={
            '':'src'
        },
        package_data={
            'data': [f'*.{suffix}']
        },
        data_files=[('/usr/local/bin',scripts)]
    )

# case 1
makePackage(prefix='FLP',name='FLPFile',keyword='FL Studio Project',suffix='flp')
# case 2
makePackage(prefix='MIDI',name='MIDIFile',keyword='MIDI',suffix='mid')

setup(
    name='MIDIFile',
    version='0.2.0',
    description='A simple MIDI File parser',
    long_description=long_description,
    author='Julian Porter',
    author_email='julian@porternet.org',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Multimedia :: Sound/Audio :: MIDI'
    ],
    keywords='MIDI',
    packages=packages,
    python_requires='>=3.6, <4',
    package_dir={
        '':'src'
    },
    package_data={
        'data': ['*.mid','*.lp']
    },
    data_files=[('/usr/local/bin',scripts)]
)


