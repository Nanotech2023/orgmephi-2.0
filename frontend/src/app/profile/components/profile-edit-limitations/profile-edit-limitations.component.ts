import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { UserLimitations } from '@api/users/models'


@Component( {
    selector: 'app-profile-edit-limitations',
    templateUrl: './profile-edit-limitations.component.html',
    styleUrls: [ './profile-edit-limitations.component.scss' ]
} )
export class ProfileEditLimitationsComponent
{
    @Input() model!: UserLimitations
    @Output() modelChange = new EventEmitter<UserLimitations>()

    onModelChange(): void
    {
        this.modelChange.emit( this.model )
    }
}