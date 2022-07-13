#*******************************************************************************

# Rules for name cleaning; supports multiple

def reprule(revval):

  revval = revval.upper()

  revval = revval.replace('Â',    'A')
  revval = revval.replace('Á',    'A')
  revval = revval.replace('Ç',    'C')
  revval = revval.replace('Ê',    'E')
  revval = revval.replace('É',    'E')
  revval = revval.replace('È',    'E')
  revval = revval.replace('Ï',    'I')
  revval = revval.replace('Ã¯',   'I')
  revval = revval.replace('Í',    'I')
  revval = revval.replace('Ñ',    'NY')
  revval = revval.replace('Ô',    'O')
  revval = revval.replace('Ó',    'O')
  revval = revval.replace('Û',    'U')
  revval = revval.replace('Ú',    'U')

  revval = revval.replace(' ',    '_')
  revval = revval.replace('-',    '_')
  revval = revval.replace('/',    '_')
  revval = revval.replace(',',    '_')
  revval = revval.replace('\\',   '_')

  revval = revval.replace('\'',   '')
  revval = revval.replace('"',    '')
  revval = revval.replace('.',    '')
  revval = revval.replace('(',    '')
  revval = revval.replace(')',    '')
  revval = revval.replace('\x00', '')

  while(revval.count('__')):
    revval = revval.replace('__','_')
  revval = revval.strip('_')

  return revval

#*******************************************************************************

# Dictionary of three letter country codes;

tlc_dict = \
{
  'COD':'DEMOCRATIC_REPUBLIC_OF_THE_CONGO',
  'ETH':'ETHIOPIA',
  'GBR':'UNITED_KINGDOM',
  'GHA':'GHANA',
  'IND':'INDIA',
  'NGA':'NIGERIA',
  'PAK':'PAKISTAN'
}

#*******************************************************************************

# Dictionary of aliases for DHS regions; supports multiple

dhs_groups = \
{
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

#*******************************************************************************

# Dictionary of admin01 aliases; supports mc1 coverage estimates
#     IHME GHA uses pre-2018 nameset

adm01_alias_dict = \
{
  'IHME':
  {
    'COD':
    {
    },
    'GHA':
    {
      #
    },
    'NGA':
    {
      'NASSARAWA':'NASARAWA',
      'FEDERAL_CAPITAL_TERRITORY':'FCT_ABUJA'
    }
  }
}

#*******************************************************************************

# Dictionary of admin02 aliases; supports mcv1 coverage estimates
#     IHME GHA uses pre-2018 nameset

adm02_alias_dict = \
{
  'IHME':
  {
    'COD':
    {
    },
    'GHA':
    {
      #'AFIGYA_KWABRE':'',
      #'AFIGYA_SEKYERE':'',
      #'AHAFO_ANO_SOUTH':'',
      #'ATWIMA_NWABIAGYA':'',
      #'BOSOMTWE_ATWIMA_KWANWOMA':'',
      #'EJISU_JUABEN':'',
      #'EJURA_SEKYE_DUMASE':'',
      #'KMA':'',
      #'KWABRE':'',
      #'SEKYERE_AFRAM_PLAINS':''
    },
    'NGA':
    {
      'AROCHUKW':'AROCHUKWU',
      'ISUIKWUA':'ISUIKWUATO',
      'OBOMA_NGWA':'OBI_NGWA',
      'OHAFIA_ABIA':'OHAFIA',
      'GIRIE':'GIREI',
      'MAYO_BEL':'MAYO_BELWA',
      'TEUNGO':'TOUNGO',
      'ESSIEN_U':'ESSIEN_UDIM',
      'ETIMEKPO':'ETIM_EKPO',
      'IKOT_ABA':'IKOT_ABASI',
      'IKOT_EKP':'IKOT_EKPENE',
      'ORUK_ANA':'ORUK_ANAM',
      'URUEOFFO':'URUE_OFFONG_ORUKO',
      'AWKANORT':'AWKA_NORTH',
      'AWKASOUT':'AWKA_SOUTH',
      'NNEWINORT':'NNEWI_NORTH',
      'NNEWISOU':'NNEWI_SOUTH',
      'ORUMBANO':'ORUMBA_NORTH',
      'ORUMBASO':'ORUMBA_SOUTH',
      'GAMJUWA':'GANJUWA',
      'ITAS_GAD':'ITAS_GADAU',
      'TAFAWA_B':'TAFAWA_BALEWA',
      'GWERWEST':'GWER_WEST',
      'KATSINA_BENUE':'KATSINA_ALA',
      'KONSHISH':'KONSHISHA',
      'VANDEIKY':'VANDEIKYA',
      'ASKIRA_U':'ASKIRA_UBA',
      'MAIDUGUR':'MAIDUGURI',
      'CALABAR':'CALABAR_MUNICIPAL',
      'YALA_CROSS':'YALA',
      'ANIOCHAN':'ANIOCHA_NORTH',
      'ANIOCHAS':'ANIOCHA_SOUTH',
      'ETHIOPEE':'ETHIOPE_EAST',
      'IKANORTH':'IKA_NORTH_EAST',
      'ISOKONOR':'ISOKO_NORTH',
      'IKASOUTH':'IKA_SOUTH',
      'ISOKOSOU':'ISOKO_SOUTH',
      'ABAKALIK':'ABAKALIKI',
      'AFIKPO':'AFIKPO_NORTH',
      'AFIKPOSO':'AFIKPO_SOUTH',
      'AKOKO_ED':'AKOKO_EDO',
      'ESANCENT':'ESAN_CENTRAL',
      'ESANNORT':'ESAN_NORTH_EAST',
      'ESANSOUT':'ESAN_SOUTH_EAST',
      'ESANWEST':'ESAN_WEST',
      'ETSAKOEA':'ETSAKO_EAST',
      'ETSAKOWE':'ETSAKO_WEST',
      'OREDO_EDO':'OREDO',
      'ORHIONMW':'ORHIONMWON',
      'OVIANORT':'OVIA_NORTH_EAST',
      'OVIASOUTH_WEST':'OVIA_SOUTH_WEST',
      'OWANWEST':'OWAN_WEST',
      'EKITIEAS':'EKITI_EAST',
      'EKITISOUTH_WEST':'EKITI_SOUTH_WEST',
      'EKITIWEST':'EKITI_WEST',
      'EMURE_ISE_ORUN':'EMURE',
      'GBOYIN':'AIYEKIRE_GBONYIN',
      'ENUGUSOU':'ENUGU_SOUTH',
      'IGBO_ETI':'IGBO_ETITI',
      'ABUJAMUN':'ABUJA_MUNICIPAL',
      'GWAGWALA':'GWAGWALADA',
      'NAFADA':'NAFADA_BAJOGA',
      'YAMALTU':'YAMALTU_DEBA',
      'ABOH_MBA':'ABOH_MBAISE',
      'AHIZU_MB':'AHIAZU_MBAISE',
      'EHIME_MB':'EHIME_MBANO',
      'EZINIHIT':'EZINIHITTE',
      'IDEATONO':'IDEATO_NORTH',
      'IHITTE_U':'IHITTE_UBOMA',
      'ISIALAMB':'ISIALA_MBANO',
      'NGOR_OKP':'NGOR_OKPALA',
      'OHAJI_EG':'OHAJI_EGBEMA',
      'BIRNINKU':'BIRNIN_KUDU',
      'KAFINHAU':'KAFIN_HAUSA',
      'KIRIKASA':'KIRI_KASAMMA',
      'MALAMMAD':'MALAM_MADORI',
      'SULE_TAN':'SULE_TANKARKAR',
      'BIRNIN_G':'BIRNIN_GWARI',
      'SABON_GA':'SABON_GARI',
      'ZANGONKA':'ZANGON_KATAF',
      'DAWAKINK':'DAWAKIN_KUDU',
      'DAWAKINT':'DAWAKIN_TOFA',
      'KANO':'KANO_MUNICIPAL',
      'NASSARAW':'NASARAWA',
      'RIMINGAD':'RIMIN_GADO',
      'TUNDUN_WADA':'TUDUN_WADA',
      'DANMUSA':'DAN_MUSA',
      'DUTSIN_M':'DUTSIN_MA',
      'KANKIYA':'KANKIA',
      'KATSINA_K':'KATSINA',
      'AREWA':'AREWA_DANDI',
      'BIRNINKE':'BIRNIN_KEBBI',
      'DANKO_WASAGU':'WASAGU_DANKO',
      'KOKO_BES':'KOKO_BESSE',
      'KABBA_BU':'KABBA_BUNU',
      'KOTONKAR':'KOGI',
      'OLAMABOR':'OLAMABOLO',
      'ILORINWE':'ILORIN_WEST',
      'BADAGARY':'BADAGRY',
      'LAGOSISLAND':'LAGOS_ISLAND',
      'MAINLAND':'LAGOS_MAINLAND',
      'NASSARAWA_EGON':'NASARAWA_EGON',
      'KONTOGUR':'KONTAGORA',
      'ABEOKUTANORTH':'ABEOKUTA_NORTH',
      'ADOODO_OTA':'ADO_ODO_OTA',
      'EGBADONORTH':'YEWA_NORTH',
      'EGBADOSOUTH':'YEWA_SOUTH',
      'IJEBUEAST':'IJEBU_EAST',
      'IJEBUNORTH':'IJEBU_NORTH',
      'IJEBUODE':'IJEBU_ODE',
      'OGUNWATERSIDE':'OGUN_WATERSIDE',
      'AKOKONORTHWEST':'AKOKO_NORTH_WEST',
      'ILAJEESEODO':'ILAJE',
      'ILEOLUJI_OKEIGBO':'ILE_OLUJI_OKEIGBO',
      'AYEDAADE':'AIYEDADE',
      'AYEDIRE':'AIYEDIRE',
      'IFECENTRAL':'IFE_CENTRAL',
      'ODO0TIN':'ODO_OTIN',
      'IBADANNORTH':'IBADAN_NORTH',
      'IBADANNORTH_EAST':'IBADAN_NORTH_EAST',
      'IBADANNORTH_WEST':'IBADAN_NORTH_WEST',
      'IBADANSOUTH_EAST':'IBADAN_SOUTH_EAST',
      'IBADANSOUTH_WEST':'IBADAN_SOUTH_WEST',
      'OGO_OLUW':'OGO_OLUWA',
      'QUAANPA':'QUAAN_PAN',
      'ABUA_ODU':'ABUA_ODUAL',
      'AKUKUTOR':'AKUKU_TORU',
      'ANDONI_O':'ANDONI',
      'ASARI_TO':'ASARI_TORU',
      'EMUOHA':'EMOHUA',
      'OBIO_AKP':'OBIO_AKPOR',
      'OGBA_EGBE':'OGBA_EGBEMA_NDONI',
      'GWADABAW':'GWADABAWA',
      'TAMBAWAL':'TAMBUWAL',
      'TANGAZAR':'TANGAZA',
      'KARIM_LA':'KARIM_LAMIDO',
      'BORSARI':'BURSARI',
      'KAURA_NA':'KAURA_NAMODA'
    }
  }
}

#*******************************************************************************
