# firmswap
My Python 3 implementation of the hardmod downgrade for Nintendo 3DS.

Yes, I know Python isn't the best language for this (something in C could probably run in a second or less), but it works and it's all I know.

## Default behavior
* Create backup of `NAND.bin` named `NAND.bin.bak`
* determine if `NAND.bin` is for New3DS/Old3DS
* read FIRM0FIRM1 partition
* xor FIRM0 with `firm_110_<model>3DS.bin` and `firm_104_<model>3DS.bin`
* write to `NAND.bin`

`firm_110_<model>3DS.bin` and `firm_104_<model>3DS.bin` should be extracted from decrypted 11.0/10.4 FIRM CIAs ExeFS.

## Usage
```bash
python3 firmswap.py [options]
```
* `--nandimage=<file>` - use <file> instead of default `NAND.bin`, backup file will be `filename.bak`
* `--nobackup` - do not create a backup of NANDimage
* `--firm110=<file>` - use <file> instead of `firm_110_<model>3DS.bin`
* `--firm104=<file>` - use <file> instead of `firm_104_<model>3DS.bin`
* `--swapfirm1` - xor FIRM1 partition in addition to FIRM0
* `--forcenew` - assume NANDimage is for New3DS
* `--forceold` - assume NANDimage is for Old3DS

## License
`firmswap.py` is under the MIT license.
