Feature: tweetTrack
    Use the front end app

    Scenario: User clicks the contact button
        Given a user
        When I click the Contact button
        Then I see the Contact Form

    Scenario: User clicks the send message button
        Given a user
        And a name
        And an email
        And a subject
        And a message
        And I fill out the contact form
        When I click the send button
        Then I receive a response

    Scenario: User clicks the about button
        Given a user
        When I click the about button
        Then I see the about section

    Scenario: User clicks the track me button
        Given a user
        When I click the track me button
        Then I see the track me form

    Scenario: User submits the track form
        Given a user
        And a twitter handle
        And I fill out the twitter form
        When I click the submit button
        Then I see a new location on the map
