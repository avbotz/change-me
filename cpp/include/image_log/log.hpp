#include "image/image.hpp"

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <cv.h>

#include <thread>
#include <chrono>
#include <regex>
#include <string>
#include <sstream>

void imageWrite(const cv::Mat&, const char*, const char*);
