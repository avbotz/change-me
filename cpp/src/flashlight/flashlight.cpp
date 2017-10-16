#include "vision/flashlight.hpp"
#include "vision/buoys.hpp"

void flashlight(const cv::Mat& in, Output* out, char* pref)
{
	cv::Mat img_mat, out_mat;
	in.copyTo(img_mat);

    cv::resize(img_mat(cv::Rect(img_mat.cols*(1-cropx)/2, img_mat.rows*(1-cropy-offset)/2,
			img_mat.cols*cropx, img_mat.rows*cropy)), img_mat,
			cv::Size(cropx*scalex, cropy*scaley));

	img_mat.copyTo(out_mat);
	cv::Mat filtered = HSV_V(img_mat);

	//used to be b
	cv::Point p = brightest(filtered);
	
//	cv::Point3d p = center(filtered, b);	

	double theta = fhFOV * static_cast<float>(p.x - img_mat.cols/2) / img_mat.cols;
	double phi = fvFOV * static_cast<float>((img_mat.rows-p.y) - img_mat.rows/2) / img_mat.rows;

   	out->z_rotation = theta;
   	out->elevation =  phi;
	out->confidence = 1.0;

	cv::circle(out_mat, cv::Point(p.x, p.y), 20, cv::Scalar(0,0,255), 1, 0);

	imageWrite(out_mat, pref, "flashlight/");
}
