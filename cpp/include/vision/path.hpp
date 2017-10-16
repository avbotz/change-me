#include <iostream>
#include <vector>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <cv.h>

#include "common/defs.hpp"
#include "common/config.hpp"
#include "vision/config.hpp"
#include "vision/vision.hpp"
#include "vision/pvc_vision.hpp"

#include "interface/config.hpp"
#include "image/image.hpp"

void detect_path(const cv::Mat& img, Output*, char*);
