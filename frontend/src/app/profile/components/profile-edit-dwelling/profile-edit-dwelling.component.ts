import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { Location, LocationOther, LocationRussia } from '@api/users/models'


@Component( {
    selector: 'app-profile-edit-dwelling',
    templateUrl: './profile-edit-dwelling.component.html',
    styleUrls: [ './profile-edit-dwelling.component.scss' ]
} )
export class ProfileEditDwellingComponent
{
    @Input() model!: LocationRussia
    @Output() modelChange = new EventEmitter<LocationRussia>()

    onModelChange(): void
    {
        this.modelChange.emit( this.model )
    }

    onCityChange( $event: string ): void
    {
        // @ts-ignore
        this.model.city.name = $event
        this.modelChange.emit( this.model )
    }

    onRegionChange( $event: string ): void
    {
        // @ts-ignore
        this.model.city?.region_name = $event
        this.modelChange.emit( this.model )
    }

}