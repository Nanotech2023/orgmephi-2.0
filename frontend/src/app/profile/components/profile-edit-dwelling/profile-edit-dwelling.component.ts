import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { Location, LocationOther, LocationRussia } from '@api/users/models'


@Component( {
    selector: 'app-profile-edit-dwelling',
    templateUrl: './profile-edit-dwelling.component.html',
    styleUrls: [ './profile-edit-dwelling.component.scss' ]
} )
export class ProfileEditDwellingComponent implements OnInit
{
    @Input() model!: LocationRussia
    @Output() modelChange = new EventEmitter<LocationRussia>()
    dwelling!: LocationRussia

    ngOnInit(): void
    {
        this.dwelling = this.model as LocationRussia
    }

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

}