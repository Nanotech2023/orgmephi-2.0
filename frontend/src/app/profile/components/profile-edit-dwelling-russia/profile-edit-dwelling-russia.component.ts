import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { Location, LocationRussia, LocationTypeEnum } from '@api/users/models'
import { UsersService } from '@api/users/users.service'
import { FormControl } from '@angular/forms'


@Component( {
    selector: 'app-profile-edit-dwelling-russia',
    templateUrl: './profile-edit-dwelling-russia.component.html',
    styleUrls: [ './profile-edit-dwelling-russia.component.scss' ]
} )
export class ProfileEditDwellingRussiaComponent implements OnInit
{
    @Input() model!: Location
    @Output() modelChange = new EventEmitter<Location>()
    locationRussia: LocationRussia
    regions!: string[]

    constructor( private usersService: UsersService )
    {
        this.locationRussia = this.model as LocationRussia ?? this.getEmptyLocation()
    }

    ngOnInit(): void
    {
        this.usersService.userRegistrationInfoRegionsGet().subscribe(
            items => this.regions = items.region_list.map( region => region.name )
        )
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

    onCityChange( value: string ): void
    {
        if ( this.locationRussia.city === undefined )
            return
        this.locationRussia.city.name = value
        this.modelChange.emit( this.locationRussia as Location )
    }

    onRegionChange( value: string ): void
    {
        if ( this.locationRussia.city === undefined )
            this.locationRussia.city = { region_name: value, name: "" }
        else
            this.locationRussia.city.region_name = value
        this.modelChange.emit( this.locationRussia as Location )
        console.log(this.locationRussia)
    }
}
