Feature: 99acres positive rental property flows
  As a 99acres user
  I want to search and inspect rental properties
  So that the main positive rental flows are validated

  Scenario: Verify valid property search
    When I search rental properties using the test data location
    Then the search results page should be displayed
    And the results heading should contain "rent"

  Scenario: Verify 2 BHK filter
    Given I have searched rental properties using the test data location
    When I apply the 2 BHK filter
    Then filtered results should be visible
    And the "2 BHK" filter should be applied

  Scenario: Verify searched location is displayed in search bar
    Given I have searched rental properties using the test data location
    Then the search bar should display the searched location

  Scenario: Verify property details page
    Given I have searched rental properties using the test data location
    When I open the first property from search results
    And I switch to the property details window
    Then the property title and rent amount should be visible
