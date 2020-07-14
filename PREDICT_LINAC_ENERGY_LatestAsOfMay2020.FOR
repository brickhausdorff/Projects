c	Program Name:		Predict_Linac_Energy
c	Directory Name:		Atlas_Programs:[Predict_Linac_Energy]
c	File Name:		Predict_Linac_Energy.for
c
c	Associated Files:	Predict_Linac_Energy.inc
c				EAX21.dat		15-jun-2011 Fm
c				Eax22.dat		04-Mar-2014 Cp
c				Eax31.dat
c				Eax32.dat
c				Eax33.dat
c				Eax41.dat
c				Eax42.dat
c				Eax43.dat
c				Eax44.dat
c
c	Linking Procedure:	@Predict_Linac_Energy_Link
c
c       Related Documents:
c
c       Installation:           Argonne National Laboratory
c                               Physics Division
c                               ATLAS Facility
c
c	Author(s):		J. Gura/F. Munson
c	Date:			3/29/97
c
c	Revisions:
c
c		7-Apr-2016	F. Garcia (C. Peters)
c				Modified the beginning of the program that
c				asks the user whether the energy should be 
c				calculated starting with PII to ask whether
c				energy should be calculated with PII, Booster
c				or Atlas. The rest of the program is then 
c				modified to start with one of these 3 options.
c				In addition to this, if a user picks to begin
c				with PII, PII RFQ energy is defaulted to 
c				(Mass * 0.293). 
c
c		17-Apr-2014	C. Peters
c
c				Modified the Phind subroutine to use smaller
c				step sizes when searching for the phase angle
c				with largest energy gain.  Per C. Dickerson
c				and Brahim Mustapha
c
c		16-Apr-2014	C. Peters
c
c				Yeah, since I accidentally mapped the 
c				RES_PARAMS_VDB with a channel_id of
c				type REAL instead of INT, I changed
c				the code to do a 'vget' instead of
c				a 'rget'.  See this date.
c
c		04-Mar-2014	C. Peters
c
c				Changed the logic so that
c				the program uses this new file 'EAX22' for the
c				A cryostat Resonators.  Also added logic to 
c				skip new re-buncher R241.
c
c		11-Mar-2013	C. Peters		
c
c				There are two changes being made.  1.) There are
c				cases where an early resonator might be 
c				configured to run in 'bunching' mode and would
c				not add any energy.  If this is the case, the
c				phase would be exactly 90 degrees, and the TTF
c				should not be calculated or a segfault will
c				occur.  2.) The last resonator (R338) has been
c				removed as part of a beamline upgrade.  Made a
c				change such that the program stops here instead
c				of at the current R401.
c		
c		19-Dec-2012	C. Peters
c
c				The below attempt was not successful.  Put
c				the printer parameter back to '8'.  This date
c				is also when a change to the resonator types
c				was implemented.
c
c		10-Oct-2012	C. Peters
c
c				R. Pardo pointed out that the current printout
c				takes up over one page, and is wasting space.
c				Attemped to change printer line spacing.
c
c		15-Jun-2011	F. Munson
c
c				A new 'eax' type data file has been generated
c				by B. Mustapha. The new file was renamed to
c				'eax21.dat'. This name was chosen because it
c				turns out that the 'eax' file names were
c				actually derived with some logic in mind. The
c				first digit in the file name refers to the
c				number of "gaps" the resonator has that is
c				associated with the file, and the second digit
c				refers to the resonator type (which is not as
c				clearly understood, chronological order?).
c				Since the new file is for use with the new
c				resonators in the energy upgrade cryostat "G"
c				which are two gap structures, and these are
c				the first resonators of this type, the file
c				name 'eax21.dat' was chosen.
c
c				Rather than the typical 200 record file the
c				file contained 3595 records. With RCP's
c				blessing a small program was written that
c				extracted every 18th record from the new
c				'eax21.dat' file and wrote those records to
c				yet another new 'eax21.dat' file that
c				contained 200 records typical of existing data
c				files. This allowed for the existing
c				'predict_linac_energy' program to be used
c				with the new 'eax21.dat' file with minimal
c				changes.
c
c				The first field (positional value) of the
c				first record of the newly created 'eax21.dat'
c				file was -0.1797000. This value caused the
c				version of the 'predict_linac_energy' program
c				that made use of the 200 record version of
c				the 'eax21.dat' file to have lower energy
c				gains (for R331 through R338) than the
c				'predict_linac_energy' program that made use
c				of the 3595 record version. Per RCP this value
c				was changed to -0.1798000, which made the
c				resulting calculations almost identical.
c
c				This program has been modified to accommodate
c				the new 'eax21.dat' file. See this date for
c				the changes.
c
c		06-Mar-2007	F. Munson
c
c				Due to the addition of control of the
c				pre-Tandem buncher, modified the range of
c				resonators to test in a conditional
c				statement from a range of 201 to 204 to a
c				range of 200 to 204. See this date for the
c				change.
c
c		02-Nov-2001	D. Quock
c
c				Made corrections to a logic mistake in 
c				the use of the user's typed in scale factor,
c				New_Factor.  Mistakenly, the resonator
c				parameter, fscale, also known as: 
c				RES_PARAMS_DB_NAME//::R*:Amplitude_Scale_Factor
c				was getting reset to whatever value a user
c				of this program entered for New_Factor.
c
c				The functional difference between the two
c				parameters is that fscale is a sort of fudge 
c				factor stored in the database and derived from 
c				past knowledge of a specific resonators
c				behavior.  It typically has a value of 1.
c
c				The value entered by a user of this program
c				for New_Factor, is a scale factor to be used
c				for adjusting ETUNE, the Amplitude_After_Scan
c				resonator parameter.
c
c				These two scaling parameters were mistakenly
c				getting confused. To correct this mistake,
c				one line of code was commented out.
c				Also modified the report that is printed out
c				to now show the user typed in scale factor,
c				New_Factor. The include file 
c				Predict_Linac_Energy.inc was modified to now 
c				pass the variable New_Factor in a common block.
c
c				Search this date to see changes.
c
c		22-Mar-2000	D. Quock
c
c				Added debug printout statements to aid in
c				understanding how the variable RES_TAB_MAX
c				is used in this program.
c
c				Also changed conditional test statements so
c				that they look for the new phase-shifter, R204.
c
c				Search this date to see changes.
c
c               17-Mar-2000     D. Quock
c
c                               Changed subroutine Display_Results to increase
c                               the number of digits displayed for the
c                               variable Beta.  Write format was changed from:
c                               f6.5 to f8.6.
c
c		28-FEB-2000	B. Chapin
c
c				Updated the code to use the new vista_chix
c				manipulation routines.
c
c		14-Feb-2000	B. Chapin
c
c				Changed the declaration and usage of channel
c				indexes so that they use the vista_chix data
c				structure instead of integer*4.
c
c		14-Oct-1999	D. Quock
c
c				Made changes to the write\format statements in
c				subroutine Display_Results for variable
c				Resonator_Data_Table(I).Amplitude_After_Scan.
c				A problem was found with not enough digits
c				being provided in the printout for the 
c				magnitude of this variable.
c
c	Description:
c
c		This program attempts to predict LINAC energy. The routine
c		retrieves a number of values that are used in various
c		calculations from the appropriate Vsystem run-time database.
c		In addition to this database, the program utilizes files that
c		contain field values whose names all begin with "EAX**" where
c		"**" is equivalent to a number value. An "EAX" file is opened
c		in relation with the current 'Resonator_Id_Number." Next, it
c		prompts the user for the values needed for the calculations.
c		Finally, the main body contains calls to the subroutines that
c		the user chooses through a provided menu in the subroutine
c		called "Options_Menu."

	implicit none

c	Include files...

	include 'PREDICT_LINAC_ENERGY.INC'		!Structure definition

c	Variable declarations...

	character*1	Response
	character*1	User_Response
	character*1	Factor_Response
	character*7	File_Name
	character*60	Search_String_Status
	character*60	Search_String_ID
	character*60	Search_String_Default
	character*60	Search_String_After_Scan
	character*60	Search_String_Scale_Factor
	character*60	Search_String_Intercept
	character*60	Search_String_Slope

	integer*4	Number_Of_Records
	integer*4	Error_Status
	integer*4	N
	integer*4	Ierr
	integer*4	Count
	integer*4	Integer_Charge_State(3)
	integer*4	Record	
	integer*4	I
	integer*4	J
	integer*4	Option_Choice
	integer*4	Lib_Call_Status
	integer*4	Lib$Get_Lun
	integer*4	Printer_Lun
	integer*4	Indx
	integer*4	Sql_Status_Code
	integer*4	Eax_file(70)

	real*4		Zelm(200)
	real*4 		Lt
	real*4		Mass
	real*4		Total_Energy
	real*4		Charge_State(3)
	real*4		Initial_Charge
	real*4		Charge
	real*4		Beta(200)
	real*4		Gamma0
	real*4		Ener0
	real*4		Resfreq(200)	
	real*4		Ttf(200)	
	real*4		Phizero(200)
	real*4		SPEED_OF_LIGHT
	real*4		STARTING_ENERGY
	real*4		Uzero(200)
	real*4		El(70)

ccc D. Quock 02-Nov-2001	real*4		New_Factor

	record /vista_chix/ Status_Chix_Values(100)
	record /vista_chix/ Id_Chix_Values(100)
	record /vista_chix/ Default_Chix_Values(100)
	record /vista_chix/ After_Scan_Chix_Values(100)
	record /vista_chix/ Scale_Factor_Chix_Values(100)
	record /vista_chix/ Calibrate_Intercept_Chix_Values(100)
	record /vista_chix/ Calibrate_Slope_Chix_Values(100)	
	record /vista_chix/ Status_Chix
	record /vista_chix/ Id_Chix
	record /vista_chix/ Default_Chix
	record /vista_chix/ After_Scan_Chix
	record /vista_chix/ Scale_Factor_Chix
	record /vista_chix/ Calibrate_Intercept_Chix
	record /vista_chix/ Calibrate_Slope_Chix
	record /vdb_descrip/ vDesc
	record /vtime/	atime

c	Data statements...

	data  SPEED_OF_LIGHT	/  2.997928e8 /
	data  STARTING_ENERGY	/  0.293      /

c	Begin code...

	!Prompt user for the injector beam to use...

1	type *,' '
	type *,'Should the energy be calculated with starting with: '
	type *,'1. PII '
	type *,'2. Booster '
	type *,'3. Atlas '
	read(5,3) User_Response
3	format(a1)
	
	do while (User_Response .ne. '3' .and. User_Response .ne. '2' .and.
	1	  User_Response .ne. '1') 
	  type *,' '
	  type *,'Error: Invalid input '
          type *,'Should the energy be calculated with starting with: '
	  type *,'1. PII '
	  type *,'2. Booster '
	  type *,'3. Atlas '
	  read(5,4) User_Response
4	  format(a1)
        end do	

	if (User_Response .eq. '1') then
          Possible_Charges = 3
	else if (User_Response .eq. '2') then
          Possible_Charges = 2
	else 
 	  Possible_Charges = 1
        endif

	type *,' '
	type *,'Should a scale factor other than that stored in'
	type '(1x,a,$)','the database be used? (enter y or n) '
	read(5,3) Factor_Response
	  if (Factor_Response .eq. 'y' .or. Factor_Response .eq. 'Y') then
	    type '(1x,a,$)','Please enter the new scale factor: '
	    accept *, New_Factor
	  else 
	    New_Factor = 1.0
	  endif

	!Prompt user for the properties of the beam...

2	type *,' '
	type '(1x,a,$)','Please enter the mass of the ion: '
	accept *, Mass

	if (User_Response .eq. '1') then
	  type *,'Total energy is being calculated '
	  Total_Energy = Mass * STARTING_ENERGY
	  type *,' '
	  write(6,30) Total_Energy
30	  format(' PII RFQ Energy Defaulted to: ', f6.2, ' MeV ')
	  type *,' '
	else if (User_Response .eq. '2') then
	  type '(1x,a,$)','Please enter the starting energy from ' // 
	1                 'Booster(MeV): '
	  accept *, Total_Energy
	  type *,' '
	else 
	  type '(1x,a,$)','Please enter the starting energy from Atlas(MeV): '
	  accept *, Total_Energy
	  type *,' '
	endif

	!If operator is using PII resonators, then ask for this charge state...
	
	if (Possible_Charges .eq. 3) then
	  type *,'Please enter PII, BOOSTER, and ATLAS charge states ' //
	1	 'in that order.'
	  type '(1x,a,$)','Separate the values with commas, spaces ' //
	1                 'or a carriage return: '
	  accept *, Charge_State(1), Charge_State(2), Charge_State(3)
	else if (Possible_Charges .eq. 2) then
	  type *,'Please enter BOOSTER and ATLAS charge states ' //
	1	 'in that order.'
	  type '(1x,a,$)','Separate the values with commas, spaces ' //
	1                 'or a carriage return: '
	  accept *, Charge_State(1), Charge_State(2)
	else 
	  type '(1x,a,$)','Please enter ATLAS charge state '
	1
	  accept *, Charge_State(1) 
	endif

	if (Option_Choice .ne. 1) then

	  type *,' '
	  type *,'Working, please wait....'

	  call VDB_Zero_Chix(Status_Chix)
	  call VDB_Zero_Chix(Id_Chix)
	  call VDB_Zero_Chix(Default_Chix)
	  call VDB_Zero_Chix(After_Scan_Chix)
	  call VDB_Zero_Chix(Scale_Factor_Chix)
	  call VDB_Zero_Chix(Calibrate_Intercept_Chix)
	  call VDB_Zero_Chix(Calibrate_Slope_Chix)	  
	  Indx = 1

100	  do while (Indx .le. RES_TAB_MAX)

	    !Here, the program will go out to the "RES_PARAMS_VDB" database and
	    !retrieve the chix for that resonator id number channel...

	    Search_String_Status = RES_DB_NAME // '::R*:Status'
	    Search_String_Id = RES_PARAMS_DB_NAME //
	1		      '::R*:Id_Number'
	    Search_String_Default = RES_PARAMS_DB_NAME // 
	1			   '::R*:Default_Acceleration_Phase'
	    Search_String_After_Scan = RES_PARAMS_DB_NAME //
	1		      '::R*:Amplitude_After_Scan'
	    Search_String_Scale_Factor = RES_PARAMS_DB_NAME // 
	1				'::R*:Amplitude_Scale_Factor'
	    Search_String_Intercept = RES_PARAMS_DB_NAME //
	1		      '::R*:Amplitude_Calibrate_Intercept'
	    Search_String_Slope = RES_PARAMS_DB_NAME // 
	1				   '::R*:Amplitude_Calibrate_Slope'

	    call VDB_Search(Search_String_Status, Status_Chix)
	    Status_Chix_Values(Indx) = Status_Chix

	    call VDB_Search(Search_String_Id, Id_Chix)
	    Id_Chix_Values(Indx) = Id_Chix

	    call VDB_Search(Search_String_Default, Default_Chix)
	    Default_Chix_Values(Indx) = Default_Chix

	    call VDB_Search(Search_String_After_Scan, After_Scan_Chix)
	    After_Scan_Chix_Values(Indx) = After_Scan_Chix

	    call VDB_Search(Search_String_Scale_Factor, Scale_Factor_Chix)
	    Scale_Factor_Chix_Values(Indx) = Scale_Factor_Chix

	    call VDB_Search(Search_String_Intercept, 
	1		    Calibrate_Intercept_Chix)
	    Calibrate_Intercept_Chix_Values(Indx) = Calibrate_Intercept_Chix

	    call VDB_Search(Search_String_Slope, 
	1		    Calibrate_Slope_Chix)
	    Calibrate_Slope_Chix_Values(Indx) = Calibrate_Slope_Chix

	    !Get the values for each of the previously gotten chixes...

	    if (.not. VDB_IGet(Status_Chix_Values(Indx),
	1       Resonator_Data_Table(Indx).Status)) then
	      call VDB_Error_Status(Status_Chix_Values(Indx), Error_Status)
	      type *,'PREDICT -- Error in getting RESONATOR STATUS from'
	      type *,'		 database...'
	      type *,'           Error_Status = ',Error_Status
	      goto 999
	    endif

c	16-Apr-2014  C. Peters - Changed to vget to get real or int
	    vDesc.dsc_a_pointer = 
	1	%loc(Resonator_Data_Table(Indx).Resonator_Id_Number)
	    vDesc.dsc_w_length = 
	1	sizeof(Resonator_Data_Table(Indx).Resonator_Id_Number)*4
	    vDesc.dsc_b_type = VDB_DTYPE_INT
	    if (.not. VDB_VGet(Id_Chix_Values(Indx),vDesc,atime,VDB_EXTERNAL))
	1   then
	      call VDB_Error_Status(Id_Chix_Values(Indx), Error_Status)
	      type *,'PREDICT -- Error in getting RESONATOR_ID_NUMBER from'
	      type *,'		 database...'
	      type *,'           Error_Status = ',Error_Status
	      goto 999
	    endif

	    if (.not. VDB_RGet(Default_Chix_Values(Indx),
	1       Resonator_Data_Table(Indx).Default_Acceleration_Phase)) then
	      call VDB_Error_Status(Default_Chix_Values(Indx), Error_Status)
	      type *,'PREDICT -- Error in getting DEFAULT_ACCELERATION_PHASE'
	      type *,'		 from database...'
	      type *,'           Error_Status = ',Error_Status
	      goto 999
	    endif

	    if (.not. VDB_RGet(After_Scan_Chix_Values(Indx),
	1       Resonator_Data_Table(Indx).Amplitude_After_Scan)) then
	      call VDB_Error_Status(After_Scan_Chix_Values(Indx), Error_Status)
	      type *,'PREDICT -- Error in getting AMPLITUDE_AFTER_SCAN from'
	      type *,'		 database...'
	      type *,'           Error_Status = ',Error_Status
	      goto 999
	    endif

	    if (.not. VDB_RGet(Scale_Factor_Chix_Values(Indx),
	1       Resonator_Data_Table(Indx).Amplitude_Scale_Factor)) then
	      call VDB_Error_Status(Scale_Factor_Chix_Values(Indx), 
	1			    Error_Status)
	      type *,'PREDICT -- Error in getting AMPLITUDE_SCALE_FACTOR from'
	      type *,'		 database...'
	      type *,'           Error_Status = ',Error_Status
	      goto 999
	    endif

	    if (.not. VDB_RGet(Calibrate_Intercept_Chix_Values(Indx),
	1       Resonator_Data_Table(Indx).Amplitude_Calibrate_Intercept)) then
	      call VDB_Error_Status(Calibrate_Intercept_Chix_Values(Indx), 
	1			    Error_Status)
	      type *,'PREDICT -- Error in getting' 
	      type *,'		 AMPLITUDE_CALIBRATE_INTERCEPT from database..'
	      type *,'           Error_Status = ',Error_Status
	      goto 999
	    endif

	    if (.not. VDB_RGet(Calibrate_Slope_Chix_Values(Indx),
	1       Resonator_Data_Table(Indx).Amplitude_Calibrate_Slope)) then
	      call VDB_Error_Status(Calibrate_Slope_Chix_Values(Indx), 
	1		  	    Error_Status)
	      type *,'PREDICT -- Error in getting Amplitude_Calibrate_Slope'
	      type *,'		 from database...'
	      type *,'           Error_Status = ',Error_Status
	      goto 999
	    endif
  
	    if (User_Response .eq. '2') then 
	      if (Resonator_Data_Table(Indx).Resonator_Id_Number .lt. 211) then
	        goto 100
	      endif
	    else if (User_Response .eq. '3') then 
	      if (Resonator_Data_Table(Indx).Resonator_Id_Number .lt. 311) then
		goto 100
	      endif
	    endif
			
	    !This set of 'if' statements will skip bunchers and choppers...
	    if (Resonator_Data_Table(Indx).Resonator_Id_Number .le. 103) then
	      goto 100
	    endif	

	    !22-Mar-2000  Changed limit from 203 to 204, new phase-shifter.

	    !Changed the range from 201 to 204 to range 200 to 204, to
	    !accomodate new pre-Tandem buncher....		06-Mar-2007 Fm

	    !if (Resonator_Data_Table(Indx).Resonator_Id_Number .ge. 201 .and.
	    if (Resonator_Data_Table(Indx).Resonator_Id_Number .ge. 200 .and.
	1       Resonator_Data_Table(Indx).Resonator_Id_Number .le. 204) then
	      goto 100
	    endif

	    !04-Mar-2014  C. Peters - Skip new rebuncher R241
	    if (Resonator_Data_Table(Indx).Resonator_Id_Number .eq. 241) then
	      goto 100
	    endif

	    if (Resonator_Data_Table(Indx).Resonator_Id_Number .eq. 301 .or.
	1       Resonator_Data_Table(Indx).Resonator_Id_Number .eq. 302) then
	      goto 100
	    endif

ccc	    11-Mar-2013     C. Peters
ccc	    R338 has been removed from the linac.  Stop there instead of 401 
ccc	    if (Resonator_Data_Table(Indx).Resonator_Id_Number .eq. 401) then 
	    if (Resonator_Data_Table(Indx).Resonator_Id_Number .eq. 338) then 
	      Number_Of_Records = Indx - 1
	      Indx = RES_TAB_MAX
	    endif

	    !Use the operator supplied scale factor instead of the default from
	    !the database...

	    if (Factor_Response .eq. 'y' .or. Factor_Response .eq. 'Y') then

ccc D. Quock 02-Nov-2001	      
ccc 	      Resonator_Data_Table(Indx).Amplitude_Scale_Factor = New_Factor

	      Resonator_Data_Table(Indx).Amplitude_After_Scan =
	1         Resonator_Data_Table(Indx).Amplitude_After_Scan * New_Factor 
	    endif

d	    type*,' '
d	    type*,'Resonator Status		= ',
d	1	   Resonator_Data_Table(Indx).Status
d	    type*,'Resonator_Id_Number            = ',
d	1          Resonator_Data_Table(Indx).Resonator_Id_Number
d	    type*,'Default_Acceleration_Phase     = ',
d	1          Resonator_Data_Table(Indx).Default_Acceleration_Phase
d	    type*,'Amplitude_After_Scan           = ',
d	1          Resonator_Data_Table(Indx).Amplitude_After_Scan
d	    type*,'Amplitude_Scale_Factor         = ',
d	1          Resonator_Data_Table(Indx).Amplitude_Scale_Factor
d	    type*,'Amplitude_Calibrate_Intercept  = ',
d	1          Resonator_Data_Table(Indx).Amplitude_Calibrate_Intercept
d 	    type*,'Amplitude_Calibrate_Slope      = ',
d	1          Resonator_Data_Table(Indx).Amplitude_Calibrate_Slope
d	    type*,' '

	    !This set of 'if' statements will create another array that will
	    !tell the program which 'EAX*' file data should be taken from...'
	    ! modified 19-DEC-2012 for new RFQ/Alpha Cryostat changes

!	    if (Resonator_Data_Table(Indx).Resonator_ID_Number .eq. 111) then
!	      Eax_File(Indx) = 41  
!	    else
!	      if (Resonator_Data_Table(Indx).Resonator_ID_Number .eq. 112 .or.
!	1         Resonator_Data_Table(Indx).Resonator_ID_Number .eq. 113) then
!	        Eax_File(Indx) = 42
!	      else
!            if (Resonator_Data_Table(Indx).Resonator_ID_Number .ge. 114

            if (Resonator_Data_Table(Indx).Resonator_ID_Number .ge. 111
	1	   .and.
	1	    Resonator_Data_Table(Indx).Resonator_ID_Number .le. 122) 
	1	    then
		  Eax_File(Indx) = 43
	        else
		  if (Resonator_Data_Table(Indx).Resonator_ID_Number .ge. 123 
	1	      .and. Resonator_Data_Table(Indx).Resonator_ID_Number .le.
	1	      136) then
		    Eax_File(Indx) = 44
		  else
c		    04-Mar-2014 - C. Peters - New A Cryostat file 'EAX22'
		    if (Resonator_Data_Table(Indx).Resonator_ID_Number .ge. 211
	1	        .and. Resonator_Data_Table(Indx).Resonator_ID_Number
	1	        .le. 217) then
		      Eax_File(Indx) = 22
		    else
	              if (Resonator_Data_Table(Indx).Resonator_ID_Number .ge.
	1                 221 .and.  
	1		  Resonator_Data_Table(Indx).Resonator_ID_Number
	1                 .le. 226) then
	!!!             Eax_File(Indx) = 31		!04-Mar-2014
			Eax_File(Indx) = 32		! Old Dtank is now B
		      else
		        if (Resonator_Data_Table(Indx).Resonator_ID_Number .ge. 
	1		  231 .and. 
	1		  Resonator_Data_Table(Indx).Resonator_ID_Number
	!!1		  .le. 338) then 
	1		  .le. 326) then		!15-Jun-2011

		          Eax_File(Indx) = 32

                        !15-Jun-2011

		        else
	                  if (Resonator_Data_Table(Indx).Resonator_ID_Number 
	1                   .ge. 331 .and.
	1                   Resonator_Data_Table(Indx).Resonator_ID_Number
	1                   .le. 338) then
		            Eax_File(Indx) = 21
	                  endif
		        endif
	              endif
		    endif
		  endif
	        endif
!	      endif
!	    endif

	    !Calculate the value 'EL'

	    El(Indx) =
	1	  (Resonator_Data_Table(Indx).Amplitude_Calibrate_Intercept +
	1	  Resonator_Data_Table(Indx).Amplitude_Calibrate_Slope * 
	1	  Resonator_Data_Table(Indx).Amplitude_After_Scan) * 
	1	  Resonator_Data_Table(Indx).Amplitude_Scale_Factor	 

d	    type *,'El(Indx) = ', El(Indx)

	    Indx = Indx + 1

	  end do          

	  Indx = Number_Of_Records
d	  type *,'Number_Of_Records = ', Number_Of_Records
d	  type *,'Indx = ', Indx

	endif

	!The initial charge state is assumed to be charge state 1...

	Charge = Charge_State(1)
	Initial_Charge = 1

	!Files need to be closed here, because in case the user wants to 
	!start the program over from the top, these files will be open
	!already upon descent through the program and consequently will
	!not run properly... 

	close(1)
	close(2)
	close(3)

	!Find Beta, Gamma, and energy...

	Beta(1) = sqrt(1 - (1 + Total_Energy / (931.502 * Mass)) ** (-2))
	Gamma0 = sqrt(1 - Beta(1) ** 2)
	Ener0 = Mass * 931.502 * (1.0 / Gamma0 - 1.0)

	call Resonator_Position(Eax_File, Resfreq, Zelm, Indx, Lt)

	!Force first iteration of loop...
	
	Response = 'N'
	do while (Response .eq. 'N' .or. Response .eq. 'n')
	
	  !Convert 'Charge_State' array to integers for printout...

	  Count = 1
	    do while (Count .le. Possible_Charges)
	      Integer_Charge_State(Count) = int(Charge_State(Count))
	      Count = Count + 1
	    end do

	  !Write out a heading for the menu options...

	  if (Possible_Charges .eq. 3) then	  
	    write(6,5)Indx, Mass, Ener0, Integer_Charge_State(1), 
	1	      Integer_Charge_State(2),Integer_Charge_State(3), 
ccc 02-Nov-2001	1      Resonator_Data_Table(1).Amplitude_Scale_Factor
	1	      New_Factor
5	    format(//,' ','Total_Resonators: ',I4,
	1	  /,' Accelerated Beam:',/,t5,'Mass = ',f4.0,
	1	  '  Energy = ',f6.2,' MeV',/,t5,'PII Charge = ',I3,2x,
	1	  'Booster Charge = ',I3,2x,'ATLAS Charge = ',I3,/,t5,
	1	   'Amplitude After Scan  -  Scale Factor Used: ',f6.3)
	  else if (Possible_Charges .eq. 2) then
	    write(6,6)Indx, Mass, Ener0, Integer_Charge_State(1), 
	1 	      Integer_Charge_State(2),
ccc 02-Nov-2001	1     Resonator_Data_Table(1).Amplitude_Scale_Factor
	1	      New_Factor
6	    format(//,' ','Total_Resonators: ',I4,
	1	  /,' Acclerated Beam:',/,t5,'Mass = ',f4.0,'  Energy = ',f6.2,
	1	   ' MeV',/,t5'Booster Charge = ',I3,2x,'ATLAS Charge = ',I3,/,
	1	  t5,'Amplitude After Scan  -  Scale Factor Used: ',f6.3)
	  else
	    write(6,7)Indx, Mass, Ener0, Integer_Charge_State(1),
	1	  New_Factor
7	    format(//,' ','Total_Resonators: ',I4,
	1     /,' Acclerated Beam:',/,t5,'Mass = ',f4.0,'  Energy = ',f6.2,
	1     ' MeV',/,t5'ATLAS Charge = ',I3,/,
	1     t5,'Amplitude After Scan  -  Scale Factor Used: ',f6.3)
	  endif
	  
	  !Type out the menu choices...

	  call Options_Menu(Option_Choice)

	  !Upon return from the subroutine, take option of the user and
	  !execute appropriate code...

	  !Enter new beam properties...

	  if (Option_Choice .eq. 1) goto 2

	  !Calculate energy gains...
	
	  if (Option_Choice .eq. 2) then

	    call Calculate_Energy_Gains(Eax_File, Charge_State, Indx, Beta,
	1			        Mass, Charge, Initial_Charge,
	1				Uzero, Phizero, Ttf, El)

	  endif

	  !Change device settings...

	  if (Option_Choice .eq. 3) then
	    call Change_Settings(Eax_File, Indx, Resfreq, Zelm, Lt, El)
	  endif

	  !List Present Hardware Settings...

	  if (Option_Choice .eq. 4) then
	    call List_Settings(Mass, Ener0, Beta, Integer_Charge_State, 
	1   		       Indx, Zelm, Resfreq, Eax_File, El)
	  endif

	  !Display results...

	  if (Option_Choice .eq. 5) then

	    !'Printer_Lun' is the variable that determines whether to 
	    !output the results to the screen or to the laser printer...

	    Printer_Lun = 6

	    call Display_Results(Printer_Lun, Mass, Ener0, Beta, File_Name,
	1		         Integer_Charge_State, Indx,
	1		         Ttf, Phizero, Uzero, Eax_File, El)
    
	  endif


	  !Print results...

	  if (Option_Choice .eq. 6) then

	    !Get a logical unit number for the laser printer...

	    Lib_Call_Status = Lib$Get_Lun(Printer_Lun)

	    open (unit = Printer_Lun,
	1         file = 'Predict_Energy_Gains',
	1         form = 'FORMATTED',
	1         status = 'NEW',
	1         shared,
	1         err = 1001)

	    !Now, go to the 'Display results' option section of code and
	    !execute same commands...
	
	    call Display_Results(Printer_Lun, Mass, Ener0, Beta, File_Name,
	1			 Integer_Charge_State, Indx,
	1			 Ttf, Phizero, Uzero, Eax_File, El)
	    close (Printer_Lun, dispose = 'PRINT/DELETE')

	  endif
     
	  !Restart program from the very top...

	  if (Option_Choice .eq. 7) then
	    close(1)
	    goto 1
	  endif
	
	  !Quit program...

	  if (Option_Choice .eq. 8) then
	    type *,' '
	    type '(1x,a,$)','Are you sure you want to quit? (enter y or n) '
	    read (5,15,iostat=Ierr) Response
15	    format(a1)
	  endif

	end do	
	
	goto 1002

999	type *,'PREDICT -- Error in retrieving information from the RES_VDB' 
	type *,'	   VDB database...'

	goto 1002
	
1001	type *,'PREDICT -- Error in getting the logical unit'
	type *,'           number for the printer. Program aborted...'

1002	stop
	end



c	----------------------------------------------------------------------
	subroutine Resonator_Position(Eax_File, Freq, Zelm, Indx, Totl)

	implicit none	

c	Local variables...
	
	integer*4	Msh
	integer*4	Indx
	integer*4	Eax_File(70)
	integer*4	I

	real*4		Zelm(200)
	real*4		Freq(200)
	real*4		Pi
	real*4		DEGTORAD
	real*4		Speed_Of_Light
	real*4		Dummy
	real*4		Cavity_Length
	real*4		Z1
	real*4		Z2
	real*4		Totl

	

c	Data statements...

	data Pi /3.1415927/
	data Speed_Of_Light /2.997928e8/

c	Include files...

	include 'PREDICT_LINAC_ENERGY.INC'

c	Begin code...

	Totl = 0.0

d	type *,'----------------------------------------------'
d	type *,'In Subroutine Resonator_Position, Indx = ',Indx

	I = 1
	do while (I .le. Indx)

	  !!If (Eax_File(I) .gt. 40) then	15-Jun-2011

	  if (Eax_File(I) .eq. 41) then
	    open (unit = 2, file = 'ATLAS_DATA:EAX41.dat', status = 'old')
	  else
	    if (Eax_File(I) .eq. 42) then
	      open (unit = 2, file = 'ATLAS_DATA:EAX42.dat', status = 'old')
	    else
	      if (Eax_File(I) .eq. 43) then
	        open (unit = 2, file = 'ATLAS_DATA:EAX43.dat', status = 'old')
	      else
	        if (Eax_File(I) .eq. 44) then
	          open (unit = 2, file = 'ATLAS_DATA:EAX44.dat', 
	1       	status = 'old')
	        else
	          if (Eax_File(I) .eq. 31) then
	            open (unit = 2, file = 'ATLAS_DATA:EAX31.dat', 
	1                 status = 'old')
	          else
	            if (Eax_File(I) .eq. 32) then
	              open (unit = 2, file = 'ATLAS_DATA:EAX32.dat', 
	1                   status = 'old')
	            else
	              if (Eax_File(I) .eq. 33) then
	                open (unit = 2, file = 'ATLAS_DATA:EAX33.dat', 
	1       	      status = 'old')
	              else

	                !15-Jun-2011

	                if (Eax_File(I) .eq. 21) then
	                  open (unit = 2, file = 'ATLAS_DATA:EAX21.dat', 
	1       	        status = 'old')
			else 
	               
			  !04-Mar-2014  CP
	                  if (Eax_File(I) .eq. 22) then
	                    open (unit = 2, file = 'ATLAS_DATA:EAX22.dat', 
	1       	        status = 'old')
			  endif
			endif
	              endif
		    endif
		  endif
		endif
	      endif
	    endif
	  endif
	
	  rewind (2)

	  read(2, *) Msh, Freq(I)

	  Freq(I) = Freq(I) * 1.0e-6

	  read(2, *) Z1
	  read(2, *) Z2

	  Totl = Totl + (Z2 - Z1) * Msh
	  Zelm(I) = Totl
	
	  close (2)


ccc	  15-Jun-2011

ccc	  else
ccc
ccc	      if (Eax_File(I) .eq. 31) then
ccc	        Cavity_Length = 0.208
ccc		Freq(I) = 97.0
ccc	      endif
ccc
ccc	      if (Eax_File(I) .eq. 32) then
ccc	        Cavity_Length = 0.355
ccc		Freq(I) = 97.0
ccc	      endif
ccc	
ccc	      if (Eax_File(I) .eq. 33) then
ccc	        Cavity_Length = 0.355
ccc	        Freq(I) = 145.5
ccc	      endif
ccc
ccc	      Totl = Totl + Cavity_Length
ccc	      Zelm(I) = Totl
ccc
ccc	  endif


	  I = I + 1
	end do


d	type *,'Exiting subroutine Resonator_Position: I = ',I
d	type *,'----------------------------------------------'

	return
	end



c	-----------------------------------------------------------------------
	subroutine Calculate_Energy_Gains(Eax_File, Charge_State, Indx, Beta,
	1				  Mass, Charge, Initial_Charge,
	1				  Uzero, Phizero, Ttf, El)

	implicit none
	
c	Variable declarations...

	integer*4	Indx
	integer*4	Record
	integer*4	I
	integer*4	Current_Pointer
	integer*4	Next_Pointer
	integer*4	Eax_File(70)
	integer*4	File_Save

	real*4		Charge_State(3)
	real*4		Beta(200)
	real*4		Mass
	real*4		Charge
	real*4		Initial_Charge
	real*4		Uzero(200)
	real*4		Phizero(200)
	real*4		Ttf(200)
	real*4		DEGTORAD
	real*4		Timein(200)
	real*4		El(70)
	real*4		Poff
	real*4		Zinner
	real*4		Umatch
	real*4		Term

c	Data statements...

	data DEGTORAD /-0.017453/

c	Include files...

	include 'PREDICT_LINAC_ENERGY.INC'

c	Begin code...

	!Let operator know the program is running...

d	type *,'----------------------------------------------'
d	type *,'In subroutine Calculate_Energy_Gains: Indx = ',Indx

	type *,' '
	type *,'Calculating, please wait....'

	!Intialize variables for 'do while' loop...

	Record = 1
	Initial_Charge = 1
	Charge = Charge_State(1)
	Timein(1) = 0.0

	I = 1
	do while (I .le. Indx)

	  !Here, make sure the proper charge state is used with each resonator.
	  if (Possible_Charges .eq. 1) then
	    if (Resonator_Data_Table(I).Resonator_Id_Number .ge. 300 .and.
	1   Resonator_Data_Table(I).Resonator_Id_Number .le. 338) then
	      Charge = Charge_State(1)
	    endif
	  endif

	  if (Possible_Charges .eq. 2) then 

	    if (Resonator_Data_Table(I).Resonator_Id_Number .ge. 200 .and. 
	1       Resonator_Data_Table(I).Resonator_Id_Number .le. 246) then

	      Charge = Charge_State(1)

	    else 

	      if (Resonator_Data_Table(I).Resonator_Id_Number .ge. 300 .and.
	1	  Resonator_Data_Table(I).Resonator_Id_Number .le. 338) then

	        Charge = Charge_State(2)

	      endif

	    endif

	  endif
		

	  if (Possible_Charges .eq. 3) then

	    if (Resonator_Data_Table(I).Resonator_Id_Number .le. 136) then

	      Charge = Charge_State(1)

	    else

	      if (Resonator_Data_Table(I).Resonator_Id_Number .ge. 200 .and.
	1	  Resonator_Data_Table(I).Resonator_Id_Number .le. 246) then

		Charge = Charge_State(2)

	      else
	
	        if (Resonator_Data_Table(I).Resonator_Id_Number .ge. 300 .and.
	1	    Resonator_Data_Table(I).Resonator_Id_Number .le. 338) then
	
		  Charge = Charge_State(3)

		endif

	      endif

	    endif

	  endif
	
	  Current_Pointer = Record
	  Next_Pointer = Record + 1


	  !If this resonator is 'deactivated' it will be skipped, and the
	  !'beta' previously calculated for this resonator needs to be placed
	  !in the next resonator's array position. So...

	  if (Resonator_Data_Table(I).Status .eq. RES_STATUS_DEACTIVATED) then
	    Beta(Next_Pointer) = Beta(Current_Pointer)
	    go to 99
	  endif


	  !Figure out which 'EAX**' file to use...

	  Poff = DEGTORAD * 
	1	 Resonator_Data_Table(Record).Default_Acceleration_Phase

	  call Resonator_Calculation(Eax_File(I), Poff,
	1	  	      	     Beta(Current_Pointer),
	1			     Beta(Next_Pointer),
	1			     Timein(Current_Pointer),
	1			     Timein(Next_Pointer), Mass, Charge,
	1			     Phizero(Current_Pointer), File_Save,
	1			     Uzero(I), El(I))

	  if (Eax_File(I) .eq. 21) then		!15-Jun-2011
	    Zinner = 0.390
	  else 
	    if (Eax_File(I) .eq. 31) then
	      Zinner = 0.208
	    else
	      if (Eax_File(I) .eq. 32 .or. Eax_File(I) .eq. 33) then
	        Zinner = 0.355
	      else 
	        if (Eax_File(I) .eq. 41) then
	          Zinner = 0.102
	        else
	          if (Eax_File(I) .eq. 42) then
	            Zinner = 0.165
	          else
	            if (Eax_File(I) .eq. 43 .or. Eax_File(I) .eq. 44) then
	              Zinner = 0.254
	            else
		      if (Eax_File(I) .eq. 22) then
	                Zinner = 0.32
		      endif
	            endif
	          endif
	        endif
	      endif
	    endif
	  endif

	  Umatch = Charge * El(I) * Zinner * cos(Poff)
	  Term = 1 / (sqrt(1 - Beta(Next_Pointer) ** 2)) - 1 /
	1       (sqrt(1 - Beta(Current_Pointer) ** 2))

ccc	11-Mar-2013    C. Peters
ccc	If this was a 'bunching' resonator, then the phase (Poff)
ccc	will be 90deg.  This will cause cos(90) = 0 since there is no
ccc	energy gain.  This will div by zero.  So, re-set the Ttf to zero.
ccc	Compare to a 'small' value since floating points are never absolute.
 
	if (Umatch .gt. 0.001) then
	  Ttf(Record) = 931.507 * Mass * Term / Umatch
	else
	  Ttf(Record) = 0.0
	endif

99      I = I + 1
        Record = Record + 1

	end do


d	type *,'Exiting subroutine Calculate_Energy_Gains: I = ',I
d	type *,'----------------------------------------------'

	  !'File_Save' is a variable that determines whether to read an input
	  !file or not. Here it is reset to '0' for the next time through the 
	  !program...

	  File_Save = 0

	  return
	  end



c	----------------------------------------------------------------------
	subroutine Resonator_Calculation(Eax_File, Poff, B0, Bf, Timein,
	1				 Timeout, Mass, Charge, Phi00, 
	1				 File_Save, Uzero, El)

	implicit none

c	Local variable declarations...

	integer*4	Eax_File
	integer*4	Count
	integer*4	Mesh
	integer*4	File_Save
	integer*4	J

	real*4		El
	real*4		Poff	
	real*4		B0
	real*4		Bf
	real*4		TimeIn
	real*4		TimeOut
	real*4		Mass
	real*4		Charge
	real*4		Phi00
	real*4		PI
	real*4		SPEED_OF_LIGHT
	real*4		Freq
	real*4		Z0(200)
	real*4		Ez0(200)
	real*4		Om
	real*4		Omc
	real*4		Qdm0
	real*4		Qdm0c
	real*4		Ug00
	real*4		Phitmp
	real*4		Btmp
	real*4		Dz
	real*4		Phi0(200)
	real*4		Beta0(200)
	real*4		Eztmp
	real*4		Uzero
	real*4		Term1
	real*4		Term2

c	Data statements...

	data  PI 		/3.1415927/
	data  SPEED_OF_LIGHT	/2.997928e8/

c	Include files...

	include 'PREDICT_LINAC_ENERGY.INC'

c	Begin code...

	!First, check to see if 'Eax_File' is the same as before. If it is,
	!then don't read the same file again...

	if (File_Save .ne. Eax_File) then
	  File_Save = Eax_File

	  !15-Jun-2011

	  if (Eax_File .eq. 21) then
	    open (unit = 3, file = 'ATLAS_DATA:Eax21.dat', status = 'OLD')
	  else
	    if (Eax_File .eq. 31) then
	      open (unit = 3, file = 'ATLAS_DATA:Eax31.dat', status = 'OLD')
	    else
	      if (Eax_File .eq. 32) then
	        open (unit = 3, file = 'ATLAS_DATA:Eax32.dat', status = 'OLD')
	      else
	        if (Eax_File .eq. 33) then
	          open (unit = 3, file = 'ATLAS_DATA:Eax33.dat',
	1               status = 'OLD')
	        else
	          if (Eax_File .eq. 41) then
	            open (unit = 3, file = 'ATLAS_DATA:Eax41.dat',
	1                 status = 'OLD')
	          else
		    if (Eax_File .eq. 42) then
	     	      open (unit = 3, file = 'ATLAS_DATA:Eax42.dat', 
	1	  	    status = 'OLD')
	  	    else
	  	      if (Eax_File .eq. 43) then
	    	        open (unit = 3, file = 'ATLAS_DATA:Eax43.dat', 
	1		      status = 'OLD')
	  	      else
	  	        if (Eax_File .eq. 44) then
	     	          open (unit = 3, file = 'ATLAS_DATA:Eax44.dat', 
	1		        status = 'OLD')	        
			else
			  if (Eax_File .eq. 22) then
	     	            open (unit = 3, file = 'ATLAS_DATA:Eax22.dat', 
	1		          status = 'OLD')
			  endif
	                endif
	  	      endif
		    endif
		  endif
	        endif
	      endif
	    endif
	  endif
	
	  rewind 3
	  read(3,*)Mesh, Freq

	  Count = 1
	  do while (Count .le. Mesh)
	    read(3,*)Z0(Count), Ez0(Count)
	    Count = Count + 1
	  end do

	endif		!if (File_Save .ne. Eax_File)...
	 
	Om = 2. * PI * Freq
	Omc = Om / SPEED_OF_LIGHT
	Qdm0 = Charge * 9.580838e7 / (Mass * SPEED_OF_LIGHT)
	Qdm0c = Qdm0 / SPEED_OF_LIGHT

	call Phind(El, Ez0, Z0, Mesh, B0, Freq, Phi00, Ug00, Qdm0c)

	Phitmp = Phi00 + Poff
	Btmp = B0
	Dz = Z0(2) - Z0(1)
	Timeout = Timein

	J = 1
	do while (J .le. Mesh)
	  Phi0(J) = Phitmp
	  Beta0(J) = Btmp
	  Eztmp = El * Ez0(J) * cos(Phitmp)
	  Phitmp = Phitmp + Omc * Dz / Btmp
	  Btmp = Btmp + Eztmp * Qdm0c * Dz / Btmp
	  Timeout = Timeout + Dz / (Btmp * SPEED_OF_LIGHT)
	  J = J + 1
	end do
	
	Uzero = 931.507 * Mass * (1 / (sqrt(1 - Beta0(Mesh) ** 2)) - 1)

	Bf = Beta0(Mesh)
	Term1 = Mass * B0 * 9.315e5
	Term2 = Term1 * Bf / B0

	close (3)
	return
	end



!------ The subroutine "Phind" new with 1 deg phase interval & more ------!

c	-----------------------------------------------------------------------
	subroutine Phind(El,Eax,Zax,N,Beta,Freq,Phi,Vgain,Qdm)

	implicit none

c	Variable declarations...

	real*4		Dz
	real*4		El
	real*4		Speed_Of_Light
	real*4		Pi
	real*4 		Eax(1)
	real*4		Zax(1)
	real*4		Freq
	real*4		Beta
	real*4		Phi
	real*4		Vgain
	real*4		Qdm
	real*4		Om
	real*4		Phitmp
	real*4		Dphi
	real*4		Pre
	real*4		Bmax
	real*4		Bfor
	real*4		T
	real*4		Btmp
	real*4		Bmor
	real*4		Bles
	real*4		Phiint

	integer*4	N
	integer*4	J
	integer*4	I	

c	Logical statements...

	logical 	Newmax

c	Data statements...

	data  Speed_Of_Light /2.997928E8/
	data  Pi	     /3.141593/

c	Include files...

c	include 'PREDICT_LINAC_ENERGY.INC'

c	Begin code...
c	type *,'...Brahims new Phind 17-Apr-2014'

	Newmax = .FALSE.
     	Om = 2. * Pi * Freq
    	Phitmp = - Pi / 360.      ! <- reduced from 1/50 to 1/360 (BM-041714)
   	Dphi = Pi / 180.          ! <- reduced from 1/25 to 1/180 (BM-041714)
  	Dz = abs(Zax(N) - Zax(1)) / float(N-1)
 	Pre = El * Qdm * Dz
	Bmax = 0
	Bfor = Beta
	T = 0.

	!Calculate one point outside loop to initialize parabolic fit info 
	!correctly.

	do 5 I = 1, N
     	  Bfor = Bfor + Pre * Eax(I) * cos(Om * T + Phitmp) / Bfor
    	  T = T + Dz / (Bfor * Speed_Of_Light)
5     	continue

	do 20 J = 1, 360          ! <- increased from 50 to 360 (BM-041714)
      	  Btmp = Beta
      	  T = 0.
      	  Phitmp = Phitmp + Dphi
      	  do 10 I = 1, N
      	    Btmp = Btmp + Pre * Eax(I) * cos(Om * T + Phitmp) / Btmp
      	    T = T + Dz / (Btmp * Speed_Of_Light)
10    	  continue
      	  if (Newmax) then
	    Bmor = Btmp    !SAVE VELOCITY AT + DPHI FROM PRESENT MAX
	    Newmax = .FALSE.
	  endif
     	  if (Btmp .gt. Bmax) then      !IS THIS A NEW MAX. ENERGY GAIN??
	    Bmax = Btmp
	    Bles = Bfor    !SAVE VELOCITY AT - DPHI FROM PRESENT MAX
	    Newmax = .TRUE.
	    Phi = Phitmp
	  endif
	  Bfor = Btmp       !HOLD LAST BETA VALUE TO ASSOCIATE WITH BMAX
20	continue

C  	If the last calculated phase had the largest energy gain, then it
C  	is necessary to calculate the next point in the phase loop.

	if (Newmax) then
	  Btmp = Beta
	  T = 0.
	  Phitmp = Phitmp + Dphi
	  do 25 I = 1,N
	    Btmp = Btmp + Pre * Eax(I) * cos(Om * T + Phitmp) / Btmp
	    T = T + Dz / (Btmp * Speed_Of_Light)
25	  continue
          Bmor = Btmp                    ! <- it was missing (BM-041714)
	endif

C  	Now do a parabolic interpolation on the three points bracketing the
C   	maximum to do determine the maximum phase angle.

	Phiint = -Dphi * (0.5 + (Bmor**2 - Bmax**2) /
	1        (Bmor**2 - 2 * Bmax**2 + Bles**2))
	Phi = Phiint + Phi + Dphi
c	Vgain = Speed_Of_Light * Speed_Of_Light *    ! <- Old Bmax (BM-041714)
c     1	(Bmax * Bmax - Beta * Beta) / (2. * Qdm)

C  	Recalculate Bmax and Vgain at interpolated Phi (BM-041714)
	Btmp = Beta
	T = 0.
	Phitmp = Phi
	do 30 I = 1,N
	  Btmp = Btmp + Pre * Eax(I) * cos(Om * T + Phitmp) / Btmp
	  T = T + Dz / (Btmp * Speed_Of_Light)
30	continue
	Bmax = Btmp

	Vgain = Speed_Of_Light * Speed_Of_Light *   ! <- New Bmax (BM-041714)
	1	(Bmax * Bmax - Beta * Beta) / (2. * Qdm)

	return
	end



c	17-Apr-2014 C. Peters - Changed name to Phine_old, and replaced with new
c	-----------------------------------------------------------------------
	subroutine Phind_Old(El,Eax,Zax,N,Beta,Freq,Phi,Vgain,Qdm)

	implicit none

c	Variable declarations...

	real*4		Dz
	real*4		El
	real*4		Speed_Of_Light
	real*4		Pi
	real*4 		Eax(1)
	real*4		Zax(1)
	real*4		Freq
	real*4		Beta
	real*4		Phi
	real*4		Vgain
	real*4		Qdm
	real*4		Om
	real*4		Phitmp
	real*4		Dphi
	real*4		Pre
	real*4		Bmax
	real*4		Bfor
	real*4		T
	real*4		Btmp
	real*4		Bmor
	real*4		Bles
	real*4		Phiint

	integer*4	N
	integer*4	J
	integer*4	I	

c	Logical statements...

	logical 	Newmax

c	Data statements...

	data  Speed_Of_Light /2.997928E8/
	data  Pi	     /3.141593/

c	Include files...

	include 'PREDICT_LINAC_ENERGY.INC'

c	Begin code...

	Newmax = .FALSE.
     	Om = 2. * Pi * Freq
    	Phitmp = - Pi / 50.
   	Dphi = Pi / 25.
  	Dz = abs(Zax(N) - Zax(1)) / float(N-1)
 	Pre = El * Qdm * Dz
	Bmax = 0
	Bfor = Beta
	T = 0.

	!Calculate one point outside loop to initialize parabolic fit info 
	!correctly.

	do 5 I = 1, N
     	  Bfor = Bfor + Pre * Eax(I) * cos(Om * T + Phitmp) / Bfor
    	  T = T + Dz / (Bfor * Speed_Of_Light)

5     	continue
      	do 20 J = 1, 50
      	  Btmp = Beta
      	  T = 0.
      	  Phitmp = Phitmp + Dphi
      	  do 10 I = 1, N
      	    Btmp = Btmp + Pre * Eax(I) * cos(Om * T + Phitmp) / Btmp
      	    T = T + Dz / (Btmp * Speed_Of_Light)
10    	  continue
      	  if (Newmax) then
	    Bmor = Btmp    !SAVE VELOCITY AT + DPHI FROM PRESENT MAX
	    Newmax = .FALSE.
	  endif
     	  if (Btmp .gt. Bmax) then      !IS THIS A NEW MAX. ENERGY GAIN??
	    Bmax = Btmp
	    Bles = Bfor    !SAVE VELOCITY AT - DPHI FROM PRESENT MAX
	    Newmax = .TRUE.
	    Phi = Phitmp
	  endif
	  Bfor = Btmp       !HOLD LAST BETA VALUE TO ASSOCIATE WITH BMAX
20	continue


C  If the last calculated phase had the largest energy gain, then it
C  is necessary to calculate the next point in the phase loop.

	if (Newmax) then
	  Btmp = Beta
	  T = 0.
	  Phitmp = Phitmp + Dphi
	  do 25 I = 1,N
	    Btmp = Btmp + Pre * Eax(I) * cos(Om * T + Phitmp) / Btmp
	    T = T + Dz / (Btmp * Speed_Of_Light)
25	  continue
	endif

C  Now do a parabolic interpolation on the three points bracketing the
C   maximum to do determine the maximum phase angle.

	Phiint = -Dphi * (0.5 + (Bmor**2 - Bmax**2) /
	1        (Bmor**2 - 2 * Bmax**2 + Bles**2))
	Phi = Phiint + Phi + Dphi
	Vgain = Speed_Of_Light * Speed_Of_Light * 
	1	(Bmax * Bmax - Beta * Beta) / (2. * Qdm)

	return
	end



c	-----------------------------------------------------------------------
	subroutine Change_Settings(Eax_File, Indx, Resfreq, Zelm, Lt, El)

	implicit none

c	Variable declarations...

	integer*2	Resonator_ID
	integer*4	Indx
	integer*4	Success
	integer*4	I
	integer*4	Eax_File(70)
	integer*4	Record

	real*4		Zelm(200)
	real*4		Resfreq
	real*4		El(70)
	real*4		Lt

c	Include files...

	include 'PREDICT_LINAC_ENERGY.INC'

c	Begin code...

	type '(1x,a,$)','Please enter the NUMBER of the Resonator you ' //
	1               'wish to modify: '
	accept *, Resonator_ID


	!Now, loop through all resonators and find a match...

	Success = 0
	I = 1
	do while (I .le. Indx)
	  if (Resonator_ID .eq. Resonator_Data_Table(I).Resonator_Id_Number) 
	1   then
	    Success = 1
	    Record = I
	    write (6,25) Resonator_Data_Table(Record).Resonator_Id_Number,
	1		 Eax_File(Record), El(Record),
	1               Resonator_Data_Table(Record).Default_Acceleration_Phase
25	    format(' ','Resonator: R',I4,' Class: ',I4,' Setting: ',f4.2,
	1	   ' MV/m ',f6.1,' Degrees')

	    type '(1x,a,$)','Please enter the new class: '
	    accept *, Eax_File(Record)

	    type '(1x,a,$)','Please enter the acceleration field(MV/m): '
	    accept *, El(Record)

	    type '(1x,a,$)','Please enter the phase offset(Deg.): '
	    accept *,Resonator_Data_Table(Record).Default_Acceleration_Phase 
	
	    !After changing the 'Field' value for a resonator, it is now 
	    !necessary to change the 'Pot' value for it also...

	    Resonator_Data_Table(Record).Amplitude_After_Scan = 
	1    (((El(Record)/Resonator_Data_Table(Record).Amplitude_Scale_Factor)	
	1     - Resonator_Data_Table(Record).Amplitude_Calibrate_Intercept) /
	1       Resonator_Data_Table(Record).Amplitude_Calibrate_Slope)  	

	    call Resonator_Position(Eax_File, Resfreq, Zelm, Indx, Lt) 

	    I = Indx + 1

	  else

	    if (I .eq. Indx .and. Success .eq. 0) then
	      type *,'***** DESIRED RESONATOR ID WAS NOT FOUND *****'
	     endif

	    I = I + 1

	  endif
	end do

	return
	end



c	-----------------------------------------------------------------------
	subroutine List_Settings(Mass, Ener0, Beta, Integer_Charge_State,
	1			 Indx, Zelm, Resfreq, Eax_File, El)

	implicit none

c	Variable declaratiions...

	character*7	File_Name	

	integer*4	Integer_Charge_State(3)
	integer*4	Indx
	integer*4	Eax_File(70)
	integer*4	I
	integer*4	J

	real*4		Mass
	real*4		Ener0
	real*4		Beta(200)
	real*4		Charge_State(3)
	real*4		Zelm(200)
	real*4		Resfreq(200)
	real*4		Zinner
	real*4		Axis
	real*4		Totl
	real*4		El(70)

c	Include files...

	include 'PREDICT_LINAC_ENERGY.INC'

c	Begin code...

	!Write out heading...

	if (Possible_Charges .eq. 3) then
	  write(6,30) Mass, Ener0, Beta(1), Integer_Charge_State(1), 
	1	      Integer_Charge_State(2), Integer_Charge_State(3)
30	  format(t15,'Mass: ',f4.0,'  Initial_Energy: ',f6.2,' MeV  Beta: ',
	1        f6.4,/,t12,'PII Charge = ',I3,2x,'Booster Charge = ',I3,
	1        2x,'ATLAS Charge = ',I3,//,t28,'PRESENT HARDWARE SETTINGS',/)
	else if (Possible_Charges .eq. 2) then	
	  write(6,31) Mass, Ener0, Beta(1), Integer_Charge_State(1), 
	1	      Integer_Charge_State(2)
31	  format(t15,'Mass: ',f4.0,'  Initial_Energy: ',f6.2,' MeV  Beta: ',
	1        f6.4,/,t21,'Booster Charge = ',I3,2x,'ATLAS Charge = ',I3,//,
	1	 t28,'PRESENT HARDWARE SETTINGS',/)
	else 
	  write(6,32) Mass, Ener0, Beta(1), Integer_Charge_State(1)
32	  format(t15,'Mass: ',f4.0,'  Initial_Energy: ',f6.2,' MeV  Beta: ',
	1 	 f6.4,/,t21,'ATLAS Charge = ',I3,//,
	1	 t28,'PRESENT HARDWARE SETTINGS',/)
	endif

	write(6,35)
35	format(t18,'Name',3x,'Type',3x,'Length',2x,
	1     'Amplitude',2x,'Phase',2x,'Freq',2x,/,
	1     t18,'----   ----   ------  ---------  -----  ----')

	!Now, loop through and list settings...

	I = 1
	do while (I .le. Indx)

	    Zinner = Zelm(I) - Zelm(I - 1)
	    Axis = Zinner

	    if (Eax_File(I) .eq. 41) then 
	      Zinner = 0.10
	    else
	      if (Eax_File(I) .eq. 42) then 
	        Zinner = 0.165
	      else
		if (Eax_File(I) .eq. 22) then
		  Zinner = 0.32
		else
	          if (Eax_File(I) .eq. 43 .or. Eax_File(I) .eq. 44) then 
	            Zinner = 0.254
		  endif
	        endif
	      endif
	    endif

	    Totl = Totl + Zinner

	    if (Resonator_Data_Table(I).Status .eq. 1) then
	      write(6,57)Resonator_Data_Table(I).Resonator_Id_Number
57	      format(t18,'R',I3,t30,'RESONATOR DEACTIVATED')
	    else
	      write(6,40) Resonator_Data_Table(I).Resonator_Id_Number, 
	1		  Eax_File(I), Axis, El(I),
	1 	          Resonator_Data_Table(I).Default_Acceleration_Phase,
	1	          Resfreq(I)
40	      format(t18,'R',I3,4x,I2,4x,f5.3,'m',4x,
	1  	     f5.3,3x,f5.1,2x,f5.1)
	    endif

	    I = I + 1
	end do

	return
	end



c	-----------------------------------------------------------------------
	subroutine Display_Results(Printer_Lun, Mass, Ener0, Beta, File_Name,
	1			   Integer_Charge_State, Indx, Ttf, 
	1			   Phizero, Uzero, Eax_File, El)

	implicit none

c	Variable declarations...

	character*7	File_Name
	character*23	Process_Date_and_Time

	integer*4	Printer_Lun
	integer*4	Integer_Charge_State(3)
	integer*4	Indx
	integer*4	Eax_File(70)
	integer*4	I
	integer*4	J

	real*4		Mass
	real*4		Beta(200)
	real*4		Ttf(200)
	real*4		Phizero(200)
	real*4		Timein(200)
	real*4		DEGTORAD
	real*4		Uzero(200)
	real*4		Ener0
	real*4		El(70)

c	Data statements...

	data DEGTORAD /-0.017453/

c	Include files...

	include 'PREDICT_LINAC_ENERGY.INC'

c	Begin code...

d	type *,'----------------------------------------------'
d	type *,'In subroutine Display_Results, Indx = ',Indx

	!Get time and date...

	call Lib$Date_Time(Process_Date_And_Time)
	Process_Date_And_Time = Process_Date_And_Time(1:20)

	!Set up printer so that all information will fit on one page...
	!The first parameter is the logical unit number and the second
	!parameter is the number of lines per inch...

c	10-Oct-2012	C. Peters  Changed to '8'
	call Set_Line_Spacing(Printer_Lun, 8)

	write(Printer_Lun,70)Process_Date_And_Time
70	format(t33,'LINAC ENERGY PROFILE',/,t33,a20,/)	    

	!Write out headings...

	if (Possible_Charges .eq. 3) then
	  write(Printer_Lun,30) Mass, Ener0, Beta(1), Integer_Charge_State(1),
	1		      	Integer_Charge_State(2), 
	1		  	Integer_Charge_State(3),
ccc D. Quock 02-Nov-2001 1	Resonator_Data_Table(1).Amplitude_Scale_Factor
	1			New_Factor

30	  format(t16,'Mass: ',f4.0,'  Initial_Energy: ',f6.2,
	1        ' MeV  Beta: ',f9.6,/,t13,'PII Charge = ',I3,2x,
	1	 'Booster Charge = ',I3,2x,'ATLAS Charge = ',I3,/,t13,
ccc D. Quock 02-Nov-2001 1	 'Amplitude Scale Factor Used: ',f6.3,
	1	 'Amplitude After Scan  -  Scale Factor Used: ',f6.3,
	1        //,t33,'CALCULATED RESULTS',/)
	else if (Possible_Charges .eq. 2) then

	  write(Printer_Lun,31) Mass, Ener0, Beta(1), Integer_Charge_State(1),
	1		        Integer_Charge_State(2),
ccc D. Quock 02-Nov-2001 1	Resonator_Data_Table(1).Amplitude_Scale_Factor
	1			New_Factor
31	  format(t16,'Mass: ',f4.0,'  Initial_Energy: ',f6.2,
	1        ' MeV  Beta: ',f9.6,/,t22,'Booster Charge = ',I3,2x,
ccc 02-Nov-2001	1 'ATLAS Charge = ',I3,/,t22,'Amplitude Scale Factor Used: ',
	1	 'ATLAS Charge = ',I3,/,t22,
	1	'Amplitude After Scan  -  Scale Factor Used: ',
	1	  f6.3,//,t33,'CALCULATED RESULTS',/)
	else 
	  write(Printer_Lun,32) Mass, Ener0, Beta(1), Integer_Charge_State(1),
	1			New_Factor
32	  format(t16,'Mass: ',f4.0,'  Initial_Energy: ',f6.2,
	1	 ' MeV  Beta: ',f9.6,/,t22,'ATLAS Charge = ',I3,/,t22,
	1	 'Amplitude After Scan  -  Scale Factor Used: ',
	1	   f6.3,//,t33,'CALCULATED RESULTS',/)
	endif

	write(Printer_Lun,50) 
50	format(30x,t10,2x,'Label',2x,'Type',3x,'Pot',2x,'Field',2x,'Phase',
	1      2x,'Energy',4x,'Beta',5x,'TTF')
        write(Printer_Lun,52)
52	format(t12,'-----  ----  ----  -----  -----  ------   ------    ---')

	I = 1
	do while (I .le. Indx)

	  if (Resonator_Data_Table(I).Status .eq. 1) then
	    write(Printer_Lun,57)Resonator_Data_Table(I).Resonator_Id_Number
57	    format(t19,'R',I3,t30,'RESONATOR DEACTIVATED')
	  else
	    write(Printer_Lun,60)Resonator_Data_table(I).Resonator_Id_Number,
	1		         Eax_File(I), Resonator_Data_Table(I).
	1		         Amplitude_After_Scan, El(I), 
	1		         Resonator_Data_Table(I).
	1			 Default_Acceleration_Phase, Uzero(I), 
	1			 Beta(I+1), Ttf(I) 
60	    format(t10,3x,'R',I3,3x,I2,2x,f5.2,f7.2,1x,f6.1,1x,f7.2,2x,
	1	   f8.6,2x,f6.4)
	  endif

	  I = I + 1

	end do

d	type *,'Exiting subroutine Display_Results, I = ',I
d	type *,'----------------------------------------------'

	return
	end



c	-----------------------------------------------------------------------
	subroutine Options_Menu(Option_Choice)

	implicit none

c	Local variable declarations...

	integer*4	Option_Error
	integer*4	Option_Choice

c	Begin code...

       !Now put out the available options...
	type *,' '
	type *,'Parameter input complete '
	type *,' '
	type *,'**** Please select Option #2 to perform Energy '//
	1      'calculations ****' 
	type *,' '
	type *,'Please choose an option:'

	write(6,20)
20	format(/,' ',5x,'1. Change Beam Type',
	1      /,' ',5x,'2. Calculate Energy Gains',
	1      /,' ',5x,'3. Change Device Settings',
	1      /,' ',5x,'4. List Present Hardware Settings',
	1      /,' ',5x,'5. Display Results',
	1      /,' ',5x,'6. Print Results',
	1      /,' ',5x,'7. Restart',
	1      /,' ',5x,'8. Quit')

	type *,' '
	type '(1x,a,$)','Choice: '
	read(5,*, iostat = Option_Error) Option_Choice

	do while (Option_Error .gt. 0)
	  type*,' '
	  type*,'*** You entered an invalid option. Please try again. ***'
	  write(6,20)
	  type *,' '
	  type '(1x,a,$)','Choice: '
	  read(5,*, iostat = Option_Error) Option_Choice
	end do

	return
	end

