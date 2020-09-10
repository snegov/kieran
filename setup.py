from setuptools import setup, find_namespace_packages

setup(
    name="spqr.kieran",
    version="0.0.1",
    author="Maks Snegov",
    author_email="snegov@spqr.link",
    description="Helpers for SPQR projects",
    packages=find_namespace_packages(include=['spqr.*']),
    python_requires=">=3.8",
)
