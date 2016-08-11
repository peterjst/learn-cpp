#include <iostream>
#include <stdexcept>
#include <vector>

using namespace::std;

int main()
{
    vector<int> v;

    try {
        cout<< v.at(20) << endl;
    }
    catch (out_of_range) {
       cout << "out of range!";
    }
    return 0;
}
