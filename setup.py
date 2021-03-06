#!/usr/bin/env python

# sudo yum install epel-release
# sudo yum -y update
# sudo yum -y install python-pip
# sudo pip install --upgrade pip
# sudo yum install ansible pycrypto
#

# import os
import os.path
import sys
import yaml
import subprocess

sys.path.insert(0, os.path.abspath('lib'))

roles_path = os.path.dirname(os.path.realpath(__file__)) + 'roles/'

with open('requirements.txt') as requirements_file:
	install_requirements = requirements_file.read().splitlines()
	if not install_requirements:
		print("Unable to read requirements from the requirements.txt file  That indicates this copy of the source code is incomplete.")
		sys.exit(2)

	subprocess.call(['pip', 'install', '--user', '--upgrade', '-r','requirements.txt'])

try:
	from ansible.release import __version__, __author__
except ImportError:
	print("Ansible is not properly installed.")
	sys.exit(1)


with open(roles_path + '/requirements.yml') as stream:
	requirements_list = []
	try:
		requirements_list = yaml.load(stream)
	except yaml.YAMLError as exc:
		print(exc)
		sys.exit(3)

	for req in requirements_list:
		if 'src' in req and 'name' in req and 'scm' in req and ['src'] is not None and req['name'] is not None and req['scm'] is not None and req['scm'] == 'git':
			subprocess.call(['git', 'clone', req['src'], roles_path + req['name']])

	subprocess.call(['ansible-galaxy', 'install', '-r', 'requirements.yml', '--ignore-errors'], cwd=roles_path)
