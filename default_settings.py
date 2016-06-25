"""  Here we set the default values  """

## use_defalut_path: if False the interface opens a file menu to allow to
##choose the directory where with the data.
##Otherwise, the interface uses the data in the default_path

use_default_path = False
default_path='C:\Users\weezy\Dropbox\MESA_python_interface\DATA\M8.0_g0.0_z0.02'


# Widows position and size

window_position_x=50
window_position_y=30

window_size_x=1500
window_size_y=1000


## if load_all_profiles = True, the interface uploads all the profiles.
## if it is set to False, it will upload only the first num_profiles_to_load profiles
load_all_profiles = True
num_profiles_to_load = 10


##        style
font_size_for_plot_labels = 14
plot_line_color = 'black'
lbl_color='blue'
age_line_color='red'

## default abundances and reactions
default_central_abundances=['h1', 'he4', 'c12', 'o16']
default_profile_abundances=['h1', 'he4', 'c12', 'o16']
default_central_reactions=['pp','cno','tri_alfa','burn_c']
default_profile_reactions=['pp','cno','tri_alfa','burn_c'] 

## What format to export plot images as. Valid file types: pgf,svgz,tiff,jpg,raw,jpeg,png,ps,emf,svg,eps,rgba,pdf,tif
plotExportFileType = 'png'
