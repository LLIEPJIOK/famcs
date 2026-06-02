#pragma once
#include "RolePlayer.h"
#include <cassert>

class WizardPlayer : public RolePlayer
{
private:
    uint32_t max_mana;
    uint32_t curr_mana;
    vector<uint32_t> session;
    int size;
public:
    WizardPlayer();
    WizardPlayer(string name, Status status, Race race, bool can_move, uint32_t max_mana_,
        uint32_t curr_mana_, vector<uint32_t>& session_, int size);
    uint32_t get_max_mana();
    uint32_t get_curr_mana();
    vector<uint32_t>& get_session();
    int get_size();

    void  set_max_mana(uint32_t max_mana_);
    void set_curr_mana(uint32_t curr_mana_);
    void set_session(vector<uint32_t>& session_);
    void set_size(int size_);

    WizardPlayer& operator =(const WizardPlayer& w);
    friend ostream& operator<<(ostream& out, WizardPlayer& w);
    ~WizardPlayer() {};
};