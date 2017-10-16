#include "image_log/log.hpp"
void imageWrite(const cv::Mat& img, const char* prefix, const char* task)
{
	auto now = std::time(NULL);
	std::tm* local = std::localtime(&now);
	char date[256];
	char format[256];

	snprintf(format, sizeof(format) / sizeof(char), "%%Y-%%m%%d_%%H-%%M-%%S");
	strftime(date, sizeof(date) / sizeof(char), format, local);

	cv::imwrite(std::string(prefix) + std::string(task) + std::string(date) + std::string(".jpg"), img);
}

