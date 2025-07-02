CC ?= gcc

INC_CFLAGS=-I.
CORE=core
# -fPIC is required to deal with the globals that the driver uses
CFLAGS+=$(INC_CFLAGS) -I$(CORE) -Wall -g -D_LINUX_  -fPIC

ifdef POLLING
	CFLAGS+=-D POLLING
endif

MAIN_OBJ = main.o
CORE_OBJ =  $(CORE)/VL53L1X_api.o  \
 		$(CORE)/VL53L1X_calibration.o
PLTF_OBJ =  vl53l1_linux_platform.o

%.o: %.c
	$(CC) ${LDFLAGS} -c -o $@ $< $(CFLAGS)


tof: $(CORE_OBJ) $(PLTF_OBJ) $(MAIN_OBJ)
	$(CC) ${LDFLAGS} -o $@ $^ $(CFLAGS) -lpthread

libtof: $(CORE_OBJ) $(PLTF_OBJ) $(MAIN_OBJ)
	$(CC) ${LDFLAGS} -shared -o $@.so $^ $(CFLAGS) -lpthread 

clean:
	find . -name "*.o" | xargs rm -f
	rm -f app ultra_lite
