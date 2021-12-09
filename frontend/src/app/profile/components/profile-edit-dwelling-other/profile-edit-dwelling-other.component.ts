import { Component, EventEmitter, Input, Output } from '@angular/core'
import { Location, LocationOther, LocationRussia, LocationTypeEnum } from '@api/users/models'


@Component( {
    selector: 'app-profile-edit-dwelling-other',
    templateUrl: './profile-edit-dwelling-other.component.html',
    styleUrls: [ './profile-edit-dwelling-other.component.scss' ]
} )
export class ProfileEditDwellingOtherComponent
{
    @Input() model!: LocationOther | undefined
    @Output() modelChange = new EventEmitter<LocationOther>()
    locationOther!: LocationOther

    constructor()
    {
        this.locationOther = this.model ?? this.getEmptyLocation()
    }

    onModelChange(): void
    {
        this.modelChange.emit( this.locationOther )
    }

    getEmptyLocation(): LocationOther
    {
        return {
            location_type: LocationTypeEnum.Foreign,
            country: "",
            location: "",
            rural: false
        }
    }
}
