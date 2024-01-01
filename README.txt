NAV TXT Object Explorer 

Given a selected file, this shows all objects identified in that file. Expand each object to find certain key sections, and functions,  clicking a point-of-interest
in the tree will take you to that part in the relevant object's code.  Search results also show up in the tree view too.

Search is subtractive, it removes non-matching objects each time.  (think NAV setrange). The thing you last searched for is added as child item of the object. "Clear search" to start again.

Tested with NAV 2013 TXT export. Definitely won't work with AL files, but not far off.  Although VS Code probably has better tools for this.

You can change the 'KEYWORDS' list at the top of the script, if you want to highlight other things,  and you can uncomment the appropriate code in the main function to open a file by default.

Disclaimers:
99% coded by ChatGPT (in parts) and assembled by me, the result is not optimal or pretty but it loads a ~300mb object file in a few seconds and does the job.  

Quite naive about how it identifies objects and procedures, there are almost certainly things you could do in code that would break this (Like having a variable called 'OBJECT') the vanilla NAV 2013 GB codebase seems to load fine.  
If you do stupid things like search for 'e' it will oblige, with hilarious results.

Helper scripts also included for generating the icons, and for concatenating text files with the appropriate encoding.

