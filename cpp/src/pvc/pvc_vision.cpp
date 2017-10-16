#include "vision/pvc_vision.hpp"


Solution::Solution(cv::Point point1, cv::Point point2) 
{
    // Set the points
    this->pt1 = point1;
    this->pt2 = point2;
    this->midpoint = cv::Point((pt1.x + pt2.x)/2, (pt1.y + pt2.y)/2);

    // Calculate distance and rotation
    this->dist = std::sqrt(std::pow(std::abs(point1.x - point2.x), 2) + std::pow(std::abs(point1.y - point2.y), 2));
    this->rotation = std::acos(std::abs(point1.y - point2.y) / this->dist) * 180/M_PI;
}

void Solution::print() 
{
    std::cout << "Dist:     " << this->dist << std::endl;
    std::cout << "Rotation: " << this->rotation << std::endl;
}

cv::Mat fixImgIllum(cv::Mat input) 
{
    // Convert to diff colorspace and split 
    cv::Mat img;
    std::vector<cv::Mat> channels;
    cv::cvtColor(input, img, cv::COLOR_BGR2Lab);
    cv::split(img, channels);

    // Use CLAHE
    cv::Ptr<cv::CLAHE> clahe = cv::createCLAHE();
    cv::Mat temp0, temp1, temp2;
    clahe->setClipLimit(2);
    clahe->apply(channels[0], temp0);
    clahe->apply(channels[1], temp1);
    clahe->apply(channels[2], temp2);
    temp0.copyTo(channels[0]);
    temp1.copyTo(channels[1]);
    temp2.copyTo(channels[2]);
    cv::merge(channels, img);

    // Convert back to BGR
    cv::Mat dst;
    cv::cvtColor(img, dst, cv::COLOR_Lab2BGR);

    return dst;
}

cv::Mat correctImg(cv::Mat img) 
{
    // Pull apart the blue channel
    std::vector<cv::Mat> channels;
    cv::split(img, channels);
    cv::equalizeHist(channels[0], channels[0]);
    cv::equalizeHist(channels[1], channels[1]);
    cv::equalizeHist(channels[2], channels[2]);

    // Remerge together
    cv::Mat corrected;
    cv::merge(channels, corrected);

    return corrected;
}

cv::Mat denoiseImg(cv::Mat img) 
{
    // Blur image
    cv::Mat temp, blurred; 
    cv::bilateralFilter(img, temp, 20, 40, 10);
    cv::GaussianBlur(temp, blurred, cv::Size(3, 3), 0, 0, cv::BORDER_DEFAULT);

    return blurred;
}
