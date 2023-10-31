from typing import Dict, List, Optional, Self


from pydantic import BaseModel, Field
from uuid import UUID, uuid4

def str_uuid4() -> str:
    return str(uuid4())

class TwinoidUserStat(BaseModel):
    name: str
    rare: int
    description: Optional[str] = None
    score: int
    id: str

class TwinoidUserAchievement(BaseModel):
    date: str
    name: str
    stat: str
    npoints: float
    description: Optional[str] = None
    points: int
    score: int
    id: str

class MushSeason(BaseModel):
    desc: str
    picto: str
    options: List[str]
    id: int
    start: str
    publicName: str

class MushGroup(BaseModel):
    desc: str
    name: str
    banner: Optional[str] = None
    avatar: Optional[str] = None
    id: int
    xp: int
    triumphRemap: Optional[str] = None
    creation: str
    domain: str
    resultDesc: str
    invests: int

class MushUserHistoryShip(BaseModel):
    conf: int
    counter_all_spore: int
    counter_explo: int
    counter_hunter_dead: int
    counter_mushes: int
    counter_planet_scanned: int
    counter_projects: int
    counter_rebel_bases: int
    counter_research: int
    creationDate: str
    deathCycle: int
    destructionDate: str
    group: Optional[MushGroup] = None
    id: int
    pilgredDone: bool
    projects: List[str]
    researches: List[str]
    season: Optional[MushSeason] = None
    shipId: int
    triumphRemap: Optional[str] = None

class MushUserHistoryHero(BaseModel):
    charId: Optional[int] = None
    date: str
    deathCycle: int
    deathId: int
    deathLocation: int
    epitaph: str
    group: Optional[MushGroup] = None
    heroId: int
    log: List[str]
    rank: int
    season: Optional[MushSeason] = None
    shipId: int
    skillList: List[str]
    triumph: int
    user: Dict[str, int]
    wasMush: bool

    @staticmethod
    def from_history_hero_data(history_hero_data: dict) -> Self:
        if history_hero_data["group"] is None or history_hero_data["group"] == {}:
            history_hero_data["group"] = None
        if history_hero_data["season"] is None or history_hero_data["season"] == {}:
            history_hero_data["season"] = None

        return MushUserHistoryHero(**history_hero_data)

class MushUserCharacterLevel(BaseModel):
    name: str
    level: int

class LegacyUser(BaseModel):
    id: str = Field(default_factory=str_uuid4)
    twinoid_id: int
    twinoid_username: str
    stats: List[TwinoidUserStat]
    achievements: List[TwinoidUserAchievement]
    history_ships: List[MushUserHistoryShip]
    history_heroes: List[MushUserHistoryHero]
    available_experience: int
    character_levels: Optional[List[MushUserCharacterLevel]] = None
    klix: Optional[int] = None
    skins: Optional[List[str]] = None
    flairs: Optional[List[str]] = None