#include <stdio.h>
#include <stdlib.h>
#include <pcap/pcap.h>

int main (int argc, char* argv[])
{
    /* the error code buf of libpcap, PCAP_ERRBUF_SIZE = 256 */
    char ebuf[PCAP_ERRBUF_SIZE];
    char *dev;
    int pcap_loop_ret;

    /* grab a device to peak into */
    dev = pcap_lookupdev(ebuf);
    if(dev == NULL) {
        /* e.g. "no suitable device found" */
        printf("pcap_lookupdev error: %s\n", ebuf);
        return 1;
    } else {
        printf("pcap_lookupdev returned: %s\n", dev);
        return 0;
    }
}
