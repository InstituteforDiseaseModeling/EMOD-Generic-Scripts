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

# Dictionary of aliases for DHS regions

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