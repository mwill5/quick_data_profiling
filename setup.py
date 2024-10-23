from setuptools import setup

setup(
    name='quick_data_profiling',
    version='1.0.0',
    description='A comprehensive data profiling tool for exploratory data analysis.',
    author='Myles Williams',
    author_email='mylesm.w@outlook.com',
    url='https://github.com/mwill5/quick_data_profiling',
    license='MIT',
    packages=['quick_data_profiling'],
    include_package_data=True,
    install_requires=[
        'pandas',
        'numpy',
        'matplotlib',
        'seaborn',
        'jinja2',
    ],
    entry_points={
        'console_scripts': [
            'quickprof = quick_data_profiling.quick_data_profiling:main',
        ],
    },
)
