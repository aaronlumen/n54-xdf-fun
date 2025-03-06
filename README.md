# n54-xdf-fun
XDF customizer - category renamer, this tool allows you to choose certain table names and categories as well as tune math used to program or tune n54 bmw 335i roadsters

Usage Summary

    Place this script in the same folder as your I8A0S Custom.xdf file.
    Run the script.
        It will prompt you for which features you want to rename or toggle.
    The script writes out a new .xdf (e.g., I8A0S_Custom_HighPerformance.xdf) containing your updated naming / “fastest race mode” text.

How This Script Works

  Parsing XML
  
        We use Python’s xml.etree.ElementTree to parse the XDF, which is essentially an XML file.

    Renaming Categories
        The <CATEGORY> elements are children of <XDFHEADER> in the XDF.
        The script loops through them, checks if the name attribute is in our rename_map, and if so, updates it.

    Renaming Table Titles
        Each parameter table is represented by <XDFTABLE> elements in the XDF.
        We find the <title> child element, check if the old title matches some pattern or text, and then rename it.
        You can customize this logic to rename or otherwise modify descriptions, addresses, or scaling.

    Optional “High-Performance” Param Changes
        Example lines (currently commented out) show how you could adjust numeric fields like max or the address/scaling in <EMBEDDEDDATA>.
        This is how you might remove OEM “caps” for boost, torque, or rev limits.

    Prompting the User
        The script is interactive. It asks for new category titles. If the user hits Enter, we apply default “RACE” naming.
        You can expand this to prompt for many more items (like ignition scaling, fueling, etc.) and apply them in code.

    Output
        The script writes a new .xdf file, preserving the structure but reflecting your “race mode” renames.
Future Extending for Performance Edits

To truly create a one-click “fastest race mode,” we might:

    Prompt for “target max boost” or “desired load limit,” then go find any <XDFTABLE> that stores the relevant limit.
    Adjust the <max> element or <MATH> scale factor.
    Update embedded addresses or data for fueling or ignition timing if you know the hex offsets.

This is more advanced because each table has distinct addresses, row/col counts, etc. We’ll need to confirm them from the XDF definition or tuning references.
Important Notes

    Backup your original .xdf before editing.
    If you also want to directly change the underlying BIN (the actual calibration data) via script, that’s a different workflow. The XDF is just a definition map telling TunerPro how to interpret the BIN.
    Using this script, you can rename categories, add “RACE” flair, or unify parameter naming to be more user-friendly for track cars. Then, when you open TunerPro, you’ll see your newly labeled categories/parameters.
