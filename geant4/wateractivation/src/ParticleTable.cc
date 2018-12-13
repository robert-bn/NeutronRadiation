#include "ParticleTable.hh"

ParticleTable::ParticleTable()
{ }

ParticleTable::~ParticleTable()
{ }

ParticleTable ParticleTable::operator+(ParticleTable const& b) const
{
    // addition
    ParticleTable merged(*this);
    for(auto pair : b){
        merged[pair.first] += pair.second;
    }
    return merged;
}

void ParticleTable::operator+=(ParticleTable const& b)
{
    // addition equality
    for(auto pair : b){
        (*this)[pair.first] += pair.second;
    }
}

ParticleTable ParticleTable::operator*(ParticleTable const& b) const
{
    // Compiler breaks unless * operator is defined
    // Why? Just Why.
    ParticleTable merged(*this);
    for(auto pair : b){
        merged[pair.first] += pair.second;
    }
    return merged;
}

ParticleTable operator*(const ParticleTable& a, const ParticleTable& b){
    // Why? Just Why.
    ParticleTable merged(a);
    for(auto pair : b){
        merged[pair.first] += pair.second;
    }
    return merged;
}
