# Vehicles — fort_vehicle

Source :
https://dev.epicgames.com/documentation/fortnite/verse-api/fortnitedotcom/vehicles/fort_vehicle

Module :

`/Fortnite.com/Vehicles`

`fort_vehicle` expose actuellement notamment :

- `Speed`
- `BoostRemaining`
- `BoostCapacity`
- `IsOnGround`
- `IsInAir`
- `IsInWater`
- `GetPassengers`
- `GetOccupants`
- `GetDrivers`
- `GetFuelRemaining`
- `GetFuelCapacity`
- `TeleportTo`
- `RemoveAgent`
- `RemoveAll`
- `AddAgent`
- `GetSeats`

Conversion depuis un personnage :

```verse
(InCharacter:fort_character).GetVehicle<public><native>()<transacts><decides>:fort_vehicle
```

Cette conversion est faillible.

Signatures vérifiées supplémentaires :

```verse
GetDrivers<public>():[]agent
GetSeats<public>():[]fort_vehicle_seat
```
