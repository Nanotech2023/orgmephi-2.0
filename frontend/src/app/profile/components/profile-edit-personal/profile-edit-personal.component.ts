import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core'
import { UserInfo, UserLimitations } from '@api/users/models'


@Component( {
    selector: 'app-profile-edit-personal',
    templateUrl: './profile-edit-personal.component.html',
    styleUrls: [ './profile-edit-personal.component.scss' ]
} )
export class ProfileEditPersonalComponent implements OnInit
{
    @Input() model!: UserInfo
    @Output() modelChange = new EventEmitter<UserInfo>()
    userInfo: UserInfo = this.model

    onModelChange( $event: UserInfo )
    {
        this.modelChange.emit( $event )
    }

    ngOnInit(): void
    {
        console.log( this.userInfo )
    }
}