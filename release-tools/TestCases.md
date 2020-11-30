# Test Cases for CodeFreeze Project

## Security:
 - Validate that no credentials are displayed to the console or stored within the code.

## GIT:
 - Validate invalid credentials fails gracefully

## Releases:
 - Test 1: Trying to use an older release then defined in plist.
 - Test 2: Trying to create a "Next" release when there is no "Next" release defined and the "Current" release already exists.
 - Test 3: Validate that Feature Flag diff works as expected when current release is the first within defined releases index.
 - 
 ## Misc
 - Validate handle of diff when there is no actual diff between feature flag files.