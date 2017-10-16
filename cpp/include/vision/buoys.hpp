#include <vector>
#include <algorithm>
#include <thread>
#include <chrono>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <cv.h>

#include "common/defs.hpp"
#include "common/config.hpp"
#include "vision/config.hpp"
#include "vision/vision.hpp"
#include "vision/buoys_vision.hpp"

#include "interface/config.hpp"
#include "image/image.hpp"

const bool atComp = true;

const float cropx = 1.0;
const float cropy = 0.6;
const float offset = 0.0 * (1 - cropy);
const float scalex = 512;
const float scaley = 240;
const int diffDist = 8;
const float buoyWidth = .16;

struct Found
{
	bool use;
	float theta;
	float phi;
	float rho;
	float dist;
};
void printNums(std::string s, std::vector<int> in);

cv::Mat redBuoy(const cv::Mat& in);
cv::Mat greenBuoy(const cv::Mat& in);
cv::Mat yellowBuoy(const cv::Mat& in);
cv::Point brightest(const cv::Mat& in);
int sizeFloodFill(const cv::Mat& in, const cv::Point& p, cv::Rect& r);
cv::Point3d center(const cv::Mat& in, const cv::Point& p);
bool checkColor(cv::Point3d  p, const cv::Mat& in, int thresh, int color);
Found getFound(int color, cv::Point3d p, const cv::Mat& img);
void rbuoys(const cv::Mat& in, Output*, char*);
void gbuoys(const cv::Mat& in, Output*);
void ybuoys(const cv::Mat& in, Output*);
int main(int, char**);
