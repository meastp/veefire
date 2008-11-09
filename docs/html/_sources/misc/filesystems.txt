Filesystems in veefire
========================

Some filesystems, like FAT32, treats lots of characters that are common in TV show titles as invalid. veefire implements functions to avoid this problem, by registering invalid characters for filesystems, and their replacement. The filesystems are kept in filesystems.xml, and this file contains every registered filesystem.

**Structure - the Filesystem logic:**

 | *<filetypes>* *root*
 |   *<filetype>* :class:`api.dbapi.Filesystem` ( name ) 
 |      *<invalid_char>* :class:`api.dbapi.InvChar` ( descr, char, replacement )

**Example:**

.. code-block:: xml
    
    <?xml version="1.0" encoding="UTF-8"?>
    <filetypes>
        <filetype name="ext3">
            <invalid_char name="SLASH, VIRGULE" char="002F" replacement="or" />
            <invalid_char name="QUOTATION MARK" char="0022" replacement="" />
        </filetype>
        <filetype name="ntfs">
            <invalid_char name="COMMERCIAL AT" char="0040" replacement="at" />
            <invalid_char name="POUND SIGN" char="00A3" replacement="GBP" />
            <invalid_char name="DOLLAR SIGN" char="0024" replacement="USD" />
            <invalid_char name="NUMBER SIGN" char="0023" replacement="No." />
            <invalid_char name="PERCENT SIGN" char="0025" replacement="PerCent" />
            <invalid_char name="QUESTION MARK" char="003F" replacement="Qo" />
            <invalid_char name="EXCLAMATION MARK" char="0021" replacement="" />
            <invalid_char name="PLUS SIGN" char="002B" replacement="plus" />
            <invalid_char name="ASTERISK" char="002A" replacement="" />
            <invalid_char name="REVERSE SOLIDUS" char="005C" replacement=" " />
            <invalid_char name="AMPERSAND" char="0026" replacement="and" />
            <invalid_char name="SLASH, VIRGULE" char="002F" replacement="or" />
            <invalid_char name="QUOTATION MARK" char="0022" replacement="" />
            <invalid_char name="COLON" char="003A" replacement="" />
            <invalid_char name="APOSTROPHE" char="0027" replacement="" />
        </filetype>
    </filetypes>
    
.. note::
    The char field is the unicode value of the invalid character
    
.. note::
    name and replacement can be whatever you like, but keep in mind that replacement needs to be a valid character in the filesystem.
