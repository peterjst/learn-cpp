#include <iostream>
#include <stdexcept>
#include <vector>
#include <string>

using namespace::std;

class Vehicle
{ 
public:
    Vehicle(string color) : color_(color)
    {
       cout << "construct vehicle" << endl;
    }
    virtual void move() = 0;
    virtual ~Vehicle()
    {
       cout << "destruct vehicle" << endl;
    }
protected:
    string color_;
};

class Car : public Vehicle
{ 
public:
    Car(string color, string type)
        : Vehicle(color),       
          type_(type)
    {
       cout << "construct car" << endl;
    }

    void move() override
    {
       cout << color_ << " " << type_ << " move" << endl;
    }

    ~Car()
    {
       cout << "destruct car" << endl;
    }

private:
    string type_;
};

class Honda : public Car
{
public:
    Honda(string color, string type, string make)
        : Car(color, type),
          make_(make)
    {
       cout << "construct honda" << endl;
    }
    void move() override
    {
        Car::move();
        cout << color_ << " Honda " << make_ << " move" << endl;
    }
    ~Honda()
    {
       cout << "destruct honda" << endl;
    }
private:
    string make_;
};

void use(Vehicle & v)
{
    v.move();
}

int main()
{
    {
        Vehicle * v = new Honda("silver", "sedan", "Accord");
        use(*v);
        delete v;
    }
    return 0;
}

