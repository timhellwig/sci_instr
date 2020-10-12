""" Scientific - Instrumentation module based on pyvisa

"""

__author__ = 'Tim Hellwig'



import sci_instr.generic
import os
import numpy as np



class AQ6370C(sci_instr.generic.Instrument):
    """Allows easy communication with Yokogawa OSA AQ6370C
    
    Note: Does only work when active trace is TRA
    """  
    
    def __init__(self,visa_rm,address):
        
        
        """Call generic init to connect and prepare instrument"""
        super(AQ6370C, self).__init__(visa_rm,address,conffile=os.path.join('Osa','Yokogawa_AQ6370C.yaml'))
        
        self._visa.write(':init:smode 0;*CLS;:init')
        self._visa.write(':FORMat:DATA REAL,64')
        self._binary_datatype = 'd'
        self._binary_big_endian = False
        self._binary_container = np.array

        
    def start_sweep(self):
        """Sends the trigger to start a sweep"""
        self._visa.write('*CLS;:init')
        
    def is_ready(self):
        """ Query the instrument whether it has succesfully completed
        all operations"""
        out = self._visa.query('STAT:OPER:COND?')
        
        return bool(int(out[0]))
        
    def get_bw_cwl(self):
        """ Query the current cwl and bw (anaylsis mode has to be on"""
        temp = np.fromstring(self._visa.query('CALC:DATA?'),sep = ',')
        fwhm=temp[1]
        cwl=temp[0]
        return fwhm,cwl
    

class HP71451B(sci_instr.generic.Instrument):
    """Allows easy communication with HP OSA HP71451B; GPIB 23 standard port
    
    Note: Does only work when active trace is TRA
    """  
    _getString = '?;'
    def __init__(self,visa_rm,address):
        
        
        """Call generic init to connect and prepare instrument"""
        super(HP71451B, self).__init__(visa_rm,address,conffile=os.path.join('Osa','HP71451B.yaml'))
        
        self._visa.write('TDF P')
        self._visa.values_format.use_ascii('f', ',', np.array)
        
    def start_sweep(self):
        """Sends the trigger to start a sweep"""
        self._visa.write('TS;')
        
    # def is_ready(self):
        """ Query the instrument whether it has succesfully completed
        all operations"""
        # out = self._visa.query('STAT:OPER:COND?')
        
        # return bool(int(out[0]))
        
        
    def _process_read_values(self,string,value_type):
        """Usually we expect returning a float; inhereted classes can specify"""
        if value_type == 'float':
           return float(string)*1e9 # nm
        elif value_type == 'int':
            return int(string)
        else:
            return string
            
    def get_wavelength(self):
        center = self.centerwl
        span = self.span
        return np.linspace(center-span/2,center+span/2,num=self.points,endpoint=True)    
