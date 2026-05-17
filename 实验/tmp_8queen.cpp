#include<iostream>
using namespace std;
int a[9];
int b[9]={0};
int c[16]={0};
int d[16]={0};
int sum=0;

void printSolution()
{
    for(int i=1;i<=8;i++)
    {
        cout << a[i];
        if(i<8) cout << ' ';
    }
    cout << endl;
}

void searchh(int i)
{
    for(int j=1;j<=8;j++)
    {
        if((!b[j])&&(!c[i+j])&&(!d[i-j+7]))
        {
            a[i] = j;
            b[j] = 1;
            c[i+j] = 1;
            d[i-j+7] = 1;

            if(i == 8)
            {
                sum++;
            }
            else
            {
                searchh(i + 1);
            }

            b[j] = 0;
            c[i+j] = 0;
            d[i-j+7] = 0;
        }
    }
}

int main()
{
    searchh(1);
    cout << "sum=" << sum << endl;
    return 0;
}
