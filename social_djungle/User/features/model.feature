Feature: Validating User Model

	Scenario: Validating User Login
		When I create a sample user
		Then password length is correct
		Then It should be created correctly
		 
	Scenario: Wrong email
		When I create a sample user
		Then The email cannot be empty
		And The email should not be longer than 50 characters
		And The email should not accept "foo.@bar."
		
	Scenario: User already exists
		When I create a sample user
		Then It should be created correctly
		And saved
		If I try to create it again
		Then It should not be valid
		
	Scenario: User session is correctly set
		I try to log in with the user
		The user is authenticated
		The cookie should have a "user_session" field
		The cookie should have a "id" field
		Finally I log out
		The cookie should not have a "user_session" field
		The cookie should not have a "id" field
	
	Scenario: User attributes are correctly stored
		When I create a new user with personal information
		And I retrieve it from the database
		Then It should have a name
		And It should have a surname
		And It should have a birthdate
		And It should have a gender
		And It should have a country
		
		