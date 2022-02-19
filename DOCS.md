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
            <li><a href="#Methods">Methods</a></li>
          </ul>
      </ul>
      <ul>
        <li><a href="#FlexIm">FlexIm object</a></li>
          <ul>
            <li><a href="#Methods">Methods</a></li>
          </ul>
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
          <ul>
            <li><a href="#Methods">Methods</a></li>
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
## Methods
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
def save(self, path)
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
def edge(self)                                                                                             
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





<p align="right">(<a href="#top">back to top</a>)</p>
