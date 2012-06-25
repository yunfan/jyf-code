#include <stdio.h>
#include <fcntl.h>
#include <unistd.h>
#include <signal.h>
#include <sys/stat.h>
#include <linux/kd.h>
#include <sys/types.h>
#include <sys/ioctl.h>

#define ERROR -1

int main(void){
    int fd,i;
    int usec,statu;

    usec=500000;
    statu=0x7;
    
    fd = opendevice();
    
    for(i=1;i<10;i++){
        usleep(usec);

        ioctl(fd, KDSETLED, statu);

        usleep(usec);

        ioctl(fd , KDSETLED , 0x0);
    }

    close(fd);
    return 0;
}

int opendevice(){
    int fd;
    
    if( (fd = open("/dev/console" , O_NOCTTY)) == ERROR ){
        perror("open");
        exit(ERROR);
    }

    return fd;
}
