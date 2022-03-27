import setuptools
from sphinx.setup_command import BuildDoc

cmdclass = {'build_sphinx': BuildDoc}

with open("../README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()


with open('requirements.txt') as fp:
    install_requires = fp.read(),

name = "DS_package"
version = "v0.0.1"

setuptools.setup(
    name=name,
    version=version,
    install_requires=install_requires,
    author="INBO11",
    # author_email="<your-email>",
    description="Django project",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DaniilMpala/saitDiscount",
    project_urls={
        "Bug Tracker": "https://github.com/DaniilMpala/saitDiscount/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "."},
    packages=setuptools.find_packages(where="."),
    python_requires=">=3.9",
    scripts=["manage.py"],
    command_options={
        'build_sphinx': {
            'project': ('setup.py', name),
            'version': ('setup.py', version),
            # 'release': ('setup.py', version),
            'source_dir': ('setup.py', 'source')}},
)
