Feature: Frontend

    Scenario: Login page
        Given I access the url "/"
        Then I see the title "Bienvenido a Social Djungle"
        And There is the form "login"
        And I see a "text" input named "username"
        And I see a "password" input named "password"
        And There is the form "registro"
        And I see a "text" input named "username"
        And I see a "text" input named "email"
        And I see a "password" input named "password_register"
        And I see a "password" input named "password_register_checker"
        
    Scenario: Home page
    	Given I access the url "/home"
    	Then I see the title "Social Djungle - Home"
    
    Scenario: Profile page
    	Given I access the url "/profile"
    	Then I see the title "Social Djungle - Perfil"
	
