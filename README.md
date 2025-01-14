# RDown: Markdown for Receipts

Rdown is a simple renderer that allows converts Markdown syntax (including tables) into the ReceiptLine syntax common used for receipts, which can itself be converted into a series of ESCPOS commands as used by most common receipt printers.

Rdown supports bitmap images as base64-encoded PNG images formated as data URIs, and it converts "auto links", ie URLs surrounded by angle brackets, into QR codes.