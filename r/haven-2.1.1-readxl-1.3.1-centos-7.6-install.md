haven 2.1.1 & readxl 1.3.1 - CentOS (7.6)
=========================================

## Issue

Encountered error 'missing symbol `libiconv` during loading test.

Install information:

* R 3.5.3 and R 3.6.1 (confirmed)
* `install.packages("tidyverse")`

Actual reason no clear. `objdump` shows `haven.so` and `readxl.so` looks for `libiconv`, `libiconv_open` and `libiconv_close` symbols.
These symbols not found in `libR.so`.

## Solution

We solve this by force linking the library to `libiconv.so`.
Make sure that `libiconv.so` and appropriate head files are installed.
Then run
```r
install.packages("tidyverse")
```
until failure.
Above installation session should leave a temporary folder (default in `/tmp/Rtmp****`, `****` is random string).
Note, exiting `R` session will also remove this temporary folder.
Enter its subfolder `downloaded_packages`, do manual installation (example for `haven`):
```bash
tar -zxvf haven_2.1.1.tar.gz
cd haven
R CMD INSTALL --build .
```

This will lead an identical failure.
Then enter `src` subdirectory, re-run the last linking `g++`/`gcc` invocation with additional flag `-liconv` at the end.
Back to upper directory and run
```bash
R CMD INSTALL --install-test .
```
to finish the installation and load test (should pass).

Identical solution for `readxl`.
After installation of these two packages, re-run `install.packages("tidyverse")`.
