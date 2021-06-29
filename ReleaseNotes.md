# Release Notes #



## RC-3 ##

+ Rewrote the backend that represents the "template" file using python dataclasses
+ Display error message in proper context	
+ Fixed CheckBox now allowing the custom inputs on the create template side to be disabled Changed the usetreemodel's checklist breaking the list, but instead putting up a warning on all the items missing.	
+ Bug Fix #25 Solution: Now switches back to Create Template when restoring Template	
+ Bug Fix #25: Switch UI to "Use Template" when opening a package Solution: Added a line to switch over to Use Template	
+ Bug Fix #20: Packages Save/Save as... Solution: Changed names from Save Package to Save Package as	
+ Bug Fix #24:HT Names for custom fields not showing up on the "Use Template" UI Solution Seperate Statement for Custom Inputs
Changed Use Template so that only newly created Custom Inputs can be deleted Added Remove All Rows when a new extracted file is put in Changed certain names to their ENUMS	
+ Changed Add Extracted Metadata File To File List's Default to enabled	
+ Bug Fix #13: After restore template, if a new data file is selected, then any custom fields are removed Solution: added a list of custom inputs that can be added back into new files	
+ Bug Fix #19: Checkbox to auto include parsed file on "Use Template"	
+ Bug Fix #18: If 'Use Source' is unchecked, then HT Value should be used.
+ Reverted open and save package to taking ez files and made sure it took self.editables
+ changed naming of dialog to fileName
+ Fixed data type and data parser not changing when restoring a template
+ Bug Fix #5: Create Template: Tri-state checkbox should appear in file tree for parents that have some children checked and some children unchecked.
+ Bug Fix #16: MetaData values that are "arrays" of values (LatticeConstants) are not being parsed into the UseTemplate Table. Solution: Lines were being parsed and uploaded to HyperThought, it was not being displayed as a string in the tableview.
+ Bug Fix #9 Defined custom fields are not showing up on the Use Template side Solution: Now adds in custom inputs as existing and copies everything over


## RC-4 ##

+ Restore Application Icon and other icons
+ Add a few Jupyter Notebooks that show how to programmatically create models and upload them to HT	
+ Remove debugging print statementsAM


## RC-5 ##

+ Bug Fix #14 Keyboard Shortcuts:	
+ Bug Fix #14: Add "command-s" to save a template file and other keyboard shortcuts Solution: Added a ctrl+s to save a template.
+ Small adjustments to column naming
+ Bug Fix #7: Resize columns to fill the table space in a way that makes sense, and wrap header labels.	
+ Bug Fix: Check boxes uncentered. Solution: Added back in Checkbox delegates. Also wrapped value column data in string wrappers to see the List from Lattice Constants
+ Bug Fix #13: Allow upload to HT if NO “Other Data file” was selected. I.e. a pure custom template. Solution: Got rid of the rule to look for the other data file line edit to be empty
+ Bug Fix: Putting back the trash icons
+ Updating File menu item names to be more consistent.
