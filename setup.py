from setuptools import setup, find_packages

setup(name='smart-things-serverless',
      setup_requires=['lambda_setuptools'],
      install_requires=['requests', 'jinja2'],
      version='0.1',
      description='SmartThings Utilities',
      url='https://gitlab.com/aolaru-home-automation/smart-things-serverless',
      author='Sandu Potter',
      author_email='sandupotter@gmail.com',
      license='MIT',
      packages=find_packages(exclude=['tests']),
      zip_safe=False,
      package_data={
          'battery_reports': ['templates/*.html'],
      })
