from setuptools import setup

with open("requirements.txt") as f:
    content = f.readlines()
requirements = [x.strip() for x in content if "git+" not in x]

setup(name='traindelays',
      version="0.0.1",
      description="Predict London Overground Lateness",
      license="MIT",
      author="Ben Fairbairn, Debora Ramella, Joel Okwuchukwu, Lewis Trudeau",
      install_requires=requirements)
