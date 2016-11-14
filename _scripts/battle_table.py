from os.path import expanduser, dirname, basename, join
from sys import argv

ranking_changes_filename = expanduser(argv[1])
ranking_filename = expanduser(argv[2])
post_content_filename = expanduser(argv[3])

changes_lines = open(ranking_changes_filename, "r").readlines()
ranking_lines = open(ranking_filename, "r").readlines()
post_content = open(post_content_filename, "r").read(-1)
post_name = basename(post_content_filename).replace(".draft", "")
post_name = join(dirname(dirname(dirname(post_content_filename))), post_name)
asset_folder = join(dirname(post_name), "assets/images")

ranks = []
changed_bands_start = False
new_bands_start = False
new_bands = []
changed_bands = {}

for i in range(0, len(changes_lines)):
    parts = changes_lines[i].split(",")
    if changed_bands_start:
        band = (",".join(parts[0:-1]).replace("(", "")[:-1])[1:].decode("unicode_escape")
        ranking = parts[-1][:-1].replace(")", "").replace("'", "")
        band = ''.join(chr(ord(c)) for c in band).decode('utf8')
        changed_bands[band] = int(float(ranking))
    if new_bands_start:
        band = parts[0].replace("('", "")[:-1]
        new_bands.append(band)

    if changes_lines[i].find("New Bands") == 0:
        changed_bands_start = False
        new_bands_start = True
    if changes_lines[i].find("Changed Ranks") == 0:
        changed_bands_start = True
        new_bands_start = False

start_appending = False

for i in range(0, len(ranking_lines)):
    if start_appending and ranking_lines[i].find("Rank") < 0:
        ranks.append(" ".join(ranking_lines[i].split("\t")[0].split(" ")[1:]))
    if len(ranks) >= 100:
        break
    if ranking_lines[i].find("Combined Ranking") >= 0:
        start_appending = True
font_size = 50

green = "#24631e"
red = "#63241E"
yellow = "#63631e"
grey = "#969696"
arrow_font = "style=\"font-family: Verdana; font-size: "+str(font_size*0.8)+"px;" \
             " stroke: #ffffff; fill: #ffffff;\""
#'down_arrow'
icon_filenames = {'up': 'up_arrow', 'down': 'down_arrow', 'new': 'new', 'same': 'same'}
icon_colors = {'up': green, 'down': red, 'new': yellow, 'same': grey}


def format_icon(icon_type, rank_change=0):

    table_str = open(join(asset_folder, icon_filenames[icon_type]+".svg"))\
                .read(-1).replace(grey, icon_colors[icon_type])
    if rank_change != 0:
        y_pos = int(font_size - (font_size - font_size*0.8)/2.0)
        table_str = table_str.replace("</svg>",
                                     "<text text-anchor=\"middle\" x=\"25\" y=\""+str(y_pos)+"\" "
                                                + arrow_font + ">"+ str(abs(rank_change)) + "</text></svg>")
    return table_str



table_out = "<table>"
for i in range(len(ranks)):
    ranks[i] = ''.join(chr(ord(c)) for c in ranks[i]).decode('utf8')
    #ranks[i] = repr(ranks[i])[1:-1]
    table_out += "<tr><td><font size='"+str(font_size)+"'>"+str(i+1)+"</font></td><td>"
    if ranks[i] in new_bands:
        table_out += format_icon('new')
    elif ranks[i] in changed_bands.keys():
        if changed_bands[ranks[i]] > 0:
            table_out += format_icon('up', changed_bands[ranks[i]])
        elif changed_bands[ranks[i]] < 0:
            table_out += format_icon('down', changed_bands[ranks[i]])
        else:
            table_out += format_icon('same', changed_bands[ranks[i]])
    else:
        print(ranks[i]+" not found, "+str(type(ranks[i])))
    table_out += "</td><td><font size='"+str(font_size)+"'>"+ranks[i].encode('ascii', 'xmlcharrefreplace')+"</font></td></tr>\n"
table_out += "</table>"

post_content = post_content.replace("$BATTLE_ROYALE$", table_out)
print("post name: ", post_name)
open(post_name, "w+").write(post_content)


