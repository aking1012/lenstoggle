from setuptools import setup

setup(
    name='LensToggler',
    version='0.1.1',
    description='Simple App to Toggle Lenses.',
    author='aking1012.com@gmail.com',
    author_email='aking1012.com@gmail.com',
    url='http://www.github.com/aking1012/pyeggtut',
    packages=['LensToggle'],
      long_description="""\
Simple App to Toggle Lenses.  \
I did not like that unity --replace & moved my screenlets around, so I took that part out.  Just log out and log in.  \
""",
      classifiers=[
          "License :: Not OSI Approved :: BSD + Non-Commercial",
          "Programming Language :: Python",
          "Development Status :: 3 - Alpha",
          "Intended Audience :: Users that want to temporarily disable lenses without uninstalling them",
          "Topic :: Ubuntu Lenses",
      ],
      keywords='python lens toggle Gtk',
      license='GPL',
      install_requires=[
        'setuptools'
      ],
      )


