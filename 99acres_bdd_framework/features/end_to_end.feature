@end_to_end
Feature: 99acres end-to-end rental property flow
  As a logged-in 99acres user
  I want to search, filter, shortlist, and view owner contact details
  So that the complete rental property journey is validated

  Scenario: Complete end-to-end property search and owner contact flow
    When I log in using the test data mobile number
    And I wait 20 seconds for manual OTP entry
    And I verify the OTP and continue
    And I search rental properties using the test data location
    Then the search results page should be displayed
    When I close blocking popups on the search results page
    And I apply the 2 BHK filter
    And I apply the Flat/Apartment filter
    And I apply the Owner filter
    And I apply the Single Men filter
    And I sort results by price low to high
    Then all required filters should be applied
    And filtered results should be visible
    When I open the first property from search results
    And I switch to the property details window
    Then the property title and rent amount should be visible
    When I click the shortlist button
    And I open the owner details section
    And I click the view phone number button
    Then the contact section should be displayed
