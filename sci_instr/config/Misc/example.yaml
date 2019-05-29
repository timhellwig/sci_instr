spec: "1.0"

readOnlyProps:
    name        : '*IDN'

readWriteProps:
    prop1    :
       command        : 'test:prop1'
       doc_string     : 'Function of the command; [val1 val2] allowed'
       suffix         : 'chan1'
       value_type     : 'double'    # string, int
       allowed_values : [0.0 , 1.0] # only these values / strings are allowed
       min_value      : 0           # values bigger than this int/double are allowed
       max_value      : 1           # values smaller than this int/double are allowed
       
    prop2   : 'test:prop2'


readBinaryTraces:
    wavelength  :
     command    : :TRAC:X
     suffix     : TRA
    data        :
     command    : :TRAC:Y
     suffix     : TRA