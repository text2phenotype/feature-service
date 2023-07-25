from setuptools import setup, find_packages

from text2phenotype.common.test_command import TestCommand


def parse_requirements(file_path):
    with open(file_path, 'r') as reqs:
        req_list = []
        for line in reqs.readlines():
            if line.startswith('#'):
                continue
            if line.startswith('-r '):
                sub_req = parse_requirements(f"{line.split('-r ')[-1].replace('/n', '').strip()}")
                req_list.extend(sub_req)
                continue
            req_list.append(line)
        return req_list


setup(name='feature-service',
      version='0.0.0.0',
      license='Other/Proprietary License',
      packages=find_packages(exclude=['tests']),
      install_requires=parse_requirements('requirements.txt'),
      package_data={'': ['open_api_spec.yml']},
      include_package_data=True,
      entry_points={'console_scripts': ['feature_service=feature_service.__main__:main']},
      tests_require=['pytest'],
      cmdclass={'test': TestCommand})
