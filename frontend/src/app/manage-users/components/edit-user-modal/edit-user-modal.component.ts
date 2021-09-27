import { Component, ElementRef, EventEmitter, Input, Output, ViewChild } from '@angular/core'
import { User } from '@api/users/models'


@Component( {
    selector: 'app-edit-user-modal',
    templateUrl: './edit-user-modal.component.html',
    styleUrls: [ './edit-user-modal.component.scss' ],
    host: {
        '(document:click)': 'onClick($event)'
    }
} )
export class EditUserModalComponent
{
    @Input() modalVisible!: boolean
    @Input() user!: User
    @Output() modalVisibleChange: EventEmitter<boolean> = new EventEmitter<boolean>()
    @Output() userEdit: EventEmitter<User> = new EventEmitter<User>()
    @ViewChild( 'modal' ) modal!: ElementRef

    registerTypes: User.TypeEnum[] = [ User.TypeEnum.PreUniversity, User.TypeEnum.School, User.TypeEnum.Enrollee ]
    roles: User.RoleEnum[] = [ User.RoleEnum.Admin, User.RoleEnum.Creator, User.RoleEnum.System, User.RoleEnum.Participant ]

    confirm()
    {
        if ( !!( this.user ) )
        {
            this.userEdit.emit( this.user )
        }

        this.modalVisible = false
        this.modalVisibleChange.emit( this.modalVisible )
    }

    resetPassword()
    {
        //TODO
    }

    onClick( $event: any )
    {
        if ( $event.target == this.modal?.nativeElement )
            this.hideModal()
    }

    hideModal()
    {
        this.modalVisible = false
        this.modalVisibleChange.emit( this.modalVisible )
    }
}
