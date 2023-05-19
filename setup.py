from setuptools import setup

setup(
    name='memory_graph',
    version='0.1.0',    
    description='Draws a graph of memory to understand the structure of references.',
    readme='README.md',
    url='https://github.com/bterwijn/memory_graph',
    author='Bas Terwijn',
    author_email='bterwijn@gmail.com',
    license='BSD 2-clause',
    packages=['memory_graph'],
    install_requires=['graphviz',],

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Education',
        'License :: OSI Approved :: BSD License',  
        'Programming Language :: Python :: 3',
        'Topic :: Multimedia :: Graphics',
    ],
)
