Feature: Validating User Model

	Scenario: Validating User Login
		When I create a sample user
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
		