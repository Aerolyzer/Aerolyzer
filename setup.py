# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os.path
from setuptools import find_packages, setup

# Package data
# ------------
_author = 'Aerolyzer Developers'
_author_email = 'aerolyzer@googlegroups.com'
_classifiers = [
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: Information Technology',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering',
    'Development Status :: 1 - Planning',
    'License :: OSI Approved :: Apache Software License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
]
_description = 'Aerolyzer analyzes images to infer atmospheric composition'
_download_url = 'https://github.com/Aerolyzer/Aerolyzer/archive/0.0.0.1.tar.gz'
_requirements = ['exifread', 'numpy', 'opencv-python']
_keywords = ['atmospheric composition', 'sunsets', 'image analysis', 'aerosols']
_license = 'Apache License, Version 2.0'
_long_description = 'A Python suite for analyzing images to infer aerosol types in the image.'
_name = 'aerolyzer'
_namespaces = []
_packages = ['aerolyzer']
_test_suite = 'aerolyzer.tests'
_url = 'https://github.com/Aerolyzer/Aerolyzer'
_version = '0.0.0.1'
_zip_safe = False

# Setup Metadata
# --------------
setup(
    author=_author,
    author_email=_author_email,
    classifiers=_classifiers,
    description=_description,
    download_url=_download_url,
    include_package_data=True,
    install_requires=_requirements,
    keywords=_keywords,
    license=_license,
    long_description=_long_description,
    name=_name,
    namespace_packages=_namespaces,
    packages=_packages,
    test_suite=_test_suite,
    url=_url,
    version=_version,
    zip_safe=_zip_safe,
)