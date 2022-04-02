#!/usr/bin/env python3

import xmltodict
import os
import argparse

parts_list = []


def process_parts_list_from_file(file, arg):
    if file == "result.xml":
        return

    print(f"Processing {file}")
    f = open(file, "r")
    part_list = xmltodict.parse(f.read())
    part_list_items = part_list["INVENTORY"]["ITEM"]

    # todo: handle MAXPRICE and NOTIFY

    if arg.condition:
        i = 0
        for key in part_list_items:
            part_list_items[i]["CONDITION"] = arg.condition
            i = i + 1

    # Process the list
    for inventory_item in part_list_items:
        contains_match = False
        for main_list in parts_list:
            if inventory_item["ITEMTYPE"] == main_list["ITEMTYPE"] and \
                    inventory_item["ITEMID"] == main_list["ITEMID"] and \
                    inventory_item["COLOR"] == main_list["COLOR"] and \
                    inventory_item["CONDITION"] == main_list["CONDITION"]:
                contains_match = True
                main_list["MINQTY"] = str(int(inventory_item["MINQTY"]) + int(main_list["MINQTY"]))
                break

        if not contains_match:
            parts_list.append(inventory_item)


def process_extra_args(arg):
    for inventory_item in parts_list:
        if arg.add_extra > 0:
            inventory_item["MINQTY"] = str(int(inventory_item["MINQTY"]) + arg.add_extra)
        if arg.min_qty > 0 and int(inventory_item["MINQTY"]) < arg.min_qty:
            inventory_item["MINQTY"] = str(arg.min_qty)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('--add_extra', type=int, help='Add extra quantity to all the parts', default=0)
    parser.add_argument('--min_qty', type=int, help='Minimum quantity to be applied', default=0)
    parser.add_argument('--path', type=str, help='Path to read from', default='.')
    parser.add_argument('--condition', type=str, help='Override all conditions to this value')

    args = parser.parse_args()

    # Set the path
    path = args.path

    # Process the xml files
    for x in os.listdir(path):
        if x.endswith(".xml"):  # only select xml files
            process_parts_list_from_file(x, args)

    # Process any extra arguments
    process_extra_args(args)

    # Generate XML
    xml = "<INVENTORY>\n"

    for part in parts_list:
        xml = f"""{xml}
<ITEM>
<ITEMTYPE>{part["ITEMTYPE"]}</ITEMTYPE>
<ITEMID>{part["ITEMID"]}</ITEMID>
<COLOR>{part["COLOR"]}</COLOR>
<MAXPRICE>{part["MAXPRICE"]}</MAXPRICE>
<MINQTY>{part["MINQTY"]}</MINQTY>
<CONDITION>{part["CONDITION"]}</CONDITION>
<NOTIFY>{part["NOTIFY"]}</NOTIFY>
</ITEM>        
        """

    xml = f"{xml}\n</INVENTORY>"

    # Write xml to a file
    text_file = open("result.xml", "w")
    n = text_file.write(xml)
    text_file.close()
