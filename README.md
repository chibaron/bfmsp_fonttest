# bfmsp_fonttest
To test betaflight's extended font feature.
Reads and writes extended fonts.

## read extended font
Reads font data from 0x0 to 0x1ff
```
bfmsp_readfont.py MSP_COMPORT
```
ex python bfmsp_readfont.py COM3

## write extended font
Write betaflight.mcm
```
bfmsp_writefont.py MSP_COMPORT
```
ex python bfmsp_writefont.py COM3
