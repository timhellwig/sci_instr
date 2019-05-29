import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sci_instr",
    version="0.0.1",
    author="Tim Hellwig",
    author_email="tim.hellwig@gmail.com",
    description="VISA communication with scientific instruments",
    url="https://github.com/timhellwig/sci_instr",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)