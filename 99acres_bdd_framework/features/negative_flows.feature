Feature: 99acres negative rental property flows
  As a 99acres user
  I want invalid or unauthenticated actions to be handled correctly
  So that negative rental flows are validated

  Scenario: Verify shortlist requires login
    Given I have searched rental properties using the test data location
    When I apply the 2 BHK filter
    And I apply the Owner filter
    And I open the first property from search results
    And I switch to the property details window
    And I click the shortlist button
    Then the login popup should be displayed

  Scenario: Verify empty location validation
    Given I remember the current page URL
    When I select the Rent tab
    And I submit the search without a location
    Then I should remain on the same page
