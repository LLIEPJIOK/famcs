#include "RolePlayer.h"

int RolePlayer::next = 1;
RolePlayer::RolePlayer() : race(human), ID(next++) {
    name = "";
    status = alive;
    can_move = true;
}
RolePlayer::RolePlayer(string name, Status status, Race _race, bool can_move) : race(_race), ID(next++) {
    this->name = name;
    this->status = status;
    this->can_move = can_move;
}
int RolePlayer::get_ID() { return ID; }
string RolePlayer::get_name() { return name; }
Status RolePlayer::get_status() { return status; }
Race RolePlayer::get_race() { return race; }
bool RolePlayer::get_can_move() { return can_move; }

void RolePlayer::set_name(string name) { this->name = name; }
void RolePlayer::set_status(Status status) { this->status = status; }
void RolePlayer::set_can_move(bool b) { can_move = b; }
const RolePlayer& RolePlayer::operator = (const RolePlayer& rp) {
    name = rp.name;
    status = rp.status;
    can_move = rp.can_move;
    return *this;
}
bool RolePlayer::operator ==(const RolePlayer& rp) {
    return (rp.can_move == can_move && rp.name == name && rp.race == race && rp.status == status);
}
ostream& operator << (ostream& out, const RolePlayer& rp) {
    out << "Раса: ";
    if (rp.race == human)
        out << "Человек\n";
    else if (rp.race == elf)
        out << "Эльф\n";
    else
        out << "Гном\n";
    out << "ID: " << rp.ID << "\n"
        << "Имя: " << rp.name << "\n"
        << "Состояние: ";
    if (rp.status == alive)
        out << "Живой\n";
    else if (rp.status == dead)
        out << "Мёртвый\n";
    else
        out << "Парализован\n";
    out << "Возможность двигаться: ";
    if (rp.can_move)
        out << "Может\n";
    else
        out << "Не может\n";
    return out;
}