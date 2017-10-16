#include <thread>
#include <vector>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <cv.h>

#include "image_log/log.hpp"
#include "interface/config.hpp"
#include "vision/buoys.hpp"
#include "vision/flashlight.hpp"

int main(int argc, char** argv){
	if(argc<2){
		fprintf(stdout, "./vision_test [vision task] [image]\n");
		fflush(stdout);
		return 1;
	}
	cv::Mat in = cv::imread(argv[2]);
	std::string task = argv[1];
	Output out(argv[1]);
	if(task == "rbuoys"){
		rbuoys(in, &out, "vtest/");
	}
	if(task == "flashlight"){
		// flashlight(in, &out, "vtest/");
	}
	out.write(stdout);
}
