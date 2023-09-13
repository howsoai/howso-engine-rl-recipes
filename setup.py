from setuptools import find_packages, setup


def get_version(rel_path):
    """Return the version."""
    with open(rel_path) as f:
        for line in f.read().splitlines():
            if line.startswith('__version__'):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
        else:
            raise RuntimeError("Unable to find version string.")


def parse_requirements(requirements):
    """Parse and return requirements."""
    with open(requirements) as requirements_file:
        return [
            line.strip('\n') for line in requirements_file
            if line.strip(' \t\n') and not line.startswith('#')
        ]


setup(
    name='howso-recipes-engine-rl',
    version=get_version("howso_recipes_engine_rl/__init__.py"),
    description='Howso Recipes Engine RL',
    author='Howso Incorporated',
    author_email='support@howso.com',
    license='GNU Affero General Public License v3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Machine Learning',
        'Topic :: Scientific/Engineering :: Data Mining',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Programming Language :: Python :: 3'
    ],
    include_package_data=True,
    install_requires=parse_requirements('requirements.in'),
    keywords='reinforcement learning',
    python_requires='>=3.8',
    project_urls={'Documentation': 'https://docs.community.howso.com/'},
    packages=find_packages(),
    url='https://howso.com'
)
