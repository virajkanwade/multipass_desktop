import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="multipass_desktop-viraj-kanwade", # Replace with your own username
    version="0.0.1",
    author="Viraj Kanwade",
    author_email="virajk.oib@gmail.com",
    description="Desktop interface for Multipass",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/virajkanwade/multipass_desktop",
    project_urls={
        "Bug Tracker": "https://github.com/virajkanwade/multipass_desktop/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    scripts=["bin/multipass_desktop"]
)
