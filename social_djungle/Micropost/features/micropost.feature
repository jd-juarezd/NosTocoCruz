Feature: Micropost

    Scenario: Writing a Micropost
        I create a sample micropost
        Then The text length is correct
    	Then micropost should be created correctly
        
    Scenario: Publishing a Micropost
        When I publish a micropost the written text will be the same as the published text
        And The user that published a micropost will be the owner
        