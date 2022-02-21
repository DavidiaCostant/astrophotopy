# AstroPhotoPy
Astrophotography pre and post processing tools

[![LinkedIn][linkedin-shield]][linkedin-url]


<!-- PROJECT LOGO -->
<br />
<div align="center">
    
  <a href="https://github.com/DavidiaCostant/astrophotopy">
    <img src="https://github.com/DavidiaCostant/astrophotopy/blob/main/crab.jpg" alt="Logo" width="100" height="100">
  </a>
  <h1 align="center">AstroPhotoPy</h1>

  <p align="center">
    Flexible image processing with the astrophotographer in mind
  
  </p>
  <p align="center">

  
  </p>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#Simple usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

Once I approached astrophotography several months ago, I searched for a tool grouping all my needs in term of image processing workflow. Much of those instruments are counterintuitive and/or platform/OS restricted (and not less important not free). 
So I wrote this simple library including all I need at the moment for a flexible processing workflow.\
Remember that the AstroPhotoPy library can only be used inside a Jupiter / IPython notebook. 
I hope you'll enjoy it!

<p align="right">(<a href="#top">back to top</a>)</p>


### Built With

This library is based essentially on two image processing libraries and a front-end library: 

* opencv
* skimage
* IPython 


<p align="right">(<a href="#top">back to top</a>)</p>



<!-- GETTING STARTED -->
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
  
* pyfits
  ```sh
  pip install pyfits
  ```
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
1. Import the library, you can create a setup (optics + sensor) and an observation site first then you have to create your project:
 ```python
   import astrophotopy as ap 
   my_optics = ap.Optics(model="RC 8", diameter = 203, f_len = 1604, f_len_ep = 22)
   my_sensor = ap.Sensor(model = "Sony IMX", px_dim = 2.9, sens_diag = 23)
   my_site = ap.Observation_Site(location_name = "Tre cime di Lavaredo", altitude = 2320, latitude = 46.6, air_temp = -5.5, fwhm = 1)
   crab = ap.Project(subject="M1", path="My_folder", optics = my_optics, sensor = my_sensor, observation_site = my_site)

```
2. After copying your images (rough, dark and flat frames) in their respective folders, you have to load them (only .jpg, .png, .bmp, .tiff e .fits can be imported) and then perform set cleaning by means of master dark and flat frame subtraction:
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



<!-- ROADMAP -->
## Roadmap

- [x] Add Changelog
- [ ] Write documentation
- [ ] Add .ser file import/export
- [ ] Add monochromatic camera workflow
- [ ] Add additional examples


See the [open issues](https://github.com/DavidiaCostant/astrophotopy/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Davidia - d.costantini.stcerello@gmail.com

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/davide-costantini-299805113/
