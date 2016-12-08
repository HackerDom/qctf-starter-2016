#include <iostream>
#include <vector>
#include <algorithm>
#include <assert.h>
#include <valarray>
#include <fstream>
using namespace std;

const int N = 256;
const int mod = 1 << 16;

int add(int a, int b)
{
	return (a + b) % mod;
}

valarray<int> add(valarray<int> a, valarray<int> b)
{
	assert(a.size() == b.size());
	valarray<int> result(a.size());
	for (int i = 0; i < (int)a.size(); i++)
		result[i] = add(a[i], b[i]);
	return result;
}

int mult(int a, int b)
{
	return ((long long)a * b) % mod;
}

valarray<int> mult(valarray<int> a, int b)
{
	valarray<int> result(a.size());
	for (int i = 0; i < (int)a.size(); i++)
		result[i] = mult(a[i], b);
	return result;
}

struct Random
{
	int seed;
	Random () {}
	Random (int seed_) : seed(seed_) {}
	int next()
	{
		seed = (seed * 25173 + 13849) % (1 << 16);
		return seed;
	}
};

void generateRandomMartix(Random &rnd, int matrix[N][N])
{
	for (int x = 0; x < N; x++)
	{
		for (int y = 0; y < N; y++)
		{
			matrix[y][x] = rnd.next();
		}
	}
}

void generateRandomVector(Random &rnd, int vect[N])
{
	for (int x = 0; x < N; x++)
	{
		vect[x] = rnd.next();
	}
}

void copyMatrix(int from[N][N], int to[N][N])
{
	for (int i = 0; i < N; i++)
		for (int j = 0; j < N; j++)
			to[i][j] = from[i][j];
}

void generateIdentityMatrix(int result[N][N])
{
	for (int i = 0; i < N; i++)
	{
		for (int j = 0; j < N; j++)
		{
			if (i == j)
				result[i][j] = 1;
			else
				result[i][j] = 0;
		}
	}
}

void multiplyMatrices(int a[N][N], int b[N][N], int result[N][N])
{
	int local_result[N][N];
	for (int x = 0; x < N; x++)
	{
		for (int y = 0; y < N; y++)
		{
			local_result[y][x] = 0;
			for (int i = 0; i < N; i++)
			{
				local_result[y][x] = add(local_result[y][x], mult(a[y][i], b[i][x]));
			}
		}
	}
	copyMatrix(local_result, result);
}

void multMatrixOnVector(int matrix[N][N], int vect[N], int result[N])
{
	int local_result[N];
	for (int y = 0; y < N; y++)
	{
		local_result[y] = 0;
		for (int i = 0; i < N; i++)
		{
			local_result[y] = add(local_result[y], mult(matrix[y][i], vect[i]));
		}
	}
	for (int i = 0; i < N; i++)
		result[i] = local_result[i];
}

void matrixPow(int a[N][N], int pow, int result[N][N])
{
	if (pow == 0)
	{
		generateIdentityMatrix(result);
		return;
	}
	int b[N][N];
	matrixPow(a, pow / 2, b);
	multiplyMatrices(b, b, b);
	if (pow % 2)
	{
		multiplyMatrices(b, a, b);
	}
	copyMatrix(b, result);
}

void shiftMatrixLeft(int matrix[N][N], int result[N][N])
{
	for (int y = 0; y < N; y++)
	{
		for (int x = 0; x < N - 1; x++)
			result[y][x] = matrix[y][x + 1];
	}
	for (int y = 0; y < N; y++)
		result[y][N - 1] = 0;
}

void printMatrix(int matrix[N][N])
{
	for (int y = 0; y < N; y++)
	{
		for (int x = 0; x < N; x++)
		{
			cout << matrix[y][x] << " ";
		}
		cout << endl;
	}
}

void matrixToPermutation(int matrix[N][N], int permutation[N])
{
	int xors[N];
	for (int i = 0; i < N; i++)
		xors[i] = 0;
	for (int y = 0; y < N; y++)
		for (int x = 0; x < N; x++)
			xors[x] ^= matrix[y][x];

	pair<int, int> xorsWithInds[N];
	for (int i = 0; i < N; i++)
		xorsWithInds[i] = make_pair(xors[i], i);
	
	sort(xorsWithInds, xorsWithInds + N);

	for (int i = 0; i < N; i++)
		permutation[i] = xorsWithInds[i].second;
}

void generateShiftedMatrixTop(Random rnd, int matrix[N][N])
{
	for (int x = 0; x < N; x++)
	{
		int vect[N];
		generateRandomVector(rnd, vect);
		for (int y = 0; y < N; y++)
			matrix[y][x] = 0;
		for (int y = x; y < N; y++)
		{
			matrix[y][x] = vect[y - x];
		}
	}
}

void generateShiftedMatrixBottom(Random rnd, int matrix[N][N])
{
	for (int x = 0; x < N; x++)
	{
		int vect[N];
		generateRandomVector(rnd, vect);
		for (int y = 0; y < N; y++)
			matrix[y][x] = 0;
		for (int y = 0; y < x; y++)
		{
			matrix[y][x] = vect[N - x + y];
		}
	}
}

void generateSpecialMatrix(Random rnd, int matrix[N][N])
{
	int shiftedMatrix[N][N];
	generateShiftedMatrixBottom(rnd, shiftedMatrix);
	valarray<int> vect[N];

	for (int i = 0; i < N; i++)
	{
		vect[i] = valarray<int>(N);
		vect[i][i] = 1;
		for (int j = 0; j < i; j++)
		{
			vect[i] = add(vect[i], mult(vect[j], shiftedMatrix[j][i]));
		}
	}

	for (int y = 0; y < N; y++)
	{
		for (int x = 0; x < N; x++)
		{	
			matrix[y][x] = vect[x][y];
		}
	}
}

void simple()
{
	int matrix[N][N];
	Random rnd = Random(42);
	generateRandomMartix(rnd, matrix);

	for (int i = 0; i < N; i++)
	{
		int vect[N];
		generateRandomVector(rnd, vect);
		multMatrixOnVector(matrix, vect, vect);
		shiftMatrixLeft(matrix, matrix);
		for (int j = 0; j < N; j++)
		{
			matrix[j][N - 1] = vect[j];
		}
	}

	printMatrix(matrix);
}

string getSecret(int matrix[N][N], int len)
{
	int result[N];
	for (int i = 0; i < N; i++)
		result[i] = 0;
	for (int i = 0; i < N; i++)
	{
		for(int j = 0; j < N; j++)
		{
			result[(i * N + j) % len] ^= matrix[i][j] % 256;
			result[(i * N + j) % len] ^= matrix[i][j] / 256;
		}
	}
	string str;
	for (int i = 0; i < len; i++)
		str += (char)result[i];

	return str;
}

int hexCharToInt(char a)
{
	if (a >= '0' && a <= '9')
		return a - '0';
	if (a >= 'a' && a <= 'f')
		return a - 'a' + 10;
	throw;
}

int hexToInt(string s)
{
	int result = 0;
	for (int i = 0; i < (int)s.length(); i++)
	{
		result *= 16;
		result += hexCharToInt(s[i]);
	}
	return result;
}

void getMatrixFromHexFile(string filename, int matrix[N][N])
{
	ifstream in(filename);

	string line;
	for (int i = 0; i < N; i++)
	{
		in >> line;
		for (int j = 0; j < N; j++)
		{
			matrix[i][j] = hexToInt(line.substr(j * 4, 4));
		}
	}

	in.close();
}

int main()
{
	int matrix[N][N];
	Random rnd = Random(35812);
	//generateRandomMartix(rnd, matrix);
	getMatrixFromHexFile("enc.txt", matrix);
	int special[N][N];
	generateSpecialMatrix(rnd, special);
	int top[N][N];
	generateShiftedMatrixTop(rnd, top);

	int A[N][N];
	multiplyMatrices(top, special, A);
	matrixPow(A, (1 << 30), A);

	multiplyMatrices(matrix, A, matrix);

	cout << getSecret(matrix, 35);

	//cout << "\n" << clock() * 1000 / CLOCKS_PER_SEC << " ms\n";

	return 0;
}
