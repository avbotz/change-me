#include "vision/pvc_vision.hpp"
#include "vision/pvc.hpp"

const float cropx = 0.8;
const float cropy = 0.8;
const float offset = 0.0 * (1 - cropy);
const float offsetx = cropx*0.3;
const float scalex = 600;
const float scaley = 360;

const float MAX_ROTATION = 20.0f;

/* For Laplacian, not being used atm
const int kernel_size = 3;
const int scale = 1;
const int delta = 0;
const int ddepth = CV_16S;
*/

void findBestSolution(std::vector<Solution> solutions, int &a, int &b)
{
    // Stores highest dist sum for X and Y
    int max_sum = -100000;

    for (int i = 0; i < solutions.size(); i++)
    {
        // Calculate midpoint 
        int mid_x_i = solutions[i].midpoint.x;
        int mid_y_i = solutions[i].midpoint.y;

        for (int j = i+1; j < solutions.size(); j++)
        {
            // Calculate midpoint
            int mid_x_j = solutions[j].midpoint.x;
            int mid_y_j = solutions[j].midpoint.y;

            // Make sure lines are reasonable 
            if (// std::abs(mid_x_i - mid_x_j) > MIN_DIST &&
                // std::abs(mid_y_i - mid_y_j) > MIN_DIST &&
                std::abs(solutions[i].rotation - solutions[j].rotation) < MAX_ROTATION)
            {
                // Make sure Y distance diff is at a minimum
                int x_dist = std::abs(mid_x_i - mid_x_j);
                int y_dist = std::abs(mid_y_i - mid_y_j);
                int sum = x_dist - y_dist;
                if (sum > max_sum) 
                {
                    max_sum = sum;
                    a = i;
                    b = j;
                }
            }       
        }
    }
}

void detect_pvc(const cv::Mat& image, Output* out, char* pref)
{
    // Illuminate the image to show underwater 
    cv::Mat illuminated = fixImgIllum(image);

    // Pull apart the blue channel
    cv::Mat corrected = correctImg(illuminated);

    // Denoised
    cv::Mat denoised = denoiseImg(corrected);

    // Resize image
    cv::resize(denoised(cv::Rect(denoised.cols*(1-cropx)/2, denoised.rows*(1-cropy-offset)/2, 
                    denoised.cols*cropx, denoised.rows*cropy)), denoised, 
            cv::Size(cropx*scalex, cropy*scaley));

    // Laplacian filter
    /*
       cv::Mat src, src_abs;
       cv::Laplacian(denoised, src, ddepth, kernel_size, scale, delta, cv::BORDER_DEFAULT);
       cv::convertScaleAbs(src, src_abs);
       cv::namedWindow("Laplacian!");
       cv::imshow("Laplacian!", src_abs);
       */

    // Canny image to find lines
    cv::Mat dst, cdst;
    cv::Canny(denoised, dst, 50, 200, 3);
    cv::cvtColor(dst, cdst, cv::COLOR_GRAY2BGR);

    // Get lines with HoughLinesP
    std::vector<cv::Vec4i> lines;
    std::vector<Solution> solutions;
    cv::HoughLinesP(dst, lines, 1, CV_PI/180, 50, 20, 20);
    for (int i = 0; i < lines.size(); i++) 
    {
        cv::Vec4i line = lines[i];
        //cv::line(cdst, cv::Point(line[0], line[1]), cv::Point(line[2], line[3]), cv::Scalar(0, 0, 255), 3, CV_AA);
        Solution solution(cv::Point(line[0], line[1]), cv::Point(line[2], line[3]));
        if (solution.rotation <= 30)
        {
            solutions.push_back(solution); 
            cv::line(cdst, solution.pt1, solution.pt2, cv::Scalar(0, 0, 255), 3, CV_AA);
        }
    }

    // Find vertical lines
    std::sort(solutions.begin(), solutions.end(), [](Solution a, Solution b){ return a.rotation < b.rotation; });

    // Find the best solution
    int a=0, b=0;
    bool found = false; 
    if (solutions.size() > 1) 
    {
        findBestSolution(solutions, a, b);
        //std::cout << "A: " << a << "\tB: " << b << std::endl;
        if (a != 0 || b != 0) 
        {
            // PVC is found
            found = true;

            // Get needed data
            cv::Point loc ((solutions[a].midpoint.x + solutions[b].midpoint.x)/2, (solutions[a].midpoint.y + solutions[b].midpoint.y)/2);
            cv::line(cdst, solutions[a].pt1, solutions[a].pt2, cv::Scalar(0, 255, 0), 3, CV_AA);
            cv::line(cdst, solutions[b].pt1, solutions[b].pt2, cv::Scalar(0, 255, 0), 3, CV_AA); 
            cv::circle(cdst, loc, 4, cv::Scalar(102, 0, 102), -1, 8, 0);

            // Set output struct 
            float theta = cropx * fhFOV * (float)(loc.x - dst.cols/2) / dst.cols;
            out->z_rotation = theta;
            out->confidence = 1.0;
        }
    } 

    // Print out 0 if nothing found
    if (!found) 
    {
        out->z_rotation = -10;
        out->confidence = 0.0;
    }
}
