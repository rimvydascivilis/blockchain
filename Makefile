CC = g++
GO = go
CFLAGS = -Wall -std=c++2a
TARGET = main
BUILD_DIR = build
SRC_DIR = src
RM = rm -f
PYTHON = python3
 
all: $(TARGET)

release: CFLAGS += -O3
release: $(TARGET)

$(TARGET): $(BUILD_DIR) $(SRC_DIR)/$(TARGET).cpp
	$(CC) $(CFLAGS) -o $(BUILD_DIR)/$(TARGET) $(SRC_DIR)/$(TARGET).cpp

$(BUILD_DIR):
	mkdir $(BUILD_DIR)

test: release requirements functions
	$(PYTHON) test/main.py

requirements:
	$(PYTHON) -m pip install -r test/requirements.txt

functions:
	$(GO) build -o $(BUILD_DIR)/functions test/main.go

clean:
	$(RM) -r $(BUILD_DIR)