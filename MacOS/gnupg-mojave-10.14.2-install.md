GnuPG - Mojave (10.14.2)
========================

Installing GPG is motivated by signing commits to GitHub.
On the other hand, also want to keep the direct dependencies
	to be isolated from major environment.

## Dependency tree

![](misc/gnupg-mojave-10.14.2-install.dependency-tree.gv.png)

## Basal libraries/tools

```bash
brew install gmake # then make sure make calls the correct version
brew install bzip2 zlib readline ncurses qt5 libiconv
```

## libgpg-error

```bash
cd libgpg-error-1.35
mkdir build && cd build
# check to ensure --disable-rpath is off
../configure --prefix=$HOME/.local \
	--with-libiconv-prefix=/usr/local/Cellar/libiconv/1.15 \
	--with-readline=/usr/local/Cellar/readline/7.0.3_1
make -j 8
make check && make install
```

## libksba 1.3.5

```bash
cd libksba-1.3.5
mkdir build && cd build
# check to ensure --disable-rpath is off
../configure --prefix=$HOME/.local \
	--with-libgpg-error-prefix=$HOME/.local
make -j 8
make check && make install
```

## npth

```bash
cd npth-1.6
mkdir build && cd build
# check to ensure --disable-rpath is off
../configure --prefix=$HOME/.local
make -j 8
make check && make install
```

## libgcrypt

```bash
cd libgcrypt-1.8.4
mkdir build && cd build
# check to ensure --disable-rpath is off
../configure --prefix=$HOME/.local \
	--with-libgpg-error-prefix=$HOME/.local \
	--with-pth-prefix=$HOME/.local
make -j 8
make check && make install
```

## ntbtls

```bash
cd ntbtls-0.1.2
mkdir build && cd build
# check to ensure --disable-rpath is off
../configure --prefix=$HOME/.local \
	--with-libgpg-error-prefix=$HOME/.local \
	--with-libgcrypt-prefix=$HOME/.local \
	--with-ksba-prefix=$HOME/.local \
	--with-zlib=/usr/local/Cellar/zlib/1.2.11
make -j 8
make check && make install
```

## libassuan

```bash
cd libassuan-2.5.3
mkdir build && cd build
# check to ensure --disable-rpath is off
../configure --prefix=$HOME/.local \
	--with-libgpg-error-prefix=$HOME/.local
make -j 8
make check && make install
```

## pinentry

```bash
cd pinentry-1.1.0
mkdir build && cd build
# add qt5 so configure can find it
PATH=$PATH:/usr/local/Cellar/qt/5.12.1/bin # moc used to compile qt code
PKG_CONFIG_PATH=$PKG_CONFIG_PATH:/usr/local/Cellar/qt/5.12.1/lib/pkgconfig
# pkgconfig can be checked with pkg-config --modversion Qt5Core
# check to ensure --disable-rpath is off
../configure --prefix=$HOME/.local \
	--with-libgpg-error-prefix=$HOME/.local \
	--with-libassuan-prefix=$HOME/.local \
	--with-ncurses-include-dir=/usr/local/Cellar/ncurses/6.1/include \
	--with-libiconv-prefix=/usr/local/Cellar/libiconv/1.15 \
	--enable-pinentry-qt
make -j 8
make check && make install
```

## gnupg

```bash
cd gnupg-2.2.13
mkdir build && cd build
# check to ensure --disable-rpath is off
../configure --prefix=$HOME/.local \
	--with-pinentry-pgm=$HOME/.local/bin/pinentry \
	--with-libgpg-error-prefix=$HOME/.local \
	--with-libgcrypt-prefix=$HOME/.local \
	--with-libassuan-prefix=$HOME/.local \
	--with-ksba-prefix=$HOME/.local \
	--with-npth-prefix=$HOME/.local \
	--with-ntbtls-prefix=$HOME/.local \
	--with-libiconv-prefix=/usr/local/Cellar/libiconv/1.15 \
	--with-zlib=/usr/local/Cellar/zlib/1.2.11 \
	--with-bzip2=/usr/local/Cellar/bzip2/1.0.6_1 \
	--with-readline=/usr/local/Cellar/readline/7.0.3_1 \
	--enable-all-tests
make -j 8
make check && make install
```
