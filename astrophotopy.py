import cv2
import numpy as np
from matplotlib import pyplot as plt
import os
from IPython.display import HTML, display
import re
import shutil
from skimage.color import rgb2yuv, yuv2rgb
import logging
import pyfits

#Class for image objects 
class Image:
    def __init__(self, *name):
        self.image = np.array([])
        self.name = ""
        if name:
            self.name = name
        self.hist = None #histogram vector
        self.norm = None #norm of histogram vector
        self.dev = None  #standard deviation of the image within the set
        
    def load(self, path, filename):
        if filename.find('.') == 0 or filename.find('.') == -1:
            pass
        elif filename.find('.jpg')>0 or filename.find('.png')>0 or filename.find('.bmp')>0 or filename.find('.tiff')>0:                                                                                     
            self.image = cv2.imread(path+"/"+filename)
            self.name = filename
            print(filename+" successfully loaded\n")
                                                                                                  
    def histogram(self):
        im_gray = cv2.cvtColor(self.image,cv2.COLOR_BGR2GRAY)
        self.hist = cv2.calcHist(im_gray,[0],None,[256],[0,256])    
        self.norm = np.dot(np.transpose(self.hist),self.hist) #norm of the image (intended as a vector) normalized on pixel number
    
    def export_hist(self, path, *dpi):
        if dpi:
            pass
        else:
            dpi = 150
        plt.plot(self.hist)
        plt.savefig(path+"/hist/hist_"+self.name,dpi=dpi)
        plt.clf()
        
    def save(self, path):
        try:
            os.chdir(path)
        except Exception as e:
            logging.exception("Exception occurred")
        cv2.imwrite(re.sub("\.[a-zA-Z]{2,4}","",self.name)+".tiff",self.image)
    
    def cos_phi(self, image):
        dot = np.dot(self.hist, image.hist)
        return dot/(np.sqrt(self.norm,image.norm))   
        
    def yuv_decompose(self):
        self.image = rgb2yuv(self.image)
                                                                                                      
    def yuv_recompose(self):
        self.image = yuv2rgb(self.image)
    
    def conv2d(self, kernel):
        self.image = cv2.filter2D(src=self.image, ddepth=-1, kernel=kernel)
                                                                                                  
    def blur(self, width):
        self.image = cv2.blur(self.image, (width, width))
    
    def sharpen(self):                                                                                              
        kernel = np.array([[0, -1, 0],[-1, 5,-1],[0, -1, 0]])
        self.conv2d(kernel)
        
    def edge(self):                                                                                              
        kernel = np.array([[-1, -1, -1],[-1, 8, -1],[-1, -1, -1]])
        self.conv2d(kernel)
                                                                                                  
    def resize(self, factor):
        width = int(img.shape[1] * factor / 100)
        height = int(img.shape[0] * factor / 100)
        dim = (width, height)
        # resize image
        if factor < 100:
            self.image = cv2.resize(self.image, dim, interpolation = cv2.INTER_AREA)
        else:
            self.image = cv2.resize(self.image, dim, interpolation = cv2.INTER_CUBIC)
    
    def show(self):
        plt.title(self.name)
        plt.imshow(self.image)
        plt.show()

#images container for flexible processing, a FlexIm object is a set homogeneus images/frames
class FlexIm:
    def __init__(self, *name):
        self.name = ""
        if name:
            self.name = name
        self.container = []
        
    def avg(self): #average of the values over the set
        summa = 0
        for item in self.container:
            summa += item.norm
        return summa/len(self.container)
    
    def stdev(self):
        summa = 0
        average = self.avg()
        for item in self.container:
            summa += (item.norm - average)**2
        return np.sqrt(summa/len(self.container))
    
    def update_devs(self):
        avg = self.avg()
        stdev = self.stdev()
        for item in self.container:
            item.histogram()
            item.dev = abs((item.norm-avg)/stdev) 
            
    def load(self, path): #wrapper for multifile loading within a given folder
        for filename in os.listdir(path):
            if filename.find('.fits') > 0:#dealing with .fits file
                try:
                    hdulist = pyfits.open('input.fits')
                    self.name = hdulist[0].header['targname']
                    for i in range(1,len(hdulist)):
                        self.container.append(hdulist[i].data) 
                    hdulist.close()
                except Exception as e:
                    logging.exception("Exception occurred")
            else:
                try:
                    img = Image(filename)
                    img.load(path,filename)
                    img.histogram()
                    self.container.append(img)
                except Exception as e:
                    logging.exception("Exception occurred")
        try:
            self.container.update_devs()
        except Exception as e:
                logging.exception("Exception occurred")
    
    def save(self, path): #wrapper for multifile saving within a given folder        
        for item in self.container:
            item.save(path)
                                                                                                  
    def depack(self):#extraction of image contents only
        imgs = []
        for item in container:
            imgs.append(item.image)
        return imgs
            
    def mean(self):#mean of the set
        result = Image("mean")                                                                                         
        result.image = np.mean(self.depack(), axis=0)
        return result                                                                                         
                                                                                                  
    def median(self):#median of the set                                                                                     
        result = Image("median")                                                                                         
        result.image = np.median(self.depack(), axis=0)
        return result
                                                                                                  
    def summation(self):#summation of the set                                                                                              
        result = Image("sum")                                                                                         
        result.image = np.sum(self.depack(), axis = 0)
        return result                                                                                              

    def subtraction(self, image):#subtraction of an image over the whole set
        result = FlexIm("sub")                                                                                          
        index = 0   
        for im in self.container:
            im.image = im.image-image.image
            result.container.append(im)                                                                                         
        return result
    
    def find_representative(self):#find the representative image within a set (on st.dev. basis)
        best_k = 10
        index = 0
        for item in self.container:
            if item.dev < best_k:
                best_k = item.dev
                best_index = index
            index += 1
        return best_index
    
    def align_frames(self,*arg,**args):#align frames within a set
        i = self.find_representative()
        # Convert average image to grayscale
        im_gray_avg = cv2.cvtColor(self.container[i].image,cv2.COLOR_BGR2GRAY)
        # Find size of average image
        sz = self.container[i].image.shape
        
        number_of_iterations = 800
        termination_eps = 1e-7
        
        if arg == False:
            number_of_iterations = 800
            termination_eps = 1e-7
            print("Precision is set to \"normal\"")   
        elif arg == "low":
            number_of_iterations = 500
            termination_eps = 1e-5   
        elif arg == "normal":
            number_of_iterations = 800
            termination_eps = 1e-7   
        elif arg== "high":
            number_of_iterations = 1200
            termination_eps = 1e-8     
        elif arg == "very_high":
            number_of_iterations = 2500
            termination_eps = 1e-10 
        else: 
            print("\nPrecision is set to \"normal\" ")
        
        warp_mode = cv2.MOTION_AFFINE
        
        # Define transformation model   
        if args == False:
            warp_mode = cv2.MOTION_AFFINE
            print("Transform is set to \"affine\"")
        else:
            for ar in args:
                if ar["transform"] == "euclidean":
                    warp_mode = cv2.MOTION_EUCLIDEAN
                elif ar["transform"] == "affine":
                    warp_mode = cv2.MOTION_AFFINE
                elif ar["transform"] == "homography":
                    warp_mode = cv2.MOTION_HOMOGRAPHY
                else:
                    print("\nInvalid choice for transform type. Transform is set to \"affine\" ")
                    warp_mode = cv2.MOTION_AFFINE
        
        # Define 2x3 or 3x3 matrices and initialize the matrix to identity
        if warp_mode == cv2.MOTION_HOMOGRAPHY:
            warp_matrix = np.eye(3, 3, dtype=np.float32)   
        else:
            warp_matrix = np.eye(2, 3, dtype=np.float32)

        criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, number_of_iterations, termination_eps)

        aligned_pics = FlexIm("aligned_"+self.name)

        print("\nAlligning pictures (It'll take a while): ", end="")
    
        tot = len(self.container)
        count = 0
    
        for item in self.container:
            aligned_pic = Image("aligned_"+item.name)
            print(str(round(count*100/tot))+"% ... ", end = "") #process 
            im_gray = cv2.cvtColor(item.image,cv2.COLOR_BGR2GRAY)
            # Run the ECC algorithm. The results are stored in warp_matrix
            (cc, warp_matrix) = cv2.findTransformECC(im_gray_avg, im_gray, warp_matrix, warp_mode, criteria)
    
            if warp_mode == cv2.MOTION_HOMOGRAPHY :
                # Use warpPerspective for Homography  
                aligned_pic.image = cv2.warpPerspective(item.image, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
            else :
                # Use warpAffine for Translation, Euclidean and Affine
                aligned_pic.image = cv2.warpAffine(item.image, warp_matrix, (sz[1],sz[0]), flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP)
            aligned_pic.show()   
            aligned_pics.container.append(aligned_pic)
            count +=1 
            
        print("Done!\n", end="")
        return aligned_pics
        
class Optics:
    def __init__(self, **kwargs):
        for arg in kwargs:
            if arg=='model':
                self.model = kwargs[arg]
            if arg=='diameter': #the diameter of the aperture
                self.diameter = kwargs[arg]
            if arg=='f_len':
                self.focal_length = kwargs[arg]
            if arg=='lens': #magnifying factor of additional lenses (i.e. focal reducer <1 or Barlow >1)
                self.lens = kwargs[arg]
            if arg=='f_len_ep': #eyepiece's focal length in mm
                self.eyepiece = kwargs[arg]

        print("Optics "+self.model+" created\n")
        
class Sensor:
    def __init__(self, **kwargs):
        for arg in kwargs:
            if arg=='model':
                self.model = kwargs[arg]
            if arg=='px_dim': #dimension of pixel micrometer
                self.pixel_dim = kwargs[arg]
            if arg=='sens_diag': #ccd diagonal in mm
                self.sensor_diagonal = kwargs[arg]
        print("Sensor "+self.model+" created\n")
            
class Observation_Site: 
    def __init__(self, **kwargs):
        for arg in kwargs:
            if arg=='location_name':
                self.location_name = kwargs[arg]
            if arg=='altitude':
                self.altitude = kwargs[arg]
            if arg=='latitude':
                self.latitude = kwargs[arg]
            if arg=='air_temp':
                self.air_temp = kwargs[arg]
            if arg=='fwhm':
                self.fwhm= kwargs[arg]
        print("Observation site created\n")

#class for astrophotography projects and operations                                
class Project:
    def __init__(self, **kwargs):
        self.object_name = kwargs['subject']
        self.path = kwargs['path']
        self.telescope = None
        self.observation_site = None
        for arg in kwargs:
            if arg=='subject':
                self.object_name = kwargs[arg]
            if arg=='path':
                self.path = kwargs[arg]
            if arg=='DF_path':
                self.DF_path = kwargs[arg]
            else:
                self.DF_path = self.path+"/"+self.object_name+"/DF"
            if arg=='FF_path':
                self.FF_path = kwargs[arg]
            else:
                self.FF_path = self.path+"/"+self.object_name+"/FF"
            if arg=='tot_exposure':
                self.total_exposure = kwargs[arg]
            if arg=='frame_exposure':
                self.frame_exposure = kwargs[arg] 
            if arg=='optics':
                self.optics = arg
            if arg=='sensor':
                self.sensor = arg 
            if arg=='observation_site':
                self.observation_site = arg
        try:
            os.mkdir(self.path+"/"+self.object_name)
            print("Sub folder created")
        except Exception as e:
            logging.exception("Exception occurred")
        try:
            os.mkdir(self.DF_path)
            print("DF (dark frames) folder created")
        except Exception as e:
            logging.exception("Exception occurred")
        try:
            os.mkdir(self.FF_path)
            print("FF (flat frames) folder created")
        except Exception as e:
            logging.exception("Exception occurred")
        
        try:
            os.mkdir(self.path+"/hist")
        except Exception as e:
            logging.exception("Exception occurred")
            
        if self.telescope == None:
            print("No telescope!\n")
                    
        if self.observation_site == None:
            print("No observation site!\n")
        
        self.frames = FlexIm("Rough")
        self.dark_frames = FlexIm("DF")
        self.flat_frames = FlexIm("FF")
 
        print("Project \""+ self.object_name +"\" created\n \nCOPY your files in the selected folders!")
    
    def load(self):
        self.frames.load(self.path)
        self.dark_frames.load(self.DF_path)
        self.flat_frames.load(self.FF_path)
        
    def display_HTML(self, html_data):#method for inline data visualization
        print("==================\n")
        print(" Visualizing data\n")
        print("==================\n")
        display(HTML(
           '<table><tr>{}</tr></table>'.format(
               '</tr><tr>'.join(
                   '<td>{}</td>'.format('</td><td>'.join(str(_) for _ in row)) for row in html_data)
                   )
            ))
        
    def show_select_and_drop(self, *arg, **kwargs):#select and drop images for set cleaning purpose 
        res = FlexIm()
        if arg == "DF":
            res = self.dark_frames
            path = self.DF_path
            
        elif arg == "FF":
            res = self.flat_frames
            path = self.FF_path
        else:
            res = self.frames
            path = self.path 
            
        drop_toll = 1.
        for ar in kwargs:
            if ar == 'drop_toll':
                drop_toll = kwargs['drop_toll']
                print("Tollerance: "+str(drop_toll)+" times std.dev.")
            else:
                print("Tollerance is set to 1 times std.dev.")

        avg = res.avg()
        sd = res.stdev()
        print("Average for this set = "+str(*avg)[1:-1])
        print("Std. dev. for this set (sigma) = "+str(*sd)[1:-1]+"\n")
        
        retained_images = []

        html_data = []
        
        i = 0
        res.update_devs()
        
        for item in res.container:
            item.export_hist(self.path)
            norm = ("Picture norm = "+str(*item.norm)[1:-1])
            std_dev = ("Picture std. dev. = "+str(*item.dev)[1:-1])
            html_data.append(["<b>"+item.name+"</b>","","",""])
            html_data.append(['<img src='+self.path+"/"+item.name+' width="100" height="100"/>','<img src='+self.path+"/hist/hist_"+item.name+' width="225" height="150"/>',norm,std_dev])
        
            if item.dev > drop_toll:
                print("\n"+item.name+" is out of std. dev. range and will be dropped. ("+std_dev+" sigma)")
                item.show()
                ans = input("Do you confirm? (Y/N) ")
            
                if ans == "Y" or ans == "y":
                    mess = "<b>Picture dropped</b>"  
                else:
                    mess = "Picture retained"
                    retained_images.append(item) 
                print("\n")
            else:
                mess = "Picture retained"
                retained_images.append(item)
            
            html_data.append([" ","Action:",mess])
        #displaying html formatted output    
        self.display_HTML(html_data)
        
        if arg == "DF":
            self.dark_frames.container = retained_images
            self.dark_frames.name = "DF"
            
        elif arg == "FF":
            self.flat_frames.container = retained_images
            self.flat_frames.name = "FF"
        else:
            self.frames.container = retained_images
            self.frames.name = "Rough"

    def align_frames(self,*arg,**args): 
        path = self.path+"/Aligned"
        try:
            os.mkdir(path)
            print("Aligned pictures folder created")    
        except Exception as e:
            logging.exception("Exception occurred")
        #creating folder for aligned pictures
        self.frames.align_frames(arg,args)
        self.frames.save(path)#save the aligned set
    
    #create master frame
    def master_frame(self,*arg):
        #perform selection and drop on st.dev basis
        self.show_select_and_drop(arg)
        #median of remaining frames
        if arg == "DF":
            master = self.dark_frames.median(arg)
            file = "masterDF_"+str(self.frame_exposure)+"_"+str(round(self.observation_site['air_temp']))+".tiff"
            cv2.imwrite(self.DF_path+"/"+file,master.image)
            print("Master dark frame created")
        elif arg == "FF":
            master = self.flat_frames.median(arg)
            file = "masterFF.tiff"
            cv2.imwrite(self.FF_path+"/"+file,master.image)
            print("Master flat frame created")
        else:
            #it could be passed a custom image (not yet implemented)
            print("I wish you'll tell me if I'm dealing with a dark or flat frame")
        return master
            
    def calc_super_res_number(self, magnification):
        #utility method for calculation of the minimal set dimension for "bayesian multi-image upscaling" approach

        resolution = (np.sqrt(2)*self.sensor.sens_diag*1000/(self.sensor.px_dim))*np.arctan(0.5*self.sens.px_dim/self.optics.f_length)
        return round((self.observation_site.fwhm*magnification/resolution)**2)

    def subtract_master_dark_and_flat(self):
        masterDF = master_frame("DF")
        self.frames.subtraction(masterDF)
        masterFF = master_frame("FF")
        self.frames.subtraction(masterFF)

    def create_integration_sets(self,*n_passed):
        #number of frames per set
        if n_passed:
            n = n_passed
        else:     
            n = int(self.total_exposure/self.frame_exposure)
        print("=============================")
        print("Creating integration sets ...\n") 
        for set_id in range(n):
            try:
                os.mkdir(self.path+"/"+str(set_id))
            except OSError:
                print ("Creation of the directory %s failed" % path)
                
        set_id = 0
        for filename in os.listdir(self.path):
            shutil.move(self.path+filename,self.path+"/"+str(set_id)+"/"+filename)
            print(filename+" to set(folder): "+set_id)
            set_id += 1
            set_id = set_id % n
            
    #for every integration set, it integrates frames within the integration set     
    def integrate_over_sets(self):
        print("===============")
        print("Integrating ...\n")
        integration_set = FlexIm() 
        n = int(self.total_exposure/self.frame_exposure)
        for set_id in range(n):
            integration_set = FlexIm() 
            for filename in os.listdir(self.path+"/"+str(set_id)):
                if filename.find('.') == 0 or filename.find('.') == -1:
                    print(filename+" not loaded")
                else:
                    img = Image(filename)
                    integration_set.container.append(img)
                    print(filename+" loaded")
            cv2.imwrite(self.path+"/"+str(set_id)+"_integrated.tiff",integration_set.summation())
            print("Set \""+str(set_id)+"\" integrated\n")


#projection on average picture vector instead of std!!