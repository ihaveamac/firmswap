#!/usr/bin/env python3
import os
import shutil
import sys

helptext = """usage: firmswap.py [options]
swap FIRM partition(s) from 11.0 to 10.4 FIRM

default behavior:
  - create backup of NAND.bin named NAND.bin.bak
  - determine if NAND.bin is for New3DS/Old3DS
  - read FIRM0FIRM1 partition
  - xor FIRM0 with 11.0 FIRM, then 10.4 FIRM
  - xor FIRM1 the same way
  - write to NAND.bin

options (for advanced use only):
  --nandimage=<file>  - use <file> instead of default NAND.bin
                        backup file will be filename.bak
  --nobackup          - do not create a backup of NANDimage
  --firm110=<file>    - use file instead of firm_110_<model>3DS.bin
  --firm104=<file>    - use file instead of firm_104_<model>3DS.bin
  --forcenew          - assume NANDimage is for New3DS
  --forceold          - assume NANDimage is for Old3DS"""

if "--help" in sys.argv:
    print(helptext)
    sys.exit(1)

nandimage_filename = "NAND.bin"
firm110_filename = "firm_110_{0}3DS.bin"
firm110_custom = False
firm104_filename = "firm_104_{0}3DS.bin"
firm104_custom = False
for arg in sys.argv[1:]:
    if arg[:12] == "--nandimage=":
        nandimage_filename = arg[12:]
    if arg[:10] == "--firm110=":
        firm110_filename = arg[10:]
        firm110_custom = True
    if arg[:10] == "--firm104=":
        firm104_filename = arg[10:]
        firm104_custom = True

if not os.path.isfile(nandimage_filename):
    print("! {0} doesn't exist.".format(nandimage_filename))
    sys.exit()

nandimage = open(nandimage_filename, "r+b")
nandimage.seek(0x106)
# actually part of "Size of the NCSD image", but there's only two sizes
# (even given NAND chip size differences)
nand_type_byte = nandimage.read(1)
nand_type = ""
if ord(nand_type_byte) == 0x20:
    nand_type = "Old"
elif ord(nand_type_byte) == 0x28:
    nand_type = "New"
else:
    print("! unknown NAND type? ({0})".format(nand_type_byte))
    nandimage.close()
    sys.exit(1)

if "--forcenew" in sys.argv:
    nand_type = "New"
    print("- assuming New3DS since --forcenew was used")
elif "--forceold" in sys.argv:
    nand_type = "Old"
    print("- assuming Old3DS since --forceold was used")

if not firm110_custom:
    firm110_filename = firm110_filename.format(nand_type)
if not firm104_custom:
    firm104_filename = firm104_filename.format(nand_type)

if not os.path.isfile(firm110_filename):
    print("! {0} doesn't exist.".format(firm110_filename))
    sys.exit()
if not os.path.isfile(firm104_filename):
    print("! {0} doesn't exist.".format(firm104_filename))
    sys.exit()

if "--nobackup" not in sys.argv:
    nandimage.close()
    # not sure if I really need to close nandimage before copying
    # but I imagine Windows will throw an error if I do it, because it loves to
    print("- copying {0} to {0}.bak".format(nandimage_filename))
    shutil.copy(nandimage_filename, "{0}.bak".format(nandimage_filename))
    nandimage = open(nandimage_filename, "r+b")
else:
    print("- not backing up {0} since --nobackup was used".format(nandimage_filename))

print("- reading FIRM0FIRM1 of {0}".format(nandimage_filename))
nandimage.seek(0xB130000)
orig_firm = list(nandimage.read(0x800000))
firm110_file = open(firm110_filename, "rb")
firm104_file = open(firm104_filename, "rb")
firm110 = firm110_file.read(0x800000)
firm104 = firm104_file.read(0x800000)

print("- xoring FIRM0FIRM1 with {0} and {1}".format(firm110_filename, firm104_filename))
for b in range(0, 0x400000):
    orig_firm[b] = (orig_firm[b] ^ firm110[b]) ^ firm104[b]
    print("- progress: 0x%X out of 0x800000" % (b + 1), end='\r')
for b in range(0x400000, 0x800000):
    orig_firm[b] = (orig_firm[b] ^ firm110[b - 0x400000]) ^ firm104[b - 0x400000]
    print("- progress: 0x%X out of 0x800000" % (b + 1), end='\r')

print("\n- writing to NAND.bin")
nandimage.seek(0xB130000)
nandimage.write(bytes(orig_firm))
print("- done!")
