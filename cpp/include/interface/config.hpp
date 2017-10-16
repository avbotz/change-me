#ifndef INTERFACE_CONFIG_HPP
#define INTERFACE_CONFIG_HPP

#include <vector>
#include <functional>

#include "common/config.hpp"
#include "interface/data.hpp"
#include "interface/functions.hpp"

struct Connection
{
	template <typename F, typename... A>
	Connection(F _function, A... args) :
		function(std::bind(_function, std::placeholders::_1, args...))
	{
	}

	const std::function<bool(Data*)> function;
};

std::vector<Connection> defaultConnections();

struct Output{
	double z_rotation, radius_distance, elevation;
	double distance, confidence;

	const char* prefix;

	Output(const char* in) :
		prefix(in),
		z_rotation(-100.0),
		radius_distance(-100.0),
		elevation(-100.0),
		distance(-100.0),
		confidence(0.0)
	{
	}

	void write(FILE* out){
		fprintf(out, "%s %.5e %.5e %.5e %.5e %.5e\n",
			prefix,
			z_rotation, radius_distance, elevation,
			distance, confidence);
	}
};


#endif

