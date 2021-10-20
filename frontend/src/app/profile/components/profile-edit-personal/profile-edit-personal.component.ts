import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { UserInfo, UserLimitations } from '@api/users/models'


@Component( {
    selector: 'app-profile-edit-personal',
    templateUrl: './profile-edit-personal.component.html',
    styleUrls: [ './profile-edit-personal.component.scss' ]
} )
export class ProfileEditPersonalComponent
{
    @Input() model!: UserInfo
    @Output() modelChange = new EventEmitter<UserInfo>()

    onModelChange(): void
    {
        this.modelChange.emit( this.model )
    }
}