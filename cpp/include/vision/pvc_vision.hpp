#ifndef VISION_PVC_HPP
#define VISION_PVC_HPP

#include <opencv2/core/core.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <opencv2/highgui/highgui.hpp>

#include <iostream>
#include <vector>
#include <functional>

cv::Mat fixImgIllum(cv::Mat img);
cv::Mat correctImg(cv::Mat img);
cv::Mat denoiseImg(cv::Mat img);

class Solution 
{
public:
    cv::Point pt1, pt2, midpoint;
    float dist, rotation;
    Solution(cv::Point, cv::Point);
    void print();
};

#endif
