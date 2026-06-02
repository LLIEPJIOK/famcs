#include <iostream>
#include <fstream>
#include <algorithm>

using namespace std;

class Point3D
{
public:
	Point3D() 
	{
		x = y = z = 0;
	}
	Point3D(int _x, int _y, int _z)
	{
		x = _x;
		y = _y;
		z = _z;
	}
private:
	int x;
	int y;
	int z;
public:
	int getX()
	{
		return x;
	}	
	int getY()
	{
		return y;
	}	
	int getZ()
	{
		return z;
	}
	double getDist()
	{
		return sqrtl(x*x + y*y + z*z);
	}
};

//должен возращать true если елемент p1 в масиве должен стоять левее 
//иначе false
bool comp(Point3D& p1, Point3D& p2)
{
	if (p1.getDist() < p2.getDist())
		return false;
	if (p1.getDist() == p2.getDist())
		if (p1.getX() > p2.getX())
			return false;

	return true;
}

int main()
{
	ifstream fin;
	fin.open("in.txt");
	//проверка
	ofstream fout;
	fout.open("out.txt");
	//проверка
	int N;
	fin >> N;
	Point3D* arr = new Point3D[N];

	for (int i = 0; i < N; i++)
	{
		int a, b, c;
		fin >> a >> b >> c;
		arr[i] = Point3D(a, b, c);
	}
	
	sort(arr, arr + N, comp);

	for (int i = 0; i < N; i++)
	{
		fout << arr[i].getX() << " " << arr[i].getY() << " " << arr[i].getZ();
		if (i != N - 1)
			fout << "\n";
	}
}