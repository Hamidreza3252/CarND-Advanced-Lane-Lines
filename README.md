## An Overview of Advanced Lane Finding Pipeline  

**Note:** This project is also available on [https://github.com/Hamidreza3252/CarND-Advanced-Lane-Lines](Gitbub)  

**Here are the steps I took to develop advanced lane detection pipeline**  

Below, I have explained the classes I have introduced just to improve logic design, code readability and traceability. 

## 1. Defining `Camera` Class  

`Camera` class implements the methods required to calibrate, undistort, warp, and unwarp an image. These methods are used in the pipeline below to extract the lanes. It also keeps and encapsulates the calibrated paramters. 

- `class Camera`  
  - `calibrate` : To compute the camera calibration matrix and distortion coefficients. it should be called only once. To do so, this function reads all the chessboard images uploaded in the specifed folder and it tries to calibrate based on these pics. 
  - `undistort` : To undistort an image by applying the calibrated parameters.  
  - `calibratePerspectiveTransform` : To calibrate perspective transfrm paramters using the following steps. These params are used for both warp and unwarp functions. 
    * Identify four source points for the perspective transform. In this case, we assume the road is a flat plane. This isn't strictly true, but it can serve as an approximation for this project. 

    * Pick four points in a trapezoidal shape (similar to region masking) that would represent a rectangle when looking down on the road from above. The easiest way to do this is to investigate an image where the lane lines are straight, and find four points lying along the lines that, after perspective transform, make the lines look straight and vertical from a bird's eye view perspective.
    
    * Those same four source points will now work to transform any image (again, under the assumption that the road is flat and the camera perspective hasn't changed). When applying the transform to new images, the test of whether or not you got the transform correct, is that the lane lines should appear parallel in the warped images, whether they are straight or curved.


  - `warp` : To warp an image - to eye-bird view transformation. 
  - `unwarp` : To warp an image - to perspective view transformation. 
  
***

**Note:** Source points are the `x` and `y` pixel values of any four corners on the chessboard. They can be extracted from the corners array output from `cv2.findChessboardCorners()`. So, the destination points are the `x` and `y` pixel values of where we want those four corners to be mapped on in the output image.  


## 2. Defining `ImageColorTransform` Class  

`ImageColorTransform` class implements the methods required to transform an image to a binary image, capturing lanes using different approaches and thresholds. It also introduces some variable to bookkeep Sobel calculated values and lane-fit paramters. This bookkeeping helps to get improved perfrmance by avoding some unnecesary re-calculations. Example of these variables are `sobelX`, `sobelY`, `leftLanePolyFitParams`, and `rightLanePolyFitParams`. The local threshold variables, that are introduced within these methods, are calibrated after several trials on test and challenge videos - although more works need to be done to get better result for '*even-harder*' challenge video.  

- `class ImageColorTransform`  
  - `regionOfInterest` :  
      To extract an image focused on a the front side of the car / camera. This is done by defining a trapezoidal mask applied to the input image. 
  - `sobelAbsoluteFilter`, `sobelMagnitudeFilter`, and `sobelDirectionFilter` methods :  
      These methods are used to calculate Sobel gradient measures in `x` and `y` durections and apply threshods to obtain binary images, filtering out the lanes.  
    
  - `getCombinedFiltersImage` :  
      This function takes an input image and returns a binary image by combining the best approaches to extract lanes. These approaches are combinations of Saturation and Red channels together with the gradients with some ligh-depedent thresholds. It first divides the y-zone into `zoneCount` portions and then each parameter is applied based on the ligh condition of that zone. Here are some of the parameters calibrated based on zonal light conditions: 
    * `sSobelXThresholds` :  Sobel threshold of S-channel in `x` direction  
    * `sSobelYThresholds` :  Sobel threshold of S-channel in `y` direction  
    * `rSobelXThresholds` :  Sobel threshold of Red-channel in `x` direction  
    * `rSobelYThresholds` :  Sobel threshold of Red-channel in `y` direction  
    * `saturationIntensityFactor` : An intensity factor that is multiplied with the average saturation value of each zone to filter out some noises based on lighting conditions 
    * `lightIntensityFactor` : An intensity factor that is multiplied with the average light value of each zone to filter out pixels with less lighting value  
    
    It should be noted that these parameters are calibrated for different lighting conditions. `meanZoneLight < 50`, `meanZoneLight < 100`, `meanZoneLight < 130`, `meanZoneLight < 150`, and `meanZoneLight > 150`. This function returns `combinedBinaryImage` which is obtained by combining different thresholds - ref to the maon body of the function below.  

  - `findLanePixels` :  
    This function takes a binary warped (transformed to bird-eye view) image as input and returns the coordinates of the points that are likely placed at the left and right lanes. It performs a *window-based* search to identify the white points on the lanes. One big difference - or improvement  - done to the counter method implemented as a part of the quiz is as follows: I noticd that the previous implementaion would treat the points that are closer to the camera the same way as the ones that are far from it. This usually creates a problem of confusing the algorithm available sources of noises far from the camera. So I have introduced a weight-based pixel counting to mitigate this situaiton.  
    
  - `mapNewPolynomialToLanes` :  
    This function takes a binary warped (transformed to bird-eye view) image as an input and it performs a while lane search method using a fresh start approach, by searching for windows containing the lanes - as explained above. It returns `yPoints`, `leftLaneFitXs` (parabola fit parameters of the left lane), `rightLaneFitXs` (parabola fit parameters of the right lane), `leftLaneCurveRad` (curvature of the left lane), `rightLaneCurveRad` (curvature of the right lane), and `resultImage` in which the area between the lanes are shaded by green color.  
    
  - `mapPolynomialToLanesBySearch` :  
    This function takes a binary warped (transformed to bird-eye view) image as an input and it performs a while lane search method using search method. Search method works with the previoudly calculated lane fit paramters and finds the new lane parameters using the previous fit parameters. This should improve the performance as compared to the method above, searching for windows in each frame. Like `mapNewPolynomialToLanes` function, it returns `yPoints`, `leftLaneFitXs` (parabola fit parameters of the left lane), `rightLaneFitXs` (parabola fit parameters of the right lane), `leftLaneCurveRad` (curvature of the left lane), `rightLaneCurveRad` (curvature of the right lane), and `resultImage` in which the area between the lanes are shaded by green color. 
    **Note:** If this functin fails to find new lanes, it returns a None value as `fitLaneImage` variable, trigerring the fresh *window-based* search algorithm. 


### Some OpenCV functions used for this project  

- `cv2.inRange()` for color selection  
- `cv2.fillPoly()` for regions selection  
- `cv2.line()` to draw lines on an image given endpoints  
- `cv2.addWeighted()` to coadd / overlay two images  
- `cv2.cvtColor()` to grayscale or change color  
- `cv2.imwrite()` to output images to file  
- `cv2.bitwise_and()` to apply a mask to an image


******************************

## Sample Videos 

### Project Video  

[![](https://img.youtube.com/vi/V-sJOy1lv6I/0.jpg)](https://youtu.be/V-sJOy1lv6I "Click to play on YouTube")

### Challenge Video  

[![](https://img.youtube.com/vi/RbLHkC7lZT8/0.jpg)](https://youtu.be/RbLHkC7lZT8 "Click to play on YouTube")

### Harder Challenge Video  

[![](https://img.youtube.com/vi/7VhWT4HIIok/0.jpg)](https://youtu.be/7VhWT4HIIok "Click to play on YouTube")

