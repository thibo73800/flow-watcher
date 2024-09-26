from setuptools import setup, find_packages

# Read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="flow_watcher",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python-based application that monitors a specific folder in Google Drive for real-time changes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/thibo73800/flow-watcher",
    packages=find_packages(),
    install_requires=[
        "google-api-python-client==2.70.0",
        "google-auth-httplib2==0.1.0",
        "google-auth-oauthlib==0.4.6",
        "openai",
        "notion2markdown==0.2.0",
        "gtts"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)