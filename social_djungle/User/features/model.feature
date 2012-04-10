Feature: Validating User Model

	Scenario: Validating User Login
		 When I create a sample user
		 Then It should be created correctly
		 
	Scenario: Wrong email
		When I create a sample user
		Then The "email" cannot be empty
		And The "email" should have the right format
		And the "username" cannot be empty
		