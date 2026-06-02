#include "WizardPlayer.h"
#include <algorithm>
#include <typeinfo>

int main() 
{
	setlocale(LC_ALL, ".1251");
	vector<uint32_t> temp = { 1,2,3,4,5,6 };
	WizardPlayer rp1("Эвелина", alive, elf, 1, uint32_t(100), uint32_t(58), temp, 6);
	vector<uint32_t> temp1 = { 6,5,4,3,2,1,0 };
	WizardPlayer rp2("Никита", dead, dwarf, 0, uint32_t(150), uint32_t(62), temp1, 7);
	cout << (rp1 == rp2) << "\n";
	cout << rp1;
	cout << rp2;
	rp1 = rp2;
	cout << rp1;
	system("pause");
	system("cls");

	vector <RolePlayer*> players;
	players.push_back(new WizardPlayer("Эвелина", alive, elf, 1, uint32_t(100), uint32_t(58), temp, 6));
	players.push_back(new WizardPlayer ("Никита", dead, dwarf, 0, uint32_t(150), uint32_t(62), temp1, 7));
	players.push_back(new RolePlayer("Вова", paralized, elf, 0));
	players.push_back(new RolePlayer("Антон", alive, human, 1));
	temp1 = { 45, 56543, 3456, 23, 6, 7, 4};
	players.push_back(new WizardPlayer("Даша", alive, human, 1, 100000, 100000, temp1, 7));
	players.push_back(new RolePlayer("Матвей", alive, dwarf, 1));

	sort(players.begin(), players.end(), [](RolePlayer* a, RolePlayer* b) {
		return a->get_name() < b->get_name();
		});
	for (int i = 0; i < players.size(); ++i)
	{
		if (typeid(*players[i]) == typeid(RolePlayer))
		{
			std::cout << *players[i] << '\n';
			continue;
		}
		std::cout << *(dynamic_cast<WizardPlayer*>(players[i])) << '\n';
	}

	int role_counter = count_if(players.begin(), players.end(), [](RolePlayer* a) {
		return typeid(*a) == typeid(RolePlayer);
		});

	int wizard_counter = count_if(players.begin(), players.end(), [](RolePlayer* a) {
		return typeid(*a) != typeid(RolePlayer);
		});

	std::cout << "\nRolePlayers - " << role_counter << '\n';
	std::cout << "WizardPlayer - " << wizard_counter << "\n\n";

	bool flag = 0;
	for (const auto& i : players)
	{
		if (!flag && typeid(*i) == typeid(WizardPlayer) && dynamic_cast<WizardPlayer*>(i)->get_curr_mana() < 100)
		{
			flag = 1;
			std::cout << "Объекты, у которых текущее значение маны меньше 100:\n";
		}
		if (typeid(*i) == typeid(WizardPlayer) && dynamic_cast<WizardPlayer*>(i)->get_curr_mana() < 100)
			std::cout << *dynamic_cast<WizardPlayer*>(i);
	}
	if (!flag)
		std::cout << "Нет таких объектов\n";
	for (int i = 0; i < players.size(); ++i)
		delete players[i];
	return 0;
}