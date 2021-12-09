import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { City, Location, LocationRussia, LocationTypeEnum, Region } from '@api/users/models'
import { UsersService } from '@api/users/users.service'
import { Observable } from 'rxjs'
import { map } from 'rxjs/operators'


@Component( {
    selector: 'app-profile-edit-dwelling-russia',
    templateUrl: './profile-edit-dwelling-russia.component.html',
    styleUrls: [ './profile-edit-dwelling-russia.component.scss' ]
} )
export class ProfileEditDwellingRussiaComponent implements OnInit
{
    @Input() model!: Location | undefined
    @Output() modelChange = new EventEmitter<Location>()
    locationRussia: LocationRussia
    regions$!: Observable<Region[]>
    cities$!: Observable<City[]>
    selectedRegion!: string
    selectedCity!: string

    constructor( private usersService: UsersService )
    {
        this.locationRussia = this.model as LocationRussia ?? this.getEmptyLocation()
    }

    ngOnInit(): void
    {
        this.regions$ = this.usersService.userRegistrationInfoRegionsGet().pipe( map( item => item.region_list ) )
    }

    getEmptyLocation(): LocationRussia
    {
        return {
            location_type: LocationTypeEnum.Russian,
            country: "Россия",
            city: { region_name: "", name: "" },
            rural: false
        }
    }

    onModelChange(): void
    {
        this.modelChange.emit( this.locationRussia as Location )
    }

    onCityChange(): void
    {
        if ( this.locationRussia.city === undefined )
            return
        this.locationRussia.city.name = this.selectedCity
        this.modelChange.emit( this.locationRussia as Location )
    }

    onRegionChange(): void
    {
        if ( this.locationRussia.city === undefined )
            this.locationRussia.city = { region_name: this.selectedRegion, name: "" }
        else
            this.locationRussia.city.region_name = this.selectedRegion
        this.modelChange.emit( this.locationRussia as Location )
        this.cities$ = this.usersService.userRegistrationInfoCitiesRegionGet( this.selectedRegion ).pipe( map( item => item.city_list ) )
    }
}
