/*********************************************************************************/
/* (C) 2001-2016 Altera Corporation. All rights reserved.                        */
/* Your use of Altera Corporation's design tools, logic functions and other      */
/* software and tools, and its AMPP partner logic functions, and any output      */
/* files any of the foregoing (including device programming or simulation        */
/* files), and any associated documentation or information are expressly subject */
/* to the terms and conditions of the Altera Program License Subscription        */
/* Agreement, Altera MegaCore Function License Agreement, or other applicable    */
/* license agreement, including, without limitation, that your use is for the    */
/* sole purpose of programming logic devices manufactured by Altera and sold by  */
/* Altera or its authorized distributors.  Please refer to the applicable        */
/* agreement for further details.                                                */
/*********************************************************************************/

/*********************************************************************************/
/* INCLUDE FILES                                                                 */
/*********************************************************************************/

#include <string.h>
#include <stdlib.h>

#include "rte_qosdev.h"
#include "dynamic_pf_app.h"
#include "dynamic_plat_reg.h"

#include <stdio.h>
#include <unistd.h>
#include <stdint.h>
#include <sys/mman.h>
#include <fcntl.h>

/********************************************************************************/
/* Global Variables  & Memories                                                 */
/********************************************************************************/
struct rte_qosdev_cap_s         returned_qos_cap;
u8*                                             mmap_ptr[6] = { NULL,     NULL,    NULL,    NULL,    NULL,    NULL };
u32                                             mmap_sz[6] = { 0x8000000 , 0,       0,       0,       0,       0 };

/********************************************************************************/
/* Main                                                                         */
/********************************************************************************/

int main(int argc, char* argv[])
{
	int         rc = 0, fd = 0, i, tc_num = 0;
	unsigned    j;

	struct rte_qosdev_sched_shap_cfg_s             *layer0_sched = NULL;
	struct rte_qosdev_sched_shap_cfg_s             *layer1_sched = NULL;
	struct rte_qosdev_sched_shap_cfg_s             *layer2_sched = NULL;
	struct rte_qosdev_cngst_cntrl_queue_profile_s  *cngst_cntrl_profiles = NULL;
	//struct rte_qosdev_cap_s                        qos_cap;

	const char* name = "/dev/alt_pf";
	if (argc > 1)
	{
		name = argv[1];
		fprintf(stderr, "Using device %s\n", name);
	}
	else
	{
		fprintf(stderr, "No device selected, using default %s\n", name);
	}

	printf("HW QOS Device Driver\n");
	//initialise hwif.

	fprintf(stderr, "\nOpening '%s'...\n", name);

	/* Open the /dev/uio0 file */
	fd = open(name, O_RDWR);

	if (fd < 1)
	{
		fprintf(stderr, "Unable to open '%s'\n", name);

		return -1;
	}

	fprintf(stderr, "Mapping regions...\n");

	for (j = 0; j < sizeof(mmap_ptr) / sizeof(u8*); ++j)
	{
		if (mmap_sz[j] == 0)
		{
			continue;
		}

		mmap_ptr[j] = (u8*)mmap(NULL, mmap_sz[j], PROT_READ | PROT_WRITE, MAP_SHARED, fd, j);

		if (mmap_ptr[j] == MAP_FAILED)
		{
			fprintf(stderr, "Unable to mmap '%s', region %d\n", name, j);

			close(fd);

			return -1;
		}
	}
	printf("Connected to HW\n");
	printf("HW QOS Initilize basic configuration\n");

	fd = rte_qosdev_init();
	if (fd < 0) {
		printf("[rte_qosdev_init]: rte_qosdev_hwif_init returend an error code of (%d)!\n", fd);
		rc = -1;
		return rc;
	}

	printf("\nHW Acc PoC FPGA Version: %08x\n\n", dynamic_get_fpga_version());

#ifdef ALT_QOS_ON

/*
Building the following QoS structure:

                                                               |
                                                              40G
                                                               |
  Layer 2          1                                         Sch0                              Max of 4K inputs
  (Port Layer)                                                 |
                                               ---WRR--------------WRR----------
                                              /          |                      \
                                           8M W1       8M W1                   8M W1
                                             |           |                       | 
  Layer 1       4000                       Sch0        Sch1        .....       Sch 3999        Fixed 8 inputs
                                             |           |                       |
                                       ---SP--          -----SP---               -----SP-----
                                      /       \         |         \               |          \
                                  Max W1   Max W1      Max W1    Max W1         Max W1     Max W1
                                     |        |           |         |   .....     |           |
  Layer 0       8000               Sch 0     Sch 1       Sch2     Sch 3        Sch 7998    Sch 7999
  Queue Layer
  One profile with 2 thresholds is used for all queues (High = 0x18, Low = 0x18)
*/
	{
		//Create 8000 queue layer shapers, this should probably be part of the Init sequece!
		int n = returned_qos_cap.sched_shap_cap.num_of_schedulers[0];
		layer0_sched = (struct rte_qosdev_sched_shap_cfg_s*)malloc(n * sizeof(struct rte_qosdev_sched_shap_cfg_s));

		for (i = 0; i < n; i++) {
			struct rte_qosdev_sched_shap_cfg_s *p = &layer0_sched[i];

			p->inputs_active = 1;
			p->inputs_weights = 0; // N/A
			p->inputs_pir = 0; // N/A
			p->algorithm = returned_qos_cap.sched_shap_cap.layer_algorithm[0];
		}
	}

	{
		//Create 4000 queue layer shapers with 2 inputs, Max BW Shaping SP!
		int n = returned_qos_cap.sched_shap_cap.num_of_schedulers[1];
		layer1_sched = (struct rte_qosdev_sched_shap_cfg_s*)malloc(n * sizeof(struct rte_qosdev_sched_shap_cfg_s));

		for (i = 0; i < n; i++) {
			struct rte_qosdev_sched_shap_cfg_s *p = &layer1_sched[i];

			p->inputs_active = returned_qos_cap.sched_shap_cap.num_of_schedulers[0] / returned_qos_cap.sched_shap_cap.num_of_schedulers[1];
			p->inputs_weights = 1;
			p->inputs_pir = 0xf3ff; // MAX BW
			p->algorithm = returned_qos_cap.sched_shap_cap.layer_algorithm[1];
		}
	}

	{
		//Create 1 Port layer shaper with 40G
		int n = returned_qos_cap.sched_shap_cap.num_of_schedulers[2];
		layer2_sched = (struct rte_qosdev_sched_shap_cfg_s*)malloc(n * sizeof(struct rte_qosdev_sched_shap_cfg_s));


                /*********************** ADD PART BY LITIANQI ******************************************/
		int pir[n];
		{
			//read sh_pir.csv file
			FILE *fp;
			char temp_pir[n][20];

			//read csvfile line by line
			fp = fopen("sh_pir.csv", "r");
			for(int i = 0; i < n; i++) {
				fgets(temp_pir[i], 20, fp);
			}
			fclose(fp);

			//transform string to int
			for(int i = 0; i < n; i++) {
				sscanf(temp_pir[i], "%x", &pir[i]);
			}
		}
		/*************************** ADD END *************************************************************/


		for (i = 0; i < n; i++) {
			struct rte_qosdev_sched_shap_cfg_s *p = &layer2_sched[i];

			p->inputs_active = returned_qos_cap.sched_shap_cap.num_of_schedulers[1] / returned_qos_cap.sched_shap_cap.num_of_schedulers[2];
			p->inputs_weights = 1;

		/***************************** CHANGE PART BY LITIANQI *******************************************/
			//assignment from array pir[]
			p->inputs_pir = pir[i];

			//p->inputs_pir = 0x13e8; //8Mbit/sec
		/******************************* CHANGE END ******************************************************/
			p->algorithm = returned_qos_cap.sched_shap_cap.layer_algorithm[2];
		}
	}

	{
		//Create 1 Congestion Control Profile
		int n = CNGST_NUM_OF_PROFILES;
		cngst_cntrl_profiles = (struct rte_qosdev_cngst_cntrl_queue_profile_s*)malloc(n * sizeof(struct rte_qosdev_cngst_cntrl_queue_profile_s));
		for (i = 0; i < n; i++) {
			struct rte_qosdev_cngst_cntrl_queue_profile_s *p = &cngst_cntrl_profiles[i];

			p->threshold_low = 0x18;
			p->threshold_high = 0x18;
		}
	}


	print_qos_capabilities(&returned_qos_cap, POL_ENABLED, CNGST_ENABLED, SCHED_ENABLED);

	printf("Running an Initialization Script. \n\n");

	printf("Configuring Layer 1, %d shapers\n", returned_qos_cap.sched_shap_cap.num_of_schedulers[1]);
	for (i = 0; i < (returned_qos_cap.sched_shap_cap.num_of_schedulers[1]); i++) {
		rc = rte_qosdev_sched_shap_cfg_set(1, i, layer1_sched);
		if (rc < 0) {
			printf("[main]: rte_qosdev_shap_cfg_input_pir_set returned an error code of (%d)\n", rc);
			goto __dynamic_pf_app_exit;
		}
	}
	printf("\nDone\n");
	
	printf("Configuring Port Layer, %d shapers, %d inputs\n", returned_qos_cap.sched_shap_cap.num_of_schedulers[2], returned_qos_cap.sched_shap_cap.num_of_schedulers[1]);
	for (i = 0; i < (returned_qos_cap.sched_shap_cap.num_of_schedulers[2]); i++) {
		rc = rte_qosdev_sched_shap_cfg_set(2, i, layer2_sched);
		if (rc < 0) {
			printf("[main]: rte_qosdev_shap_cfg_input_pir_set returned an error code of (%d)\n", rc);
			goto __dynamic_pf_app_exit;
		}
	}
	printf("\nDone\n");

	printf("Map between Layer 1, %d nodes and Port Layer %d inputs\n", returned_qos_cap.sched_shap_cap.num_of_schedulers[1], returned_qos_cap.sched_shap_cap.num_of_schedulers[1]);
	for (i = 0; i < (returned_qos_cap.sched_shap_cap.num_of_schedulers[1]); i++) {
		rc = rte_qosdev_sched_map_set(1, i, 0); //Layer 1 node i to Layer 2 node 0 input i
		if (rc < 0) {
			printf("[main]: rte_qosdev_shap_cfg_input_pir_set returned an error code of (%d)", rc);
			goto __dynamic_pf_app_exit;
		}
	}
	printf("\nDone\n");

	
	printf("Configure %d Profiles\n", returned_qos_cap.cngst_cntrl_cap.num_of_queue_profiles);
	for (i = 0; i < (returned_qos_cap.cngst_cntrl_cap.num_of_queue_profiles); i++) {
		//altera_message_print(&hpe_pf_app_message_id, ALTERA_MESSAGE_ALL, "Configure Profile %d\n", i);
		rc = rte_qosdev_cngst_cntrl_queue_profile_set(0, cngst_cntrl_profiles); //Configure profile ID 0
		if (rc < 0) {
			printf("[main]: rte_qosdev_cngst_cntrl_queue_profile_set returned an error code of (%d)", rc);
			goto __dynamic_pf_app_exit;
		}
	}
	printf("\nDone\n");

	tc_num = returned_qos_cap.sched_shap_cap.num_of_schedulers[0] / returned_qos_cap.sched_shap_cap.num_of_schedulers[1];
	printf("Map %d Queues to Profile 0 using %d TCs.\n", returned_qos_cap.cngst_cntrl_cap.number_of_queues, tc_num);
	for (i = 0; i < (returned_qos_cap.cngst_cntrl_cap.number_of_queues/tc_num); i++) {
		//altera_message_print(&hpe_pf_app_message_id, ALTERA_MESSAGE_ALL, "Map Queues %d to Profile 0\n",i);
		//Queue IDs are assigned per TC, in general there are 32K Queues for 4K schedulers, we are only using 8K
		//2 for each scheduler, the complicated equesion is only in order to set TC0 and TC1 for every scheduler
		// setting up queues 0,1, 8,9, 16,17 and so on.
		// assigning a profile to each TC
		rc = rte_qosdev_cngst_contrl_queue_profile_assignment_set((i*8)+0, 0); //Map all queues TC 0 to profile ID 0
		rc = rte_qosdev_cngst_contrl_queue_profile_assignment_set((i*8)+1, 0); //Map all queues TC 1 to profile ID 0
		//rc = rte_qosdev_cngst_contrl_queue_profile_assignment_set((i*8)+2, 0); //Map all queues TC 2 to profile ID 0
		//rc = rte_qosdev_cngst_contrl_queue_profile_assignment_set((i*8)+3, 0); //Map all queues TC 3 to profile ID 0
		if (rc < 0) {
			printf("[main]: rte_qosdev_cngst_contrl_queue_profile_assignment_set returned an error code of (%d)", rc);
			goto __dynamic_pf_app_exit;
		}
	}
	printf("\nDone\n");

	//read_mac_stats(PLAT_MAC0_OFFST, "MAC 0");

	
#endif

	printf("HW QOS Device Driver\n");
	printf("[rte_qosdev_init] Driver Initilized!\r\n");


	
__dynamic_pf_app_exit:

	//close hwif.
	for (j = 0; j < sizeof(mmap_ptr) / sizeof(u8*); ++j)
	{
		if (mmap_sz[j] == 0)
		{
			continue;
		}

		munmap(mmap_ptr[j], mmap_sz[j]);
	}

	close(fd);

	printf("Done\n\n");

	return rc;

}




//HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
//HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH Supporting Functions HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH
//HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH

void  flush_screen(void) {

#ifdef _WIN32

	DWORD written;
	COORD curhome = { 0,0 };
	DWORD N;
	HANDLE hndl = GetStdHandle(STD_OUTPUT_HANDLE);
	CONSOLE_SCREEN_BUFFER_INFO csbi;

	GetConsoleScreenBufferInfo(hndl, &csbi);
	N = csbi.dwSize.X * csbi.dwCursorPosition.Y +
		csbi.dwCursorPosition.X + 1;

	FillConsoleOutputCharacter(hndl, ' ', N, curhome, &written);
	csbi.srWindow.Bottom -= csbi.srWindow.Top;
	csbi.srWindow.Top = 0;
	SetConsoleWindowInfo(hndl, TRUE, &csbi.srWindow);
	SetConsoleCursorPosition(hndl, curhome);

#else
	system("clear");
#endif
}
/********************************************************************************/
/* EOF                                                                          */
/********************************************************************************/



