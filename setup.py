import os

from setuptools import find_namespace_packages, setup


setup(
    name="imbalance_analysis",
    version='0.1',
    packages=find_namespace_packages(),
    include_package_data=True,
    description="daily reporting tool for analysing electricity system imbalance costs and prices using BMRS data",
    author="Saeed Bidi",
    author_email="saeed.bidi@qmul.ac.uk",
    python_requires=">=3.8",
    install_requires=["numpy", "requests", "matplotlib", "pandas", "pytest"],
)
