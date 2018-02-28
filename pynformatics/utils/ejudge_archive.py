import struct
import zlib


def strip_cstring(cstring):
    """cstring is c style string with ending zero, return string withoout any extra characters in the end"""
    return cstring.split("\x00")[0]


class VersionError(object):
    """VersionError is exception class for error, when version of Ejudge Archive
    is different from current version of EjudgeArchiveReader"""
    def __init__(self, arg):
        super (VersionError, self).__init__()
        self.arg = arg


class EjudgeArchiveReader:
    """class implements reading ejudge archive format"""

    EJUDGE_ARCHIVE_HEADER_FMT = "8sI4s" #layout of ejudge archive header struct
    EJUDGE_ARCHIVE_ENTRY_HEADER_FMT = "3iI"
    VERSION = 1

    @staticmethod
    def read_header(file):
        """read ejudge_archive_header sructure from begin of file-like object file, 
        return dict: field name -> value"""
        archive_header = dict(zip(
            ("signature", "version", "padding"),
            struct.unpack(
                EjudgeArchiveReader.EJUDGE_ARCHIVE_HEADER_FMT, 
                file.read(struct.calcsize(EjudgeArchiveReader.EJUDGE_ARCHIVE_HEADER_FMT))
                )
            ))
        del archive_header["padding"]
        archive_header["signature"] = strip_cstring(archive_header["signature"].decode('ascii'))
        return archive_header

    @staticmethod
    def read_entry_header(file):
        """read ejudge_archive_entry_header sructure from begin of file-like object file, 
        return dict: field name -> value"""
        read_entry_header = dict(zip(
            ("size", "row_size", "header_size", "flags"),
            struct.unpack(
                EjudgeArchiveReader.EJUDGE_ARCHIVE_ENTRY_HEADER_FMT,
                file.read(struct.calcsize(EjudgeArchiveReader.EJUDGE_ARCHIVE_HEADER_FMT))
                )
            ))
        #in the structure 4 + 4 + 4 + 4 bytes. There are not alignment bytes. After the structure lie name of the file.
        read_entry_header["name"] = strip_cstring(file.read(
            read_entry_header["header_size"] - struct.calcsize(EjudgeArchiveReader.EJUDGE_ARCHIVE_ENTRY_HEADER_FMT)).decode('ascii'))
        return read_entry_header

    def __init__(self, path):
        """arg. path is path to ejudge archive file or file-like(need reading by bytes)
        object with ejudge archve"""
        
        if type(path) == str:
            self.file = open(path, "rb")
        else:
            self.file = path

        if (self.file.read(7) != b'Ej. Ar.'):
            raise ValueError("file is not ejudge archive")

        self.file.seek(0, 2)
        self.arch_size  =  self.file.tell() #getting archive size

        self.file.seek(0)
        self.archive_header = self.read_header(self.file)

        if (self.archive_header["version"] != self.VERSION):
            raise VersionError("Ejudge Archive version is {0}, current supported version is {1}".format(self.archive_header["version"], self.VERSION))

        self.entry_headers_list = list() #list of entry_headers with sequence like in file
        self.files_positions = dict() #filename -> position in ejudge archive

        while self.file.tell() < self.arch_size:
            self.entry_headers_list.append(self.read_entry_header(self.file))
            self.files_positions[self.entry_headers_list[-1]["name"]] = (self.file.tell(), len(self.entry_headers_list) - 1)
            self.file.seek(self.entry_headers_list[-1]["size"], 1) #skip archive data
            self.file.seek((self.file.tell() + 15) & ~15) #alignment

    def namelist(self):
        """return set-like object of strings which contains names of files in archive"""
        return self.files_positions.keys()

    def getfile(self, name):
        """return bytes with data from file
           raise KeyError if is not an file with that name in archive"""
        if name not in self.files_positions:
            raise KeyError("thare is not file with name {0} in archive".format(name))

        if self.entry_headers_list[self.files_positions[name][1]]['size'] == 0:
            return b''

        self.file.seek(self.files_positions[name][0])
        file_row = self.file.read(self.entry_headers_list[self.files_positions[name][1]]['size'])
        data = zlib.decompress(file_row)

        return data
