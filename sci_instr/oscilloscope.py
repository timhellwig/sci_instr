""" Scientific - Instrumentation module based on pyvisa

implements different Oscilloscopes
"""

__author__ = 'Tim Hellwig'



import sci_instr.generic
import os


class RS_RTO1044(sci_instr.generic.Instrument):
    """Allows easy communication with R&S Oscilloscope RTO1044"""  
    
    def __init__(self,visa_rm,address):
        
        
        """Call generic init to connect and prepare instrument"""
        super(RS_RTO1044, self).__init__(visa_rm,address,conffile=os.path.join('Oscilloscopes','RS_RTO1044.yaml'))
        
        self._visa.write('FORM REAL,32;')
        

        
    def is_ready(self):
        """ Query the instrument whether it has succesfully completed
        all operations"""
        out = self._visa.query(':stat:oper:even?')
        
        return bool(out[0])
    
        
