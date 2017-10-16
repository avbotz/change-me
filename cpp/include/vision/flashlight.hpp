#include <vector>
#include <algorithm>
#include <thread>
#include <chrono>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <cv.h>

#include "image_log/log.hpp"
#include "common/defs.hpp"
#include "common/config.hpp"
#include "vision/config.hpp"
#include "vision/vision.hpp"
#include "vision/buoys_vision.hpp"
#include "image/image.hpp"

#include "interface/config.hpp"

//const float cropx = 1.0;
//const float cropy = 0.6;

cv::Point brightest(const cv::Mat& in);
cv::Point3d center(const cv::Mat& in, const cv::Point& p);
cv::Mat HSV_V(const cv::Mat& in);
void flashlight(const cv::Mat& in, Output* out, char* pref);
