#include <stdlib.h>
#include <stdio.h>

typedef struct{
    char station_name[24];
    double temperature;
} Measurement;

int main(int argc, char **argv) {
    if (argc != 2) {
        printf("Usage: %s filename", argv[0]);
        return 1;
    }
    
    FILE *input = fopen(argv[1], "r");
    if (input == 0)
    {
        printf("Problems opening the file\n");
        return 1;
    }
    
    fseek(input, 0, SEEK_END);
    int file_size = ftell(input);
    rewind(input);
    
    if (file_size % sizeof(Measurement) != 0) {
        printf("The file doesn't have the required format\n");
        return 1;
    }
    int number_of_measurements = file_size / sizeof(Measurement);
    if (number_of_measurements > 10000) {
        printf("Sorry, cannot handle a file that large\n");
        return 1;
    }
    Measurement *measurements = malloc(number_of_measurements * sizeof(Measurement));
    if (measurements == 0) {
        printf("Unable to get enough memory\n");
        return 1;
    }
    
    int read = fread(measurements, sizeof(Measurement), number_of_measurements, input);
    
    printf("Here are your measurements:\n");
    for (int i = 0; i < number_of_measurements; i++) {
        printf("%-24s %.01f\n", measurements[i].station_name, measurements[i].temperature);
    }
    
    free(measurements);
    fclose(input);
    return 0;
}