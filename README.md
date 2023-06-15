# Auto-Label-Generator
Automatic Label Printer for the ITS Depot

## First Setup:
  Create the following text files in the directory:
  ```
  out_mac.txt
  out_note.txt
  out_username.txt
  out.txt
  .env
  ```
  Add the following variables to the .env: `app_username` and `app_password` which are the gmail API keys.

## Activate:
  `python parse.py`
  or
  run `STARTSCRIPT.bat`
  
## Usage:
  1. Navigate to Service Now RITM
  2. Click print label
  3. Script will print label
  
## Notes:
  If a certain department keeps showing up as blank in the pc name, ex `___-sssaraiy-___`, the script cannot find a department that matches with at least 70% similarity.
  Departments can be added in departments.csv with the following format:
  `DEPTNAME,ABBREVIATION`
  Example: `Information Technology,ITS`
