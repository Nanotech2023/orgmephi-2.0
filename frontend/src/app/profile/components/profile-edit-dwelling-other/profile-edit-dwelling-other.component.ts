import { Component, EventEmitter, Input, Output } from '@angular/core'
import { Location, LocationOther, LocationRussia, LocationTypeEnum } from '@api/users/models'


@Component( {
    selector: 'app-profile-edit-dwelling-other',
    templateUrl: './profile-edit-dwelling-other.component.html',
    styleUrls: [ './profile-edit-dwelling-other.component.scss' ]
} )
export class ProfileEditDwellingOtherComponent
{
    @Input() model!: LocationOther
    @Output() modelChange = new EventEmitter<LocationOther>()
    locationOther!: LocationOther

    constructor()
    {
        this.locationOther = this.getEmptyLocation()
    }

    onModelChange(): void
    {
        this.modelChange.emit( this.model )
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
