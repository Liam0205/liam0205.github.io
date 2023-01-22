#!/usr/bin/env bash
set -eux

rm -rf ./Packages*
dpkg-scanpackages deb/ > Packages
tar zcvf Packages.gz Packages
bzip2 -k Packages

