import { Component, ElementRef, EventEmitter, Input, OnInit, Output, ViewChild } from '@angular/core'
import { Agreements } from '@/auth/agreements'
import {
    RequestRegistrationSchool,
    TypeRegistrationPersonalInfo,
    TypeUserType,
    TypeUserTypeSchool
} from '@/auth/api/models'
import { Store } from '@ngrx/store'
import { AuthState } from '@/auth/store'


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
    @Output() userAdd: EventEmitter<RequestRegistrationSchool> = new EventEmitter<RequestRegistrationSchool>()
    @ViewChild( 'modal' ) modal!: ElementRef

    registerTypes: TypeUserTypeSchool[] = [ TypeUserTypeSchool.PreUniversity, TypeUserTypeSchool.School, TypeUserTypeSchool.Enrollee ]
    registerAttempt: RequestRegistrationSchool // TODO support RequestRegistrationUniversity
    isRegistered: boolean
    selectedUserType: TypeUserType | null
    hasRegisterNumber: boolean
    agreementAccepted: boolean

    constructor()
    {
        this.registerAttempt = {
            auth_info: { email: '', password: '' },
            register_type: this.registerTypes[ 0 ],
            personal_info: { first_name: '', second_name: '', middle_name: '', date_of_birth: '' },
            register_confirm: { registration_number: '', password: '' }
        }
        this.isRegistered = false
        this.agreementAccepted = true
        this.selectedUserType = null
        this.hasRegisterNumber = false
    }

    selectRegisterType( userType: TypeUserTypeSchool ): void
    {
        this.selectedUserType = userType
    }

    isAvailable(): boolean
    {
        return this.selectedUserType !== null && this.selectedUserType == TypeUserTypeSchool.School
    }

    isValid( registration: RequestRegistrationSchool ): boolean
    {
        return !!( this.registerAttempt.personal_info.date_of_birth && this.registerAttempt.personal_info.first_name &&
            this.registerAttempt.personal_info.middle_name &&
            this.registerAttempt.personal_info.second_name &&
            this.registerAttempt.auth_info.email &&
            this.registerAttempt.auth_info.password
        )
    }

    register( registerUser: RequestRegistrationSchool ): void
    {
        this.isRegistered = true
        this.userAdd.emit( registerUser )
    }


    onClick( $event: any )
    {
        if ( $event.target == this.modal?.nativeElement )
            this.modalVisible = false
    }
}
