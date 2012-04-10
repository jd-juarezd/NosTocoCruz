Feature: Frontend

    Scenario: Login page
        Given I access the url "/"
        Then I see the title "Inicio"
        And There is the form "login"
        And I see a "text" input named "user_name"
        And I see a "password" input named "password"
        And There is the form "registro"
        And I see a "text" input named "nombre"
        And I see a "text" input named "apellidos"
        And I see a "text" input named "email"
        And I see a "password" input named "password_register"
        
    Scenario: Home page
    	Given I access the url "/home"
    	Then I see the title "Home"
    
    Scenario: Profile page
    	Given I access the url "/profile"
    	Then I see the title "Perfil"
	