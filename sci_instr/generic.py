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
            
            options = {}
            options['doc_string'] = ''
            options['suffix']  = ''
            options['value_unit']=''
            options['min_value'] = None
            options['max_value'] = None
            options['allowed_values'] = None
            options['value_type'] = 'float'
            
            
            #Simple format for this property?
            if not(type(self._readWriteProps[prop]) is dict):
                
                visa_string_get = self._readWriteProps[prop]+self._getString
                visa_string_set = self._readWriteProps[prop]+self._setString+self._formatString
                
                def getter( self ):
                    return self._process_read_values(self._visa.query(visa_string_get),options['value_type'])
                def setter( self,value ):
                    self._visa.write(visa_string_set.format(value))
                    if self._expctResponse is not None:
                        response = self._visa.read()
                        if not response == self._expctResponse:
                            msg = 'Response was: {}; expected: {}'.format(response,self._expctResponse)
                            raise AttributeError(msg)
                
                    retvalue = self.__getattribute__(prop)
                    if not value == retvalue:
                        msg = 'Set value: {}; returned value: {}'.format(value,retvalue)
                        raise AttributeError(msg)
                
            # Complex format readWriteProps[prop] is a dictionary with additional information
            else:
                prop_dict = self._readWriteProps[prop]
                
                # First check for command as this is needed
                if 'command' in prop_dict:
                    command = prop_dict['command']
                else:
                    raise AttributeError('No Command specified for property ' + prop)
                
                #Check if any other known option is present
                for value in (('doc_string','suffix','value_type','allowed_values','min_value','max_value','value_unit')):
                    if  value in prop_dict:
                     options[value] = prop_dict[value]
                
                visa_string_get = command+self._getString + ' ' + options['suffix']
                visa_string_set = command+self._setString + ' ' + options['suffix'] + self._formatString + options['value_unit']
                
                def getter( self ):
                    return self._process_read_values(self._visa.query(visa_string_get),options['value_type'])
                    
                def setter( self,value ):
                    #first check if value is within allowed values
                    if not(options['allowed_values'] is None):
                        if not(value in options['allowed_values']):
                            msg = 'Tried to set: {}; allowed only: {}'.format(value,options['allowed_values'])
                            raise AttributeError(msg)
                    
                    #check if value is within min/max
                    if not(options['min_value'] is None):
                        if value <= options['min_value']:
                            msg = 'Tried to set: {}; allowed only values >= {}'.format(value,options['min_value'])
                            raise AttributeError(msg)
                    if not(options['max_value'] is None):
                        if value >= options['max_value']:
                            msg = 'Tried to set: {}; allowed only values <= {}'.format(value,options['max_value'])
                            raise AttributeError(msg)
                    
                    self._visa.write(visa_string_set.format(value))
                    if self._expctResponse is not None:
                        response = self._visa.read()
                        if not response == self._expctResponse:
                            msg = 'Response was: {}; expected: {}'.format(response,self._expctResponse)
                            raise AttributeError(msg)
                
                    retvalue = self.__getattribute__(prop)
                    if not value == retvalue:
                        msg = 'Set value: {}; returned value: {}'.format(value,retvalue)
                        raise AttributeError(msg)
                
                
            return property(getter,setter,doc = options['doc_string'])
            
        def make_read_only_instr_prop(prop):
            """ Getter for read only properties"""
            
            def getter( self ):
                return self._visa.query(self._readOnlyProps[prop]+self._getString)
            return property(getter)
            
        def make_read_binary_instr_data(prop):
            """ Getter for binary arrays"""
            
            #Sometimes we need a suffix to address the different traces
            if type(self._readBinaryTraces[prop]) is dict:
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

    def _process_read_values(self,string,value_type):
        """Usually we expect returning a float; inhereted classes can specify"""
        if value_type == 'float':
            return float(string)
        elif value_type == 'int':
            return int(string)
        else:
            return string

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