import { Component, EventEmitter, Input, Output } from '@angular/core'
import { Location, LocationRussiaCity, LocationTypeEnum } from '@api/users/models'
import { getLocationDisplay } from '@/shared/localizeUtils'


@Component( {
    selector: 'app-profile-edit-dwelling',
    templateUrl: './profile-edit-dwelling.component.html',
    styleUrls: [ './profile-edit-dwelling.component.scss' ]
} )
export class ProfileEditDwellingComponent
{
    @Input() model!: Location
    @Output() modelChange = new EventEmitter<Location>()
    @Input() city!: LocationRussiaCity
    @Output() cityChange = new EventEmitter<LocationRussiaCity>()
    @Input() country!: string
    @Output() countryChange = new EventEmitter<string>()

    readonly locationTypes: LocationTypeEnum[] = [
        LocationTypeEnum.Russian,
        LocationTypeEnum.Foreign
    ]

    onModelChange(): void
    {
        this.modelChange.emit( this.model )
    }

    onCityChange(): void
    {
        this.cityChange.emit( this.city )
    }

    onCountryChange()
    {
        this.countryChange.emit( this.country )
    }

    getLocationDisplay( locationType: LocationTypeEnum ): string
    {
        return getLocationDisplay( locationType )
    }

    onLocationTypeChange( $event: Event )
    {
        // @ts-ignore
        this.model.location_type = $event.target.value
        this.modelChange.emit( this.model )
    }
}