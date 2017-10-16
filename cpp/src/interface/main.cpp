#include <thread>
#include <vector>
#include <functional>

#include <opencv2/core/core.hpp>
#include <opencv2/highgui/highgui.hpp>
#include <opencv2/imgproc/imgproc.hpp>
#include <cv.h>

#include "camera/camera.hpp"
#include "image_log/log.hpp"
#include "interface/config.hpp"
#include "vision/buoys.hpp"
#include "vision/pvc.hpp"
#include "vision/path.hpp"
#include "vision/flashlight.hpp"

bool logdown = false;
bool logfront = true;

// {  [red buoy], [pvc], [path], [dropper], [flashlight]  }
int run_tasks[] = {0,0,0,0,1};

bool isfront = true;
bool isdown = true;

int main(int argc, char** argv)
{
	FILE* log = stderr;
	FILE* out = stdout; //fopen("pipes/vision", "w+");

	char* prefix = argv[1];

	Camera front, down;
	isfront = front.init(0);
	isdown = down.init(1);

	// If neither camera available, end program
	if(!isfront && !isdown)
		return 1;

	while(true){
		rewind(out);

		//if front camera works
		if(isfront){
			cv::Mat f = front.capture(true);
			imageWrite(f, prefix, "original/f_");

			if(run_tasks[4]==1){
				//simulates red buoy, but is meant to work with light underwater
				Output flash("red_buoy");
				flashlight(f, &flash, prefix);
				flash.write(out);
			}
			if(run_tasks[0]==1){
				Output rbuoy_output("red_buoy");
				rbuoys(f, &rbuoy_output, prefix);
				rbuoy_output.write(out);
			}
			if(run_tasks[1]==1){
				Output pvc_output("pvc");
				detect_pvc(f, &pvc_output, prefix);
				pvc_output.write(out);
			}
		}

		//if down camera works continue
		if(isdown){
			cv::Mat d = down.capture(false);
			imageWrite(d, prefix, "original/d_");

			if(run_tasks[2]==1){
				Output path_output("path");
				detect_path(d, &path_output, prefix);
				path_output.write(out);
			}
			if(run_tasks[3]==1){
				// dropper
			}
		}

		fprintf(out, "\n");
		fflush(out);
	}
	if(isfront)
		front.quit();
	if(isdown)
		down.quit();
	return 0;
}

