import { Component, OnInit } from '@angular/core'
import { SchoolRegistrationRequestUser } from '@api/users/models'
import { AuthActions, AuthState } from '@/auth/store'
import { Store } from '@ngrx/store'


export interface SchoolRegistrationRequestUserAttempt extends SchoolRegistrationRequestUser
{
    passwordConfirm: string
}


@Component( {
    selector: 'app-register-school',
    templateUrl: './register-school.component.html',
    styleUrls: [ './register-school.component.scss' ]
} )
export class RegisterSchoolComponent implements OnInit
{
    registerAttempt: SchoolRegistrationRequestUserAttempt
    hasRegisterNumber!: boolean
    agreementAccepted: boolean

    constructor( private readonly store: Store<AuthState.State> )
    {
        this.registerAttempt = {
            auth_info: { email: '', password: '' },
            register_type: SchoolRegistrationRequestUser.RegisterTypeEnum.School,
            personal_info: { first_name: '', second_name: '', middle_name: '', date_of_birth: '' },
            passwordConfirm: ''
        }
        this.agreementAccepted = false
    }

    ngOnInit(): void
    {
    }

    isValid(): boolean
    {
        return this.agreementAccepted
    }

    register( registerUser: SchoolRegistrationRequestUser ): void
    {
        this.store.dispatch( AuthActions.registerRequest( { registrationRequestUser: registerUser } ) )
    }
}
