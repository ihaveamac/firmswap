# firmswap
My Python 3 implementation of the hardmod downgrade for Nintendo 3DS.

## Default behavior
* Create backup of `NAND.bin` named `NAND.bin.bak`
* determine if `NAND.bin` is for New3DS/Old3DS
* read FIRM0FIRM1 partition
* xor FIRM0 with `firm_110_<model>3DS.bin`, `firm_104_<model>3DS.bin`
* write to `NAND.bin`

## Usage
```bash
firmswap.py [options]
```
* `--nandimage=<file>` - use <file> instead of default `NAND.bin`, backup file will be `filename.bak`
* `--nobackup` - do not create a backup of NANDimage
* `--firm110=<file>` - use <file> instead of `firm_110_<model>3DS.bin`
* `--firm104=<file>` - use <file> instead of `firm_104_<model>3DS.bin`
* `--swapfirm1` - xor FIRM1 partition in addition to FIRM0
* `--forcenew` - assume NANDimage is for New3DS
* `--forceold` - assume NANDimage is for Old3DS
