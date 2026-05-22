import datetime
import logging

from django import template
from common.constants import PLAYER_CLASSES
from common.constants import PLAYER_DEITIES
from common.constants import PLAYER_LANGUAGES
from common.constants import PLAYER_RACES
from common.constants import RACES
from common.constants import ZONE_SHORT_TO_LONG

register = template.Library()

logger = logging.getLogger(__name__)

@register.filter(name='clean_name')
def clean_name(value):
    """Remove underscores and prepended # from NPC names"""
    if value:
        value = value.replace('_', ' ')
        return value.replace('#', '')
    return value


@register.filter(name="can_bind_filter")
def can_bind(value):
    match value:
        case 0:
            return "No"
        case 1:
            return "Self"
        case 2:
            return "Others"
        case 3:
            return "Area"
        case _:
            return "Unknown"


@register.filter(name="zone_type_filter")
def zone_type_filter(value):
    match value:
        case 0:
            return "Unknown"
        case 1:
            return "Regular"
        case 2:
            return "Instanced"
        case 3:
            return "Hybrid"
        case 4:
            return "Instanced"
        case 5:
            return "Hybrid"
        case 6:
            return "Raid"
        case 7:
            return "City"
        case _:
            return "Unknown"


@register.filter(name='yes_no')
def yes_no(value):
    return "yes" if value == 1 else "no"


@register.filter(name='django_range')
def django_range(value=5):
    return range(1,value)


@register.filter(name='gender')
def gender_filter(value):
    match value:
        case 0:
            return "Male"
        case 1:
            return "Female"
        case 2:
            return "Neuter"
        case _:
            return "Unknown"


@register.filter(name='from_timestamp')
def from_timestamp(value):
    return datetime.datetime.fromtimestamp(value)


@register.filter(name='time_played')
def time_played(value):
    return datetime.timedelta(seconds=value)


@register.filter(name='inventory_slot')
def inventory_slot(value):
    slot = {
        0: "slotCursor",
        1: "Left Ear",
        2: "Head",
        3: "Face",
        4: "Right Ear",
        5: "Neck",
        6: "Shoulders",
        7: "Arms",
        8: "Back",
        9: "Left Wrist",
        10: "Right Wrist",
        11: "Range",
        12: "Hands",
        13: "Primary",
        14: "Secondary",
        15: "Left Finger",
        16: "Right Finger",
        17: "Chest",
        18: "Legs",
        19: "Feet",
        20: "Waist",
        21: "Ammo",
        22: "General 1 (Left, 1st)",
        23: "General 2 (Left, 2nd)",
        24: "General 3 (Left, 3rd)",
        25: "General 4 (Left, 4th)",
        26: "General 5 (Right, 1st)",
        27: "General 6 (Right, 2nd)",
        28: "General 7 (Right, 3rd)",
        29: "General 8 (Right, 4th)",
        250: "General 1, Slot 1 (Left)",
        251: "General 1, Slot 2 (Right)",
        252: "General 1, Slot 3 (Left)",
        253: "General 1, Slot 4 (Right)",
        254: "General 1, Slot 5 (Left)",
        255: "General 1, Slot 6 (Right)",
        256: "General 1, Slot 7 (Left)",
        257: "General 1, Slot 8 (Right)",
        258: "General 1, Slot 9 (Left)",
        259: "General 1, Slot 10 (Right)",
        260: "General 2, Slot 1 (Left)",
        261: "General 2, Slot 2 (Right)",
        262: "General 2, Slot 3 (Left)",
        263: "General 2, Slot 4 (Right)",
        264: "General 2, Slot 5 (Left)",
        265: "General 2, Slot 6 (Right)",
        266: "General 2, Slot 7 (Left)",
        267: "General 2, Slot 8 (Right)",
        268: "General 2, Slot 9 (Left)",
        269: "General 2, Slot 10 (Right)",
        270: "General 3, Slot 1 (Left)",
        271: "General 3, Slot 2 (Right)",
        272: "General 3, Slot 3 (Left)",
        273: "General 3, Slot 4 (Right)",
        274: "General 3, Slot 5 (Left)",
        275: "General 3, Slot 6 (Right)",
        276: "General 3, Slot 7 (Left)",
        277: "General 3, Slot 8 (Right)",
        278: "General 3, Slot 9 (Left)",
        279: "General 3, Slot 10 (Right)",
        280: "General 4, Slot 1 (Left)",
        281: "General 4, Slot 2 (Right)",
        282: "General 4, Slot 3 (Left)",
        283: "General 4, Slot 4 (Right)",
        284: "General 4, Slot 5 (Left)",
        285: "General 4, Slot 6 (Right)",
        286: "General 4, Slot 7 (Left)",
        287: "General 4, Slot 8 (Right)",
        288: "General 4, Slot 9 (Left)",
        289: "General 4, Slot 10 (Right)",
        290: "General 5, Slot 1 (Left)",
        291: "General 5, Slot 2 (Right)",
        292: "General 5, Slot 3 (Left)",
        293: "General 5, Slot 4 (Right)",
        294: "General 5, Slot 5 (Left)",
        295: "General 5, Slot 6 (Right)",
        296: "General 5, Slot 7 (Left)",
        297: "General 5, Slot 8 (Right)",
        298: "General 5, Slot 9 (Left)",
        299: "General 5, Slot 10 (Right)",
        300: "General 6, Slot 1 (Left)",
        301: "General 6, Slot 2 (Right)",
        302: "General 6, Slot 3 (Left)",
        303: "General 6, Slot 4 (Right)",
        304: "General 6, Slot 5 (Left)",
        305: "General 6, Slot 6 (Right)",
        306: "General 6, Slot 7 (Left)",
        307: "General 6, Slot 8 (Right)",
        308: "General 6, Slot 9 (Left)",
        309: "General 6, Slot 10 (Right)",
        310: "General 7, Slot 1 (Left)",
        311: "General 7, Slot 2 (Right)",
        312: "General 7, Slot 3 (Left)",
        313: "General 7, Slot 4 (Right)",
        314: "General 7, Slot 5 (Left)",
        315: "General 7, Slot 6 (Right)",
        316: "General 7, Slot 7 (Left)",
        317: "General 7, Slot 8 (Right)",
        318: "General 7, Slot 9 (Left)",
        319: "General 7, Slot 10 (Right)",
        320: "General 8, Slot 1 (Left)",
        321: "General 8, Slot 2 (Right)",
        322: "General 8, Slot 3 (Left)",
        323: "General 8, Slot 4 (Right)",
        324: "General 8, Slot 5 (Left)",
        325: "General 8, Slot 6 (Right)",
        326: "General 8, Slot 7 (Left)",
        327: "General 8, Slot 8 (Right)",
        328: "General 8, Slot 9 (Left)",
        329: "General 8, Slot 10 (Right)",
        2000: "Bank 1 (Left)",
        2001: "Bank 2 (Left)",
        2002: "Bank 3 (Left)",
        2003: "Bank 4 (Left)",
        2004: "Bank 5 (Right)",
        2005: "Bank 6 (Right)",
        2006: "Bank 7 (Right)",
        2007: "Bank 8 (Right)",
        2030: "Bank Bag 1, Slot 1 (Left)",
        2031: "Bank Bag 1, Slot 2 (Right)",
        2032: "Bank Bag 1, Slot 3 (Left)",
        2033: "Bank Bag 1, Slot 4 (Right)",
        2034: "Bank Bag 1, Slot 5 (Left)",
        2035: "Bank Bag 1, Slot 6 (Right)",
        2036: "Bank Bag 1, Slot 7 (Left)",
        2037: "Bank Bag 1, Slot 8 (Right)",
        2038: "Bank Bag 1, Slot 9 (Left)",
        2039: "Bank Bag 1, Slot 10 (Right)",
        2040: "Bank Bag 2, Slot 1 (Left)",
        2041: "Bank Bag 2, Slot 2 (Right)",
        2042: "Bank Bag 2, Slot 3 (Left)",
        2043: "Bank Bag 2, Slot 4 (Right)",
        2044: "Bank Bag 2, Slot 5 (Left)",
        2045: "Bank Bag 2, Slot 6 (Right)",
        2046: "Bank Bag 2, Slot 7 (Left)",
        2047: "Bank Bag 2, Slot 8 (Right)",
        2048: "Bank Bag 2, Slot 9 (Left)",
        2049: "Bank Bag 2, Slot 10 (Right)",
        2050: "Bank Bag 3, Slot 1 (Left)",
        2051: "Bank Bag 3, Slot 2 (Right)",
        2052: "Bank Bag 3, Slot 3 (Left)",
        2053: "Bank Bag 3, Slot 4 (Right)",
        2054: "Bank Bag 3, Slot 5 (Left)",
        2055: "Bank Bag 3, Slot 6 (Right)",
        2056: "Bank Bag 3, Slot 7 (Left)",
        2057: "Bank Bag 3, Slot 8 (Right)",
        2058: "Bank Bag 3, Slot 9 (Left)",
        2059: "Bank Bag 3, Slot 10 (Right)",
        2060: "Bank Bag 4, Slot 1 (Left)",
        2061: "Bank Bag 4, Slot 2 (Right)",
        2062: "Bank Bag 4, Slot 3 (Left)",
        2063: "Bank Bag 4, Slot 4 (Right)",
        2064: "Bank Bag 4, Slot 5 (Left)",
        2065: "Bank Bag 4, Slot 6 (Right)",
        2066: "Bank Bag 4, Slot 7 (Left)",
        2067: "Bank Bag 4, Slot 8 (Right)",
        2068: "Bank Bag 4, Slot 9 (Left)",
        2069: "Bank Bag 4, Slot 10 (Right)",
        2070: "Bank Bag 5, Slot 1 (Left)",
        2071: "Bank Bag 5, Slot 2 (Right)",
        2072: "Bank Bag 5, Slot 3 (Left)",
        2073: "Bank Bag 5, Slot 4 (Right)",
        2074: "Bank Bag 5, Slot 5 (Left)",
        2075: "Bank Bag 5, Slot 6 (Right)",
        2076: "Bank Bag 5, Slot 7 (Left)",
        2077: "Bank Bag 5, Slot 8 (Right)",
        2078: "Bank Bag 5, Slot 9 (Left)",
        2079: "Bank Bag 5, Slot 10 (Right)",
        2080: "Bank Bag 6, Slot 1 (Left)",
        2081: "Bank Bag 6, Slot 2 (Right)",
        2082: "Bank Bag 6, Slot 3 (Left)",
        2083: "Bank Bag 6, Slot 4 (Right)",
        2084: "Bank Bag 6, Slot 5 (Left)",
        2085: "Bank Bag 6, Slot 6 (Right)",
        2086: "Bank Bag 6, Slot 7 (Left)",
        2087: "Bank Bag 6, Slot 8 (Right)",
        2088: "Bank Bag 6, Slot 9 (Left)",
        2089: "Bank Bag 6, Slot 10 (Right)",
        2090: "Bank Bag 7, Slot 1 (Left)",
        2091: "Bank Bag 7, Slot 2 (Right)",
        2092: "Bank Bag 7, Slot 3 (Left)",
        2093: "Bank Bag 7, Slot 4 (Right)",
        2094: "Bank Bag 7, Slot 5 (Left)",
        2095: "Bank Bag 7, Slot 6 (Right)",
        2096: "Bank Bag 7, Slot 7 (Left)",
        2097: "Bank Bag 7, Slot 8 (Right)",
        2098: "Bank Bag 7, Slot 9 (Left)",
        2099: "Bank Bag 7, Slot 10 (Right)",
        2100: "Bank Bag 8, Slot 1 (Left)",
        2101: "Bank Bag 8, Slot 2 (Right)",
        2102: "Bank Bag 8, Slot 3 (Left)",
        2103: "Bank Bag 8, Slot 4 (Right)",
        2104: "Bank Bag 8, Slot 5 (Left)",
        2105: "Bank Bag 8, Slot 6 (Right)",
        2106: "Bank Bag 8, Slot 7 (Left)",
        2107: "Bank Bag 8, Slot 8 (Right)",
        2108: "Bank Bag 8, Slot 9 (Left)",
        2109: "Bank Bag 8, Slot 10 (Right)",
        # RoF2: extra personal inventory container slots
        30: "General 9",
        31: "General 10",
        # RoF2: extra bank container slots (24-slot bank)
        2008: "Bank 9",  2009: "Bank 10", 2010: "Bank 11", 2011: "Bank 12",
        2012: "Bank 13", 2013: "Bank 14", 2014: "Bank 15", 2015: "Bank 16",
        2016: "Bank 17", 2017: "Bank 18", 2018: "Bank 19", 2019: "Bank 20",
        2020: "Bank 21", 2021: "Bank 22", 2022: "Bank 23", 2023: "Bank 24",
        # RoF2: shared bank container slots
        2500: "Shared Bank 1",
        2501: "Shared Bank 2",
        # RoF2 bag content slots — formula:
        #   personal bag in slot N (22-31): content = 4010 + (N-22)*200 + slot_index
        #   bank bag in slot N (2000-2023): content = 6810 + (N-2000)*200 + slot_index
        4010: "General 1, Slot 1 (Left)",   4011: "General 1, Slot 2 (Right)",
        4012: "General 1, Slot 3 (Left)",   4013: "General 1, Slot 4 (Right)",
        4014: "General 1, Slot 5 (Left)",   4015: "General 1, Slot 6 (Right)",
        4016: "General 1, Slot 7 (Left)",   4017: "General 1, Slot 8 (Right)",
        4018: "General 1, Slot 9 (Left)",   4019: "General 1, Slot 10 (Right)",
        4210: "General 2, Slot 1 (Left)",   4211: "General 2, Slot 2 (Right)",
        4212: "General 2, Slot 3 (Left)",   4213: "General 2, Slot 4 (Right)",
        4214: "General 2, Slot 5 (Left)",   4215: "General 2, Slot 6 (Right)",
        4216: "General 2, Slot 7 (Left)",   4217: "General 2, Slot 8 (Right)",
        4218: "General 2, Slot 9 (Left)",   4219: "General 2, Slot 10 (Right)",
        4410: "General 3, Slot 1 (Left)",   4411: "General 3, Slot 2 (Right)",
        4412: "General 3, Slot 3 (Left)",   4413: "General 3, Slot 4 (Right)",
        4414: "General 3, Slot 5 (Left)",   4415: "General 3, Slot 6 (Right)",
        4416: "General 3, Slot 7 (Left)",   4417: "General 3, Slot 8 (Right)",
        4418: "General 3, Slot 9 (Left)",   4419: "General 3, Slot 10 (Right)",
        4610: "General 4, Slot 1 (Left)",   4611: "General 4, Slot 2 (Right)",
        4612: "General 4, Slot 3 (Left)",   4613: "General 4, Slot 4 (Right)",
        4614: "General 4, Slot 5 (Left)",   4615: "General 4, Slot 6 (Right)",
        4616: "General 4, Slot 7 (Left)",   4617: "General 4, Slot 8 (Right)",
        4618: "General 4, Slot 9 (Left)",   4619: "General 4, Slot 10 (Right)",
        4810: "General 5, Slot 1 (Left)",   4811: "General 5, Slot 2 (Right)",
        4812: "General 5, Slot 3 (Left)",   4813: "General 5, Slot 4 (Right)",
        4814: "General 5, Slot 5 (Left)",   4815: "General 5, Slot 6 (Right)",
        4816: "General 5, Slot 7 (Left)",   4817: "General 5, Slot 8 (Right)",
        4818: "General 5, Slot 9 (Left)",   4819: "General 5, Slot 10 (Right)",
        5010: "General 6, Slot 1 (Left)",   5011: "General 6, Slot 2 (Right)",
        5012: "General 6, Slot 3 (Left)",   5013: "General 6, Slot 4 (Right)",
        5014: "General 6, Slot 5 (Left)",   5015: "General 6, Slot 6 (Right)",
        5016: "General 6, Slot 7 (Left)",   5017: "General 6, Slot 8 (Right)",
        5018: "General 6, Slot 9 (Left)",   5019: "General 6, Slot 10 (Right)",
        5210: "General 7, Slot 1 (Left)",   5211: "General 7, Slot 2 (Right)",
        5212: "General 7, Slot 3 (Left)",   5213: "General 7, Slot 4 (Right)",
        5214: "General 7, Slot 5 (Left)",   5215: "General 7, Slot 6 (Right)",
        5216: "General 7, Slot 7 (Left)",   5217: "General 7, Slot 8 (Right)",
        5218: "General 7, Slot 9 (Left)",   5219: "General 7, Slot 10 (Right)",
        5410: "General 8, Slot 1 (Left)",   5411: "General 8, Slot 2 (Right)",
        5412: "General 8, Slot 3 (Left)",   5413: "General 8, Slot 4 (Right)",
        5414: "General 8, Slot 5 (Left)",   5415: "General 8, Slot 6 (Right)",
        5416: "General 8, Slot 7 (Left)",   5417: "General 8, Slot 8 (Right)",
        5418: "General 8, Slot 9 (Left)",   5419: "General 8, Slot 10 (Right)",
        5610: "General 9, Slot 1 (Left)",   5611: "General 9, Slot 2 (Right)",
        5612: "General 9, Slot 3 (Left)",   5613: "General 9, Slot 4 (Right)",
        5614: "General 9, Slot 5 (Left)",   5615: "General 9, Slot 6 (Right)",
        5616: "General 9, Slot 7 (Left)",   5617: "General 9, Slot 8 (Right)",
        5618: "General 9, Slot 9 (Left)",   5619: "General 9, Slot 10 (Right)",
        5810: "General 10, Slot 1 (Left)",  5811: "General 10, Slot 2 (Right)",
        5812: "General 10, Slot 3 (Left)",  5813: "General 10, Slot 4 (Right)",
        5814: "General 10, Slot 5 (Left)",  5815: "General 10, Slot 6 (Right)",
        5816: "General 10, Slot 7 (Left)",  5817: "General 10, Slot 8 (Right)",
        5818: "General 10, Slot 9 (Left)",  5819: "General 10, Slot 10 (Right)",
        6810: "Bank Bag 1, Slot 1 (Left)",  6811: "Bank Bag 1, Slot 2 (Right)",
        6812: "Bank Bag 1, Slot 3 (Left)",  6813: "Bank Bag 1, Slot 4 (Right)",
        6814: "Bank Bag 1, Slot 5 (Left)",  6815: "Bank Bag 1, Slot 6 (Right)",
        6816: "Bank Bag 1, Slot 7 (Left)",  6817: "Bank Bag 1, Slot 8 (Right)",
        6818: "Bank Bag 1, Slot 9 (Left)",  6819: "Bank Bag 1, Slot 10 (Right)",
        7010: "Bank Bag 2, Slot 1 (Left)",  7011: "Bank Bag 2, Slot 2 (Right)",
        7012: "Bank Bag 2, Slot 3 (Left)",  7013: "Bank Bag 2, Slot 4 (Right)",
        7014: "Bank Bag 2, Slot 5 (Left)",  7015: "Bank Bag 2, Slot 6 (Right)",
        7016: "Bank Bag 2, Slot 7 (Left)",  7017: "Bank Bag 2, Slot 8 (Right)",
        7018: "Bank Bag 2, Slot 9 (Left)",  7019: "Bank Bag 2, Slot 10 (Right)",
        7210: "Bank Bag 3, Slot 1 (Left)",  7211: "Bank Bag 3, Slot 2 (Right)",
        7212: "Bank Bag 3, Slot 3 (Left)",  7213: "Bank Bag 3, Slot 4 (Right)",
        7214: "Bank Bag 3, Slot 5 (Left)",  7215: "Bank Bag 3, Slot 6 (Right)",
        7216: "Bank Bag 3, Slot 7 (Left)",  7217: "Bank Bag 3, Slot 8 (Right)",
        7218: "Bank Bag 3, Slot 9 (Left)",  7219: "Bank Bag 3, Slot 10 (Right)",
        7410: "Bank Bag 4, Slot 1 (Left)",  7411: "Bank Bag 4, Slot 2 (Right)",
        7412: "Bank Bag 4, Slot 3 (Left)",  7413: "Bank Bag 4, Slot 4 (Right)",
        7414: "Bank Bag 4, Slot 5 (Left)",  7415: "Bank Bag 4, Slot 6 (Right)",
        7416: "Bank Bag 4, Slot 7 (Left)",  7417: "Bank Bag 4, Slot 8 (Right)",
        7418: "Bank Bag 4, Slot 9 (Left)",  7419: "Bank Bag 4, Slot 10 (Right)",
        7610: "Bank Bag 5, Slot 1 (Left)",  7611: "Bank Bag 5, Slot 2 (Right)",
        7612: "Bank Bag 5, Slot 3 (Left)",  7613: "Bank Bag 5, Slot 4 (Right)",
        7614: "Bank Bag 5, Slot 5 (Left)",  7615: "Bank Bag 5, Slot 6 (Right)",
        7616: "Bank Bag 5, Slot 7 (Left)",  7617: "Bank Bag 5, Slot 8 (Right)",
        7618: "Bank Bag 5, Slot 9 (Left)",  7619: "Bank Bag 5, Slot 10 (Right)",
        7810: "Bank Bag 6, Slot 1 (Left)",  7811: "Bank Bag 6, Slot 2 (Right)",
        7812: "Bank Bag 6, Slot 3 (Left)",  7813: "Bank Bag 6, Slot 4 (Right)",
        7814: "Bank Bag 6, Slot 5 (Left)",  7815: "Bank Bag 6, Slot 6 (Right)",
        7816: "Bank Bag 6, Slot 7 (Left)",  7817: "Bank Bag 6, Slot 8 (Right)",
        7818: "Bank Bag 6, Slot 9 (Left)",  7819: "Bank Bag 6, Slot 10 (Right)",
        8010: "Bank Bag 7, Slot 1 (Left)",  8011: "Bank Bag 7, Slot 2 (Right)",
        8012: "Bank Bag 7, Slot 3 (Left)",  8013: "Bank Bag 7, Slot 4 (Right)",
        8014: "Bank Bag 7, Slot 5 (Left)",  8015: "Bank Bag 7, Slot 6 (Right)",
        8016: "Bank Bag 7, Slot 7 (Left)",  8017: "Bank Bag 7, Slot 8 (Right)",
        8018: "Bank Bag 7, Slot 9 (Left)",  8019: "Bank Bag 7, Slot 10 (Right)",
        8210: "Bank Bag 8, Slot 1 (Left)",  8211: "Bank Bag 8, Slot 2 (Right)",
        8212: "Bank Bag 8, Slot 3 (Left)",  8213: "Bank Bag 8, Slot 4 (Right)",
        8214: "Bank Bag 8, Slot 5 (Left)",  8215: "Bank Bag 8, Slot 6 (Right)",
        8216: "Bank Bag 8, Slot 7 (Left)",  8217: "Bank Bag 8, Slot 8 (Right)",
        8218: "Bank Bag 8, Slot 9 (Left)",  8219: "Bank Bag 8, Slot 10 (Right)",
        8410: "Bank Bag 9, Slot 1 (Left)",  8411: "Bank Bag 9, Slot 2 (Right)",
        8412: "Bank Bag 9, Slot 3 (Left)",  8413: "Bank Bag 9, Slot 4 (Right)",
        8414: "Bank Bag 9, Slot 5 (Left)",  8415: "Bank Bag 9, Slot 6 (Right)",
        8416: "Bank Bag 9, Slot 7 (Left)",  8417: "Bank Bag 9, Slot 8 (Right)",
        8418: "Bank Bag 9, Slot 9 (Left)",  8419: "Bank Bag 9, Slot 10 (Right)",
        8610: "Bank Bag 10, Slot 1 (Left)", 8611: "Bank Bag 10, Slot 2 (Right)",
        8612: "Bank Bag 10, Slot 3 (Left)", 8613: "Bank Bag 10, Slot 4 (Right)",
        8614: "Bank Bag 10, Slot 5 (Left)", 8615: "Bank Bag 10, Slot 6 (Right)",
        8616: "Bank Bag 10, Slot 7 (Left)", 8617: "Bank Bag 10, Slot 8 (Right)",
        8618: "Bank Bag 10, Slot 9 (Left)", 8619: "Bank Bag 10, Slot 10 (Right)",
        8810: "Bank Bag 11, Slot 1 (Left)", 8811: "Bank Bag 11, Slot 2 (Right)",
        8812: "Bank Bag 11, Slot 3 (Left)", 8813: "Bank Bag 11, Slot 4 (Right)",
        8814: "Bank Bag 11, Slot 5 (Left)", 8815: "Bank Bag 11, Slot 6 (Right)",
        8816: "Bank Bag 11, Slot 7 (Left)", 8817: "Bank Bag 11, Slot 8 (Right)",
        8818: "Bank Bag 11, Slot 9 (Left)", 8819: "Bank Bag 11, Slot 10 (Right)",
        9010: "Bank Bag 12, Slot 1 (Left)", 9011: "Bank Bag 12, Slot 2 (Right)",
        9012: "Bank Bag 12, Slot 3 (Left)", 9013: "Bank Bag 12, Slot 4 (Right)",
        9014: "Bank Bag 12, Slot 5 (Left)", 9015: "Bank Bag 12, Slot 6 (Right)",
        9016: "Bank Bag 12, Slot 7 (Left)", 9017: "Bank Bag 12, Slot 8 (Right)",
        9018: "Bank Bag 12, Slot 9 (Left)", 9019: "Bank Bag 12, Slot 10 (Right)",
        9210: "Bank Bag 13, Slot 1 (Left)", 9211: "Bank Bag 13, Slot 2 (Right)",
        9212: "Bank Bag 13, Slot 3 (Left)", 9213: "Bank Bag 13, Slot 4 (Right)",
        9214: "Bank Bag 13, Slot 5 (Left)", 9215: "Bank Bag 13, Slot 6 (Right)",
        9216: "Bank Bag 13, Slot 7 (Left)", 9217: "Bank Bag 13, Slot 8 (Right)",
        9218: "Bank Bag 13, Slot 9 (Left)", 9219: "Bank Bag 13, Slot 10 (Right)",
        9410: "Bank Bag 14, Slot 1 (Left)", 9411: "Bank Bag 14, Slot 2 (Right)",
        9412: "Bank Bag 14, Slot 3 (Left)", 9413: "Bank Bag 14, Slot 4 (Right)",
        9414: "Bank Bag 14, Slot 5 (Left)", 9415: "Bank Bag 14, Slot 6 (Right)",
        9416: "Bank Bag 14, Slot 7 (Left)", 9417: "Bank Bag 14, Slot 8 (Right)",
        9418: "Bank Bag 14, Slot 9 (Left)", 9419: "Bank Bag 14, Slot 10 (Right)",
        9610: "Bank Bag 15, Slot 1 (Left)", 9611: "Bank Bag 15, Slot 2 (Right)",
        9612: "Bank Bag 15, Slot 3 (Left)", 9613: "Bank Bag 15, Slot 4 (Right)",
        9614: "Bank Bag 15, Slot 5 (Left)", 9615: "Bank Bag 15, Slot 6 (Right)",
        9616: "Bank Bag 15, Slot 7 (Left)", 9617: "Bank Bag 15, Slot 8 (Right)",
        9618: "Bank Bag 15, Slot 9 (Left)", 9619: "Bank Bag 15, Slot 10 (Right)",
        9810: "Bank Bag 16, Slot 1 (Left)", 9811: "Bank Bag 16, Slot 2 (Right)",
        9812: "Bank Bag 16, Slot 3 (Left)", 9813: "Bank Bag 16, Slot 4 (Right)",
        9814: "Bank Bag 16, Slot 5 (Left)", 9815: "Bank Bag 16, Slot 6 (Right)",
        9816: "Bank Bag 16, Slot 7 (Left)", 9817: "Bank Bag 16, Slot 8 (Right)",
        9818: "Bank Bag 16, Slot 9 (Left)", 9819: "Bank Bag 16, Slot 10 (Right)",
        10010: "Bank Bag 17, Slot 1 (Left)", 10011: "Bank Bag 17, Slot 2 (Right)",
        10012: "Bank Bag 17, Slot 3 (Left)", 10013: "Bank Bag 17, Slot 4 (Right)",
        10014: "Bank Bag 17, Slot 5 (Left)", 10015: "Bank Bag 17, Slot 6 (Right)",
        10016: "Bank Bag 17, Slot 7 (Left)", 10017: "Bank Bag 17, Slot 8 (Right)",
        10018: "Bank Bag 17, Slot 9 (Left)", 10019: "Bank Bag 17, Slot 10 (Right)",
        10210: "Bank Bag 18, Slot 1 (Left)", 10211: "Bank Bag 18, Slot 2 (Right)",
        10212: "Bank Bag 18, Slot 3 (Left)", 10213: "Bank Bag 18, Slot 4 (Right)",
        10214: "Bank Bag 18, Slot 5 (Left)", 10215: "Bank Bag 18, Slot 6 (Right)",
        10216: "Bank Bag 18, Slot 7 (Left)", 10217: "Bank Bag 18, Slot 8 (Right)",
        10218: "Bank Bag 18, Slot 9 (Left)", 10219: "Bank Bag 18, Slot 10 (Right)",
        10410: "Bank Bag 19, Slot 1 (Left)", 10411: "Bank Bag 19, Slot 2 (Right)",
        10412: "Bank Bag 19, Slot 3 (Left)", 10413: "Bank Bag 19, Slot 4 (Right)",
        10414: "Bank Bag 19, Slot 5 (Left)", 10415: "Bank Bag 19, Slot 6 (Right)",
        10416: "Bank Bag 19, Slot 7 (Left)", 10417: "Bank Bag 19, Slot 8 (Right)",
        10418: "Bank Bag 19, Slot 9 (Left)", 10419: "Bank Bag 19, Slot 10 (Right)",
        10610: "Bank Bag 20, Slot 1 (Left)", 10611: "Bank Bag 20, Slot 2 (Right)",
        10612: "Bank Bag 20, Slot 3 (Left)", 10613: "Bank Bag 20, Slot 4 (Right)",
        10614: "Bank Bag 20, Slot 5 (Left)", 10615: "Bank Bag 20, Slot 6 (Right)",
        10616: "Bank Bag 20, Slot 7 (Left)", 10617: "Bank Bag 20, Slot 8 (Right)",
        10618: "Bank Bag 20, Slot 9 (Left)", 10619: "Bank Bag 20, Slot 10 (Right)",
        10810: "Bank Bag 21, Slot 1 (Left)", 10811: "Bank Bag 21, Slot 2 (Right)",
        10812: "Bank Bag 21, Slot 3 (Left)", 10813: "Bank Bag 21, Slot 4 (Right)",
        10814: "Bank Bag 21, Slot 5 (Left)", 10815: "Bank Bag 21, Slot 6 (Right)",
        10816: "Bank Bag 21, Slot 7 (Left)", 10817: "Bank Bag 21, Slot 8 (Right)",
        10818: "Bank Bag 21, Slot 9 (Left)", 10819: "Bank Bag 21, Slot 10 (Right)",
        11010: "Bank Bag 22, Slot 1 (Left)", 11011: "Bank Bag 22, Slot 2 (Right)",
        11012: "Bank Bag 22, Slot 3 (Left)", 11013: "Bank Bag 22, Slot 4 (Right)",
        11014: "Bank Bag 22, Slot 5 (Left)", 11015: "Bank Bag 22, Slot 6 (Right)",
        11016: "Bank Bag 22, Slot 7 (Left)", 11017: "Bank Bag 22, Slot 8 (Right)",
        11018: "Bank Bag 22, Slot 9 (Left)", 11019: "Bank Bag 22, Slot 10 (Right)",
        11210: "Bank Bag 23, Slot 1 (Left)", 11211: "Bank Bag 23, Slot 2 (Right)",
        11212: "Bank Bag 23, Slot 3 (Left)", 11213: "Bank Bag 23, Slot 4 (Right)",
        11214: "Bank Bag 23, Slot 5 (Left)", 11215: "Bank Bag 23, Slot 6 (Right)",
        11216: "Bank Bag 23, Slot 7 (Left)", 11217: "Bank Bag 23, Slot 8 (Right)",
        11218: "Bank Bag 23, Slot 9 (Left)", 11219: "Bank Bag 23, Slot 10 (Right)",
        11410: "Bank Bag 24, Slot 1 (Left)", 11411: "Bank Bag 24, Slot 2 (Right)",
        11412: "Bank Bag 24, Slot 3 (Left)", 11413: "Bank Bag 24, Slot 4 (Right)",
        11414: "Bank Bag 24, Slot 5 (Left)", 11415: "Bank Bag 24, Slot 6 (Right)",
        11416: "Bank Bag 24, Slot 7 (Left)", 11417: "Bank Bag 24, Slot 8 (Right)",
        11418: "Bank Bag 24, Slot 9 (Left)", 11419: "Bank Bag 24, Slot 10 (Right)",
    }
    return slot[value] if value in slot else value


@register.filter(name='player_class')
def player_class(value):
    return PLAYER_CLASSES[value] if value in PLAYER_CLASSES else "Unknown"


@register.filter(name='spell_target_type')
def spell_target_type(value):
    target_type = {
        0: "Rag'Zhezum Special",
        1: "Line of Sight",
        3: "Group V1",
        4: "PBAE",
        5: "Single",
        6: "Self",
        8: "Targeted Area of Effect",
        9: "Animal",
        10: "Undead",
        11: "Summoned",
        13: "Lifetap",
        14: "Pet",
        15: "Corpse",
        16: "Plant",
        17: "Uber Giants",
        18: "Uber Dragons",
        20: "Targeted Area of Effect Life Tap",
        24: "Area of Effect Undead",
        25: "Area of Effect Summoned",
        32: "Area of Effect Caster",
        33: "NPC Hate List",
        34: "Dungeon Object",
        35: "Muramite",
        36: "Area - PC Only",
        37: "Area - NPC Only",
        38: "Summoned Pet",
        39: "Group No Pets",
        40: "Area of EffectPC V2",
        41: "Group v2",
        42: "Self (Directional)",
        43: "Group With Pets",
        44: "Beam",
    }
    return target_type[value] if value in target_type else "Unknown"


@register.simple_tag
def define(value=None):
    return value


@register.filter(name='npc_class')
def npc_class(value):
    classes = {
        0: 'Soldier',
        1: 'Warrior',
        2: 'Cleric',
        3: 'Paladin',
        4: 'Ranger',
        5: 'Shadowknight',
        6: 'Druid',
        7: 'Monk',
        8: 'Bard',
        9: 'Rogue',
        10: 'Shaman',
        11: 'Necromancer',
        12: 'Wizard',
        13: 'Magician',
        14: 'Enchanter',
        15: 'Beastlord',
        16: 'Berserker',
        17: 'Banker',
        18: 'Unknown18',
        19: 'Unknown19',
        20: 'Warrior GM',
        21: 'Cleric GM',
        22: 'Paladin GM',
        23: 'Ranger GM',
        24: 'Shadowknight GM',
        25: 'Druid GM',
        26: 'Monk GM',
        27: 'Bard GM',
        28: 'Rogue GM',
        29: 'Shaman GM',
        30: 'Necromancer GM',
        31: 'Wizard GM',
        32: 'Magician GM',
        33: 'Enchanter GM',
        34: 'Beastlord GM',
        35: 'Berserker GM',
        36: 'Unknown36',
        37: 'Unknown37',
        38: 'Unknown38',
        39: 'Unknown39',
        40: 'Banker',
        41: 'Shopkeeper'
    }
    return classes[value] if value in classes else "Unknown"


@register.filter(name="npc_race")
def npc_race(value):
    return RACES[value] if value in RACES else value


@register.filter(name='player_race')
def player_race(value):
    return PLAYER_RACES[value] if value in PLAYER_RACES else value


@register.filter(name='player_deity')
def player_deity(value):
    """
    Converts a deity id to a human-readable player deity name

    :param value: the deity id piped to the filter
    :return: a human-readable player deity name
    """
    return PLAYER_DEITIES[value] if value in PLAYER_DEITIES else "Unknown"


@register.filter(name='player_skill')
def player_skill(value):
    """
    Converts a player skill id to a human-readable skill name
    :param value: player skill id
    :return: a human-readable player skill name
    """
    player_skills = {
        0: "1H Blunt",
        1: "1H Slashing",
        2: "2H Blunt",
        3: "2H Slashing",
        4: "Abjuration",
        5: "Alteration",
        6: "Apply Poison",
        7: "Archery",
        8: "Backstab",
        9: "Bind Wound",
        10: "Bash",
        11: "Block",
        12: "Brass Instruments",
        13: "Channeling",
        14: "Conjuration",
        15: "Defense",
        16: "Disarm",
        17: "Disarm Traps",
        18: "Divination",
        19: "Dodge",
        20: "Double Attack",
        21: "Dragon Punch / Tail Rake",
        22: "Dual Wield",
        23: "Eagle Strike",
        24: "Evocation",
        25: "Feign Death",
        26: "Flying Kick",
        27: "Forage",
        28: "Hand to Hand",
        29: "Hide",
        30: "Kick",
        31: "Meditate",
        32: "Mend",
        33: "Offense",
        34: "Parry",
        35: "Pick Lock",
        36: "1H Piercing",
        37: "Riposte",
        38: "Round Kick",
        39: "Safe Fall",
        40: "Sense Heading",
        41: "Singing",
        42: "Sneak",
        43: "Specialize Abjure",
        44: "Specialize Alteration",
        45: "Specialize Conjuration",
        46: "Specialize Divination",
        47: "Specialize Evocation",
        48: "Pick Pockets",
        49: "Stringed Instruments",
        50: "Swimming",
        51: "Throwing",
        52: "Tiger Claw",
        53: "Tracking",
        54: "Wind Instruments",
        55: "Fishing",
        56: "Make Poison",
        57: "Tinkering",
        58: "Research",
        59: "Alchemy",
        60: "Baking",
        61: "Tailoring",
        62: "Sense Traps",
        63: "Blacksmithing",
        64: "Fletching",
        65: "Brewing",
        66: "Alcohol Tolerance",
        67: "Begging",
        68: "Jewelrymaking",
        69: "Pottery",
        70: "Percussion Instruments",
        71: "Intimidation",
        72: "Berserking",
        73: "Taunt",
        74: "Count",
    }
    return player_skills[value] if value in player_skills else "Unknown " + str(value)


@register.filter(name='player_language')
def player_language(value):
    return PLAYER_LANGUAGES[value] if value in PLAYER_LANGUAGES else "Unknown" + str(value)


@register.filter(name='zone_short_to_long')
def zone_short_to_long(value):
    return ZONE_SHORT_TO_LONG[value] if value in ZONE_SHORT_TO_LONG else "Unknown" + str(value)


@register.filter(name='zone_filter')
def zone_filter(value, arg):
    """
    Converts a zone_id to a zones long name or short name

    :param value: The zone_id piped to the filter
    :param arg: "long" if the zones's long name is desired, defaults to the zones short name
    :return: a zones long name or short name
    """
    zones = {
        1: ("South Qeynos", "qeynos"),
        2: ("North Qeynos", "qeynos2"),
        3: ("The Surefall Glade", "qrg"),
        4: ("The Qeynos Hills", "qeytoqrg"),
        5: ("Highpass Hold", "highpass"),
        6: ("High Keep", "highkeep"),
        7: ("Unused", "Unused"),
        8: ("North Freeport", "freportn"),
        9: ("West Freeport", "freportw"),
        10: ("East Freeport", "freporte"),
        11: ("The Liberated Citadel of Runnyeye", "runneye"),
        12: ("The Western Plains of Karana", "qey2hh1"),
        13: ("The Northern Plains of Karana", "northkarana"),
        14: ("The Southern Plains of Karana", "southkarana"),
        15: ("Eastern Plains of Karana", "eastkarana"),
        16: ("Gorge of King Xorbb", "beholder"),
        17: ("Blackburrow", "blackburrow"),
        18: ("The Lair of the Splitpaw", "paw"),
        19: ("Rivervale", "rivervale"),
        20: ("Kithicor Forest", "kithicor"),
        21: ("West Commonlands", "commons"),
        22: ("East Commonlands", "ecommons"),
        23: ("The Erudin Palace", "erudint"),
        24: ("Erudin", "erudnext"),
        25: ("The Nektulos Forest", "nektulos"),
        26: ("Sunset Home", "cshome"),
        27: ("The Lavastorm Mountains", "lavastorm"),
        28: ("Nektropos", "nektropos"),
        29: ("Halas", "halas"),
        30: ("Everfrost Peaks", "everfrost"),
        31: ("Solusek's Eye", "soldunga"),
        32: ("Nagafen's Lair", "soldungb"),
        33: ("Misty Thicket", "misty"),
        34: ("Northern Desert of Ro", "nro"),
        35: ("Southern Desert of Ro", "sro"),
        36: ("Befallen", "befallen"),
        37: ("Oasis of Marr", "oasis"),
        38: ("Toxxulia Forest", "tox"),
        39: ("The Hole", "hole"),
        40: ("Neriak - Foreign Quarter", "neriaka"),
        41: ("Neriak - Commons", "neriakb"),
        42: ("Neriak - 3rd Gate", "neriakc"),
        43: ("Neriak Palace", "neriakd"),
        44: ("Najena", "najena"),
        45: ("The Qeynos Aqueduct System", "qcat"),
        46: ("Innothule Swamp", "innothule"),
        47: ("The Feerott", "feerott"),
        48: ("Accursed Temple of CazicThule", "cazicthule"),
        49: ("Oggok", "oggok"),
        50: ("The Rathe Mountains", "rathemtn"),
        51: ("Lake Rathetear", "lakerathe"),
        52: ("Grobb", "grobb"),
        53: ("Aviak Village", "aviak"),
        54: ("The Greater Faydark", "gfaydark"),
        55: ("Ak'Anon", "akanon"),
        56: ("Steamfont Mountains", "steamfont"),
        57: ("The Lesser Faydark", "lfaydark"),
        58: ("Crushbone", "crushbone"),
        59: ("The Castle of Mistmoore", "mistmoore"),
        60: ("South Kaladim", "kaladima"),
        61: ("Northern Felwithe", "felwithea"),
        62: ("Southern Felwithe", "felwitheb"),
        63: ("The Estate of Unrest", "unrest"),
        64: ("Kedge Keep", "kedge"),
        65: ("The City of Guk", "guktop"),
        66: ("The Ruins of Old Guk", "gukbuttom"),
        67: ("North Kaladim", "kaladimb"),
        68: ("Butcherblock Mountains", "butcher"),
        69: ("Ocean of Tears", "oot"),
        70: ("Dagnor's Cauldron", "cauldron"),
        71: ("The Plane of Sky", "airplane"),
        72: ("The Plane of Fear", "fearplane"),
        73: ("The Permafrost Caverns", "permafrost"),
        74: ("Kerra Isle", "kerraridge"),
        75: ("Paineel", "paineel"),
        76: ("Plane of Hate", "hateplane"),
        77: ("The Arena", "arena"),
        78: ("The Field of Bone", "fieldofbone"),
        79: ("The Warsliks Woods", "warslikswood"),
        80: ("The Temple of Solusek Ro", "soltemple"),
        81: ("The Temple of Droga", "droga"),
        82: ("Cabilis West", "cabwest"),
        83: ("The Swamp of No Hope", "swampofnohope"),
        84: ("Firiona Vie", "firiona"),
        85: ("Lake of Ill Omen", "lakeofillomen"),
        86: ("The Dreadlands", "dreadlands"),
        87: ("The Burning Wood", "burningwood"),
        88: ("Kaesora", "kaesora"),
        89: ("The Ruins of Sebilis", "sebilis"),
        90: ("The City of Mist", "citymist"),
        91: ("The Skyfire Mountains", "skyfire"),
        92: ("Frontier Mountains", "frontiermtns"),
        93: ("The Overthere", "overthere"),
        94: ("The Emerald Jungle", "emeraldjungle"),
        95: ("Trakanon's Teeth", "trakanon"),
        96: ("Timorous Deep", "timorous"),
        97: ("Kurn's Tower", "kurn"),
        98: ("Erud's Crossing", "erudsxing"),
        99: ("Unused", "unused"),
        100: ("The Stonebrunt Mountains", "stonebrunt"),
        101: ("The Warrens", "warrens"),
        102: ("Karnor's Castle", "karnor"),
        103: ("Chardok", "chardok"),
        104: ("The Crypt of Dalnir", "dalnir"),
        105: ("The Howling Stones", "charasis"),
        106: ("Cabilis East", "cabeast"),
        107: ("The Mines of Nurga", "nurga"),
        108: ("Veeshan's Peak", "veeshan"),
        109: ("Veksar", "veksar"),
        110: ("Iceclad Ocean", "iceclad"),
        111: ("Tower of Frozen Shadow", "frozenshadow"),
        112: ("Velketor's Labyrinth", "velketor"),
        113: ("Kael Drakkal", "kael"),
        114: ("Skyshrine", "skyshrine"),
        115: ("The City of Thurgadin", "thurgadina"),
        116: ("Eastern Wastes", "eastwastes"),
        117: ("Cobalt Scar", "cobaltscar"),
        118: ("The Great Divide", "greatdivide"),
        119: ("Wakening Land", "wakening"),
        120: ("Western Wastes", "westwastes"),
        121: ("Crystal Caverns", "crystal"),
        123: ("Dragon Necropolis", "necropolis"),
        124: ("Temple of Veeshan", "templeveeshan"),
        125: ("Siren's Grotto", "sirens"),
        126: ("Plane of Mischief", "mischiefplane"),
        127: ("Plane of Growth", "growthplane"),
        128: ("Sleeper's Tomb", "sleeper"),
        129: ("Icewell Keep", "thurgadinb"),
        130: ("Marauder's Mire", "erudsxing2"),
        150: ("Shadow Haven", "shadowhaven"),
        151: ("The Bazaar", "bazaar"),
        152: ("Nexus", "nexus"),
        153: ("Echo Caverns", "echo"),
        154: ("Acrylia Caverns", "acrylia"),
        155: ("The City of Shar Vahl", "sharvahl"),
        156: ("The Paladul Caverns", "paladul"),
        157: ("The Fungus Grove", "fungusgrove"),
        158: ("Vex Thal", "vexthal"),
        159: ("Sanctus Seru", "sseru"),
        160: ("Katta Castellum", "katta"),
        161: ("Netherbian Lair", "netherbian"),
        162: ("Ssraeshza Temple", "ssratemple"),
        163: ("Grieg's End", "griegsend"),
        164: ("The Deep", "thedeep"),
        165: ("Shadeweaver's Thicket", "shadeweaver"),
        166: ("Hollowshade Moor", "hollowshade"),
        167: ("Grimling Forest", "grimling"),
        168: ("Marus Seru", "mseru"),
        169: ("Mons Letalis", "letalis"),
        170: ("Twilight Sea", "twilight"),
        171: ("The Grey", "thegrey"),
        172: ("The Tenebrous Mountains", "tenebrous"),
        173: ("The Maiden's Eye", "maiden"),
        174: ("The Dawnshroud Peaks", "dawnshroud"),
        175: ("Scarlet Desert", "scarlet"),
        176: ("The Umbral Plains", "umbral"),
        179: ("Akheva Ruins", "akheva"),
        180: ("The Arena Two", "arena2"),
        181: ("Jaggedpine Forest", "jaggedpine"),
        183: ("EverQuest Tutorial", "tutorial"),
        184: ("Loading Zone", "load"),
        185: ("New Loading Zone", "load2"),
        190: ("Loading", "clz"),
    }
    if arg == "long":
        return zones[value][0] if value in zones else "Unknown"

    return zones[value][1] if value in zones else "Unknown"


@register.filter(name="datetime_delta")
def datetime_delta(value):
    return datetime.timedelta(seconds=value) if value else value


@register.filter(name="datetime_from_timestamp")
def datetime_delta(value):
    return datetime.datetime.fromtimestamp(int(value)) if value else value


@register.filter(name='guild_rank')
def guild_rank_filter(value):
    guild_ranks = {
        0: "Member",
        1: "Officer",
        2: "Leader",
    }
    return guild_ranks[value] if value in guild_ranks else "Unknown"


@register.filter(name="expansion_icon")
def expansion_icon(value):
    expansion_icons = {
        -2: "script", # This is set custom in the view
        -1: "default",
        0: "Original.gif",
        1: "Kunarkicon.gif",
        2: "Veliousicon.gif",
        3: "Luclinicon.gif",
        4: "Powericon.gif",
        5: "Ykeshaicon.gif",
        6: "Ldonicon.gif"
    }
    return expansion_icons[value] if value in expansion_icons else None

@register.filter(name="expansion_name")
def expansion_name(value):
    expansion_icons = {
        -2: "script", # This is set custom in the view
        -1: "default",
        0: "vanilla",
        1: "kunark",
        2: "velious",
        3: "luclin",
        4: "planes",
        5: "ykesha",
        6: "ldon"
    }
    return expansion_icons[value] if value in expansion_icons else None


@register.filter(name="faction_level")
def faction_level(value):
    try:
        value = int(value)
    except ValueError:
        return None
    if value >= 2000:
        return "Max Ally"
    elif value >= 1100:
        return "Ally"
    elif 750 <= value <= 1099:
        return "Warmly"
    elif 500 <= value <= 749:
        return "Kindly"
    elif 100 <= value <= 499:
        return "Amiably"
    elif 0 <= value <= 99:
        return "Indifferently"
    elif -100 <= value <= -1:
        return "Apprehensively"
    elif -500 <= value <= -101:
        return "Dubiously"
    elif -750 <= value <= -501:
        return "Threateningly"
    elif -1999 <= value <= -500:
        return "Scowls"
    else:
        return "Max Scowls"


@register.filter(name="npc_special_ability")
def npc_special_ability(values):
    """Convert NPC special ability codes into HTML for human consumption"""
    if values is None:
        return ''

    npc_special_abilities = {
        0: 'None',
        1: 'Summon',
        2: 'Enrage',
        3: 'Rampage',
        4: 'Area Rampage',
        5: 'Flurry',
        6: 'Triple Attack',
        7: 'Quad Attack',
        8: 'Dual Wield',
        9: 'Bane Attack',
        10: 'Magical Attack',
        11: 'Ranged Attack',
        12: 'Unslowable',
        13: 'Unmezable',
        14: 'Uncharmable',
        15: 'Unstunable',
        16: 'Unsnareable',
        17: 'Unfearable',
        18: 'Immune to Dispell',
        19: 'Immune to Melee',
        20: 'Immune to Magic',
        21: 'Immune to Fleeing',
        22: 'Immune to Non-Bane Damage',
        23: 'Immune to Non-Magical Damage',
        24: 'Will Not Aggro',
        25: 'Immune to Aggro',
        26: 'Resist Ranged Spells',
        27: 'See through Feign Death',
        28: 'Immune to Taunt',
        29: 'Tunnel Vision',
        30: 'Does NOT buff/heal friends',
        31: 'Unpacifiable',
        32: 'Leashed',
        33: 'Tethered',
        34: 'Destructible Object',
        35: 'No Harm from Players',
        36: 'Always Flee',
        37: 'Flee Percentage',
        38: 'Allow Beneficial',
        39: 'Disable Melee',
        40: 'Chase Distance',
        41: 'Allow Tank',
        42: 'Ignore Root Aggro',
        43: 'Casting Resist Diff',
        44: 'Counter Avoid Damage',
        45: 'Proximity Aggro',
        46: 'Immune Ranged Attacks',
        47: 'Immune Client Damage',
        48: 'Immune NPC Damage',
        49: 'Immune Client Aggro',
        50: 'Immune NPC Aggro'
    }

    result = list()
    abilities = values.split('^')
    for ability in abilities:
        codes = ability.split(',')
        try:
            ability_code = codes[0].strip()
            ability = npc_special_abilities[int(ability_code)]
            html = (f'<button class="ability-button npc_special_ability list-group-item list-group-item-action d-inline-flex align-items-center gap-2" '
                    f'data-url="{ability}" type="button">'
                    f'{ability}'
                    f'</button>')
            result.append(html)
        except (IndexError, ValueError, KeyError) as e:
            logger.warning(f"Error processing NPC ability '{ability}': {e}")
            continue
    return ''.join(result)


@register.filter(name="multiply")
def multiply(value, arg):
    return value * arg

@register.filter(name="divide")
def divide(value, arg):
    try:
        return float(value) / float(arg) if float(arg) != 0 else ''
    except (ValueError, TypeError):
        return ''

@register.filter(name="split")
def split(value, arg):
    return value.split(arg)

@register.filter(name="dict_get")
def dict_get(d, key):
    return d.get(key)

