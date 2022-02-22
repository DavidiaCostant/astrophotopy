# AstroPhotoPy 0.2.x library documentation (UNDER CONSTRUCTION)

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#Object types">Object types</a>
      <ul>
        <li><a href="#Image-object">Image object</a></li>
          <ul>
            <li><a href="#Image-methods">Methods</a></li>
          </ul>
      </ul>
      <ul>
        <li><a href="#FlexIm-object">FlexIm object</a></li>
          <ul>
            <li><a href="#FlexIm-methods">Methods</a></li>
          </ul>
      </ul>
      <ul>
        <li><a href="#Optics-object">Optics object</a></li>
      </ul>
      <ul>
        <li><a href="#Sensor-object">Sensor object</a></li>
      </ul>
      <ul>
        <li><a href="#Observation_site-object">Observation_site object</a></li>
      </ul>
      <ul>
        <li><a href="#Project-object">Project object</a></li>
          <ul>
            <li><a href="#Project-methods">Methods</a></li>
          </ul>
      </ul>
    </li>
    <li>
      <a href="#examples">Examples</a>
      <ul>
        <li><a href="#Essential workflow">Essential workflow</a></li>
        <li><a href="#Advanced examples">Advanced examples</a></li>
      </ul>
    </li>
  </ol>
</details>


<!-- OBJECT TYPES -->
# Object types
# Image object
The Image type is a container for a single image data and additional field for properties as:

* hist: the histogram of image's luminance as a vector
* norm: the norm(squared) of "hist" vector
* dev: the deviation of image's norm within a set of images

```python
class Image:
    def __init__(self, *name[optional]):
        self.image = numpy.array([])
        self.name = ""
        if name:
            self.name = name
        self.hist = None
        self.norm = None
        self.dev = None 
```
## Image methods
All the methods below are destructive, i.e. they apply to the object by overwriting the previous information.

* load
```python
def load(self, path, filename):
```
loads from a given filename within a path the image data.

* histogram
```python
def histogram(self):
```
calculates the vector of luminance and its norm then updates the respective fields.

* export_hist
```python        
def export_hist(self, path, *dpi[optional]):
```
saves to a file in the given path a plot of the luminance vector, resolution in dpi.

* save
```python 
def save(self, path):
```
saves the image data to a image file.

* cos_phi
```python 
def cos_phi(self, image):
```
returns the cosine between the self.hist and the passed astrophotopy.Image.hist vectors. Cos(phi) is a measure of the degree of similarity between two image, and can be used in alternative to the statistical approach (standard deviation).

* yuv_decompose
```python 
def yuv_decompose(self):
```
transforms the RGB space of the object to YUV space.

* yuv_recompose
```python 
def yuv_recompose(self):
```
transforms the YUV space of the object to RGB space.

* conv2d
```python     
def conv2d(self, kernel):
``` 
convolves the object with the given numpy.array(kernel)

* blur
```python     
def blur(self, width):
``` 
applies a blurring of magnitude int(width)                                                                                                  

* sharpen 
```python   
def sharpen(self):                                                                                          
```  
applies sharpness to the image

* edge
```python 
def edge(self):                                                                                             
```
extracts edge from the previous image

* resize
```python 
def resize(self, factor):
```
scales the image of the given float(factor), using a equal area method for downscaling and bicubic for upscaling.

* show
```python
def show(self):
```
shows the image.

<p align="right">(<a href="#top">back to top</a>)</p>

# FlexIm object
The FlexIm object is a multi-image container. The purpose of this object is to group within it a homogeneous set of images (i.e. all the dark frames taken or the red filter frames for a monochromatic processing workflow). 

```python
class FlexIm:
    def __init__(self, *name[optional]):
        self.name = ""
        if name:
            self.name = name
        self.container = []
```
The self.container is a list of astrophotopy.Image objects.

## FlexIm methods

* avg
```python
def avg(self): 
```
returns the expected value of images' norms as a floating point number.

* stdev
```python
def stdev(self):
```
returns the standard deviation value of images' norms as a floating point number. 

* update_devs
```python
def update_devs(self):
```
For each image in self.container it calculates and updates the respective fields' value.

* load
```python            
def load(self, path):
```
given a path it loads the folder content.

* save
```python       
def save(self, path):      
```

* depack
```python                                                                                                  
def depack(self):
```
returns a list of numpy.array, each of which contains image data (only).

* mean
```python
def mean(self):
```
returns an astrophotopy.Image object containing the mean of the set.

* median
```python
def median(self):                                                                                   
```
returns an astrophotopy.Image object containing the median of the set. 

* summation
```python
def summation(self):                                                                                            
``` 
returns an astrophotopy.Image object containing the sum of the set. 

* subtraction
```python
def subtraction(self, image):
```
returns an astophotopy.FlexIm object containing the subtraction of the given astrophotopy.Image to the whole set.

* find_representative
```python
 def find_representative(self):
```
returns the index of the average's closest image.

* align_frames
```python
def align_frames(self,*precision = "normal"[optional],**transform = "affine"[optional]): 
```
returns a astrophotopy.FlexIm object containing the aligned frames.

<p align="right">(<a href="#top">back to top</a>)</p>

# Optics object
The Optics object contains all the relevant information about the optics:
* diameter of the aperture in mm
* focal lenght of the optical system in mm (self.f_len)
* magnification factor of additional lens (self.lens > 1 for Barlow lenses and self.lens < 1 for focal reducers)
* focal length of the eyepiece/camera in mm (self.f_len_ep)

```python
class Optics:
    def __init__(self, **kwargs):
        for arg in kwargs:
            if arg=='model':
                self.model = kwargs[arg]
            if arg=='diameter':
                self.diameter = kwargs[arg]
            if arg=='f_len':
                self.focal_length = kwargs[arg]
            if arg=='lens': 
                self.lens = kwargs[arg]
            if arg=='f_len_ep': 
                self.eyepiece = kwargs[arg]
```

<p align="right">(<a href="#top">back to top</a>)</p>

# Sensor object
The Sensor object contains information as:
* pixel dimension in micrometer (self.px_dim)
* sensor diagonal in mm (self.sensor_diagonal)

```python
class Sensor:
    def __init__(self, **kwargs):
        for arg in kwargs:
            if arg=='model':
                self.model = kwargs[arg]
            if arg=='px_dim': #dimension of pixel micrometer
                self.px_dim = kwargs[arg]
            if arg=='sens_diag': #ccd diagonal in mm
                self.sensor_diagonal = kwargs[arg]
```
<p align="right">(<a href="#top">back to top</a>)</p>

# Observation_Site object
The Observation_site object contains the relevant information about the site where the images was taken.
* air temperature is a floating point number and will be used for categorizing master dark frames (self.air_temp)
* latitude of the observation site, in degree but arcminutes must be converted to decimal (self.latitude)
* full width at half maximum is a measure of seeing [arcseconds]

```python
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
```
<p align="right">(<a href="#top">back to top</a>)</p>


# Project object
This is the main wrapper object for the library, it includes methods for the general purpose of the library itself and for minimal end-user's usage effort.

```python
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
        
        self.frames = FlexIm("Rough")
        self.dark_frames = FlexIm("DF")
        self.flat_frames = FlexIm("FF")
```
## Project methods

* load
```python    
def load(self):
```
loads all the files from the respective folders.

* display_HTML
```python 
def display_HTML(self, html_data):
```
displays a table of html formatted data. html_data is a list of rows, each row is an array containg cells of html formatted data. The function is used as as sub-method for visualizing data, but it can be accessed by the user if needed.

* debayering
```python 
def debayering(self):
```
performs debayering of frames.

* show_select_and_drop
```python 
def show_select_and_drop(self, *frame_type[optional], **drop_toll = 1[optional]):
```
shows the set first, then it selects the images out of a tolerance (standard deviation).

* align_frames
```python
def align_frames(self,*precision = "normal"[optional],**transform = "affine"[optional]): 
```
aligns frames within the set.

* master_frame
```python
def master_frame(self,*frame_type[optional]):
```
creates the master frame of the given frame type.

* calc_super_res_number
```python           
def calc_super_res_number(self, magnification):
```
is a routine for the calculation of the minimal frames number required for the magnification required (probabilistic upscaling).

* subtract_master_dark_and_flat
```python   
def subtract_master_dark_and_flat(self):
```
cleans up the set subtracting the master dark and flat frames.

* create_integration_set
```python 
def create_integration_sets(self,*n_passed):
```
creates the integration sets based on the total required exposure.

* integrate_over_sets
```python 
def integrate_over_sets(self):
```
for each integration set previously created it integrates the frames within a set to produce a pre master picture.

<p align="right">(<a href="#top">back to top</a>)</p>
