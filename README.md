[![Build Status](https://travis-ci.org/TRIQS/triqs_hubbardi.svg?branch=unstable)](https://travis-ci.org/TRIQS/triqs_hubbardi)

# triqs_hubbardi - A Hubbard-I solver based on triqs atom_diag

Getting Started
---------------

After setting up your application as described above you should customize the following files and directories
according to your needs (replace triqs_hubbardi in the following by the name of your application)

* Adjust or remove the `README.md` and `doc/ChangeLog.md` file
* In the `c++/triqs_hubbardi` subdirectory adjust the example files `triqs_hubbardi.hpp` and `triqs_hubbardi.cpp` or add your own source files.
* In the `test/c++` subdirectory adjust the example test `basic.cpp` or add your own tests.
* In the `python/triqs_hubbardi` subdirectory add your Python source files.
  Be sure to remove the `triqs_hubbardi_module_desc.py` file unless you want to generate a Python module from your C++ source code.
* In the `test/python` subdirectory adjust the example test `Basic.py` or add your own tests.
* Adjust any documentation examples given as `*.rst` files in the doc directory.
* Adjust the sphinx configuration in `doc/conf.py.in` as necessary.
* The build and install process is identical to the one outline [here](https://triqs.github.io/triqs_hubbardi/unstable/install.html).

### Optional ###
----------------

* If you want to wrap C++ classes and/or functions provided in the `c++/triqs_hubbardi/triqs_hubbardi.hpp` rerun the `c++2py` tool with
```bash
c++2py -r triqs_hubbardi_module_desc.py
```
* Add your email address to the bottom section of `Jenkinsfile` for Jenkins CI notification emails
```
End of build log:
\${BUILD_LOG,maxLines=60}
    """,
    to: 'user@domain.org',
```
