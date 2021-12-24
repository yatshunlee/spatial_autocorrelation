import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='spatial_autocorrelation',  # should match the package folder
    packages=['spatial_autocorrelation'],  # should match the package folder
    version='0.0.1-alpha',  # important for updates
    license='MIT',  # should match your chosen license
    description='Topological spatial autocorrelation analysis',
    long_description=long_description,  # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    author='Lee Yat Shun, Jasper',
    author_email='yatshunlee@gmail.com',
    url='https://github.com/yatshunlee/spatial_autocorrelation',
    project_urls={  # Optional
        "Bug Tracker": "https://github.com/yatshunlee/spatial_autocorrelation/issues"
    },
    install_requires=['requests'],  # list all packages that your package uses
    keywords=[
        "pypi", "spatial_autocorrelation", "Moran's I", "LISA", "geometrical", "topological",
        "spatial autocorrelation", "spatial correlation", "correlation", "spatial weighted matrix"
    ],  # descriptive meta-data
    classifiers=[  # https://pypi.org/classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],

    download_url="https://github.com/yatshunlee/spatial_autocorrelation/archive/refs/tags/v0.0.1-alpha.tar.gz",
)