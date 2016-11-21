#include <cstdio>
#include <cstring>
#include <cstdlib>


const int MIN_LENGTH = 16;
const int BASE = 20;
const int BLOCKS_LEN = 15;
const int BLOCK_SHIFT[] = {'A', 'Z' - BASE + 1};



unsigned int checksum ( char *addr, int count )
{
    /* Compute Internet Checksum for "count" bytes
     *         beginning at location "addr".
     */
    unsigned int sum = 0;

    while ( count > 1 )  {
        /*  This is the inner loop */
        sum += *(unsigned short *) addr;
        addr += 2;
        count -= 2;
    }

    /*  Add left-over byte, if any */
    if ( count > 0 )
        sum += *(unsigned char *) addr;

    /*  Fold 32-bit sum to 16 bits */
    while (sum>>16)
        sum = (sum & 0xffff) + (sum >> 16);
    
    return (~sum) & 0xffff;
}



int main()
{
    int username_length;
    char username[128], block[2][16];
    unsigned long long parts[2];    

    printf("Enter your identificator: ");
    scanf("%100s", username);
    username_length = strlen(username);
    
    if(username_length < MIN_LENGTH)
    {
        puts("Identificator too short!");
        return -1;
    }

    parts[0] = *((unsigned long long *)(username));
    parts[1] = *((unsigned long long *)(username + 8));
    memset(block, 0, sizeof(block));
  

    for(int k = 0; k < 2; k++)
    {
        for(int i = BLOCKS_LEN - 1; i >= 0; i--)
        {
            block[k][i] = BLOCK_SHIFT[k] + parts[k] % BASE;
            parts[k] /= BASE;
        }
    }
    printf("You key is: QCTF-%s-%s-%04X\n", block[0], block[1], checksum(username, username_length));
    
}
