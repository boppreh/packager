from os import path, listdir, chdir, rename
from datetime import date

DEFAULT_LICENSE = """/*

  Licensed under the MIT License

  Copyright (c) {} Lucas Boppre Niehues (lucasboppre@gmail.com)

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

*/""".format(date.today().year)

DEFAULT_CHANGES = """0.1.0 ({})
++++++++++++++++++

- Initial release.""".format(date.today().isoformat())

DEFAULT_MANIFEST = """include *.txt
recursive-include docs *.txt"""

DEFAULT_README = ''

def create_element(expected_name, default_content):
	if path.exists(expected_name):
		return

	name = path.splitext(expected_name)[0]
	similar_names = [f for f in listdir('.') if f.startswith(name) and path.isfile(f)]

	if len(similar_names) == 1:
		os.rename(similar_names[0], expected_name)
	else:
		with open(changes, 'w') as f:
			f.write(default_content)

def analyze_dir(path):
	chdir(path)

	create_element('CHANGES.txt', DEFAULT_CHANGES)
	create_element('LICENSE.txt', DEFAULT_LICENSE)
	create_element('MANIFEST.in', DEFAULT_MANIFEST)
	create_element('README.rst', DEFAULT_README)
	