# sci_instr

Module to communicate with scientific instruments via a VISA connection. Hide actual commands (e.g. SCPI) in a yaml file and access instrument features via automatically generated class properties.

### Purpose

Instead of a lot of SCPI commands that you have to memorize or look up and that clutter the code:
```
osc.write(':CHAN4:POS 0') 
osc.write(':TRIG:LEV4 0.6')
points = osc.query(':ACQuire:POINts')
```
use class properties for easier access and setting of instrument properties:

```
osc.ch4_position = 0
osc.ch4_triglvl  = 0.6
points = osc.points
```

### Prerequisites

You will need pyvisa (https://pyvisa.readthedocs.io/en/stable/), yaml and numpy (e.g. via anaconda https://www.continuum.io/downloads)


### How to use

For usage of an existing instrument you need to import visa and the instrument class you want to use.

```
import visa
from sci_instr.oscilloscope import RS_RTO1044
```
Then generate a visa resource manager and use it in combination with the visa address of your instrument to create an instance of the instrument.

```
rm = visa.ResourceManager()
osc = RS_RTO1044(rm,'TCPIP0::192.168.0.11::inst0::INSTR')
```

### How to create new instruments

For minimal usage you need to create a yaml file with your instrument commands.

*readOnlyProps* contain all instrument properties that are only read and that may return an arbitrary string.

*readWriteProps* can be read and written to and return usually doubles (if post processing of instrument answers is needed you need a subclass of Instrument and define your own *_process_read_values*)

*readBinaryTraces* usually used to transfer larger datasets in binary formats using pyvisas *query_values*

Example: Create a yaml config file in config\Oscilloscopes\TestOsc.yaml:

```
readOnlyProps:
    name        : '*IDN'

readWriteProps:
    time_range  : :TIMebase:RANGe

readBinaryTraces:
    ch1_data    : :CHAN1:WAV1:DATA
```

To then use your instrument use the generic *Instrument* class and tell it which yaml file to use for creating the class properties:


```
import visa
import os
from sci_instr.generic import Instrument


osc = Instrument(rm,'TCPIP0::192.168.0.11::inst0::INSTR',conffile=os.path.join('Oscilloscopes','TestOsc.yaml'))

print(osc.name)
print(osc.time_range)

```

## Authors

* **Tim Hellwig** - *Initial work* -

See also the list of [contributors](https://github.com/timhellwig/sci_instr/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

