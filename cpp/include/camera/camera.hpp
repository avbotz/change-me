#include <cv.h>
#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <flycapture/FlyCapture2.h>
#include <cstdio>
#include <iomanip>
#include <thread>
#include <chrono>
#include <cstdio>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <cv.h>

#include "image/image.hpp"

class Camera {
	public:
		FILE* in = stdin;
		FILE* out = stdout;
		FILE* log = stderr;
		unsigned int numCameras;
		unsigned int idx;
		FlyCapture2::PGRGuid guid;
		FlyCapture2::Camera cam;

		bool init(unsigned int i);
		void flipImage(cv::Mat& img);
		int startCamera();
		cv::Mat capture(bool flip);
		bool quit();
};
