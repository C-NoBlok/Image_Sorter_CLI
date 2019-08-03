# Image Sorter CLI

This CLI tool was written to parse through folder recovered from [TestDisk](https://www.cgsecurity.org/wiki/TestDisk).  TestDisk is a great open source tool for recovering data from hard disks.  It is particularly effective at reclaiming data from a hard disk that had accidentally been formated. TestDisk is capabale of searching through a hard disk and retrieving all the data stored on it.  The challenge is then sifting through all the various files for important ones (Pictures).  

This Image sorting tools will walk through a folder directory and move all files with a specific extention to a new folder.  Filters can be set to only fetch images greater than a particular resolution.  This will help to filter out thumbnail images, icons, and other various assets. This was mainly to fetch images but could be used for other file types as well.


<b>Python: 3.6 or greater</b>

    python img_sorter.py image -h