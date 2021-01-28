import setuptools

setuptools.setup(
    name="db-utils",
    version="0.0.1",
    packages=setuptools.find_packages(),
    python_requires=">=3.8",
    install_requires=["sqlalchemy>=1.3.22"],
)
