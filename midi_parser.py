import sys  # remove after testing
import enum

class _MidiFormat(enum.Enum):
    single = b'\x00\x00'
    multiple = b'\x00\x01'
    mal_multiple = b'\x00\x10'


_HEADER_PREFIX = b'\x4D\x54\x68\x64'
_HEADER_LENGTH = b'\x00\x00\x00\x06'
_ENDIAN = "big"


def _parse_header(byte_stream):
    if byte_stream[0:4] != _HEADER_PREFIX:  
        raise ValueError("Malformed Midi: Found %s, expected %s" % (byte_stream[0:4], _HEADER_PREFIX))        
    elif byte_stream[4:8] != _HEADER_LENGTH:
        raise ValueError("Malformed Midi: Found '%s', expected '%s'" % (byte_stream[4:8], _HEADER_LENGTH)) 

    format = int.from_bytes(byte_stream[8:10], _ENDIAN)
    if format == _MidiFormat.mal_multiple:
        raise ValueError("Program only accepts Midi format types 'single' and 'multiple'")

    tracks = int.from_bytes(byte_stream[10:12], _ENDIAN)
    deltas = int.from_bytes(byte_stream[12:14], _ENDIAN)

    return (format, tracks, deltas)

def parse_midi(midi_file_name):
    with open(midi_file_name, 'rb') as midi:
        try:
            header_values = _parse_header(midi.read(12))
        except ValueError as e:
            print(e)
            return
        format, tracks, deltas = header_values
        print(header_values)

  
def main():
    parse_midi(sys.argv[1])
        
     
if __name__ == "__main__":
    main()