# Ride Sharing System
## To run
  configure secret key, allowed and smtp credentials first, then

  sudo docker compose-up
  
## Status
We have a "shared" state in addition to the three states specified in the requirement. When a user joins an open ride, the ride becomes shared, which means the owner of the ride cannot edit the ride anymore. Drivers could search both in open rides and shared rides to claim new rides. A shared ride may get back to open when all sharers quit from the ride. 
## Capacity
Each vehicle type has a default capacity upper bound, which is defined by didi.models.py.Vehicle.DEFAULT_CAPACITY. When a user requests a new ride, the user can specify any amount of passengers from his/her party regardless of the limit, though no drivers might find this ride. The limitation works when sharers want to join the ride or edit the ride they joined, in which case the total number of passengers of a ride will be calculated and limited. The default upper bound is pretty high (e.g. 10 for cars) so it won't be a problem in most cases. 
When drivers search for rides to claim, the comparison happens between the actual capacity of their registered vehicle and the total passenger number from both owner's and all sharer's party.
## Special Feature
Drivers can edit the special features of their registered vehicle, they can also add new ones on the editing page if the desired feature is not on the list. Users could add special features from the existing feature list to their rides. 
## User Profile Edit
Users could edit their info, the password in the top navigation bar, or edit their vehicle's info in the driver's section.
## Reference
The login and user register page are modified from the templates below:

[login page template](https://jsfiddle.net/ivanov11/dghm5cu7/)
[register page template](https://jsfiddle.net/ivanov11/hzf0jxLg/)

The style part in templates needs to import bootstrap CDN as posted [here](https://getbootstrap.com/docs/4.5/getting-started/introduction/)
