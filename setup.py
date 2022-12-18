from setuptools import setup, find_packages

with open("requirements.txt") as install_requires_file:
    requirements = install_requires_file.read().strip().split("\n")

setup(
    name="prefect_utils",
    description="Prefect shared utility modules",
    license="Apache License 2.0",
    author="Prefect Community",
    author_email="hello@prefect.io",
    keywords="prefect",
    packages=find_packages(exclude=["tests"]),
    version="1.0",
    python_requires=">=3.8",
    install_requires=requirements,
    classifiers=[
        "Natural Language :: English",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries",
    ],
)
