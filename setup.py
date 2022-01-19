import setuptools

VERSION = "0.0.4"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="matplotview",
    version=VERSION,
    author="Isaac Robinson",
    author_email="isaac.k.robinson2000@gmail.com",
    description="A library for creating lightweight views of matplotlib axes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/isaacrobinson2000/matplotview",
    project_urls={
        "Bug Tracker": "https://github.com/isaacrobinson2000/matplotview/issues",
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Matplotlib',
        'License :: OSI Approved :: Python Software Foundation License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Scientific/Engineering :: Visualization',
        'Operating System :: OS Independent',
    ],
    license="PSF",
    install_requires=[
        "matplotlib>=3.5.1"
    ],
    packages=["matplotview"],
    python_requires=">=3.7",
    platforms="any"
)