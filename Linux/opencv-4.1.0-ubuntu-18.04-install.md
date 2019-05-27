OpenCV 4.1.0 - Ubuntu (18.04)
=============================

OpenCV version in Ubuntu's official repo is too old (3.2).

<!--## Dependency tree

![](auxiliary/gnupg-mojave-10.14.2-install.dependency-tree.gv.png)-->

## Online resources

Official installation documentation (including downloading portal):

* [https://docs.opencv.org/master/d7/d9f/tutorial_linux_install.html](https://docs.opencv.org/master/d7/d9f/tutorial_linux_install.html)


## Build tools and dependencies

```bash
# tools
sudo apt install cmake # make sure cmake is installed
# linear algebra libs, further explained later; optional lapack -> atlas or MKL
sudo apt install libopenblas-dev liblapack-dev liblapacke-dev
# image/video I/O libs
sudo apt install libgtk-3-dev ffmpeg libavcodec-dev libavformat-dev libswscale-dev libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev
```

`libjasper` is not in 18.04 repo, need to use earlier distro:

```bash
sudo add-apt-repository "deb http://security.ubuntu.com/ubuntu xenial-security main"
sudo apt update
sudo apt install libjasper-dev # automatically installs dependency libjasper1
```

Before configure, extra work to do:

1. Tell cmake to find openblas, in my case the path is not coded in the find cmake file

```bash
# add openblas library path to below file, if not coded there:
vim opencv-4.1.0/cmake/OpenCVFindOpenBLAS.cmake
# in my case, are /usr/include(lib)/x86_64-linux-gnu
# this is required if want to link to openblas
```

2. Softlink `lapacke.h`

`OpenCVFindLAPACK.cmake` always finds it in the same directory as `openblas` (if used); but in my case it is in a different location;

```bash
sudo ln -s /opt/include/lapacke.h /opt/include/x86_64-linux-gnu/lapacke.h
```

## Configure

```bash
mkdir build && cd build
cmake \
	-DCMAKE_BUILD_TYPE=Release \
	-DCMAKE_INSTALL_PREFIX=/opt/opencv-4.1.0 \
	-DCMAKE_INSTALL_RPATH=/opt/opencv-4.1.0/lib \
	-DBUILD_DOCS=1 \
	-DBUILD_EXAMPLES=1 \
	-DPYTHON3_EXECUTABLE=/opt/python3.7-virtual-env/bin/python3.7 \
	-DPYTHON3_INCLUDE_DIR=/opt/python3.7/include/python3.7m \
	-DPYTHON3_LIBRARY=/opt/python3.7/lib/libpython3.7m.so \
	-DPYTHON3_NUMPY_INCLUDE_DIRS=/opt/python3.7-virtual-env/lib/python3.7/site-packages/numpy/core/include \
	..
```

Expalantion:

* wish to install opencv in a non-regular path (/opt/opencv-4.1.0), configure with CMAKE\_INSTALL\_RPATH to ensure finding its own library
* python build is in a non-regular path (/opt/python3.7)
* numpy build is in another path (/opt/python3.7-virtual-env/...)
* must use /opt/python3.7-virtual-env/bin/python3.7 otherwise need more configuration to find numpy


## Build, test and install

```bash
make -j 4
```

For test, need to first download the test data, instructions can be found in top URL.

```bash
git clone https://github.com/opencv/opencv_extra.git ~/build/opencv_extra
export OPENCV_TEST_DATA_PATH="$HOME/build/opencv_extra/testdata"
# assume still in build dir
./bin/opencv_test_core
```

To install:

```bash
sudo make install
# check if rpath is correctly set
ldd /opt/opencv-4.1.0/bin/opencv_annotation
# then link the python interface to virtual env
ln -s /opt/opencv-4.1.0/lib/python3.7/site-packages/cv2 /opt/python3.7-virtual-env/lib/python3.7/site-packages/cv2
# check python interface loadable
. /opt/python3.7-virtual-env/bin/activate
python -c 'import cv2'
```
