#pragma once
#include <string>
#include <iostream>
#include <vector>

enum Status { paralized, dead, alive };
enum Race { elf, human, dwarf };
using namespace std;
class RolePlayer
{
protected:
	const int ID;
	static int next;
	string name;
	Status status;
	const Race race;
	bool can_move;
public:
	RolePlayer();
	RolePlayer(string name, Status status, Race race, bool can_move);
	int get_ID();
	string get_name();
	Status get_status();
	Race get_race();
	bool get_can_move();

	void set_name(string name);
	void set_status(Status status);
	void set_can_move(bool b);
	const RolePlayer& operator = (const RolePlayer& rp);
	bool operator ==(const RolePlayer& rp);
	friend ostream& operator << (ostream& out, const RolePlayer& rp);
	virtual ~RolePlayer() {}
};