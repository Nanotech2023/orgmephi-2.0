import { Component, EventEmitter, Input, Output } from '@angular/core'
import { Location, LocationOther, LocationRussia } from '@api/users/models'


@Component( {
    selector: 'app-profile-edit-dwelling',
    templateUrl: './profile-edit-dwelling.component.html',
    styleUrls: [ './profile-edit-dwelling.component.scss' ]
} )
export class ProfileEditDwellingComponent
{
    @Input() model!: Location | undefined
    @Output() modelChange = new EventEmitter<Location>()
    dwelling: LocationRussia = ( this.model as LocationRussia ) ?? this.getEmptyLocation()

    onModelChange(): void
    {
        this.modelChange.emit( this.dwelling )
    }

    onCityChange( $event: string ): void
    {
        // @ts-ignore
        this.dwelling.city.name = $event
        this.modelChange.emit( this.dwelling )
    }

    onRegionChange( $event: string ): void
    {
        // @ts-ignore
        this.dwelling.city?.region_name = $event
        this.modelChange.emit( this.dwelling )
    }

    getEmptyLocation(): LocationRussia
    {
        return {
            country: "Россия",
            city: {
                region_name: "",
                name: ""
            },
            location_type: LocationOther.LocationTypeEnum.Russian,
            rural: false
        } as LocationRussia
    }
}