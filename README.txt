README

(Very) Basic instructions to use MESAPlot.

MESAPlot replaces MESAFace. 
It is a lot similar to its predecessor MESAFace, but it is written in Python and so it is completely open source. 
It is also a little faster than MESAFace and it will grow to be much better.

The MESAPlot folder has several files. 
The file you run is MESAplot_v0.3.2.py by double clicking on it. A helpful settings file is default_settings.py. 
This one is for you to modify as you like. If you open default_settings, you'll see

use_default_path = False
default_path='C:\Users\weezy\Dropbox\MESA_python_interface\DATA\M8.0_g0.0_z0.02'

You can also change other things, such as the format to save plots as.

If you change use_default_path to True, and change default_path to point to the folder with the MESA output data, it will skip the folder selection window and automatically open that data when you open MESAplot_v0.3.0.2.py.
When you then run MESAplot_v0.3.2.py (for example, double click on the icon), the interface should start uploading the files in your folder. 
NOTE: you should have only one history and at least one profile in the data folder. 
The names have to be history and profile. For now, you cannot upload files with different names but we plan to implement this functionality soon.

If you set keep use_default_path on False, opening MESAplot_v0.3.2.py will immediately open a folder selection dialog.

There were previously issues on mac with this dialog, but now it seems to be fixed entirely. In any case, if it does not work just enter the path by hand in default_settings.py.

The interface is graphical and dynamical. The use is very intuitive and should require no specific instructions.

For questions, contact mgiannotti@barry.edu or mwise@barry.edu 

Let us know
Maurizio Giannotti, Michael Wise, Wesam Azaizeh, Daria Vasilyeva, Sanja Zivanovic
