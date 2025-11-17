#!/usr/bin/env python3
# This tool was created by Aaron Surina for bmw performance tuning and custom engine controller modifications.
# Author: Aaron Surina
# Creature Comforts LLC. 
# SEE FIRST COMMIT DATE #
"""
XDF High-Performance Updater

This script:
1. Reads a BMW N54 XDF (XML) file (like I8A0S Custom.xdf).
2. Prompts the user for certain “high-performance” or “race” customizations.
3. Updates XDF categories, table names, descriptions, etc.
4. Writes a new XDF file with those changes.

You can expand this script to modify table addresses, scaling, or any other
XDF elements for advanced tuning parameters.
"""

import xml.etree.ElementTree as ET
import os
import sys

def prompt_user_for_menu_updates():
    """
    Example function to ask the user which high-performance
    or race-based renaming we should apply to categories/tables.
    
    Returns a dictionary of items to rename. 
    Key = original name (exact match)
    Value = new name (renamed)
    """
    print("Welcome to the XDF High-Performance Updater!")
    print("We will rename certain categories or tables for 'race mode' usage.\n")

    # Just as an example, we prompt for some standard menus commonly used:
    rename_map = {}

    # 1) Boost Control
    rename_boost = input(
        "\nEnter new menu name for 'Boost Control' (press Enter to skip or default to 'RACE: Maximum Boost Control'): "
    ).strip()
    if not rename_boost:
        rename_boost = "RACE: Maximum Boost Control"
    rename_map["Boost Control"] = rename_boost

    # 2) Fuel
    rename_fuel = input(
        "\nEnter new menu name for 'Fuel' (press Enter to skip or default to 'RACE: Fuel & AFR'): "
    ).strip()
    if not rename_fuel:
        rename_fuel = "RACE: Fuel & AFR"
    rename_map["Fuel"] = rename_fuel

    # 3) Ignition
    rename_ign = input(
        "\nEnter new menu name for 'Ignition' (press Enter to skip or default to 'RACE: Spark & Timing'): "
    ).strip()
    if not rename_ign:
        rename_ign = "RACE: Spark & Timing"
    rename_map["Ignition"] = rename_ign

    # 4) Limits
    rename_limits = input(
        "\nEnter new menu name for 'Limits' (press Enter to skip or default to 'RACE: Safety Limits'): "
    ).strip()
    if not rename_limits:
        rename_limits = "RACE: Safety Limits"
    rename_map["Limits"] = rename_limits

    # 5) Optional - You can add more prompts for any category or table

    print("\nCollected rename map for categories:")
    for old, new in rename_map.items():
        print(f"  '{old}' --> '{new}'")

    print("\nWe'll apply these changes to any matching <CATEGORY> 'name' attributes in the XDF.\n")
    return rename_map

def update_xdf_for_high_performance(xdf_path, output_path, rename_map):
    """
    1. Parse the XDF XML at xdf_path
    2. Rename categories (or table titles) per rename_map
    3. Optionally update table descriptions, flags, etc.
    4. Write the new XDF to output_path
    """
    tree = ET.parse(xdf_path)
    root = tree.getroot()

    # --------------------------------------------------------
    # Example: rename <CATEGORY name="XYZ"> to new name
    # --------------------------------------------------------
    # The categories are under <XDFHEADER> → <CATEGORY .../>.
    xdf_header = root.find('XDFHEADER')
    if xdf_header is not None:
        categories = xdf_header.findall('CATEGORY')
        for cat in categories:
            old_name = cat.get('name', '')
            if old_name in rename_map:
                cat.set('name', rename_map[old_name])
                print(f"Renamed CATEGORY '{old_name}' -> '{rename_map[old_name]}'")

    # --------------------------------------------------------
    # Example: rename <XDFTABLE> <title> if it contains certain text
    # (You could do the same for <description>, etc.)
    # --------------------------------------------------------
    tables = root.findall('XDFTABLE')
    for table in tables:
        title_elem = table.find('title')
        if title_elem is not None:
            old_title = title_elem.text
            # For instance, if the title contains "Ignition"
            # we might rename it to "RACE - " prefix, etc.
            # This is fully customizable:
            if old_title and "Ignition" in old_title:
                new_title = f"RACE HIGH PERF {old_title}"
                title_elem.text = new_title
                print(f"Renamed TABLE title '{old_title}' -> '{new_title}'")

            # You can add more logic to rename different table titles
            # based on user prompts or patterns.

    # --------------------------------------------------------
    # Example: you could also manipulate a specific table’s
    # 'mmedaddress' or the numeric scale in <MATH> if you want
    # to automatically raise limits for a race tune.
    #
    # For instance:
    #
    # for table in tables:
    #     zAxis = table.find("XDFAXIS[@id='z']")
    #     if zAxis is not None:
    #         embed = zAxis.find('EMBEDDEDDATA')
    #         if embed is not None:
    #             # Suppose we want to raise 'max' to 300 from 255 for some race table
    #             max_elem = zAxis.find('max')
    #             if max_elem is not None:
    #                 old_val = max_elem.text
    #                 max_elem.text = "300.0"
    #                 print(f"Raised 'max' from {old_val} to 300.0 for table z-axis.")
    #
    # (That is purely illustrative.)

    # Write out the modified file
    tree.write(output_path, encoding="UTF-8", xml_declaration=True)
    print(f"\nSuccessfully wrote updated XDF to: {output_path}")

def main():
    # 1) Check for input file
    xdf_file = "I8A0S Custom.xdf"  # or change to your actual filename
    if not os.path.isfile(xdf_file):
        print(f"Error: {xdf_file} not found in current directory.")
        sys.exit(1)

    # 2) Prompt user for rename instructions
    rename_map = prompt_user_for_menu_updates()

    # 3) Build output filename
    output_file = "I8A0S_Custom_HighPerformance.xdf"

    # 4) Update the XDF
    update_xdf_for_high_performance(xdf_file, output_file, rename_map)

if __name__ == "__main__":
    main()
