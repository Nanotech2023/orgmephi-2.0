import { Component, ElementRef, EventEmitter, Input, Output, ViewChild } from '@angular/core'
import { SchoolRegistrationRequestUser, TypeRequestUser } from '@api/users/models'


@Component( {
    selector: 'app-add-user-modal',
    templateUrl: './add-user-modal.component.html',
    styleUrls: [ './add-user-modal.component.scss' ],
    host: {
        '(document:click)': 'onClick($event)'
    }
} )
export class AddUserModalComponent
{
    @Input() modalVisible!: boolean
    @Output() modalVisibleChange: EventEmitter<boolean> = new EventEmitter<boolean>()
    @Output() addClick: EventEmitter<SchoolRegistrationRequestUser> = new EventEmitter<SchoolRegistrationRequestUser>()
    @ViewChild( 'modal' ) modal!: ElementRef

    registerTypes: SchoolRegistrationRequestUser.RegisterTypeEnum[] = [ SchoolRegistrationRequestUser.RegisterTypeEnum.PreUniversity, SchoolRegistrationRequestUser.RegisterTypeEnum.School, SchoolRegistrationRequestUser.RegisterTypeEnum.Enrollee ]
    registerAttempt: SchoolRegistrationRequestUser // TODO support RequestRegistrationUniversity
    isRegistered: boolean
    selectedUserType: TypeRequestUser.TypeEnum | null
    hasRegisterNumber: boolean
    agreementAccepted: boolean

    constructor()
    {
        this.registerAttempt = {
            auth_info: { email: '', password: '' },
            register_type: this.registerTypes[ 0 ],
            personal_info: { first_name: '', second_name: '', middle_name: '', date_of_birth: '' }
            // register_confirm: { registration_number: 0, password: '' }
        }
        this.isRegistered = false
        this.agreementAccepted = true
        this.selectedUserType = null
        this.hasRegisterNumber = false
    }

    selectRegisterType( userType: SchoolRegistrationRequestUser.RegisterTypeEnum ): void
    {
        this.selectedUserType = userType
    }

    isAvailable(): boolean
    {
        return this.selectedUserType !== null && this.selectedUserType == TypeRequestUser.TypeEnum.School
    }

    isValid( registration: SchoolRegistrationRequestUser ): boolean
    {
        return !!( this.registerAttempt.personal_info.date_of_birth && this.registerAttempt.personal_info.first_name &&
            this.registerAttempt.personal_info.middle_name &&
            this.registerAttempt.personal_info.second_name &&
            this.registerAttempt.auth_info.email &&
            this.registerAttempt.auth_info.password
        )
    }

    register( registerUser: SchoolRegistrationRequestUser ): void
    {
        this.isRegistered = true
        this.addClick.emit( registerUser )
    }

    onClick( $event: any ): void
    {
        if ( $event.target == this.modal?.nativeElement )
            this.modalVisible = false
    }
}
