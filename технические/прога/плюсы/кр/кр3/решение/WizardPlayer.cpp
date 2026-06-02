#include "WizardPlayer.h"

WizardPlayer::WizardPlayer() :RolePlayer()
{
    max_mana = 0;
    curr_mana = 0;
    size = 0;
}

WizardPlayer::WizardPlayer(string name, Status status, Race race, bool can_move, uint32_t max_mana_,
    uint32_t curr_mana_, vector<uint32_t>& session_, int size_) :RolePlayer(name, status, race, can_move)
{
    max_mana = max_mana_;
    curr_mana = curr_mana_;
    session = session_;
    assert(size_ == session_.size());
    assert(size_ <= 12);
    size = size_;
}

uint32_t WizardPlayer::get_max_mana()
{
    return max_mana;
}

uint32_t WizardPlayer::get_curr_mana()
{
    return curr_mana;
}

vector<uint32_t>& WizardPlayer::get_session()
{
    return session;
}

int WizardPlayer::get_size()
{
    return size;
}

void WizardPlayer::set_max_mana(uint32_t max_mana_)
{
    max_mana = max_mana_;
    if (curr_mana > max_mana_)
        curr_mana = max_mana_;
}

void WizardPlayer::set_curr_mana(uint32_t curr_mana_)
{
    assert(curr_mana_ <= max_mana);
    curr_mana = curr_mana_;
}

void WizardPlayer::set_session(vector<uint32_t>& session_)
{
    assert(session_.size() <= 12);
    session = session_;
}

void WizardPlayer::set_size(int size_)
{
    assert(size_ <= 12);
    size = size_;
}

WizardPlayer& WizardPlayer::operator=(const WizardPlayer& w)
{
    RolePlayer::operator=(w);
    max_mana = w.max_mana;
    curr_mana = w.curr_mana;
    session = w.session;
    size = w.size;
    return *this;
}

ostream& operator<<(ostream& out, WizardPlayer& w)
{
    out << *dynamic_cast<RolePlayer*>(&w);
    out << "Максимальная мана : " << w.max_mana << endl;
    out << "Текущая мана : " << w.curr_mana << endl;
    out << "Размер массива : " << w.size << endl;
    for (int i = 0; i < w.session.size(); i++)
        out << "Кол-во м/c в месяце " << i + 1 << " = " << w.session[i] << endl;
    return out;
}