#include <iostream>
#include <stdexcept>
#include <vector>

using namespace::std;

struct box
{
    box(int b, int a) : a_(a), b_(b)
    { }

    int a_;
    int b_;
    int c_ = 11;
};

int main()
{
    box b = {4, 5};
    cout << "a: " << b.a_ << endl;
    cout << "b: " << b.b_ << endl;
    cout << "c: " << b.c_ << endl;
    return 0;
}
