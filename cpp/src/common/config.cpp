#include "common/config.hpp"

const Matrix initialModel =
{
	0,
	7,    0,
	13,    0,     0,
	18,    0,      2,
	17.5,  -1.5,   2,
	20,    -1,
	18,    8,
	17.4,  10.3,
	0,     0,
	0,
	0,
	3,
	0,     0,
};

const Matrix initialVariance =
{
	1,
	4,     4,
	9,     9,     1,
	9,     9,     1,
	9,     9,     1,
	9,     9,
	9,     9,
	9,     9,
	.5,    .5,
	1,
	1,
	1,
	4,   4,
};

const Matrix varianceGrowth =
{
	0,
	.1,    .1,
	.1,    .1,    0,
	.1,    .1,    0,
	.1,    .1,    0,
	.03,    .03,
	.1,    .1,
	.1,    .1,
	.1,   .1,
	.1,
	1,
	.1,
	.5,    .5,
};

const Matrix constants =
{
	4.8,
	4,
	30,    -15,
	5,
};

