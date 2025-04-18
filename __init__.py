"""
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
(C) Andirz Object Tuning Replacement Script for Sims 4
Homepage: https://andirz.itch.io/
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Licensed under CC-BY-NC-ND 4.0
Do not copy or use this code without the author's permission.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
"""

from objects.definition import Definition
import objects.components.live_drag_component
from sims4.common import Pack, is_available_pack

from andirz_object_tuning_replacement.injector import inject_to
from andirz_object_tuning_replacement.logger import Logger

SCRIPT_CREATOR = 'Andirz'
SCRIPT_NAME = 'Object Tuning Replacement Script'
SCRIPT_VERSION = '1.0.0'

LOG_FILE = f"{SCRIPT_CREATOR}_{SCRIPT_NAME.replace(' ', '')}.log"
LOG_TITLE = f"{SCRIPT_CREATOR} {SCRIPT_NAME} Log v.{SCRIPT_VERSION}"

log = Logger(filename=LOG_FILE, title=LOG_TITLE, force_simple_log=False, debug=False)

# ========================== OBJECT DEFINITIONS =============================
# Reminder: in range, the last number is not included, but the first one is.

def dict_to_tuple(d):
    return tuple(obj_id for group in d.values() for obj_id in group)

DINING_CHAIR = {
    'BG_DINING_CHAIR_TK1': tuple(range(12753, 12756)),  # sitDiningTK_01
    'BG_DINING_CHAIR_TK2': tuple(range(53000, 53045, 2)),  # sitDiningTK_01
    'SP08_DINING_CHAIR_WOOD': tuple(range(124393, 124418, 2)),  # sitDining_SP08WOODcurved
}

FOLDING_CHAIR = {
    'EP03_FOLDING_CHAIR': tuple(range(121671, 121688, 2)),  # sitDining_EP03METALfolding
    'EP06_DIRECTOR_CHAIR': tuple(range(200755, 200762)),    # sitDining_EP06GENdirector
    'EP15_PLASTIC_CHAIR': tuple(range(370039, 370053)),  # sitDining_EP15SEAplastic
    'EP16_FOLDING_CHAIR': tuple(range(396565, 396577)),  # sitDining_EP16GENfolding
    'SP33_FOLDING_CHAIR': tuple(range(311882, 311893)),  # sitDining_SP33GENfold
    'SP12_DIRECTOR_CHAIR': tuple(range(171898, 171910)),    # object_sitLiving_SP12GENdirector
}

LAMP_TABLE = {
    'BG_LIGHT_KID_01': (23418, 23420, 23423),  # lightTableKID_01
    'BG_LIGHT_KID_02': (29703, 29704, 29705),  # lightTableKID_02
    'BG_LIGHT_GEN_03': (30745, 30746, 30747, 32128, 32129),  # lightTableGEN_03
    'BG_LIGHT_BBY_PANDA': (37233, 37234, 37235),  # lightTableBBYPanda_01
    'BG_LIGHT_KID_ROBOT': (37237, 37238, 37239),  # lightTableKIDRobot_01
    'BG_LIGHT_BOOMERANG': (61837, 47853, 47854, 47855),  # lightTableCLBoomerang_01
    'BG_LIGHT_SPY': (27911, 27938, 27940),  # lightTableRWSpy_01
    'EP01_LIGHT_BRASS': tuple(range(78904, 78920, 2)),  # lightTableMedium_EP01GENbrass
    'EP03_LIGHT_FLEA_MARKET': (127428, 132452, 132453, 132454),  # lightTableGEN_03_EP03GENfleaMarket
    'EP12_LIGHT_DECO_BULB': tuple(range(295602, 295608)) + tuple(range(305731, 305734)),  # lightTable_EP12DECObulb
    'SP16_LIGHT_SMALL': tuple(range(238712, 238722)),  # lightTableSmall_SP16GEN
}

SP33_PILLOW = tuple(range(313185, 313197))  # objectPillow_SP33GEN
SP33_TABLE = tuple(range(311906, 311915))   # objectTableDining_SP33GEN
SP33_TENT = tuple(range(313261, 313268))    # objectTent_SP33GEN

BG_SCULPTURE_RABBIT_CERAMIC = (12071, 12072, 12074)  # sculptTableFCRabbitCeramic

# ========================== NEW OBJECT TUNINGS =============================

TUNING_SCULPTURE_INV = 180047       # object_sculpture_Inventory (Base Game)
TUNING_PLANT_INV = 201687           # object_plant_non_gardening_generic_carryable (Base Game)
TUNING_CAMPING_BED = 109806         # object_bedSingle_Camping_Cot (Base Game)
TUNING_LAMP_LANTERN = 326360        # object_light_table_offthegrid_inventoryable (Base Game)
TUNING_LAMP_CANDLE = 233659         # light_Candle_Table_Inventory (Base Game)
TUNING_CHAIR_INV = 36702            # object_sitDiningTK_02 (Base Game)
TUNING_STEREO_LOW = 14970           # object_stereoTableLOW_01 (Base Game)

TUNING_CAMPING_CHAIR = 111352       # object_sitDining_Camping_foldCut (GP01)
TUNING_CAMPING_TABLE = 110538       # object_tableGeneric_Inventory (GP01)
TUNING_LAMP_TABLE = 224082          # object_light_table_simInventory_dormStorage (EP08)
TUNING_MEDITATION = 119025          # object_MeditationStool (GP02)
TUNING_STEREO_PORTABLE = 291621     # object_StereoTable_portable (EP12)

FALLBACK_TUNINGS = {
    TUNING_CAMPING_CHAIR: TUNING_CHAIR_INV,
}

TUNING_IDS = tuple(
    value for name, value in globals().items()
    if name.startswith("TUNING_")
)

# ========================== REPLACEMENTS =============================

PACK_INFO = {
    TUNING_LAMP_TABLE: Pack.EP08,
    TUNING_CAMPING_TABLE: Pack.GP01,
    TUNING_CAMPING_CHAIR: Pack.GP01,
    TUNING_MEDITATION: Pack.GP02,
}

REPLACEMENT_DICT = {
    TUNING_CHAIR_INV: dict_to_tuple(DINING_CHAIR),
    TUNING_CAMPING_CHAIR: dict_to_tuple(FOLDING_CHAIR),
    TUNING_LAMP_TABLE: dict_to_tuple(LAMP_TABLE),
    TUNING_MEDITATION: SP33_PILLOW,
    TUNING_CAMPING_TABLE: SP33_TABLE,
    TUNING_SCULPTURE_INV: SP33_TENT,
}

REPLACEMENT_MAP = {
    obj_id: tuning_id
    for tuning_id, obj_ids in REPLACEMENT_DICT.items()
    for obj_id in obj_ids
}

objects.components.live_drag_component.force_live_drag_enable = True
log.debug(f"Live Drag Forced: {objects.components.live_drag_component.force_live_drag_enable}")
log.debug(f"Tuning IDs: {TUNING_IDS}")
log.debug(f"REPLACEMENT_MAP: {REPLACEMENT_MAP}")

def has_livedrag_component(definition):
    LIVEDRAG_COMPONENT = 2125782609
    if definition._components is None:
        return False
    if LIVEDRAG_COMPONENT not in definition._components:
        return False
    return True

def add_livedrag(definition):
    try:
        LIVEDRAG_COMPONENT = 2125782609
        if definition._components is None:
            log.info(f" → Adding new Live Drag Component to: {definition}")
            definition._components = (LIVEDRAG_COMPONENT,)
        elif LIVEDRAG_COMPONENT not in definition._components:
            log.info(f" → Adding Live Drag Component to: {definition}")
            definition._components = (LIVEDRAG_COMPONENT,) + definition._components
    except Exception as e:
        log.error(f" → Adding Live Drag Component error for {definition}: {e}")


@inject_to(Definition, '__init__')
def object_tuning_replacement(original, self, properties, definition_id):
    try:

        original(self, properties, definition_id)
        if not definition_id:
            return

        original_tuning_id = self._tuning_file_id
        if not original_tuning_id:
            return

        new_tuning_id = REPLACEMENT_MAP.get(definition_id)

        if original_tuning_id in TUNING_IDS and new_tuning_id is None:
            if not has_livedrag_component(self):
                log.empty()
                log.info(f"DEFINITION ({definition_id}) {self}:")
                log.info(f" → Object Tuning: original={original_tuning_id}")
                add_livedrag(self)
                return

        if new_tuning_id not in TUNING_IDS:
            return

        log.empty()
        log.info(f"DEFINITION ({definition_id}) {self}:")
        log.info(f" → Object Tuning: original={original_tuning_id}, new={new_tuning_id}")
        req_pack = PACK_INFO.get(new_tuning_id, Pack.BASE_GAME)
        if not is_available_pack(req_pack):
            fallback_id = FALLBACK_TUNINGS.get(new_tuning_id)
            if fallback_id is not None:
                log.info(f" → {req_pack} not available, using fallback: {fallback_id}")
                new_tuning_id = fallback_id
            else:
                log.info(f" → {req_pack} not available and no fallback defined — skipping.")
                return

        self._tuning_file_id = new_tuning_id
        if self._tuning_file_id == new_tuning_id:
            log.info(f" → Tuning replacement applied for: {self}")
            add_livedrag(self)
        else:
            log.error(f" → Tuning replacement failed for: {self}")

    except Exception as e:
        log.error(f"Fatal Error in object_tuning_replacement: {e}")
