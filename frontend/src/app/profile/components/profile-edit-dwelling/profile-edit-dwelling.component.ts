import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { Location, LocationRussiaCity, LocationTypeEnum } from '@api/users/models'
import { getLocationDisplay } from '@/shared/localizeUtils'


@Component( {
    selector: 'app-profile-edit-dwelling',
    templateUrl: './profile-edit-dwelling.component.html',
    styleUrls: [ './profile-edit-dwelling.component.scss' ]
} )
export class ProfileEditDwellingComponent implements OnInit
{
    @Input() model!: Location
    @Output() modelChange = new EventEmitter<Location>()

    readonly locationTypes: LocationTypeEnum[] = [
        LocationTypeEnum.Russian,
        LocationTypeEnum.Foreign
    ]
    selectedValue!: LocationTypeEnum

    ngOnInit(): void
    {
        this.selectedValue = this.model.location_type ?? this.locationTypes[ 0 ]
    }

    getLocationDisplay( locationType: LocationTypeEnum ): string
    {
        return getLocationDisplay( locationType )
    }
}