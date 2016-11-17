#include <stdlib.h>
#include <iostream>
#include <iomanip>

using namespace std;


typedef struct{
    char station_name[24];
    double temperature;
} Measurement;


int main(int argc, char **argv) {
    if (argc != 2) {
        cout << "Usage: " << argv[0] << " filename" << endl;
        return 1;
    }
    
    FILE *input = fopen(argv[1], "rb");
    if (input == 0)
    {
        cout << "Problems opening the file" << endl;
        return 1;
    }
    
    fseek(input, 0, SEEK_END);
    int file_size = ftell(input);
    rewind(input);
    
    if (file_size % sizeof(Measurement) != 0) {
        cout << "The file doesn't have the required format" << endl;
        return 1;
    }
    int number_of_measurements = file_size / sizeof(Measurement);
    if (number_of_measurements > 10000) {
        cout << "Sorry, cannot handle a file that large" << endl;
        return 1;
    }
    Measurement *measurements = new Measurement[number_of_measurements];
    if (measurements == 0) {
        cout << "Unable to get enough memory" << endl;
        return 1;
    }
    
    fread(measurements, sizeof(Measurement), number_of_measurements, input);
    
    cout << "Here are your measurements:" << endl;
    for (int i = 0; i < number_of_measurements; i++) {
        cout << setiosflags(ios::left | ios::fixed) << setw(24) << setprecision(1) <<
                measurements[i].station_name << " " << measurements[i].temperature << endl;
    }
    
    delete[] measurements;
    fclose(input);
    return 0;
}