
# Ref

[NFCPy](https://github.com/nfcpy/nfcpy)

[Getting Started NFCPy](https://nfcpy.readthedocs.io/en/latest/topics/get-started.html) を見るとwrite関数もある．
```
 def ndef_write(block_number, block_data, wb, we):
    global ndef_data_area
    if block_number < len(ndef_data_area) / 16:
        first, last = block_number*16, (block_number+1)*16
        ndef_data_area[first:last] = block_data
        return True
```
htps://monomonotech.jp/kurage/raspberrypi/nfc.html

https://scrapbox.io/saitotetsuya/nfcpy
