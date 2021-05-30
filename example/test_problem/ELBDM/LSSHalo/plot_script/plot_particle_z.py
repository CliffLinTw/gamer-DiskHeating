import argparse
import sys
import yt
import numpy as np

# load the command-line parameters
parser = argparse.ArgumentParser( description='Plot the gas slices and projections' )

parser.add_argument( '-p', action='store', required=False, type=str, dest='prefix',
                     help='path prefix [%(default)s]', default='../' )
parser.add_argument( '-s', action='store', required=True,  type=int, dest='idx_start',
                     help='first data index' )
parser.add_argument( '-e', action='store', required=True,  type=int, dest='idx_end',
                     help='last data index' )
parser.add_argument( '-d', action='store', required=False, type=int, dest='didx',
                     help='delta data index [%(default)d]', default=1 )

args=parser.parse_args()

# take note
print( '\nCommand-line arguments:' )
print( '-------------------------------------------------------------------' )
for t in range( len(sys.argv) ):
   print( str(sys.argv[t]))
print( '' )
print( '-------------------------------------------------------------------\n' )


idx_start   = args.idx_start
idx_end     = args.idx_end
didx        = args.didx
prefix      = args.prefix

colormap    = 'arbre'
dpi         = 150
field       = 'particle_mass'
#den_center      = [ 0.0903406605576024, 0.0897010051842892, 0.0899995110251686 ]

center = np.loadtxt('../../../tool/analysis/gamer_extract_profile/Run/Data_c8H/CenterCoords', skiprows=1, dtype=float)
print(center)

yt.enable_parallelism()

ts = yt.load( [ prefix+'/Data_%06d'%idx for idx in range(idx_start, idx_end+1, didx) ] )
ID = 0

for ds in ts.piter():
   #Box = ds.region(center=[0.0437713623,0.0441131592, 0.0437713623], left_edge=[0.0436713623,0,0], right_edge=[0.0438713623,0.0875,0.0875])
   #par = yt.SlicePlot( ds, 0, fields = field, center=[0.0437713623,0.0441131592, 0.0437713623], width = (40,'kpc') )
   par = yt.ParticleProjectionPlot( ds, 2, fields = field, width = (25,'kpc') )
   par.set_background_color( field )
   par.set_zlim( field, 5.334838e+2/1, 5.334838e+5/1, dynamic_range=None)
   par.set_cmap( field, colormap )
   par.set_font( {'size':16} )
   par.set_axes_unit( 'kpc' )
   par.set_unit( field, 'Msun' )
   par.annotate_sphere( center[ID,3:], radius=(0.05, 'kpc'),circle_args={'color':'red'})
   par.annotate_timestamp( time_unit='Myr', corner='upper_right', text_args={'color':'k'} )
   par.save( mpl_kwargs={"dpi":dpi} )
   ID += 1

