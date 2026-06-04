import memory_graph as mg

elements = ['<B>bold</B>', 
            '<I>italic</I>', 
            '<S>strikethrough</S>',
            '<U>under</U><O>over</O>',
            '<SUB>sub</SUB><SUP>sup</SUP>',
            '<FONT FACE="Courier">monospaced</FONT>', 
            '<FONT COLOR="red">red</FONT><FONT COLOR="blue">blue</FONT>',
            '<FONT POINT-SIZE="20">Large</FONT><FONT POINT-SIZE="10">small</FONT>',
            '<TABLE BORDER="1"><TR><TD>c1</TD><TD>c2</TD></TR></TABLE>',
            'line1<BR/>line2<BR/>line3<BR/>'
            ]

normal_str = '<TABLE BORDER="0">\n'
for element in elements:
    normal_str += '<TR><TD> ' + mg.utils.html_escape(element) + ' </TD><TD> ' + element+ ' </TD></TR>element\n' 
normal_str += '</TABLE>\n'

html_example = mg.html_str(normal_str)
del elements, element, normal_str
mg.render(locals(), "html_example.png")