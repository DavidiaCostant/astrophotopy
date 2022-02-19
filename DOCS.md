# AstroPhotoPy library documentation

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#Object types">Object types</a>
      <ul>
        <li><a href="#Image">Image object</a></li>
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
## Object types

Once I approached astrophotography several months ago, I searched for a tool grouping all my needs in term of image processing workflow. Much of those instruments are counterintuitive and/or platform/OS restricted (and not less important not free). 
So I wrote this simple library including all I need at the moment for a flexible processing workflow.\
Remember that the AstroPhotoPy library can only be used inside a Jupiter / IPython notebook. 
I hope you'll enjoy it!

<p align="right">(<a href="#top">back to top</a>)</p>


### Image object
The Image type is a container for a single image data and additional field for properties as:

* hist: the vector of values of luminance
* norm: the norm(squared) of hist vector
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



<!-- USAGE EXAMPLES -->
## Simple usage
1. Import the library, you can create a telescope and an observation site first then you have to create your project:
 ```python
   import astrophotopy as ap 
   my_tele = ap.Telescope(model="RC 8", diameter = 203, f_len = 1604, f_len_ep = 22, px_dim = 2.9, sens_diag = 23)
   my_site = ap.Observation_Site(location_name = "Tre cime di Lavaredo", altitude = 2320, latitude = 46.6, air_temp = -5.5, fwhm = 1)
   crab = ap.Project(subject="M1", path="My_folder", telescope = my_tele, observation_site = my_site)

```
2. After copying your images (rough, dark and flat frames) in their respective folders, you have to load them and then perform set cleaning by means of master dark and flat frame subtraction:
```python
   crab.load()
   crab.subtract_master_dark_and_flat()

```
3. Now perform an automatic selection of the best images and then align the retained frames:
```python
   crab.show_select_and_drop()
   crab.align_frames("normal", transform = "euclidean")

```
4. After prior calculation of total exposure and creation of integration sets, sets' integration can be performed:
```python
   crab.create_integration_sets()
   crab.integrate_over_sets()

```
 
_For a better description of the above (and others) astrophotopy methods, please refer to the [Documentation](https://github.com/DavidiaCostant/astrophotopy/blob/main/DOCS.md)_

<p align="right">(<a href="#top">back to top</a>)</p>
