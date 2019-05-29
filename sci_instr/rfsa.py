""" Scientific - Instrumentation module based on pyvisa

"""

__author__ = 'Tim Hellwig'



import sci_instr.generic
import os
import numpy as np



class N9000A(sci_instr.generic.Instrument):
    """Allows easy communication with Agilent RFSA N9000A
    
    
    """  
    
    def __init__(self,visa_rm,address):
        
        
        """Call generic init to connect and prepare instrument"""
        super(N9000A, self).__init__(visa_rm,address,conffile=os.path.join('RFSA','Agilent_N9000A.yaml'))
        
        # self._visa.write(':init:smode 0;*CLS;:init')
        self._visa.write(':FORMat:TRACe:DATA REAL,64')
        self._visa.write(':FORMat:BORDer SWAPped')
        self._visa.values_format.use_binary('d', False, np.array)
        
    def mark2cent(self):
        """Sets the center freq to current marker X"""
        self._visa.write(':CALC:MARK:CENT')
        
    def mark2ref(self):
        """Sets the ref lvl to current marker Y"""
        self._visa.write(':CALC:MARK:RLEV')
        
    def mark_findMax(self):
        """Sets the marker to maximum"""
        self._visa.write(':CALC:MARK:MAX')  
     
    
    def average_clear(self):
        """Clears the average acquisition when in average or max hold mode"""
        self._visa.write(':AVER:CLE')
    
        
    
    
    

class MS2721(sci_instr.generic.Instrument):
    """Allows easy communication with Anritsu RFSA MS2721
    
    
    """  
    
    def __init__(self,visa_rm,address):
        
        
        """Call generic init to connect and prepare instrument"""
        super(MS2721, self).__init__(visa_rm,address,conffile=os.path.join('RFSA','Anritsu_MS2721.yaml'))
        
        # self._visa.write(':init:smode 0;*CLS;:init')
        self._visa.write(':FORMat:DATA REAL,32')
        
        self._visa.values_format.use_binary('f', False, np.array)
        
    def mark2cent(self):
        """Sets the center freq to current marker X"""
        self._visa.write(':CALC:MARK:CENT')
        
    def mark2ref(self):
        """Sets the ref lvl to current marker Y"""
        self._visa.write(':CALC:MARK:RLEV')
        
    def mark_findMax(self):
        """Sets the marker to maximum"""
        self._visa.write(':CALC:MARK:MAX')  
     
    

        
