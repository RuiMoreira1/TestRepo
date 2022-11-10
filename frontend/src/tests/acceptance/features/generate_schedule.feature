Feature: Start the creation of a new schedule

Scenario: Start the creation of a new schedule in the Home page
    Given I am logged in as a service manager
    When I am in the create schedule page
    And I insert the schedule name
    And I select month and year
    And I click on the button with the text 'Generate new schedule'
    Then I should be presented with the text 'Request successfully submitted'
