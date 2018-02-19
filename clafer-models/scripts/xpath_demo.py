from xml.etree import ElementTree as ET

# See https://docs.python.org/2/library/xml.etree.elementtree.html#xpath-support
#   for examples and such
dict_queries = {
    'finish': './/ellipticalfinset/finish',
    'a_motor': './/innertube/motormount/motor[@configid=\'32b1ea4b-0f6c-40bc-9dac-a7ed363b81e3\']',
    'all_finishes': './/*/finish'
}

# Find the finish, but just for the elliptical finset
tree = ET.parse('template.ork')
elliptical_finish = tree.find(dict_queries['finish'])
elliptical_finish.text = 'shiny'

# Write this modification back out
tree.write('xpath_demo_out.xml')

# List all finsets, no matter who owns them
print('')
print ('all matching "finish" elements')
for match in tree.findall(dict_queries['all_finishes']):
    print ('\t' + str(match.tag) + ': ' + str(match.text))

# Find a motor with attribute with a specific value
a_motor = tree.find(dict_queries['a_motor'])
print ('')
print('find a specific motor:')
print(a_motor.attrib['configid'])
