import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { LocationRussia, SchoolInfo } from '@api/users/models'


@Component( {
    selector: 'app-profile-edit-school',
    templateUrl: './profile-edit-school.component.html',
    styleUrls: [ './profile-edit-school.component.scss' ]
} )
export class ProfileEditSchoolComponent
{
    @Input() model!: SchoolInfo
    @Output() modelChange = new EventEmitter<SchoolInfo>()

    get schoolLocation(): LocationRussia
    {
        return this.model.location as LocationRussia
    }

    set schoolLocation( location: LocationRussia )
    {
        this.model.location = location
    }

    onModelChange(): void
    {
        this.modelChange.emit( this.model )
    }
}
