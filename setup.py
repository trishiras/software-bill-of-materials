from setuptools import setup
from software_bill_of_materials.__version__ import __version__


setup(
    name="software_bill_of_materials",
    version=__version__,
    author="sumit",
    author_email="sumit@mail.com",
    description="software-bill-of-materials",
    long_description=open("README.md").read(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.12",
    entry_points={
        "console_scripts": [
            "software_bill_of_materials=software_bill_of_materials.main:main",
        ],
    },
)
