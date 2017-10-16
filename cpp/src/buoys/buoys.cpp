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
#include "vision/buoys.hpp"

void printNums(std::string s, std::vector<int> in){
	std::cout<<"\n";
	std::cout<<s<<" ";
	for(int i : in){
		std::cout<<i<<" ";
	}
	std::cout<<"\n";
}
std::vector<Found> found;
cv::Mat redBuoy(const cv::Mat& in){
	cv::Mat src;
	in.copyTo(src);
	//true when at Competition Pool
	//false when at AVHS Pool
	if(atComp)
		src = color_illumination_correction(in, 171);
	cv::Mat red = redFilter(src);
	cv::normalize(red,red, 0, 255, cv::NORM_MINMAX, CV_8UC1);
	red = erodeMat(red);
	cv::fastNlMeansDenoising(red, red, 3, 7, 21 );
	return red;
}
cv::Mat greenBuoy(const cv::Mat& in){
	cv::Mat base = redBuoy(in);
	cv::Mat green;
	cv::bitwise_not(base,green);
	cv::normalize(green,green, 0, 255, cv::NORM_MINMAX, CV_8UC1);
	whitebalance(green, green, .008f, .001f, 0, 255);
	cv::normalize(green,green, 0, 255, cv::NORM_MINMAX, CV_8UC1);

	return green;
}
cv::Mat yellowBuoy(const cv::Mat& in){
	cv::Mat yellow = yellowFilter(in);
	cv::normalize(yellow, yellow, 0, 255, cv::NORM_MINMAX, CV_8UC1);
	yellow = illumination_correction(yellow, 101);
	return yellow;
}
cv::Point brightest(const cv::Mat& in){
	double minVal; 
	double maxVal; 
	cv::Point minLoc; 
	cv::Point maxLoc;
	cv::minMaxLoc( in, &minVal, &maxVal, &minLoc, &maxLoc );
	return maxLoc;
}
cv::Point3d center(const cv::Mat& in, const cv::Point& p){
	cv::Rect r; 
//	float size = std::sqrt(cv::floodFill(in, cv::Point(p.x, p.y), cv::Scalar(255), &r, cv::Scalar(15), cv::Scalar(15), 4) * 4/M_PI);;
	float size = cv::floodFill(in, cv::Point(p.x, p.y), cv::Scalar(255), &r, cv::Scalar(10), cv::Scalar(10), 4);
	cv::Point3d centerP = cv::Point3d(r.x + r.width/2, r.y + r.height/2, (int) size);
	return centerP;
}
/*
 * These test the validity of the buoy
 * If false, it wont update the location of it
 */
bool checkColor(cv::Point3d  p, const cv::Mat& in, int thresh, int color){
	int red = in.at<cv::Vec3b>(p.y, p.x)[2];
	int green = in.at<cv::Vec3b>(p.y, p.x)[1];
	int blue = in.at<cv::Vec3b>(p.y, p.x)[0];

	if(color==1 && (abs(red-green))<thresh)
		return true;
	if(color==2 && (abs(green-blue)>thresh))
		return true;
	if(color==3 && red>thresh && std::abs(blue-green)<75 && blue<200 && green<200)
		return true;
	return false;
}
//Found getFound(int color, cv::Point3d p, const cv::Mat& img, const cv::Mat& col){
Found getFound(int color, cv::Point3d p, const cv::Mat& img, const cv::Mat& col){
	float theta = cropx *  fhFOV * static_cast<float>(p.x - img.cols/2) / img.cols;
	float phi = cropy * fvFOV * static_cast<float>((img.rows-p.y) - img.rows/2) / img.rows;
	float dist = std::max(.2, buoyWidth/2 / std::tan(p.z/img.cols * cropy * fvFOV / 2 * 2*M_PI) * .4 - 1.f);

	bool cont = false;
	switch(color){
		case 1: //yellow
			if(!checkColor(p, col, 100, 1))
				cont = true;
			break;
		case 2: //green
			if(!checkColor(p, col, 75, 2))
				cont = true;
			break;
		case 3: //red
			if(!checkColor(p, col, 150, 3))
				cont = true;
			break;
	}
	
	return {
		cont,
		theta, phi, p.z
	};
}
void resize(cv::Mat& in, int size){
	cv::resize(in, in, cv::Size(), 2, 2);
}
void setOut(Found* in, Output* out, double conf){
   	out->z_rotation = in->theta;
   	out->elevation =  in->phi;
	out->confidence = conf;
	if(in->dist >0.3 * (512 * 240)){
		//if buoy is big enough, set istance really small
		out->distance = 0.2;
		out->z_rotation = 0.0;
		out->elevation = 0.0;
	}
}
void ybuoys(const cv::Mat& in, Output* out)
{
	cv::Mat img_mat, out_mat;
	in.copyTo(img_mat);

    cv::resize(img_mat(cv::Rect(img_mat.cols*(1-cropx)/2, img_mat.rows*(1-cropy-offset)/2,
			img_mat.cols*cropx, img_mat.rows*cropy)), img_mat,
			cv::Size(cropx*scalex, cropy*scaley));

	img_mat.copyTo(out_mat);

	cv::Mat yellow = yellowBuoy(img_mat);
	cv::Point yellowBright = brightest(yellow);
	cv::Point3d yellowP = center(yellow, yellowBright);

//   	Found yfound = getFound(1, yellowP, yellow, img_mat);
//	setOut(&yfound, out, 1.0);
}
void gbuoys(const cv::Mat& in, Output* out)
{
	cv::Mat img_mat, out_mat;
	in.copyTo(img_mat);

    cv::resize(img_mat(cv::Rect(img_mat.cols*(1-cropx)/2, img_mat.rows*(1-cropy-offset)/2,
			img_mat.cols*cropx, img_mat.rows*cropy)), img_mat,
			cv::Size(cropx*scalex, cropy*scaley));

	img_mat.copyTo(out_mat);

	cv::Mat green = greenBuoy(img_mat);
	cv::Point greenBright = brightest(green);
	cv::Point3d greenP = center(green, greenBright);

//	Found gfound = getFound(2, greenP, green, img_mat);
//	setOut(&gfound, out,1.0);
}
void rbuoys(const cv::Mat& in, Output* out, char* pref)
{
	cv::Mat img_mat, out_mat, hsv_mat, yuv, yuv_split[3], ycrcb, ycrcb_split[3];
	in.copyTo(img_mat);

    cv::resize(img_mat(cv::Rect(img_mat.cols*(1-cropx)/2, img_mat.rows*(1-cropy-offset)/2,
			img_mat.cols*cropx, img_mat.rows*cropy)), img_mat,
			cv::Size(cropx*scalex, cropy*scaley));
//	resize(img_mat,2);
	img_mat.copyTo(out_mat);
	cv::cvtColor(img_mat, hsv_mat, cv::COLOR_BGR2YCrCb);
	cv::cvtColor(img_mat, yuv, cv::COLOR_BGR2YUV);
	cv::cvtColor(img_mat, ycrcb, cv::COLOR_BGR2YCrCb);
	cv::split(yuv, yuv_split);
	cv::split(ycrcb, ycrcb_split);
	
	filterLight(img_mat);

    cv::Mat red = redBuoy(img_mat);
	cv::Point redBright = brightest(red);
    cv::Point3d redP = center(red, redBright);

	int x = redBright.x;
	int y = redBright.y;

	//For Testing purposes
	int red_color = img_mat.at<cv::Vec3b>(y, x)[2];
	int green_color = img_mat.at<cv::Vec3b>(y, x)[1];
	int blue_color = img_mat.at<cv::Vec3b>(y, x)[0];
	int h = hsv_mat.at<cv::Vec3b>(y, x)[0];
	int s = hsv_mat.at<cv::Vec3b>(y, x)[1];
	int v = hsv_mat.at<cv::Vec3b>(y, x)[2];
	int yuv_y = yuv.at<cv::Vec3b>(y, x)[0];
	int yuv_u = yuv.at<cv::Vec3b>(y, x)[1];
	int yuv_v = yuv.at<cv::Vec3b>(y, x)[2];
	int yrb_y = ycrcb.at<cv::Vec3b>(y, x)[0];
	int yrb_r = ycrcb.at<cv::Vec3b>(y, x)[1];
	int yrb_b = ycrcb.at<cv::Vec3b>(y, x)[2];
	fprintf(stdout, "bgr: %d %d %d\n", blue_color, green_color, red_color);
	fprintf(stdout, "hsv: %d %d %d\n", h, s, v);
	fprintf(stdout, "yuv: %d %d %d\n", yuv_y, yuv_u, yuv_v);
	fprintf(stdout, "ycrcb: %d %d %d\n", yrb_y, yrb_r, yrb_b);

	double confidence = 0.0;
	if(red_color > green_color && red_color > blue_color){
		confidence = 0.2;	
	}
	if(red_color > green_color + 20 && red_color > blue_color + 20){
		confidence = 0.3;	
	}
	if(red_color > green_color + 50 && red_color > blue_color + 50){
		confidence = 0.4;
	}

	confidence += (double) .6 * std::abs(red_color - green_color)/255;
	confidence += (double) .6 * std::abs(red_color - blue_color)/255;

	//just in case to get rid of outliers
//	if(std::abs(blue_color-green_color) > 45 || red_color <= 120 || (yrb_r < yrb_b || yrb_r < yrb_y))
	if(std::abs(blue_color-green_color) > 45 || (yrb_r < yrb_b || yrb_r < yrb_y))
		confidence = 0.0;
	if(confidence > 1.0)
		confidence = 1.0;

	Found rfound = getFound(3, redP, red, img_mat);
	setOut(&rfound, out, confidence);
	if(confidence < 0.33) {
		//red circle
		cv::circle(red, cv::Point(redP.x, redP.y), redP.z, cv::Scalar(0,0,255), 1, 0);
		cv::circle(out_mat, cv::Point(redP.x, redP.y), redP.z, cv::Scalar(0,0,255), 1, 0);
	}
	else if(confidence >= 0.33 && confidence < 0.66){

		cv::circle(red, cv::Point(redP.x, redP.y),redP.z, cv::Scalar(255,0,255), 1, 0);
		cv::circle(out_mat, cv::Point(redP.x, redP.y), redP.z, cv::Scalar(255,0,255), 1, 0);
	}
	else if(confidence >= 0.66){
		//green circle
		cv::circle(red, cv::Point(redP.x, redP.y), 20, cv::Scalar(0,255,0), 1, 0);
		cv::circle(out_mat, cv::Point(redP.x, redP.y), redP.z, cv::Scalar(0,255,0), 1, 0);
	}
	resize(out_mat, 3);
	cv::imshow("fsdfds", out_mat);
	cv::waitKey(0);

	imageWrite(out_mat, pref, "rbuoys/");
}
