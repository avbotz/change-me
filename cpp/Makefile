CC = g++
SRC = src
BUILD = build
BIN = bin

CFLAGS = -ggdb -c -std=c++14 -Iinclude
LFLAGS = 

THIRDPARTY = ./3rdparty/

OPENCV_CFLAGS = `pkg-config --cflags opencv`
OPENCV_LFLAGS = `pkg-config --libs opencv` -pthread

FLYCAP = $(THIRDPARTY)/flycapture/
FLYCAP_CFLAGS = -I$(SRC) -I$(FLYCAP)/include/
FLYCAP_LFLAGS = -L$(FLYCAP)/lib -lflycapture -Wl,-rpath=$(FLYCAP)/lib/

COMMON = $(patsubst %,$(BUILD)/common/%.o,matrix state observation config)
COMMON_CFLAGS = 

MODEL = $(patsubst %,$(BUILD)/model/%.o,system hypothesis evidence)
MODEL_CFLAGS = 

IMAGE = $(patsubst %,$(BUILD)/image/%.o,image)
IMAGE_CFLAGS = $(OPENCV_CFLAGS)

IMAGE_LOG = $(patsubst %,$(BUILD)/image_log/%.o,log)
IMAGE_LOG_CFLAGS = $(OPENCV_CFLAGS)

VISION = $(patsubst %,$(BUILD)/vision/%.o,vision blob blob_detection neural_network config)
VISION_CFLAGS = $(OPENCV_CFLAGS)

BUOYS = $(patsubst %,$(BUILD)/buoys/%.o,buoys buoys_vision) $(IMAGE) $(VISION) $(COMMON) $(IMAGE_LOG)
BUOYS_CFLAGS = $(OPENCV_CFLAGS)
BUOYS_LFLAGS = $(OPENCV_LFLAGS)

FLASHLIGHT = $(patsubst %,$(BUILD)/flashlight/%.o,flashlight) $(IMAGE) $(VISION) $(COMMON) $(IMAGE_LOG)
FLASHLIGHT_CFLAGS = $(OPENCV_CFLAGS)
FLASHLIGHT_LFLAGS = $(OPENCV_LFLAGS)

REAL_PATH = $(patsubst %,$(BUILD)/path/%.o,path) $(IMAGE) $(VISION) $(COMMON) $(IMAGE_LOG)
PATH_CFLAGS = $(OPENCV_CFLAGS)
PATH_LFLAGS = $(OPENCV_LFLAGS)

PVC = $(patsubst %,$(BUILD)/pvc/%.o,pvc pvc_vision) $(IMAGE) $(VISION) $(COMMON)
PVC_CFLAGS = $(OPENCV_CFLAGS)
PVC_LFLAGS = $(OPENCV_LFLAGS)

CAMERA = $(patsubst %,$(BUILD)/camera/%.o,camera) $(IMAGE) $(COMMON)
CAMERA_CFLAGS = $(OPENCV_CFLAGS) $(FLYCAP_CFLAGS)
CAMERA_LFLAGS = $(OPENCV_LFLAGS) $(FLYCAP_LFLAGS)

INTERFACE = $(patsubst %,$(BUILD)/interface/%.o, main) $(MODEL) $(IMAGE) $(COMMON) $(BUOYS) $(PVC) $(CAMERA) $(FLASHLIGHT) $(REAL_PATH)
INTERFACE_CFLAGS = $(OPENCV_CFLAGS) $(CAMERA_CFLAGS)
INTERFACE_LFLAGS = $(OPENCV_LFLAGS) $(CAMERA_LFLAGS)

VISION_TEST = $(patsubst %,$(BUILD)/vision_test/%.o,main) $(IMAGE) $(VISION) $(COMMON) $(BUOYS) $(PVC) $(FLASHLIGHT) $(REAL_PATH)
VISION_TEST_CFLAGS = $(OPENCV_CFLAGS)
VISION_TEST_LFLAGS = $(OPENCV_LFLAGS)

TORPEDOES = $(patsubst %,$(BUILD)/torpedoes/%.o,main) $(IMAGE) $(VISION) $(COMMON)
TORPEDOES_CFLAGS = $(OPENCV_CFLAGS)
TORPEDOES_LFLAGS = $(OPENCV_LFLAGS)

#DROPPER = $(patsubst %,$(BUILD)/dropper/%.o,main) $(IMAGE) $(VISION) $(MODEL) $(COMMON)
#DROPPER_CFLAGS = $(OPENCV_CFLAGS)
#DROPPER_LFLAGS = $(OPENCV_LFLAGS)

EXE_NAMES = interface torpedoes vision_test

EXE = $(patsubst %,$(BIN)/%,$(EXE_NAMES))

all: $(EXE)

$(BIN)/interface: $(INTERFACE)
	$(CC) $^ $(LFLAGS) $(INTERFACE_LFLAGS) -o $@

$(BIN)/vision_test: $(VISION_TEST)
	$(CC) $^ $(LFLAGS) $(VISION_TEST_LFLAGS) -o $@

$(BIN)/pvc: $(PVC) 
	$(CC) $^ $(LFLAGS) $(PVC_LFLAGS) -o $@

$(BIN)/torpedoes: $(TORPEDOES) 
	$(CC) $^ $(LFLAGS) $(TORPEDOES_LFLAGS) -o $@

$(BUILD)/common/%.o: $(SRC)/common/%.cpp
	$(CC) $(CFLAGS) $< -o $@

$(BUILD)/model/%.o: $(SRC)/model/%.cpp
	$(CC) $(CFLAGS) $(MODEL_CFLAGS) $< -o $@

$(BUILD)/image/%.o: $(SRC)/image/%.cpp
	$(CC) $(CFLAGS) $(IMAGE_CFLAGS) $< -o $@

$(BUILD)/image_log/%.o: $(SRC)/image_log/%.cpp
	$(CC) $(CFLAGS) $(IMAGE_CFLAGS) $< -o $@

$(BUILD)/vision/%.o: $(SRC)/vision/%.cpp
	$(CC) $(CFLAGS) $(VISION_CFLAGS) $< -o $@

$(BUILD)/buoys/%.o: $(SRC)/buoys/%.cpp
	$(CC) $(CFLAGS) $(BUOYS_CFLAGS) $< -o $@

$(BUILD)/flashlight/%.o: $(SRC)/flashlight/%.cpp
	$(CC) $(CFLAGS) $(FLASHLIGHT_CFLAGS) $< -o $@

$(BUILD)/path/%.o: $(SRC)/path/%.cpp
	$(CC) $(CFLAGS) $(PATH_CFLAGS) $< -o $@

$(BUILD)/vision_test/%.o: $(SRC)/vision_test/%.cpp
	$(CC) $(CFLAGS) $(VISION_TEST_CFLAGS) $< -o $@

$(BUILD)/interface/%.o: $(SRC)/interface/%.cpp
	$(CC) $(CFLAGS) $(INTERFACE_CFLAGS) $< -o $@

$(BUILD)/camera/%.o: $(SRC)/camera/%.cpp
	$(CC) $(CFLAGS) $(CAMERA_CFLAGS) $< -o $@

$(BUILD)/torpedoes/%.o: $(SRC)/torpedoes/%.cpp
	$(CC) $(CFLAGS) $(TORPEDOES_CFLAGS) $< -o $@

$(BUILD)/pvc/%.o: $(SRC)/pvc/%.cpp
	$(CC) $(CFLAGS) $(PVC_CFLAGS) $< -o $@

#$(BUILD)/dropper/%.o: $(SRC)/dropper/%.cpp
#	$(CC) $(CFLAGS) $(DROPPER_CFLAGS) $< -o $@

clean:
	rm -f $(EXE)
	rm -f $(BUILD)/**/*.o
	rm -f $(BUILD)/*.o

