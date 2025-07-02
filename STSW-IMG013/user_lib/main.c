#include <malloc.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

#include <unistd.h>
#include <fcntl.h>
#include <linux/i2c-dev.h>
#include <sys/ioctl.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <fcntl.h>
#include <pthread.h>

#include "VL53L1X_api.h"
#include "VL53L1X_calibration.h"
#include "vl53l1_platform.h"

int init_tof(int adapter_nr)
{
	int file = 0;
	uint8_t I2cDevAddr = 0x29;
	file = VL53L1X_UltraLite_Linux_I2C_Init(0, adapter_nr, I2cDevAddr);
	if (file == -1)
		exit(1);

	int status = 0;
	uint8_t byteData, sensorState = 0;
	uint16_t wordData;

	status = VL53L1_RdByte(0, 0x010F, &byteData);
	printf("VL53L1X Model_ID: %X\n", byteData);
	status += VL53L1_RdByte(0, 0x0110, &byteData);
	printf("VL53L1X Module_Type: %X\n", byteData);
	status += VL53L1_RdWord(0, 0x010F, &wordData);
	printf("VL53L1X: %X\n", wordData);

	while (sensorState == 0) {
		status += VL53L1X_BootState(0, &sensorState);
	}

	printf("Chip booted\n");

	status = VL53L1X_SensorInit(0);
	status += VL53L1X_SetDistanceMode(0, 1); /* 1=short, 2=long */

	return status;
}

static volatile int stop_tof_requested = 0;
static pthread_t tof_poller;
static int distance = -1;

void *poll_tof ( void *ptr ) {
	VL53L1X_StartRanging(0);

	while (!stop_tof_requested) {
		uint8_t dataReady = 0;

		VL53L1X_CheckForDataReady(0, &dataReady);
		if (dataReady) {
			VL53L1X_Result_t Results;
			VL53L1X_GetResult(0, &Results);
			distance = Results.Distance;
		}

		usleep(10000);
	}

	stop_tof_requested = 0;
	VL53L1X_StopRanging(0);
	pthread_exit( NULL );
}

int start_tof() {
	tof_poller = pthread_create( &tof_poller, NULL, poll_tof, NULL);
	return 0;
}

int stop_tof() {
	stop_tof_requested = 1;
	return 0;
}

int get_distance() {
	return distance;
}
