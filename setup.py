from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(name='pyitm',
      version='0.1',
      description='Longley-Rice Irregular Terrain Model',
      long_description=readme(),
      url='https://github.com/tmd224/pyitm/tree/master/pyitm',
      download_url='https://github.com/tmd224/pyitm/archive/0.1.tar.gz',
      author='Mike DiSanto',
      author_email='tmdisanto@gmail.com',
      license='MIT',
      keywords=['Longley-Rice', 'ITM', 'RF Propagation', 'Terrain'],
      packages=['pyitm'],
      include_package_data=True,
      zip_safe=False,
      classifiers=[
                        'Development Status :: 3 - Alpha',
                        'Intended Audience :: Science/Research',
                        'License :: OSI Approved :: MIT License',
                        'Operating System :: Microsoft',
                        'Operating System :: POSIX :: Linux',
                        'Programming Language :: Python :: 3.4',
                        'Programming Language :: Python :: 3.5',
                        'Programming Language :: Python :: 3.6',
                        'Programming Language :: Python :: 3.7',
                        'Programming Language :: Python :: 3.8',
                        'Topic :: Scientific/Engineering',
                ],
      )
