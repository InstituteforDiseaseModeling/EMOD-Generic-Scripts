# *****************************************************************************
#
# *****************************************************************************


# Rules for name cleaning
def reprule(revval):

    # Upper case
    revval = revval.upper()

    # Diacritics
    revval = revval.replace('Â', 'A')
    revval = revval.replace('Á', 'A')
    revval = revval.replace('Ç', 'C')
    revval = revval.replace('Ê', 'E')
    revval = revval.replace('É', 'E')
    revval = revval.replace('È', 'E')
    revval = revval.replace('Ï', 'I')
    revval = revval.replace('Ã¯', 'I')
    revval = revval.replace('Í', 'I')
    revval = revval.replace('Ñ', 'NY')
    revval = revval.replace('Ô', 'O')
    revval = revval.replace('Ó', 'O')
    revval = revval.replace('Ü', 'U')
    revval = revval.replace('Û', 'U')
    revval = revval.replace('Ú', 'U')

    # Alias characters to underscore
    revval = revval.replace(' ', '_')
    revval = revval.replace('-', '_')
    revval = revval.replace('/', '_')
    revval = revval.replace(',', '_')
    revval = revval.replace('\\', '_')

    # Remove ASCII characters
    revval = revval.replace('\'',   '')
    revval = revval.replace('"',    '')
    revval = revval.replace('’',    '')
    revval = revval.replace('.',    '')
    revval = revval.replace('(',    '')
    revval = revval.replace(')',    '')
    revval = revval.replace('\x00', '')

    # Remove non-ASCII characters
    revval = revval.encode('ascii', 'replace')
    revval = revval.decode()
    revval = revval.replace('?', '')

    # Condence and strip underscore characters
    while (revval.count('__')):
        revval = revval.replace('__', '_')
    revval = revval.strip('_')

    return revval

# *****************************************************************************


# Dictionary of UN WPP names
tlc_wpp_dict = {
    "SSA": "SUB_SAHARAN_AFRICA",

    "ABW": "ARUBA",
    "AFG": "AFGHANISTAN",
    "AGO": "ANGOLA",
    "AIA": "ANGUILLA",
    "ALB": "ALBANIA",
    "AND": "ANDORRA",
    "ARE": "UNITED_ARAB_EMIRATES",
    "ARG": "ARGENTINA",
    "ARM": "ARMENIA",
    "ASM": "AMERICAN_SAMOA",
    "ATG": "ANTIGUA_AND_BARBUDA",
    "AUS": "AUSTRALIA",
    "AUT": "AUSTRIA",
    "AZE": "AZERBAIJAN",
    "BDI": "BURUNDI",
    "BEL": "BELGIUM",
    "BEN": "BENIN",
    "BES": "BONAIRE_SINT_EUSTATIUS_AND_SABA",
    "BFA": "BURKINA_FASO",
    "BGD": "BANGLADESH",
    "BGR": "BULGARIA",
    "BHR": "BAHRAIN",
    "BHS": "BAHAMAS",
    "BIH": "BOSNIA_AND_HERZEGOVINA",
    "BLM": "SAINT_BARTHELEMY",
    "BLR": "BELARUS",
    "BLZ": "BELIZE",
    "BMU": "BERMUDA",
    "BOL": "BOLIVIA_PLURINATIONAL_STATE_OF",
    "BRA": "BRAZIL",
    "BRB": "BARBADOS",
    "BRN": "BRUNEI_DARUSSALAM",
    "BTN": "BHUTAN",
    "BWA": "BOTSWANA",
    "CAF": "CENTRAL_AFRICAN_REPUBLIC",
    "CAN": "CANADA",
    "CHE": "SWITZERLAND",
    "CHL": "CHILE",
    "CHN": "CHINA",
    "CIV": "COTE_DIVOIRE",
    "CMR": "CAMEROON",
    "COD": "DEMOCRATIC_REPUBLIC_OF_THE_CONGO",
    "COG": "CONGO",
    "COK": "COOK_ISLANDS",
    "COL": "COLOMBIA",
    "COM": "COMOROS",
    "CPV": "CABO_VERDE",
    "CRI": "COSTA_RICA",
    "CUB": "CUBA",
    "CUW": "CURACAO",
    "CYM": "CAYMAN_ISLANDS",
    "CYP": "CYPRUS",
    "CZE": "CZECHIA",
    "DEU": "GERMANY",
    "DJI": "DJIBOUTI",
    "DMA": "DOMINICA",
    "DNK": "DENMARK",
    "DOM": "DOMINICAN_REPUBLIC",
    "DZA": "ALGERIA",
    "ECU": "ECUADOR",
    "EGY": "EGYPT",
    "ERI": "ERITREA",
    "ESH": "WESTERN_SAHARA",
    "ESP": "SPAIN",
    "EST": "ESTONIA",
    "ETH": "ETHIOPIA",
    "FIN": "FINLAND",
    "FJI": "FIJI",
    "FLK": "FALKLAND_ISLANDS_MALVINAS",
    "FRA": "FRANCE",
    "FRO": "FAROE_ISLANDS",
    "FSM": "MICRONESIA_FED_STATES_OF",
    "GAB": "GABON",
    "GBR": "UNITED_KINGDOM",
    "GEO": "GEORGIA",
    "GGY": "GUERNSEY",
    "GHA": "GHANA",
    "GIB": "GIBRALTAR",
    "GIN": "GUINEA",
    "GLP": "GUADELOUPE",
    "GMB": "GAMBIA",
    "GNB": "GUINEA_BISSAU",
    "GNQ": "EQUATORIAL_GUINEA",
    "GRC": "GREECE",
    "GRD": "GRENADA",
    "GRL": "GREENLAND",
    "GTM": "GUATEMALA",
    "GUF": "FRENCH_GUIANA",
    "GUM": "GUAM",
    "GUY": "GUYANA",
    "HKG": "CHINA_HONG_KONG_SAR",
    "HND": "HONDURAS",
    "HRV": "CROATIA",
    "HTI": "HAITI",
    "HUN": "HUNGARY",
    "IDN": "INDONESIA",
    "IMN": "ISLE_OF_MAN",
    "IND": "INDIA",
    "IRL": "IRELAND",
    "IRN": "IRAN_ISLAMIC_REPUBLIC_OF",
    "IRQ": "IRAQ",
    "ISL": "ICELAND",
    "ISR": "ISRAEL",
    "ITA": "ITALY",
    "JAM": "JAMAICA",
    "JEY": "JERSEY",
    "JOR": "JORDAN",
    "JPN": "JAPAN",
    "KAZ": "KAZAKHSTAN",
    "KEN": "KENYA",
    "KGZ": "KYRGYZSTAN",
    "KHM": "CAMBODIA",
    "KIR": "KIRIBATI",
    "KNA": "SAINT_KITTS_AND_NEVIS",
    "KOR": "REPUBLIC_OF_KOREA",
    "KWT": "KUWAIT",
    "LAO": "LAO_PEOPLES_DEMOCRATIC_REPUBLIC",
    "LBN": "LEBANON",
    "LBR": "LIBERIA",
    "LBY": "LIBYA",
    "LCA": "SAINT_LUCIA",
    "LIE": "LIECHTENSTEIN",
    "LKA": "SRI_LANKA",
    "LSO": "LESOTHO",
    "LTU": "LITHUANIA",
    "LUX": "LUXEMBOURG",
    "LVA": "LATVIA",
    "MAC": "CHINA_MACAO_SAR",
    "MAF": "SAINT_MARTIN_FRENCH_PART",
    "MAR": "MOROCCO",
    "MCO": "MONACO",
    "MDA": "REPUBLIC_OF_MOLDOVA",
    "MDG": "MADAGASCAR",
    "MDV": "MALDIVES",
    "MEX": "MEXICO",
    "MHL": "MARSHALL_ISLANDS",
    "MKD": "NORTH_MACEDONIA",
    "MLI": "MALI",
    "MLT": "MALTA",
    "MMR": "MYANMAR",
    "MNE": "MONTENEGRO",
    "MNG": "MONGOLIA",
    "MNP": "NORTHERN_MARIANA_ISLANDS",
    "MOZ": "MOZAMBIQUE",
    "MRT": "MAURITANIA",
    "MSR": "MONTSERRAT",
    "MTQ": "MARTINIQUE",
    "MUS": "MAURITIUS",
    "MWI": "MALAWI",
    "MYS": "MALAYSIA",
    "MYT": "MAYOTTE",
    "NAM": "NAMIBIA",
    "NCL": "NEW_CALEDONIA",
    "NER": "NIGER",
    "NGA": "NIGERIA",
    "NIC": "NICARAGUA",
    "NIU": "NIUE",
    "NLD": "NETHERLANDS",
    "NOR": "NORWAY",
    "NPL": "NEPAL",
    "NRU": "NAURU",
    "NZL": "NEW_ZEALAND",
    "OMN": "OMAN",
    "PAK": "PAKISTAN",
    "PAN": "PANAMA",
    "PER": "PERU",
    "PHL": "PHILIPPINES",
    "PLW": "PALAU",
    "PNG": "PAPUA_NEW_GUINEA",
    "POL": "POLAND",
    "PRI": "PUERTO_RICO",
    "PRK": "DEM_PEOPLES_REPUBLIC_OF_KOREA",
    "PRT": "PORTUGAL",
    "PRY": "PARAGUAY",
    "PSE": "STATE_OF_PALESTINE",
    "PYF": "FRENCH_POLYNESIA",
    "QAT": "QATAR",
    "REU": "REUNION",
    "ROU": "ROMANIA",
    "RUS": "RUSSIAN_FEDERATION",
    "RWA": "RWANDA",
    "SAU": "SAUDI_ARABIA",
    "SDN": "SUDAN",
    "SEN": "SENEGAL",
    "SGP": "SINGAPORE",
    "SHN": "SAINT_HELENA",
    "SLB": "SOLOMON_ISLANDS",
    "SLE": "SIERRA_LEONE",
    "SLV": "EL_SALVADOR",
    "SMR": "SAN_MARINO",
    "SOM": "SOMALIA",
    "SPM": "SAINT_PIERRE_AND_MIQUELON",
    "SRB": "SERBIA",
    "SSD": "SOUTH_SUDAN",
    "STP": "SAO_TOME_AND_PRINCIPE",
    "SUR": "SURINAME",
    "SVK": "SLOVAKIA",
    "SVN": "SLOVENIA",
    "SWE": "SWEDEN",
    "SWZ": "ESWATINI",
    "SXM": "SINT_MAARTEN_DUTCH_PART",
    "SYC": "SEYCHELLES",
    "SYR": "SYRIAN_ARAB_REPUBLIC",
    "TCA": "TURKS_AND_CAICOS_ISLANDS",
    "TCD": "CHAD",
    "TGO": "TOGO",
    "THA": "THAILAND",
    "TJK": "TAJIKISTAN",
    "TKL": "TOKELAU",
    "TKM": "TURKMENISTAN",
    "TLS": "TIMOR_LESTE",
    "TON": "TONGA",
    "TTO": "TRINIDAD_AND_TOBAGO",
    "TUN": "TUNISIA",
    "TUR": "TURKIYE",
    "TUV": "TUVALU",
    "TWN": "CHINA_TAIWAN_PROVINCE_OF_CHINA",
    "TZA": "UNITED_REPUBLIC_OF_TANZANIA",
    "UGA": "UGANDA",
    "UKR": "UKRAINE",
    "URY": "URUGUAY",
    "USA": "UNITED_STATES_OF_AMERICA",
    "UZB": "UZBEKISTAN",
    "VCT": "SAINT_VINCENT_AND_THE_GRENADINES",
    "VEN": "VENEZUELA_BOLIVARIAN_REPUBLIC_OF",
    "VGB": "BRITISH_VIRGIN_ISLANDS",
    "VIR": "UNITED_STATES_VIRGIN_ISLANDS",
    "VNM": "VIET_NAM",
    "VUT": "VANUATU",
    "WLF": "WALLIS_AND_FUTUNA_ISLANDS",
    "WSM": "SAMOA",
    "XKX": "KOSOVO_UNDER_UNSC_RES_1244",
    "YEM": "YEMEN",
    "ZAF": "SOUTH_AFRICA",
    "ZMB": "ZAMBIA",
    "ZWE": "ZIMBABWE"
}

# *****************************************************************************


# Dictionary of aliases for DHS regions
dhs_groups = {
  'AFRO:NIGERIA:NORTH_CENTRAL': [
    'AFRO:NIGERIA:BENUE',
    'AFRO:NIGERIA:FCT_ABUJA',
    'AFRO:NIGERIA:KOGI',
    'AFRO:NIGERIA:KWARA',
    'AFRO:NIGERIA:NASARAWA',
    'AFRO:NIGERIA:NIGER',
    'AFRO:NIGERIA:PLATEAU'
  ],
  'AFRO:NIGERIA:NORTH_EAST': [
    'AFRO:NIGERIA:ADAMAWA',
    'AFRO:NIGERIA:BAUCHI',
    'AFRO:NIGERIA:BORNO',
    'AFRO:NIGERIA:GOMBE',
    'AFRO:NIGERIA:TARABA',
    'AFRO:NIGERIA:YOBE'
  ],
  'AFRO:NIGERIA:NORTH_WEST': [
    'AFRO:NIGERIA:JIGAWA',
    'AFRO:NIGERIA:KADUNA',
    'AFRO:NIGERIA:KANO',
    'AFRO:NIGERIA:KATSINA',
    'AFRO:NIGERIA:KEBBI',
    'AFRO:NIGERIA:SOKOTO',
    'AFRO:NIGERIA:ZAMFARA'
  ],
  'AFRO:NIGERIA:SOUTH_EAST': [
    'AFRO:NIGERIA:ABIA',
    'AFRO:NIGERIA:ANAMBRA',
    'AFRO:NIGERIA:EBONYI',
    'AFRO:NIGERIA:ENUGU',
    'AFRO:NIGERIA:IMO'
  ],
  'AFRO:NIGERIA:SOUTH_SOUTH': [
    'AFRO:NIGERIA:AKWA_IBOM',
    'AFRO:NIGERIA:BAYELSA',
    'AFRO:NIGERIA:CROSS_RIVER',
    'AFRO:NIGERIA:DELTA',
    'AFRO:NIGERIA:EDO',
    'AFRO:NIGERIA:RIVERS'
  ],
  'AFRO:NIGERIA:SOUTH_WEST': [
    'AFRO:NIGERIA:EKITI',
    'AFRO:NIGERIA:LAGOS',
    'AFRO:NIGERIA:OGUN',
    'AFRO:NIGERIA:ONDO',
    'AFRO:NIGERIA:OSUN',
    'AFRO:NIGERIA:OYO'
  ]
}

# *****************************************************************************
