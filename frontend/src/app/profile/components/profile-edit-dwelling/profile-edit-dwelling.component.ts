import { getLocationDisplay } from '@/shared/displayUtils'
import { Component, EventEmitter, Input, Output } from '@angular/core'
import { Location, LocationRussiaCity, LocationTypeEnum } from '@api/users/models'


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

    readonly locationTypes: LocationTypeEnum[] = [
        LocationTypeEnum.Russian,
        LocationTypeEnum.Foreign
    ]
    selectedValue: LocationTypeEnum = this.locationTypes[ 0 ]


    onModelChange(): void
    {
        this.modelChange.emit( this.model )
    }

    onCityChange(): void
    {
        this.cityChange.emit( this.city )
    }

    getLocationDisplay( locationType: LocationTypeEnum ): string
    {
        return getLocationDisplay( locationType )
    }
}