from os import path, listdir, chdir, rename, mkdir, system
from datetime import date
import re

AUTHOR_NAME = 'Lucas Boppre Niehues'
AUTHOR_EMAIL = 'lucasboppre@gmail.com'

DEFAULT_LICENSE = """/*

  Licensed under the MIT License

  Copyright (c) {} {} ({})

  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files (the "Software"), to deal
  in the Software without restriction, including without limitation the rights
  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
  copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in
  all copies or substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
  THE SOFTWARE.

*/"""

DEFAULT_CHANGES = """0.1.0 ({})
++++++++++++++++++

- Initial release.""".format(date.today().isoformat())

DEFAULT_MANIFEST = """include *.txt *.md
recursive-include docs *.txt"""

DEFAULT_SETUP = """from distutils.core import setup

setup(
    name='{title}',
    version='0.1.0',
    author='{author}',
    author_email='{email}',
    packages=['{project}'],
    url='http://pypi.python.org/pypi/{title}/',
    license='LICENSE.txt',
    description='{title}',
    long_description=open('README.md').read(),
)"""


def create_element(expected_name, default_content):
    """
    Given the name of a file that needs to exist and its default contents,
    ensures the file exists, by creating it or renaming a file from a different
    extension.
    """
    if path.exists(expected_name):
        print('"{}" already exists, skipping.'.format(expected_name))
        return

    name = path.splitext(expected_name)[0]
    similar_names = [f for f in listdir('.') if f.startswith(name + '.') and path.isfile(f)]

    if len(similar_names) == 1:
        print('Renaming "{}" to "{}".'.format(similar_names[0], expected_name))
        rename(similar_names[0], expected_name)
    else:
        print('Creating "{}" with default values.'.format(expected_name))
        with open(expected_name, 'w') as f:
            f.write(default_content)

def create_all_elements(project_name, title):
    """
    Ensures all the required files for a package are present.
    """
    create_element('CHANGES.txt', DEFAULT_CHANGES)
    create_element('LICENSE.txt', DEFAULT_LICENSE.format(date.today().year,
                AUTHOR_NAME, AUTHOR_EMAIL))
    create_element('MANIFEST.in', DEFAULT_MANIFEST)

    create_element('README.md', title + '\n' + len(title) * '-')

    setup = DEFAULT_SETUP.format(title=title,
                                 author=AUTHOR_NAME,
                                 email=AUTHOR_EMAIL,
                                 project=project_name)
    create_element('setup.py', setup)

def update_module(project, name):
    """
    Ensures the Python modules are inside the correct folder.
    """
    if not path.exists(name):
        print('Creating {} module.'.format(name))
        mkdir(name)

    main = name + '.py'
    if path.exists(main):
        print('Renaming module file "{}" to "__init__.py".'.format(main))
        rename(main, path.join(name, '__init__.py'))
    else:
        print('Creating empty file "__init__.py".')
        with open(path.join(name, '__init__.py'), 'w') as f:
            f.write('')

    for python_file in [f for f in listdir('.') if f.endswith('.py')]:
        if python_file == 'setup.py':
            continue

        print('Moving sub-module "{}".'.format(python_file))
        rename(python_file, path.join(name, python_file))


def package(project):
    """
    Packages a given project, adding or renaming the required files and moving
    the folders are necessary.
    """
    if project.endswith('/'):
        project = project[:-1]

    project_name = path.basename(project)
    words = re.findall('([A-Z]?[a-z]+)', project_name)
    title = ' '.join(words).title().replace(' ', '')

    chdir(project)

    create_all_elements(project_name, title)
    update_module(project, project_name)
    
if __name__ == '__main__':
    project_name = raw_input('Project name: ')
    project = path.join('D:/', 'projects', project_name)
    package(project)

    print('Running sdist on setup.')
    system('python setup.py sdist')

    if raw_input('Do you want to upload this module to PyPi? (y/N) ') == 'y':
        system('python setup.py register')
        system('python setup.py sdist upload')
