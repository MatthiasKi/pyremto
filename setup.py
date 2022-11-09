import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pyremto",
    version="1.0.0",
    author="Matthias Kissel",
    author_email="contact@pyremto.com",
    description="Python Remote Tools: Manage Python scripts from anywhere",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/MatthiasKi/pyremto",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    tests_require=['nose'],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "qrcode",
        "Image",
        "requests",
        "matplotlib",
        "sklearn"
    ]
)
