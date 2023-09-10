#!/bin/bash
# Functions to archive and upload to artifactory the recipes file
# usage:  ./bin/build.sh release 2010.01.1
#
####

set -euo pipefail
# set -x
source config/build.properties

# Create requirements
gen_requirements() {
  local pyversion=${1:-3.9}
  echo $pyversion
  rm -fv requirements-local-${pyversion}.txt
  # https://github.com/jazzband/pip-tools/issues/973 describes use of --allow-unsafe
  CUSTOM_COMPILE_COMMAND="./bin/build.sh gen_requirements $pyversion" pip-compile --upgrade requirements.in requirements-dev.in requirements-local.in --no-emit-index-url --resolver=backtracking --allow-unsafe --output-file requirements-local-${pyversion}.txt
}

# Gets the latest version of a pacakge and pins it in the requirements file
force_latest_package() {
  local package=${1}
  local req_file=${2:-requirements-local.in}
  local latest_version=$(pip install --use-deprecated=legacy-resolver ${package}== 2>&1 | grep -oE '(\(.*\))' | awk -F: '{print$NF}' | sed -E 's/( |\))//g' | tr ',' '\n' | tail -n 1)
  echo "Latest version of ${package} is ${latest_version}"
  # Check not 'none'
  if [ "${latest_version}" == "none" ]; then
    echo "ERROR: Could not find latest version of ${package}"
    exit 1
  fi
  sed -i "/${package}==/d" "${req_file}"
  sed -i "/${package}/d" "${req_file}"
  echo "${package}==${latest_version} # Added by automation - please leave" >> requirements-local.in
}

# Achieving two things here.
# 1) Forcing an upgrade, and a failure if we can't go to the latest - this is tricky to do just with pip-compile, and a unpinned package (-U will not fail if it can't upgrade)
# 2) Allowing the backtracking resolver to work in a reasonable time, with no version range, it will download all versions
pin_local_requirements() {
   force_latest_package howso-engine requirements-local.in
}

# Create a zip file with the recipes for uploading
archive() {
  local version=${1}
  local archive_file=${archive_prefix}-${version}.zip
  rm -f target/$archive_file
  mkdir -p target
  zip -r target/${archive_file} ./ -x 'pytest.ini' -x 'requirements-*.in' -x 'requirements*.txt' -x "pip.conf" -x 'target/*' -x "*/__pycache__/*" -x "/__pycache__/*" -x '__init__.py' -x '*.git*' -x 'junit' -x '*flake8' -x '*.direnv*' -x '*ipynb_checkpoints*' -x '*.envrc' -x 'Jenkinsfile*' -x '*bin*' -x '*.vscode*' -x '*__pycache__*' -x '*.pytest_cache*' -x 'tests/*' -x 'dumps/*' -x 'config/*' -x 'howso.yml*'
  echo "archive file: target/${archive_file}"
}

# Clear out all the stuff from testing, etc
clean() {
   rm -f *.trace
   rm -rf howso_recipes_engine_rl.egg-info
   rm -rf traces
   rm -rf dist
   rm -rf build
   rm -f *rounds.txt
   rm -rf cucumber junit target html
   find ./ -name .pytest_cache -type d | xargs -rt rm -r
   find ./ -name __pycache__ -type d | xargs -rt rm -r
}

# Use jf cli to upload release to artifactory
upload(){
  local version=${1}
  local archive_file=${archive_prefix}-${version}.zip
  echo "About to upload ${archive_file} to artifactory - this will overwrite any existing release"
  read -p $'\e[33mAre you sure? (y/n)\e[0m' -n 1 -r
  if [[ $REPLY =~ ^[Yy]$ ]]
  then
     jf rt u --spec config/jf-upload-recipe.spec --spec-vars "release=${version}"
  else
    exit 4
  fi
}

# Run the tests
# Usage: ./bin/build.sh test {mark} {xdist}
# i.e. ./bin/build.sh test "smoke and not slow" 10
# To turn off xdist, use 'none' as the xdist param, leave it unset to use auto
# If no mark is specified, or set as "" then all tests will be run
test(){
  local mark=${1:-}
  local xdist=${2:-auto}
  local xdist_param=""
  if [ "$xdist" ] && [ ! "$xdist" == "none" ]; then
    xdist_param="-n ${xdist}"
  fi
  mkdir -p junit
  mkdir -p logs
  set -x
  if [ !  "$mark" ]; then
     python -m pytest ${xdist_param} --log-cli-level=INFO --log-file=./logs/test.log --log-file-level=INFO -o junit_family=xunit2 --junitxml=junit/test-results.xml -s
  else
     python -m pytest -m "$mark" ${xdist_param} --log-cli-level=INFO --log-file=./logs/test.log --log-file-level=INFO -o junit_family=xunit2 --junitxml=junit/test-results.xml -s
  fi
  set +x
}

# Updates the appropriate version file (defined in build.properties)
update_version() {
  new_version=$1
  echo "Updating version to $new_version"
  sed -i "s/__version__ = \(.*\)/__version__ = \"$new_version\"/" ${version_file}
  cat ${version_file}
}

# Logic for getting version information from appropriate .py file
get_version() {
  cat ${version_file} | grep -e '^__version__' | sed 's/.*\=\(.*\)/\1/' | tr -d '"' | tr -d '[:space:]'
}


# Archive and upload
release(){
  local version=${1}
  archive ${version}
  upload ${version}
}


# Install dependencies
install_deps() {
  local pyversion=${1}
  echo "Installing dependencies for python version ${pyversion}"
  pip install --prefer-binary -r requirements-local-${pyversion}.txt
}




# Install python modules required for building
install_build_deps() {
  pip install twine wheel
}

# Create license file
gen_licenses() {
  pip install pip-licenses
  pip-licenses --with-authors --with-urls --with-license-file --with-description --format=plain-vertical  > ./LICENSE-3RD-PARTY.txt
}

# Build the package
build() {
  # Builds a source distribution and a universal wheel
  python setup.py sdist bdist_wheel
}

# Upload to artifactory - Note, this is utility for testing - actual uploading is from an Azure Devops Artifactory task
## relies on a file at ~/.pypirc
##
#[distutils]
#index-servers = local
#[local]
#repository: https://dpbuild.jfrog.io/artifactory/api/pypi/pypi-edge
#username:
#password:

_upload() {
  python setup.py bdist_wheel upload -r local
}

# Show usage, and print functions
help() {
  echo "usage: ./bin/build.sh <build-function> {params}"
  echo " where <build-function> one of :-"
  IFS=$'\n'
  for f in $(declare -F); do
    echo "    ${f:11}"
  done
}

# Takes the cli params, and runs them, defaulting to 'help()'
if [ ! ${1:-} ]; then
  help
else
  "$@"
fi
