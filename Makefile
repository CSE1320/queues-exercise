########################################################################
####################### Makefile Template ##############################
########################################################################
# Student settings
NAME = YOURNAME
SID = YOURSID
EMAIL = YOURUTAEMAIL
SEMESTER = SPRING2024
 

####### DO NOT EDIT BELOW THIS LINE!!! #########
author: 
	@echo $(NAME)
	@echo $(SID)
	@echo $(EMAIL)
	@echo $(SEMESTER)
submit:
	zip -r "submission_$(SEMESTER)_$(SID)_$(NAME).zip" .

install:
	pip install python-benedict

cleanup:
	@rm -f .DS_Store
	@rm -f */.DS_Store
	@rm -f */mysolution
	@rm -rf */mysolution.dSYM
