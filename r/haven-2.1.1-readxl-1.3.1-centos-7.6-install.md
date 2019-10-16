haven 2.1.1 & readxl 1.3.1 - CentOS (7.6)
=========================================

## Issue

Encountered error 'missing symbol `libiconv`' during loading test.

Install information:

* `R` version 3.5.3 and 3.6.1 (confirmed)
* `install.packages("tidyverse")`

`objdump` shows `haven.so` and `readxl.so` looks for `libiconv`, `libiconv_open` and `libiconv_close` symbols.
These symbols not found in `libR.so`.
Actual cause is not clear.
Guesses:
* `R` not configured to `libiconv`;
* `libiconv` not in system/standard path, so its linker flag not configured to makefile;

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

This will lead to an identical failure.
Then enter `src` subdirectory, re-run the last linking `g++`/`gcc` invocation with an additional flag `-liconv` at the end.
As of my configuration, it looks like this:
```bash
g++ -std=gnu++11 -shared -L/shared/centos7/r-project/3.6.1/lib64/R/lib -Wl,-rpath,/home/li.gua/.local/lib,-rpath,/shared/centos7/gcc/7.2.0/lib64 -o haven.so tagged_na.o readstat/readstat_parser.o readstat/readstat_metadata.o readstat/readstat_io_unistd.o readstat/readstat_bits.o readstat/readstat_variable.o readstat/readstat_writer.o readstat/readstat_error.o readstat/readstat_convert.o readstat/CKHashTable.o readstat/readstat_malloc.o readstat/readstat_value.o readstat/sas/readstat_xport_write.o readstat/sas/readstat_sas7bcat_read.o readstat/sas/readstat_sas7bdat_write.o readstat/sas/readstat_sas7bcat_write.o readstat/sas/ieee.o readstat/sas/readstat_xport_read.o readstat/sas/readstat_sas.o readstat/sas/readstat_sas_rle.o readstat/sas/readstat_xport.o readstat/sas/readstat_sas7bdat_read.o readstat/spss/readstat_sav_compress.o readstat/spss/readstat_spss_parse.o readstat/spss/readstat_sav_read.o readstat/spss/readstat_por_read.o readstat/spss/readstat_sav.o readstat/spss/readstat_por.o readstat/spss/readstat_sav_parse_timestamp.o readstat/spss/readstat_zsav_read.o readstat/spss/readstat_sav_write.o readstat/spss/readstat_zsav_compress.o readstat/spss/readstat_spss.o readstat/spss/readstat_por_write.o readstat/spss/readstat_zsav_write.o readstat/spss/readstat_sav_parse.o readstat/spss/readstat_por_parse.o readstat/stata/readstat_dta_read.o readstat/stata/readstat_dta.o readstat/stata/readstat_dta_parse_timestamp.o readstat/stata/readstat_dta_write.o DfReader.o DfWriter.o haven_types.o RcppExports.o -lz -L/shared/centos7/r-project/3.6.1/lib64/R/lib -lR -liconv
```
Then go back to upper directory and finish the installation and load test (should pass this time):
```bash
R CMD INSTALL --install-test .
```

Identical solution for `readxl`.
Finally finish installing `tidyverse`.
