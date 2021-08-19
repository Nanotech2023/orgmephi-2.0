import { Component, ElementRef, EventEmitter, Input, OnInit, Output, ViewChild } from '@angular/core'
import { TypeRegistrationPersonalInfo, TypeUserInfo, TypeUserRole, TypeUserTypeSchool } from '@/auth/api/models'
import { AuthService } from '@/auth/api/auth.service'


@Component( {
    selector: 'app-edit-user-modal',
    templateUrl: './edit-user-modal.component.html',
    styleUrls: [ './edit-user-modal.component.scss' ],
    host: {
        '(document:click)': 'onClick($event)'
    }
} )
export class EditUserModalComponent implements OnInit
{
    @Input() modalVisible!: boolean
    @Input() user!: TypeUserInfo
    @Output() modalVisibleChange: EventEmitter<boolean> = new EventEmitter<boolean>()
    @Output() userEdit: EventEmitter<TypeUserInfo> = new EventEmitter<TypeUserInfo>()
    @ViewChild( 'modal' ) modal!: ElementRef

    registerTypes: TypeUserTypeSchool[] = [ TypeUserTypeSchool.PreUniversity, TypeUserTypeSchool.School, TypeUserTypeSchool.Enrollee ]
    roles: TypeUserRole[] = [ TypeUserRole.Admin, TypeUserRole.Creator, TypeUserRole.System, TypeUserRole.Participant ]


    constructor( private readonly service: AuthService ) { }

    ngOnInit(): void
    {
    }

    confirm()
    {
        if ( !!( this.user ) )
        {
            // // @ts-ignore
            // this.service.userUserIdRolePut( this.user.id, { role: this.user.role } )
            // // @ts-ignore
            // this.service.userUserIdTypePut( this.user.id, { type: this.user.type } )
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
