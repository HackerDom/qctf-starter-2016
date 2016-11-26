#include <cstdio>
#include <cstring>
#include <cstdlib>


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


bool valid_string( char *p )
{
    while( *p != '\0' )
    {
        if( *p > 'Z' || *p < 'A' )
            return false;
        p++;
    }
    return true;
}

bool valid_hex( char *p )
{
    while ( *p != '\0' )
    {
        if( ! ( ('0' <= *p && *p <= '9') || ('A' <= *p && *p <= 'F') ) )
            return false;
        p++;
    }
    return true;
}


int main()
{
    int username_length;
    char username[128];
    char parts[4][16];
    unsigned int check;
    unsigned long long t;

    printf("Enter your identificator: ");
    scanf("%100s", username);
    username_length = strlen(username);
    
    if(username_length < 16)
    {
        puts("Identificator too short!");
        return -1;
    }
    
    printf("Enter you key: ");
    scanf("%4s_%15s_%15s_%4s", parts[0], parts[1], parts[2], parts[3]);
    
    // check part 0
    if ( strcmp( parts[0], "QCTF" ) != 0 )
        goto ERROR; 
    

    // check part 1
    if ( !valid_string( parts[1] ) )
        goto ERROR;

    t = 0;
    for ( int i = 0; i < 15; i++ )
    {
        t *= 20;
        t += (unsigned long long)(parts[1][i] - 'A');
    }
    
    if ( t != *(unsigned long long *)username )
        goto ERROR;


    // check part 2    
    if ( !valid_string( parts[2] ) )
        goto ERROR;

    t = 0;
    for ( int i = 0; i < 15; i++ )
    {
        t *= 20;
        t += (unsigned long long)(parts[2][i] - ('Z' - 19));
    }
    
    if ( t != *(unsigned long long *)(username + 8) )
        goto ERROR;


    // check part 3
    if ( !valid_hex( parts[3] ) )
        goto ERROR;

    check = strtoul(parts[3], NULL, 16);
    if ( check != checksum(username, username_length) )
        goto ERROR;

    puts("ACCESS GRANTED!");    
    return 0;

ERROR:
    puts("ACCESS DENIED!");
    return -1;

}
