#def make_slip_slice(rupt,out):
#    '''
#    Make .slip files for GMT animation
#    '''
#    
#    from numpy import genfromtxt,savetxt,unique,where,zeros,arange,intersect1d,trapz,c_
#    from string import rjust
#    
#    #Run parameters
#    
#    dt=15
#    cumul=0 #Time slices or cumulative slip?
#    #########
#    
#    delta_t=0.01
#    f=genfromtxt(rupt)
#    trupt=f[:,12]
#    trise=f[:,7]
#    all_ss=f[:,8]
#    all_ds=f[:,9]
#    num=f[:,0]
#    #Get other parameters
#    #lon=f[0:len(unum),1]
#    #lat=f[0:len(unum),2]
#    #strike=f[0:len(unum),4]
#    #Decide on time vector
#    tslice=arange(0,trupt.max()+dt,dt)
#    #Determine triangle height at all subfaults
#    hss=2*all_ss/trise
#    hds=2*all_ds/trise
#    #Cumulative
#    ss_cumul=zeros(len(f))
#    ds_cumul=zeros(len(f))
#    #Determine time series fo each triangle
#    t=arange(0,trupt.max()+trise[0],delta_t)
#    for kslice in range(len(tslice-2)):
#        print str(kslice)+'/'+str(len(tslice)-1)
#        #And initalize slice vectors
#        ss_slice=zeros(len(f))
#        ds_slice=zeros(len(f))
#        for kfault in range(len(f)):
#            yss=zeros(t.shape)
#            yds=zeros(t.shape)
#            #Up going
#            i1=where(t>=trupt[kfault])[0]
#            i2=where(t<=(trupt[kfault]+trise[0]/2))[0] #Ascending triangle
#            i=intersect1d(i1,i2)
#            yss[i]=(2*hss[kfault]/trise[0])*t[i]-(2*hss[kfault]*trupt[kfault]/trise[0])
#            yds[i]=(2*hds[kfault]/trise[0])*t[i]-(2*hds[kfault]*trupt[kfault]/trise[0])
#            #Down going
#            i1=where(t>(trupt[kfault]+trise[0]/2))[0]
#            i2=where(t<=(trupt[kfault]+trise[0]))[0] #Ascending triangle
#            i=intersect1d(i1,i2)
#            yss[i]=(-2*hss[kfault]/trise[0])*t[i]+(2*hss[kfault]/trise[0])*(trupt[kfault]+trise[0])
#            yds[i]=(-2*hds[kfault]/trise[0])*t[i]+(2*hds[kfault]/trise[0])*(trupt[kfault]+trise[0])
#            #Now integrate slip at pertinent time interval
#            i1=where(t>=tslice[kslice])[0]
#            i2=where(t<=tslice[kslice+1])[0]
#            i=intersect1d(i1,i2)
#            ss_slice[kfault]=trapz(yss[i],t[i])
#            ds_slice[kfault]=trapz(yds[i],t[i])
#        #Combine into single model for that time slice
#        ss_cumul=ss_cumul+ss_slice
#        ds_cumul=ds_cumul+ds_slice
#        unum=unique(num)
#        lon=f[0:len(unum),1]
#        lat=f[0:len(unum),2]
#        depth=f[0:len(unum),3]
#        ss=zeros(len(unum))
#        ds=zeros(len(unum))
#        for k in range(len(unum)):
#            if cumul==0:
#                i=where(unum[k]==num)
#                ss[k]=ss_slice[i].sum()
#                ds[k]=ds_slice[i].sum()  
#                outname='slice'  
#            else:
#                i=where(unum[k]==num)
#                ss[k]=ss_cumul[i].sum()
#                ds[k]=ds_cumul[i].sum() 
#                outname='cumul'       
#        #Write outfile
#        fname=out+rjust(str(kslice),4,'0')+'.'+outname+'.slip'
#        savetxt(fname, c_[lon,lat,depth,ss,ds],fmt='%.6f\t%.6f\t%.4f\t%.2f\t%.2f')
      
def make_total_model(rupt,thresh):
    from numpy import genfromtxt,unique,where,zeros,c_,savetxt,sqrt
    
    f=genfromtxt(rupt)
    num=f[:,0]
    all_ss=f[:,8]
    all_ds=f[:,9]
    #Now parse for multiple rupture speeds
    unum=unique(num)
    ss=zeros((len(unum),1))
    ds=zeros((len(unum),1))
    lon=f[0:len(unum),1]
    lat=f[0:len(unum),2]
    for k in range(len(unum)):
        i=where(unum[k]==num)
        ss[k]=all_ss[i].sum()
        ds[k]=all_ds[i].sum()
    #Apply threshold
    i=where(sqrt(ss**2+ds**2)<thresh)[0]
    ss[i]=0
    ds[i]=0
    fname=rupt+'.total'
    savetxt(fname, c_[f[0:len(unum),0:8],ss,ds,f[0:len(unum),10:12],f[0:len(unum),13]],fmt='%d\t%10.4f\t%10.4f\t%8.4f\t%8.2f\t%6.2f\t%6.2f\t%6.2f\t%12.4e\t%12.4e\t%8.2f\t%8.2f\t%8.4e')
    
def make_subfault(rupt):
    from numpy import genfromtxt,unique,where,zeros,c_,savetxt
    
    f=genfromtxt(rupt)
    num=f[:,0]
    all_ss=f[:,8]
    all_ds=f[:,9]
    #Now parse for multiple rupture speeds
    unum=unique(num)
    ss=zeros(len(unum))
    ds=zeros(len(unum))
    lon=f[0:len(unum),1]
    lat=f[0:len(unum),2]
    for k in range(len(unum)):
        i=where(unum[k]==num)
        ss[k]=all_ss[i].sum()
        ds[k]=all_ds[i].sum()
    #Sum them
    fname=rupt+'.total.slip'
    savetxt(fname, c_[lon,lat,ss,ds],fmt='%.6f\t%.6f\t%6.2f\t%6.2f',header='# No,lon,lat,z(km),strike,dip,rise,duration(s),ss-slip(m),ds-slip(m),ss_len(m),ds_len(m),rigidity(Pa)')
    
    
    
def make_sliprate_ruptfiles(rupt,nstrike,ndip,epicenter,out,tmax,dt):
    '''
    Make sliprate .rupt files for plotting several frames with tile_slip and
    animating with ffmpeg. Only write dip slip component regardless of the actual
    rake angle. We're just plotting scalar slip rate... 
    '''
    from numpy import genfromtxt,unique,zeros,where,arange,interp,c_,savetxt
    from mudpy.forward import get_source_time_function,add2stf
    from string import rjust
    
    f=genfromtxt(rupt)
    num=f[:,0]
    nfault=nstrike*ndip
    unum=unique(num)
    lon=f[0:len(unum),1]
    lat=f[0:len(unum),2]
    depth=f[0:len(unum),3]
    #Get slips
    all_ss=f[:,8]
    all_ds=f[:,9]
    #Now parse for multiple rupture speeds
    unum=unique(num)
    #Count number of windows
    nwin=len(where(num==unum[0])[0])
    #Get rigidities
    mu=f[0:len(unum),13]
    #Get rise times
    rise_time=f[0:len(unum),7]
    #Get areas
    area=f[0:len(unum),10]*f[0:len(unum),11]
    #Get indices for plot
    istrike=zeros(nstrike*ndip)
    idip=zeros(nstrike*ndip)
    k=0
    t=arange(0,tmax,dt)
    for i in range(ndip):
         for j in range(nstrike):
             istrike[k]=nstrike-j-1
             idip[k]=i
             k+=1  
    #Loop over subfaults
    for kfault in range(nfault):
        if kfault%10==0:
            print '... working on subfault '+str(kfault)+' of '+str(nfault)
        #Get rupture times for subfault windows
        i=where(num==unum[kfault])[0]
        trup=f[i,12]
        #Get slips on windows
        ss=all_ss[i]
        ds=all_ds[i]
        #Add it up
        slip=(ss**2+ds**2)**0.5
        #Get first source time function
        t1,M1=get_source_time_function(mu[kfault],area[kfault],rise_time[kfault],trup[0],slip[0])
        #Loop over windows
        for kwin in range(nwin-1):
            #Get next source time function
            t2,M2=get_source_time_function(mu[kfault],area[kfault],rise_time[kfault],trup[kwin+1],slip[kwin+1])
            #Add the soruce time functions
            t1,M1=add2stf(t1,M1,t2,M2)
        if kfault==0: #Intialize
            M=zeros((len(t),nfault))
            T=zeros((len(t),nfault))
        Mout=interp(t,t1,M1)
        M[:,kfault]=Mout
        T[:,kfault]=t
    #Now look through time slices
    maxsr=0
    #First retain original rupture information
    ruptout=f[0:len(unum),:]
    ruptout[:,8]=0 #Set SS to 0
    print 'Writing files...'
    for ktime in range(len(t)):
        sliprate=zeros(lon.shape)
        for kfault in range(nfault):
            i=where(T[:,kfault]==t[ktime])[0]
            sliprate[kfault]=M[i,kfault]/(mu[kfault]*area[kfault])
        ruptout[:,9]=sliprate #Assign slip rate to SS component    
        maxsr=max(maxsr,sliprate.max())
        fname=out+rjust(str(ktime),4,'0')+'.sliprate'
        #Write as a rupt file
        fmtout='%6i\t%.4f\t%.4f\t%8.4f\t%.2f\t%.2f\t%.2f\t%.2f\t%12.4e\t%12.4e%10.1f\t%10.1f\t%8.4f\t%.4e'
        savetxt(fname,ruptout,fmtout,header='No,lon,lat,z(km),strike,dip,rise,dura,ss-slip(m),ds-slip(m),ss_len(m),ds_len(m),rupt_time(s),rigidity(Pa)')
    print 'Maximum slip rate was '+str(maxsr)+'m/s'    
    
    
def make_sliprate_slice(rupt,nstrike,ndip,epicenter,out,tmax,dt):
    '''
    '''
    from numpy import genfromtxt,unique,zeros,where,arange,interp,c_,savetxt
    from mudpy.forward import get_source_time_function,add2stf
    from string import rjust
    
    f=genfromtxt(rupt)
    num=f[:,0]
    nfault=nstrike*ndip
    unum=unique(num)
    lon=f[0:len(unum),1]
    lat=f[0:len(unum),2]
    depth=f[0:len(unum),3]
    #Get slips
    all_ss=f[:,8]
    all_ds=f[:,9]
    #Now parse for multiple rupture speeds
    unum=unique(num)
    #Count number of windows
    nwin=len(where(num==unum[0])[0])
    #Get rigidities
    mu=f[0:len(unum),13]
    #Get rise times
    rise_time=f[0:len(unum),7]
    #Get areas
    area=f[0:len(unum),10]*f[0:len(unum),11]
    t=arange(0,tmax,dt)
    #Loop over subfaults
    for kfault in range(nfault):
        if kfault%10==0:
            print '... working on subfault '+str(kfault)+' of '+str(nfault)
        #Get rupture times for subfault windows
        i=where(num==unum[kfault])[0]
        trup=f[i,12]
        #Get slips on windows
        ss=all_ss[i]
        ds=all_ds[i]
        #Add it up
        slip=(ss**2+ds**2)**0.5
        #Get first source time function
        t1,M1=get_source_time_function(mu[kfault],area[kfault],rise_time[kfault],trup[0],slip[0])
        #Loop over windows
        for kwin in range(nwin-1):
            #Get next source time function
            t2,M2=get_source_time_function(mu[kfault],area[kfault],rise_time[kfault],trup[kwin+1],slip[kwin+1])
            #Add the soruce time functions
            t1,M1=add2stf(t1,M1,t2,M2)
        if kfault==0: #Intialize
            M=zeros((len(t),nfault))
            T=zeros((len(t),nfault))
        Mout=interp(t,t1,M1)
        M[:,kfault]=Mout
        T[:,kfault]=t
    #Now look through time slices
    maxsr=0
    print 'Writing files...'
    for ktime in range(len(t)):
        sliprate=zeros(lon.shape)
        for kfault in range(nfault):
            i=where(T[:,kfault]==t[ktime])[0]
            sliprate[kfault]=M[i,kfault]/(mu[kfault]*area[kfault])
        maxsr=max(maxsr,sliprate.max())
        fname=out+rjust(str(ktime),4,'0')+'.sliprate'
        savetxt(fname, c_[lon,lat,depth,sliprate],fmt='%.6f\t%.6f\t%.4f\t%.6f')
    print 'Maximum slip rate was '+str(maxsr)+'m/s'
    
    
def make_slip_slice(rupt,nstrike,ndip,epicenter,out,tmax,dt):
    '''
    '''
    from numpy import genfromtxt,unique,zeros,where,arange,interp,c_,savetxt,intersect1d
    from mudpy.forward import get_source_time_function,add2stf
    from string import rjust
    from scipy.integrate import trapz
    
    f=genfromtxt(rupt)
    num=f[:,0]
    nfault=nstrike*ndip
    unum=unique(num)
    lon=f[0:len(unum),1]
    lat=f[0:len(unum),2]
    depth=f[0:len(unum),3]
    #Get slips
    all_ss=f[:,8]
    all_ds=f[:,9]
    #Now parse for multiple rupture speeds
    unum=unique(num)
    #Count number of windows
    nwin=len(where(num==unum[0])[0])
    #Get rigidities
    mu=f[0:len(unum),13]
    #Get rise times
    rise_time=f[0:len(unum),7]
    #Get areas
    area=f[0:len(unum),10]*f[0:len(unum),11]
    #Get indices for plot
    istrike=zeros(nstrike*ndip)
    idip=zeros(nstrike*ndip)
    k=0
    t=arange(0,tmax,0.1)
    for i in range(ndip):
         for j in range(nstrike):
             istrike[k]=nstrike-j-1
             idip[k]=i
             k+=1  
    #Loop over subfaults
    print nfault
    for kfault in range(nfault):
        if kfault%10==0:
            print '... working on subfault '+str(kfault)+' of '+str(nfault)
        #Get rupture times for subfault windows
        i=where(num==unum[kfault])[0]
        trup=f[i,12]
        #Get slips on windows
        ss=all_ss[i]
        ds=all_ds[i]
        #Add it up
        slip=(ss**2+ds**2)**0.5
        #Get first source time function
        t1,M1=get_source_time_function(mu[kfault],area[kfault],rise_time[kfault],trup[0],slip[0])
        #Loop over windows
        for kwin in range(nwin-1):
            #Get next source time function
            t2,M2=get_source_time_function(mu[kfault],area[kfault],rise_time[kfault],trup[kwin+1],slip[kwin+1])
            #Add the soruce time functions
            t1,M1=add2stf(t1,M1,t2,M2)
        if kfault==0: #Intialize
            M=zeros((len(t),nfault))
            T=zeros((len(t),nfault))
        Mout=interp(t,t1,M1)
        M[:,kfault]=Mout
        T[:,kfault]=t
    #Now look through time slices
    maxsr=0
    #Now integrate slip
    t=arange(0,tmax+dt*0.1,dt)
    print 'Writing files...'
    for ktime in range(len(t)-1):
        slip=zeros(lon.shape)
        for kfault in range(nfault):
            i1=where(T[:,kfault]>=t[ktime])[0]
            i2=where(T[:,kfault]<t[ktime+1])[0]
            i=intersect1d(i1,i2)
            slip[kfault]=trapz(M[i,kfault]/(mu[kfault]*area[kfault]),T[i,kfault])
        maxsr=max(maxsr,slip.max())
        fname=out+rjust(str(ktime),4,'0')+'.slip'
        savetxt(fname, c_[lon,lat,depth,slip],fmt='%.6f\t%.6f\t%.4f\t%.6f')
    print 'Maximum slip was '+str(maxsr)+'m'      



def make_psvelo(stafile,directory,fout,run_name,run_number):
    '''
    Make psvelo file
    '''
    from numpy import genfromtxt,zeros,savetxt
    from glob import glob
    
    
    sta=genfromtxt(stafile,usecols=0,dtype='S')
    out=zeros((len(sta),6))
    lonlat=genfromtxt(stafile,usecols=[1,2],dtype='S')
    for k in range(len(sta)):
        out[k,0:2]=lonlat[k,:]
        #neu=genfromtxt(glob(directory+sta[k]+'*.neu')[0])
        neu=genfromtxt(glob(directory+run_name+'.'+run_number+'.'+sta[k]+'*.neu')[0])
        out[k,2]=neu[1] #East
        out[k,3]=neu[0] #North
        out[k,4]=neu[0] #East sigma
        out[k,5]=neu[0] #North sigma
    savetxt(fout,out,fmt='%10.4f\t%10.4f\t%10.6f\t%10.6f\t%10.6f\t%10.6f\t')
    

def final_dtopo(dtopo_file,out_file):
    '''
    Extract final displacememnt from dtopo file
    '''
    from numpy import genfromtxt,savetxt,where
    
    #Read dtopo
    dtopo=genfromtxt(dtopo_file)
    tmax=dtopo[:,0].max()
    i=where(dtopo[:,0]==tmax)[0]
    out=dtopo[i,1:]
    savetxt(out_file,out,fmt='%10.6f\t%10.6f\t%10.6f')

def insar_xyz(home,project_name,run_name,run_number,GF_list,outfile):
    '''
    Make an xyz file for plotting InSAR sub_sampled residuals
    '''
    from numpy import genfromtxt,where,zeros,c_,savetxt
    
    #Decide what to plot
    sta=genfromtxt(home+project_name+'/data/station_info/'+GF_list,usecols=0,dtype='S')
    lon_all=genfromtxt(home+project_name+'/data/station_info/'+GF_list,usecols=[1],dtype='f')
    lat_all=genfromtxt(home+project_name+'/data/station_info/'+GF_list,usecols=[2],dtype='f')
    gf=genfromtxt(home+project_name+'/data/station_info/'+GF_list,usecols=[7],dtype='f')
    datapath=home+project_name+'/data/statics/'
    synthpath=home+project_name+'/output/inverse_models/statics/'
    #synthpath=home+project_name+'/output/forward_models/'
    i=where(gf==1)[0] #Which stations have statics?
    lon=lon_all[i]
    lat=lat_all[i]
    los_data=zeros(len(i))
    los_synth=zeros(len(i))
    for k in range(len(i)):
        neu=genfromtxt(datapath+sta[i[k]]+'.los')
        #neu=genfromtxt(datapath+sta[i[k]]+'.static.neu')
        los_data[k]=neu[0]
        neus=genfromtxt(synthpath+run_name+'.'+run_number+'.'+sta[i[k]]+'.los')
        #neus=genfromtxt(synthpath+sta[i[k]]+'.static.neu')
        los_synth[k]=neus[0]
    #Make plot  
    out=c_[lon,lat,los_data-los_synth]  
    savetxt(outfile,out,fmt='%.6f\t%.6f\t%.6f')


def make_shakemap_slice(home,project_name,run_name,time_epi,GF_list,dt,tmax):
    '''
    Make xyz files with current ground velocity
    '''
    from numpy import genfromtxt,arange,sqrt,zeros,where,c_,savetxt
    from string import rjust
    from obspy import read
    from mudpy.forward import lowpass
    
    t=arange(0,tmax,dt)
    fcorner=0.5
    sta=genfromtxt(home+project_name+'/data/station_info/'+GF_list,usecols=0,dtype='S')
    lonlat=genfromtxt(home+project_name+'/data/station_info/'+GF_list,usecols=[1,2])
    for ksta in range(len(sta)):
        n=read(home+project_name+'/output/forward_models/'+run_name+'.'+sta[ksta]+'.vel.n')
        e=read(home+project_name+'/output/forward_models/'+run_name+'.'+sta[ksta]+'.vel.n')
        n[0].data=lowpass(n[0].data,fcorner,1./n[0].stats.delta,2)
        e[0].data=lowpass(n[0].data,fcorner,1./e[0].stats.delta,2)
        if ksta==0:
            h=n.copy()
        else:
            h+=n[0].copy()
        h[ksta].data=sqrt(n[0].data**2+e[0].data**2)
        h[ksta].trim(starttime=time_epi)
        print h[ksta].stats.starttime
    vout=zeros(len(lonlat))
    maxv=0
    for kt in range(len(t)):
        for ksta in range(len(sta)):
            i=where(h[ksta].times()==t[kt])[0]
            vout[ksta]=h[ksta].data[i]
        if vout.max()>maxv:
            maxv=vout.max()
        out=c_[lonlat,vout]
        num=rjust(str(kt),4,'0')
        print num
        savetxt(home+project_name+'/analysis/shake/'+num+'.shake',out,fmt='%10.6f\t%10.6f\t%10.4f')
    print 'Max velocity was '+str(maxv)+'m/s'
        

    



def gmtColormap(fileName):
      '''
      Convert a cpt GMT color palette file into a matplotlib colormap object.
      Note that not all default GMT palettes can be converted with this method.
      For example hot.cpt will fail but seis.cpt will be fine. If you need
      more cpt files checkout cpt-city (http://soliton.vm.bytemark.co.uk/pub/cpt-city/)
      
      Usage:
          cm = gmtColormap(fileName)
        
      IN:
          fileName: Absolute path to cpt file
      OUT:
          cm: matplotlib colormap obejct
          
      Example:
          
          colorMap = gmtColormap('/opt/local/share/gmt/cpt/haxby.cpt')
          
      you can then use your colorMap object as you would any other matplotlib
      object, for example:
         
         pcolor(x,y,cmap=colorMap)
          
      
      Diego Melgar 2,2014, modified from original by James Boyle
      '''
      
      from matplotlib import colors
      import colorsys
      import numpy as N

      f = open(fileName)
      lines = f.readlines()
      f.close()

      x = []
      r = []
      g = []
      b = []
      colorModel = "RGB"
      for l in lines:
          ls = l.split()
          if l[0] == "#":
             if ls[-1] == "HSV":
                 colorModel = "HSV"
                 continue
             else:
                 continue
          if ls[0] == "B" or ls[0] == "F" or ls[0] == "N":
             pass
          else:
              x.append(float(ls[0]))
              r.append(float(ls[1]))
              g.append(float(ls[2]))
              b.append(float(ls[3]))
              xtemp = float(ls[4])
              rtemp = float(ls[5])
              gtemp = float(ls[6])
              btemp = float(ls[7])

      x.append(xtemp)
      r.append(rtemp)
      g.append(gtemp)
      b.append(btemp)

      x = N.array( x )
      r = N.array( r )
      g = N.array( g )
      b = N.array( b )
      if colorModel == "HSV":
         for i in range(r.shape[0]):
             rr,gg,bb = colorsys.hsv_to_rgb(r[i]/360.,g[i],b[i])
             r[i] = rr ; g[i] = gg ; b[i] = bb
      if colorModel == "HSV":
         for i in range(r.shape[0]):
             rr,gg,bb = colorsys.hsv_to_rgb(r[i]/360.,g[i],b[i])
             r[i] = rr ; g[i] = gg ; b[i] = bb
      if colorModel == "RGB":
          r = r/255.
          g = g/255.
          b = b/255.
      xNorm = (x - x[0])/(x[-1] - x[0])

      red = []
      blue = []
      green = []
      for i in range(len(x)):
          red.append([xNorm[i],r[i],r[i]])
          green.append([xNorm[i],g[i],g[i]])
          blue.append([xNorm[i],b[i],b[i]])
      colorDict = {"red":red, "green":green, "blue":blue}
      cmap=colors.LinearSegmentedColormap('cmap',colorDict,256)
      return (cmap)
    