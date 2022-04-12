# rheocal
The rheocal project aims at developing a simple tool to automatically calibrate rheological models for generalized newtonian fluids based on experimental viscosity measurements.

## Usage

```python

```
## User guide

When running the rheocal.py program, the user interface will pop up. This window can be resized or minimized. 

### 1. Input file format
The "Help" tab is by default the first tab opened. It shows a picture of how data should be entered in the input file in order for the program to execute properly. 

The file must contain two columns:
- shear rate values on the left
- viscosity values on the right

There must be no header and the period is used for decimal separator.

### 2. Select an input file
Click on the "Input" tab and then click on the "Browse file" button to select a file. On the pop-up window, you may then select a .txt or .csv (comma separated format) file from your directories. 

Once the file is selected, the name of the file will show up in the empty space at the top (see picture) and a frame on the right will show a graph of the entered data on a logarithmic scale. If the wrong file updloaded, or if the is a change to make, another file can be selected instead by direclty using the "Browse file" button again.

note: the file does not have to be in the ********

### 3. Selecting a rheology model
If the input file name and the input data graph show up correctly, you may then select a rheology model by opening the dropown menu (default model is the Power Law model). Once you have selected, click the "Ok" button.

*Once selected, the rheology model cannot be changed!

The equation of the selected model will show up in a frame below. 

### Entering guess values
Guess values can be entered in the white boxes. For Croos and Carreau models, the default values for 






It might not show on top but taskbar

## Roadmap

- incertitudes sur les valeurs
- fix a, or multiple parameters
- error warning explained to user
- flexible input
- autofit function
- guess function
- Carreau-Yasuda (5 parameters)
- p values
- change selected model
- rerun file
## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## Authors
