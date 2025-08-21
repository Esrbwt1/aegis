from setuptools import setup, find_packages

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read the contents of your requirements file
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

setup(
    name="aegis-ai",
    version="0.1.0",
    author="Esrbwt",
    author_email="esrbwt20@gmail.com",
    description="An automated AI fairness and bias auditing library.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Esrbwt1/aegis", 
    packages=find_packages(),
    include_package_data=True,  # This is crucial to include files specified in MANIFEST.in
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", # We will operate under the MIT license
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires='>=3.8',
    install_requires=requirements, # Use the dependencies from requirements.txt
)