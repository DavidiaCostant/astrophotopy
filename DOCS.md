# AstroPhotoPy 0.2.x library documentation (UNDER CONSTRUCTION)

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#Object types">Object types</a>
      <ul>
        <li><a href="#Image object">Image object</a></li>
      </ul>
      <ul>
        <li><a href="#FlexIm">FlexIm object</a></li>
      </ul>
      <ul>
        <li><a href="#Optics">Optics object</a></li>
      </ul>
      <ul>
        <li><a href="#Sensor">Sensor object</a></li>
      </ul>
      <ul>
        <li><a href="#Observation_site">Observation_site object</a></li>
      </ul>
      <ul>
        <li><a href="#Project">Project object</a></li>
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
### Object types

Once I approached astrophotography several months ago, I searched for a tool grouping all my needs in term of image processing workflow. Much of those instruments are counterintuitive and/or platform/OS restricted (and not less important not free). 
So I wrote this simple library including all I need at the moment for a flexible processing workflow.\
Remember that the AstroPhotoPy library can only be used inside a Jupiter / IPython notebook. 
I hope you'll enjoy it!

<p align="right">(<a href="#top">back to top</a>)</p>


## Image object
The Image type is a container for a single image data and additional field for properties as:

* hist: the vector of values of luminance
* norm: the norm(squared) of "hist" vector
* dev: the deviation of the image's norm within a set of images

```python
class Image:
    def __init__(self, *name):
        self.image = np.array([])
        self.name = ""
        if name:
            self.name = name
        self.hist = None
        self.norm = None
        self.dev = None 
```
# Image object's methods
all the methods below are destructive, i.e. they apply to the object by overwriting the previous information.

* load
```python
def load(self, path, filename)
```
It loads from a given filename within a path the image data.

* histogram
```python
def histogram(self)
```
It calculates the vector of luminance and its norm then updates the respective fields.

* export_hist
```python        
def export_hist(self, path, *dpi):
```
It saves to a file in the given path a plot of the luminance vector, with the (optional) resolution in dpi.

* save
```python 
save(self, path)
```
It saves the image data to a image file.

* yuv_decompose
```python 
def yuv_decompose(self)
```
It transforms the RGB space of the object to YUV space.

* yuv_recompose
```python 
def yuv_recompose(self)
```
It transforms the YUV space of the object to RGB space.

* conv2d
```python     
    def conv2d(self, kernel)
``` 
It convolves the object with the given kernel

* blur
```python     
    def blur(self, width)
``` 
It applies a blurring of magnitude int(width)                                                                                                  

* sharpen 
```python   
def sharpen(self)                                                                                          
```  
It rapplies sharpness to the image

* edge
```python 
edge(self)                                                                                             
```
It extract edge detection from the previous image

* resize
```python 
def resize(self, factor):
```
It scales the image of the given float(factor).

* show
```python
def show(self)
```
It shows the image

<p align="right">(<a href="#top">back to top</a>)</p>



<!--  -->
## Getting Started

This is an example of how you can setting up your project locally.
To get a local copy up and running, follow these simple steps:

### Prerequisites

To install the things you need first:

* numpy
  ```sh
  pip install numpy
  ```
* matplotlib
  ```sh
  pip install matplotlib
* opencv
  ```sh
  pip install opencv-python
  ```
* skimage
  ```sh
  pip install -U scikit-image
  ```
* IPython
  ```sh
  pip install ipython
  ```
### Installation

After installing dependencies, you can install the library with pip:

   ```sh
   pip install astrophotopy
   ```

<p align="right">(<a href="#top">back to top</a>)</p>





```
 
_For a better description of the above (and others) astrophotopy methods, please refer to the [Documentation](https://github.com/DavidiaCostant/astrophotopy/blob/main/DOCS.md)_

<p align="right">(<a href="#top">back to top</a>)</p>
