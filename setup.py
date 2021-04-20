import setuptools
with open("requirements.txt", "r", encoding="utf-8") as f:
    requirements = f.read().splitlines()

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Web Video Converter",
    version="0.0.1",
    author="Martin Sidén",
    author_email="martin.siden@live.se",
    description="A simple Web service for converting the bit-rate of video files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/msiden/web-video-converter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=requirements,
    python_requires='>=3.8',
)
