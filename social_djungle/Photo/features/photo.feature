Feature: Testing photo upload and access

	Scenario: Uploading Photo
	When I upload a photo
	Then I can access it
	
	Scenario: Resizing Photo
	When I try to upload a big photo
	Then It is resized to a proper size
	And It is correctly saved