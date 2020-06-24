from setuptools import find_packages, setup

with open("README.md", "r") as fh:
    long_description = fh.read()

packages = find_packages()

install_requires = [
    'arosics',
    # 'GDAL',
    'numpy',
    # 'rasterio',
]

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='validation-tools',
    url='https://github.com/fronzag/validation_tools.py',
    author='José Guilherme Fronza and Rennan de Freitas Bezerra Marujo',
    author_email='author@example.com',
    # Needed to actually package something
    packages=packages,
    # Needed for dependencies
    install_requires=install_requires,
    # *strongly* suggested for sharing
    version='0.0.1',
    # The license can be anything you like
    license='MIT',
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.5',
)
