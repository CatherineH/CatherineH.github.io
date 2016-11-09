from operator import itemgetter
from os.path import expanduser
from sys import argv

all_lvds_input_file = expanduser("~/all_lvds.tcl")
accessible_lvds_input_file = expanduser("~/accessible_lvds.tcl")
output_input_file = expanduser("~/output_lvds.tcl")


draft_in = open("../_drafts/2016-11-08-picking-lvds-pins-on-the-de0-nano.md",
                    "r").read(-1)

def parse_tcl(filename):
    p_pin_list = {}
    n_pin_list = {}
    f_lines = open(filename, "r'").readlines()

    for line in f_lines:
        if line.find("PIN_") > 0 and line.find('tmds') > 0:
            lvds_name = line.split(" -to ")[1].strip()
            lvds_number = lvds_name.split("[")[1].split("]")[0]
            pin_name = line.split(" -to ")[0].split("PIN_")[1]
            if lvds_name.find("(n)") > 0:
                p_pin_list[lvds_number] = pin_name
            else:
                n_pin_list[lvds_number] = pin_name
    return [p_pin_list, n_pin_list]

[p_pin_list, n_pin_list] = parse_tcl(all_lvds_input_file)
[accessible_p_pin_list, accessible_n_pin_list] = parse_tcl(accessible_lvds_input_file)
[output_p_pin_list, output_n_pin_list] = parse_tcl(output_input_file)

def generate_table(p_pin_list, n_pin_list, compare_p_pin_list=None,
                   compare_n_pin_list=None):
    # let's make a 6x8 table
    current_pin = 0
    num_pins = len(p_pin_list.keys())
    sorted_pins = sorted(p_pin_list.items(), key=itemgetter(1))

    table_html = "<table border=\"1\">"
    ok_color = "#AAFFA0"
    bad_color ="#FFAAA0"

    for i in range(0, 6):
        table_html += "<tr>"
        for j in range(0, 8):
            current_index = i*8+j
            if current_index < num_pins:
                pin_num = sorted_pins[current_index][0]
                color = ok_color
                if compare_p_pin_list is not None:
                    if pin_num not in compare_p_pin_list.keys():
                        color = bad_color
                table_html += '<td style = "background-color: {};">({},\t' \
                              '{})</td>'.format(color,
                                                 p_pin_list[pin_num],
                                                 n_pin_list[pin_num])
            else:
                table_html += "<td></td>"
        table_html += "</tr>"
    table_html += "</table>"
    return table_html

all_pins_html = generate_table(p_pin_list, n_pin_list)
only_gpio_html = generate_table(p_pin_list, n_pin_list, accessible_p_pin_list,
                                accessible_n_pin_list)
output_only_html = generate_table(p_pin_list, n_pin_list, output_p_pin_list,
                                  output_n_pin_list)
draft_in = draft_in.replace("$ALL_PINS$", all_pins_html)
draft_in = draft_in.replace("$ACCESSIBLE_PINS$", only_gpio_html)
draft_in = draft_in.replace("$OUTPUT_PINS$", output_only_html)



f_handle_post = open("../_posts/2016-11-08-picking-lvds-pins-on-the-de0-nano.md", "w+")
f_handle_post.write(draft_in)
f_handle_post.close()