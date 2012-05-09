Feature: Testing photo upload and access

	Scenario: Uploading Photo
	When I upload a photo
	And Its extension is correct
	Then It should be correctly stored
	
	Scenario: Accessing Photo
	When I retrieve a photo from the database
	Then I can see it
	
	Scenario: Resizing Photo
	When I upload a big photo
	Then It is resized to a proper size