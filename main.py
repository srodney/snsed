import snsedextend
from astropy.table import Table
import matplotlib.pyplot as plt
import numpy as np
import glob,os,sys
from astropy.table import vstack
from astropy.io import ascii
import sncosmo
import pickle

sndataroot = os.environ['SNDATA_ROOT']


dir='hicken'
<<<<<<< HEAD
snType=['II']
filelist=[os.path.basename(file) for file in glob.glob(os.path.join(dir,'*.dat'))]
=======
snType=['II','IIP']
filelist=[os.path.basename(file) for file in ['hicken/lc_2009ay','hicken/lc_2010bq']]#glob.glob(os.path.join(dir,'*.dat'))]
>>>>>>> master
#filelist=['lc_2002bx.dat','lc_2006ca.dat','lc_2006cd.dat','lc_2006it.dat','lc_2007aa.dat','lc_2007av.dat','lc_2008bj.dat','lc_2008bn','lc_2008in.dat','lc_2009ay.dat','lc_2009kn.dat',]
#IIn=['lc_2008ip.dat','lc_2010bq.dat']
sn,redshift=np.loadtxt(os.path.join(dir,'redshift.ref'),dtype='str',unpack=True)
redshift={sn[i]:redshift[i] for i in range(len(sn))}
sn,colors=np.loadtxt(os.path.join(dir,'color.ref'),dtype='str',unpack=True)
colors={sn[i]:colors[i] for i in range(len(sn))}
sn,dusts=np.loadtxt(os.path.join(dir,'dust.ref'),dtype='str',unpack=True)
dust={sn[i]:dusts[i] for i in range(len(sn))}
sn,types=np.loadtxt(os.path.join(dir,'type.ref'),dtype='str',unpack=True)
typ={sn[i]:types[i] for i in range(len(sn))}
sne,peaks=np.loadtxt(os.path.join(dir,'timeOfPeak.ref'),dtype='str',unpack=True)
peaks={sne[i]:float(peaks[i]) for i in range(len(sne))}

typeColors=None

for k in colors:
    if len(colors[k])>3:
        colors[k]=colors[k].split(',')
    elif not isinstance(colors[k],(list,tuple)):
        colors[k]=[colors[k]]


colorTables=[]
typeSNe=None
vrDict=dict([])
for i in range(len(filelist)):
    if typ[filelist[i][:-4]] in snType:# and filelist[i] not in ['lc_2005kl_clipped.dat','lc_2005az_clipped.dat','lc_2008aq_clipped.dat','lc_2007av_clipped.dat']:#['lc_2006fo_clipped.dat','lc_2006jc_clipped.dat','lc_2004ao_clipped.dat','lc_2007D_clipped.dat','lc_2005bf_clipped.dat','lc_2005nb_clipped.dat','lc_2006ld_clipped.dat']:

        print(filelist[i])
        #if filelist[i]:# in ['lc_2005bf_clipped.dat','lc_2005hg_clipped.dat']:
        #print(colors[filelist[i][:-12]],typ[filelist[i][:-12]],'vega',{'hostebv':(-1,1),'t0':(peaks[filelist[i][:-12]]-5,peaks[filelist[i][:-12]]+5)},{'z':redshift[filelist[i][:-12]],'hostr_v':3.1,'mwr_v':3.1,'mwebv':dust[filelist[i][:-12]]},'CCM89Dust',
        #      ['rest','obs'],['host','mw'])
        temp,vr=snsedextend.curveToColor(os.path.join(dir,filelist[i]),['U-B','r-J','r-H','r-K'],snType=typ[filelist[i][:-4]],zpsys='Vega',
                                      bounds={'hostebv':(-1,1),'t0':(peaks[filelist[i][:-4]]-5,peaks[filelist[i][:-4]]+5)},
                                      constants={'z':redshift[filelist[i][:-4]],'hostr_v':3.1,'mwr_v':3.1,'mwebv':dust[filelist[i][:-4]]},
                                      dust='CCM89Dust',effect_frames=['rest','obs'],effect_names=['host','mw'])

        #else:
        #    continue
        """
        for color in colors[filelist[i][:-12]]:
            fig=plt.figure()
            ax=plt.gca()
            ax.errorbar(np.array(colorTable['time'][colorTable[color].mask==False]),np.array(colorTable[color][colorTable[color].mask==False]),
                        yerr=np.array(colorTable[color.replace('-','')+'_err'][colorTable[color].mask==False]),fmt='x')
            ax.set_title(filelist[i][3:])
            ax.invert_yaxis()
            plt.title(color+' Color')
            fig.text(0.5, 0.01, 'Time (Since Peak)', ha='center')
            fig.text(0.01, 0.5, 'Color Magnitude (Vega)', va='center', rotation='vertical')
            plt.savefig(os.path.join(dir,"type"+type[0],"plots",filelist[i][:-12]+"_"+color[0]+color[-1]+".pdf"),format='pdf')
            plt.close()
        
        if typeColors:
            typeSNe=typeSNe+[filelist[i][:-12].replace('lc','SN') for j in range(len(colorTable))]

            typeColors=vstack([typeColors,colorTable])
        else:
            typeSNe=[filelist[i][:-12].replace('lc','SN') for j in range(len(colorTable))]
            typeColors=colorTable
        
        if typeSNe:
            typeSNe=typeSNe+[filelist[i][:-12].replace('lc','SN') for j in range(len(colorTable))]
        """
        typeSNe=[filelist[i][:-4].replace('lc','SN') for j in range(len(temp))]
        temp['SN']=typeSNe
        vrDict[typeSNe[0]]=vr
        temp.remove_columns([x for x in temp.colnames if x in ['B-J','B-H','B-K','u-B']])
        if len(temp.colnames)>1:
            colorTables.append(temp)
            #snsedextend.extendNon1a(colorTable,sedlist='SDSS-0 13449.SED',verbose=True)
#['SN']=typeSNe
#sys.exit()
#typeColors=ascii.read(os.path.join('hicken','typeII','tables','allIIColors.dat'))
#import matplotlib.pyplot as plt
#fig=plt.figure()
#ax=fig.gca()
#col='R/(B+V'
#colDict={'SN_2005hg':'b','SN_2006fo':'k','SN_2007C':'g','SN_2008D':'orange','SN_2009iz':'cyan','SN_2009jf':'violet'}
#colDict={'SN_2005kl':'b','SN_2006aj':'g','SN_2005mf':'k','SN_2007D':'orange','SN_2007I':'cyan','SN_2007gr':'violet'}
#for sn in vrDict.keys():
#    if sn in colDict.keys():
#        ax.plot(np.arange(-20,100,1),vrDict[sn],label=sn,color=colDict[sn])
#ax.legend()
#ax.set_title(col)
#plt.savefig(snType[0]+'_'+'test'+'.pdf',format='pdf',overwrite=True)
#sys.exit()
typeColors=snsedextend.colorTableCombine(colorTables)

ascii.write(typeColors,os.path.join('snsedextend','data','default','type'+snType[0],snType[0]+'Colors.dat'))
#with open('tempvr.dat','wb') as handle:
#    pickle.dump(vrDict,handle)


typeColors=ascii.read(os.path.join('snsedextend','data','default','type'+snType[0],snType[0]+'Colors.dat'))
#handle= open('tempvr.dat','rb')
#vrDict=pickle.load(handle)
curveDict=snsedextend.fitColorCurve(typeColors,type=snType[0],savefig=True)
#sys.exit()

with open(os.path.join('snsedextend','data','default','type'+snType[0],snType[0]+'Curve.pick'),'wb') as handle:
    pickle.dump(curveDict,handle)

<<<<<<< HEAD
#typeColors=ascii.read(os.path.join('snsedextend','data','default','type'+snType[0],snType[0]+'Colors.dat'))
=======

typeColors=ascii.read(os.path.join('snsedextend','data','default','type'+snType[0],snType[0]+'Colors.dat'))
>>>>>>> master

#typeColors=ascii.read(os.path.join(dir,'type'+snType[0],'tables','all'+snType[0]+'Colors.dat'))

'''
#    sys.exit()
###### for debugging#####
typeColors=ascii.read(os.path.join('snsedextend','data','default','type'+snType[0],snType[0]+'Colors.dat'))

handle= open(os.path.join('snsedextend','data','default','type'+snType[0],snType[0]+'Curve.pick'),'rb')
curveDict=pickle.load(handle)
seds=np.loadtxt(os.path.join('snsedextend','data','default','NON1A.LIST'),dtype='str',unpack=True)
sedlist=[seds[3][i]+'.SED' for i in range(len(seds[3])) if seds[2][i] in snType and seds[3][i]+'.SED' in [os.path.basename(x) for x in glob.glob(os.path.join(sndataroot,'snsed','NON1A','*.SED'))]]


#sedlist=[os.path.join(sndataroot,'snsed','NON1A','CSP-2004fe.SED')]
seds=snsedextend.extendCC(typeColors,curveDict,snType[0],outFileLoc=os.path.join('/Users','jpierel','rodney','SED_Repository','SEDs','Type_'+snType[0]),colorExtreme='median',sedlist=sedlist,zpsys='Vega',verbose=True)

#snsedextend.extendNon1a(colorTable,sedlist='SDSS-0 13449.SED',verbose=True)
#typeColors.sort('time')
#sncosmo.write_lc(typeColors,'lcs_clipped2/tables/allColors.dat')
