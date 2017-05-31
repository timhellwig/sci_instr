""" Scientific - Instrumentation module based on pyvisa

"""

__author__ = 'Tim Hellwig'

import visa 
import numpy as np
import os
import yaml



class Instrument:
    """This class should allow easy setting and getting values and
    measurement data of common Visa Instruments like Oscilloscopes,
    Optical Spectrum Analyzer or Radio Frequency Spectrum Analyzer
    
    This class is intended to inherit from and implement specific
    _readOnlyProps etc lists. Furthermore implement own is_ready
    function """
    
    _readOnlyProps = {'name':'*IDN'}
    _readWriteProps={'voltage':':VOLT:IMM:AMPL'} 
    _readBinaryTraces={'wavelength':'TRACEX'}
    
    _visa = None
    _getString = '?'
    _setString = ' '
    _expctResponse = None
    _formatString = '{}'
    
    
    def __init__(self,visa_rm,address,conffile=None):
        """Connects to the Instrument and prepares properties"""
        
        
        if conffile is not None:
            cfg_path = os.path.join(os.path.dirname(__file__), 'config',conffile)
            with open(cfg_path, 'r') as ymlfile:
                cfg = yaml.load(ymlfile)
            
            self._readOnlyProps=cfg['readOnlyProps']
            self._readWriteProps=cfg['readWriteProps']
            self._readBinaryTraces=cfg['readBinaryTraces']        
        
        _rm = visa_rm
        
        self._visa = _rm.open_resource(address)
        self._visa.values_format.use_binary('f', False, np.array)

        def make_instr_prop(prop):
            """Getter and setter dynamically for read write
            properties"""
            
            def getter( self ):
                return self._process_read_values(self._visa.query(self._readWriteProps[prop]+self._getString))
            def setter( self,value ):
                self._visa.write(self._readWriteProps[prop]+self._setString+self._formatString.format(value))
                if self._expctResponse is not None:
                    response = self._visa.read()
                    if not response == self._expctResponse:
                        msg = 'Response was: {}; expected: {}'.format(response,self._expctResponse)
                        raise AttributeError(msg)
               
                retvalue = self.__getattribute__(prop)
                if not value == retvalue:
                    msg = 'Set value: {}; returned value: {}'.format(value,retvalue)
                    raise AttributeError(msg)
            return property(getter,setter)
            
        def make_read_only_instr_prop(prop):
            """ Getter for read only properties"""
            
            def getter( self ):
                return self._visa.query(self._readOnlyProps[prop]+self._getString)
            return property(getter)
            
        def make_read_binary_instr_data(prop):
            """ Getter for binary arrays"""
            
            #Sometimes we need a suffix to address the different traces
            if type(self._readBinaryTraces['wavelength']) is dict:
                def getter( self ):
                    return self._visa.query_values(self._readBinaryTraces[prop]['command']+self._getString+' '+self._readBinaryTraces[prop]['suffix'])
            else:
                def getter( self ):
                    return self._visa.query_values(self._readBinaryTraces[prop]+self._getString)
            return property(getter)
            


        # add all the properties
        for i in self._readOnlyProps or {}:
            setattr(self.__class__, i, make_read_only_instr_prop(i))
        for i in self._readWriteProps or {}:
            setattr(self.__class__, i, make_instr_prop(i))
        for i in self._readBinaryTraces or {}:
            setattr(self.__class__, i, make_read_binary_instr_data(i))
            


    def _process_read_values(self,string):
        """Usually we expect returning a float; inhereted classes can specify"""
        return float(string)

    def is_ready(self):
        """ Query the instrument whether it has succesfully completed
        all operations"""
        
        return True
        
        
    def __del__(self):
        if self._visa is not None:
            self._visa.close()
            
        
if __name__ == "__main__":
    b = Instrument(visa.ResourceManager('@sim'),'ASRL2::INSTR')
    
    print(b.name)
    print(b.voltage)